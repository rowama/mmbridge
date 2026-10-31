"""Wake relay (ADR-0011): verifies mmbridge's HMAC-signed wakes and forwards them to a Grok Bot routine with
that bot's Bearer routine key. Own image and Coolify app; imports nothing from app/ (verify is a copy of
app.wake.verify, pinned by tests/unit/test_relay.py).

Config is env only (Coolify secrets), per bot: RELAY_BOT_<NAME>_HMAC_SECRET (copy of the bot's mmbridge wake
secret, >= 32 chars), RELAY_BOT_<NAME>_ROUTINE_URL (https), RELAY_BOT_<NAME>_ROUTINE_KEY. <NAME> is the bot
name upper-cased with '-' -> '_' (bot "my-bot" -> RELAY_BOT_MY_BOT_*). Optional: RELAY_DATA_DIR (/data),
RELAY_UPSTREAM_TIMEOUT_S (5), RELAY_RATE_PER_MIN (30), RELAY_BURST (10), RELAY_ALLOW_HTTP_UPSTREAM (tests only).
Start fails on a bot with a missing field, a short secret or a non-https URL.

POST /wake/{bot}: unknown bot 404; bad signature / stale timestamp (300 s) 401 {"reason"}; delivery already
forwarded 200 {"status": "duplicate"} (not forwarded); over the per-bot rate 429 {"reason": "rate_limited"};
else the raw body is forwarded byte-for-byte with Authorization: Bearer <key> and X-MMB-Delivery, and the
upstream result is mapped by map_upstream (2xx -> 200; 408/429/5xx/timeout/connect -> 503 so mmbridge
retries; any other status -> 424 {"upstream": code}, permanent).
Delivery guarantee (accepted risk A, Rob 2026-10-28): a delivery id is recorded in Seen only after upstream
2xx, so a lost upstream response (logged relay_delivery_ambiguous) or a crash before Seen.add can start the
routine twice; never zero times. Concurrent identical deliveries forward once (per-delivery lock + in_flight row).
GET /health: counts only. Logs: JSON lines on logger "relay", every secret and key redacted.

Tripwire (B-s2): logs relay_tripwire{reason} on HMAC failures (bad signature or stale timestamp) > 5 in 10 min
(`bad_sig`), a rate-limit hit (`rate_limited`), upstream 401/403 (`upstream_http_<code>`: key rotated/revoked) and
count drift (`double_forward`: a delivery forwarded again although an earlier forward may have started the routine,
accepted risk A). Every forward is recorded before it is sent and dropped again once the routine definitely did not
start, so a crash between upstream 2xx and Seen.add is still counted after restart. /health shows
double_forward_24h; >= 3 in 24 h is the signal to revisit option C (Rob 2026-10-28). Optional Mattermost alert
post (RELAY_ALERT_URL, RELAY_ALERT_TOKEN, RELAY_ALERT_CHANNEL = channel id; all three or none): one per reason per
10 min, for double_forward only from 3 in 24 h.
"""
import asyncio
import hashlib
import hmac
import json
import logging
import os
import re
import sqlite3
import sys
import threading
import time
from collections.abc import Mapping
from contextlib import asynccontextmanager
from dataclasses import dataclass

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

WINDOW_S = 300
MIN_SECRET = 32
SEEN_TTL_S = 24 * 3600
IN_FLIGHT_STALE_S = 60
PRUNE_EVERY_S = 3600
TRIP_WINDOW_S = 600
BAD_SIG_MAX = 5
BAD_SIG_BUCKET_S = 10    # HMAC failures counted in 10 s buckets: bounded state under a forged flood
DRIFT_ALERT = 3
ALERT_ENV = ("RELAY_ALERT_URL", "RELAY_ALERT_TOKEN", "RELAY_ALERT_CHANNEL")
FIELDS = ("HMAC_SECRET", "ROUTINE_URL", "ROUTINE_KEY")
_ENV_RE = re.compile(r"^RELAY_BOT_([A-Z0-9_]+)_(%s)$" % "|".join(FIELDS))


# --- logging with redaction ----------------------------------------------------------------------------------
_PATTERNS = [re.compile(r"(?i)bearer\s+\S+"), re.compile(r"(?i)(authorization['\"]?\s*[:=]\s*['\"]?)[^'\",}\s]+")]
_SECRETS: set[str] = set()


def register_secret(value: str) -> None:
    if isinstance(value, str) and len(value) >= 4:
        _SECRETS.add(value)


def redact(s: str) -> str:
    for p in _PATTERNS:
        s = p.sub(lambda m: (m.group(1) if m.groups() else "Bearer ") + "[REDACTED]", s)
    for v in sorted(_SECRETS, key=len, reverse=True):
        s = s.replace(v, "[REDACTED]")
    return s


class RedactFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg, record.args = redact(record.getMessage()), None
        if record.exc_info:
            record.exc_text = redact(logging.Formatter().formatException(record.exc_info))
            record.exc_info = None
        return True


log = logging.getLogger("relay")
log.setLevel(logging.INFO)
log.addFilter(RedactFilter())     # on the logger: every handler (stdout, test capture) sees redacted text


def _setup_stdout() -> None:
    if not any(getattr(h, "_relay", False) for h in log.handlers):
        h = logging.StreamHandler(sys.stdout)
        h._relay = True
        log.addHandler(h)


def _log(event: str, **fields) -> None:
    log.info(json.dumps({"event": event, **fields}))


# --- config --------------------------------------------------------------------------------------------------
class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class RelayBot:
    name: str
    hmac_secret: str
    routine_url: str
    routine_key: str


def _https_ok(url: str, allow_http: bool) -> bool:
    if url.startswith("https://") and len(url) > 8:
        return True
    return allow_http and url.startswith("http://") and len(url) > 7


def load_bots(env: Mapping[str, str]) -> dict[str, RelayBot]:
    """Bots from RELAY_BOT_<NAME>_* env vars. Errors name the bot and field, never a value."""
    raw: dict[str, dict[str, str]] = {}
    for k, v in env.items():
        m = _ENV_RE.match(k)
        if m:
            raw.setdefault(m.group(1).lower().replace("_", "-"), {})[m.group(2)] = (v or "").strip()
    allow_http = env.get("RELAY_ALLOW_HTTP_UPSTREAM", "").strip().lower() == "true"
    bots = {}
    for name, f in sorted(raw.items()):
        for field in FIELDS:
            if not f.get(field):
                raise ConfigError("bot %s: %s missing" % (name, field.lower()))
        if len(f["HMAC_SECRET"]) < MIN_SECRET:
            raise ConfigError("bot %s: hmac_secret must be at least %d characters" % (name, MIN_SECRET))
        if not _https_ok(f["ROUTINE_URL"], allow_http):
            raise ConfigError("bot %s: routine_url must be https" % name)
        bots[name] = RelayBot(name, f["HMAC_SECRET"], f["ROUTINE_URL"], f["ROUTINE_KEY"])
    return bots


# --- verify: COPY of app.wake.verify (ADR-0008); tests/unit/test_relay.py guards against drift -----------------
def _mac(secret: str, ts: str, body: bytes) -> str:
    return hmac.new(secret.encode(), ts.encode() + b"." + body, hashlib.sha256).hexdigest()


def verify(secret: str, headers: Mapping, body: bytes, now: int, window: int = WINDOW_S) -> bool:
    h = {k.lower(): v for k, v in headers.items()}
    sig, ts = h.get("x-mmb-signature"), h.get("x-mmb-timestamp")
    if not sig or not ts or not sig.startswith("v1="):
        return False
    try:
        t = int(ts)
    except ValueError:
        return False
    if abs(now - t) > window:
        return False
    if not hmac.compare_digest(sig[3:].encode(), _mac(secret, ts, body).encode()):
        return False
    # X-MMB-Delivery is not signed itself: it must equal the signed delivery_id, so a captured request
    # cannot be replayed under a new idempotency key (lb4 review 2 P2).
    try:
        signed_id = json.loads(body).get("delivery_id")
    except (ValueError, AttributeError):
        return False
    d = h.get("x-mmb-delivery")
    return bool(d) and isinstance(signed_id, str) and hmac.compare_digest(d.encode(), signed_id.encode())


def _reject_reason(headers: Mapping, now: int) -> str:
    """Reason for a failed verify: `stale` only when the timestamp itself is outside the window."""
    try:
        t = int(headers.get("x-mmb-timestamp", ""))
    except ValueError:
        return "bad_sig"
    return "stale" if abs(now - t) > WINDOW_S else "bad_sig"


def map_upstream(status: int | None) -> tuple[int, dict]:
    """Upstream routine status (None = timeout/connect error) -> relay response to mmbridge."""
    if status is not None and 200 <= status < 300:
        return 200, {"status": "forwarded"}
    if status is None or status in (408, 429) or status >= 500:
        return 503, {"reason": "upstream_unavailable", "upstream": status}
    return 424, {"upstream": status}


# --- persistent dedupe + in-flight rows ----------------------------------------------------------------------
class Seen:
    """sqlite (delivery_id PK, seen_at): deliveries the routine accepted (2xx); pruned after 24 h.
    in_flight rows guard a delivery while it is upstream; one relay process (single replica), so rows left by a
    previous process are cleared at start and rows older than IN_FLIGHT_STALE_S are taken over."""

    def __init__(self, path: str):
        self.path = path
        self._lock = threading.Lock()
        self._db = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
        self._db.execute("PRAGMA journal_mode=WAL")
        self._db.execute("CREATE TABLE IF NOT EXISTS seen (delivery_id TEXT PRIMARY KEY, seen_at INTEGER NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS in_flight (delivery_id TEXT PRIMARY KEY, "
                         "started_at INTEGER NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS forwards (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                         "delivery_id TEXT NOT NULL, at INTEGER NOT NULL)")
        self._db.execute("DELETE FROM in_flight")

    def _q(self, sql: str, args=()):
        with self._lock:
            return self._db.execute(sql, args)

    def has(self, d: str) -> bool:
        return self._q("SELECT 1 FROM seen WHERE delivery_id = ?", (d,)).fetchone() is not None

    def add(self, d: str, now: int) -> None:
        self._q("INSERT OR IGNORE INTO seen (delivery_id, seen_at) VALUES (?, ?)", (d, int(now)))

    def prune(self, now: int) -> int:
        self._q("DELETE FROM forwards WHERE at < ?", (int(now) - SEEN_TTL_S,))
        return self._q("DELETE FROM seen WHERE seen_at < ?", (int(now) - SEEN_TTL_S,)).rowcount

    # Forward rows (count drift): one per forward that may have started the routine.
    def forward_begin(self, d: str, now: int) -> int:
        """Recorded before the upstream call, so it survives a crash after the routine started."""
        return self._q("INSERT INTO forwards (delivery_id, at) VALUES (?, ?)", (d, int(now))).lastrowid

    def forward_not_started(self, row: int) -> None:
        """The routine definitely did not start (a non-2xx answer, or never reached): not a forward."""
        self._q("DELETE FROM forwards WHERE id = ?", (row,))

    def forwards_of(self, d: str, since: int) -> int:
        return self._q("SELECT COUNT(*) FROM forwards WHERE delivery_id = ? AND at >= ?",
                       (d, int(since))).fetchone()[0]

    def double_forwards_since(self, since: int) -> int:
        """Forwards beyond the first per delivery id: possible double wakes (accepted risk A)."""
        return self._q("SELECT COUNT(*) - COUNT(DISTINCT delivery_id) FROM forwards WHERE at >= ?",
                       (int(since),)).fetchone()[0]

    def count_since(self, since: int) -> int:
        return self._q("SELECT COUNT(*) FROM seen WHERE seen_at >= ?", (int(since),)).fetchone()[0]

    def claim(self, d: str, now: int) -> bool:
        with self._lock:
            self._db.execute("DELETE FROM in_flight WHERE delivery_id = ? AND started_at < ?",
                             (d, int(now) - IN_FLIGHT_STALE_S))
            return self._db.execute("INSERT OR IGNORE INTO in_flight VALUES (?, ?)", (d, int(now))).rowcount == 1

    def release(self, d: str) -> None:
        self._q("DELETE FROM in_flight WHERE delivery_id = ?", (d,))


class RateLimit:
    """Token bucket per bot: `burst` tokens, refilled at per_min/60 per second."""

    def __init__(self, per_min: float = 30, burst: int = 10):
        self.rate, self.burst = per_min / 60.0, burst
        self._b: dict[str, tuple[float, float]] = {}

    def allow(self, bot: str, now: float) -> bool:
        tokens, last = self._b.get(bot, (float(self.burst), now))
        tokens = min(float(self.burst), tokens + max(0.0, now - last) * self.rate)
        ok = tokens >= 1.0
        self._b[bot] = (tokens - 1.0 if ok else tokens, max(now, last))
        return ok


class _Counter:
    """Rejections per minute bucket, last 24 h (bounded memory under a flood)."""

    def __init__(self):
        self._m: dict[int, int] = {}

    def add(self, now: float) -> None:
        k = int(now) // 60
        self._m[k] = self._m.get(k, 0) + 1
        for old in [m for m in self._m if m < k - 24 * 60]:
            del self._m[old]

    def since(self, now: float) -> int:
        k = int(now) // 60
        return sum(v for m, v in self._m.items() if m > k - 24 * 60)


class Tripwire:
    """relay_tripwire{reason} log + optional alert(reason, fields), throttled to one alert per reason per 10 min."""

    def __init__(self, clock, alert=None):
        self.clock, self.alert = clock, alert
        self._bad: dict[int, int] = {}            # 10 s bucket -> HMAC failures (window: TRIP_WINDOW_S)
        self._alerted: dict[str, float] = {}

    def _trip(self, reason: str, alert: bool = True, **fields) -> None:
        now = self.clock()
        _log("relay_tripwire", reason=reason, **fields)
        if not alert or self.alert is None:
            return
        last = self._alerted.get(reason)
        if last is not None and now - last < TRIP_WINDOW_S:
            return
        self._alerted[reason] = now
        self.alert(reason, fields)

    def bad_sig_count(self) -> int:
        """HMAC failures in the last 10 min (bucket granularity); drops buckets that left the window."""
        k = int(self.clock()) // BAD_SIG_BUCKET_S
        for old in [b for b in self._bad if b <= k - TRIP_WINDOW_S // BAD_SIG_BUCKET_S]:
            del self._bad[old]
        return sum(self._bad.values())

    def bad_sig(self, bot: str) -> None:
        k = int(self.clock()) // BAD_SIG_BUCKET_S
        self._bad[k] = self._bad.get(k, 0) + 1
        n = self.bad_sig_count()
        if n > BAD_SIG_MAX:
            self._trip("bad_sig", bot=bot, failures_10m=n)

    def rate_limited(self, bot: str) -> None:
        self._trip("rate_limited", bot=bot)

    def upstream_denied(self, bot: str, code: int) -> None:
        self._trip("upstream_http_%d" % code, bot=bot)

    def double_forward(self, bot: str, delivery: str, count_24h: int) -> None:
        self._trip("double_forward", alert=count_24h >= DRIFT_ALERT, bot=bot, delivery=delivery,
                   double_forward_24h=count_24h)


def _alerter(env: Mapping[str, str], http: httpx.AsyncClient):
    """Mattermost alert post from RELAY_ALERT_* (all three or none). Fire and forget: never blocks a wake."""
    vals = {k: (env.get(k) or "").strip() for k in ALERT_ENV}
    if not any(vals.values()):
        return None
    if not all(vals.values()):
        raise ConfigError("alert: set all of %s or none" % ", ".join(ALERT_ENV))
    url, token, channel = (vals[k] for k in ALERT_ENV)
    if not _https_ok(url, allow_http=True):
        raise ConfigError("alert: RELAY_ALERT_URL must be http(s)")
    register_secret(token)
    tasks: set = set()

    async def post(reason: str, fields: dict) -> None:
        detail = ", ".join("%s=%s" % kv for kv in sorted(fields.items()))
        msg = "mmbridge relay tripwire: %s (%s). See the relay logs (relay_tripwire); runbook: relay/README.md." % (
            reason, detail)
        try:
            r = await http.post(url.rstrip("/") + "/api/v4/posts", json={"channel_id": channel, "message": msg},
                                headers={"Authorization": "Bearer " + token}, timeout=5)
            if r.status_code >= 300:
                _log("relay_alert_failed", reason=reason, status=r.status_code)
        except Exception as e:                    # type only: messages may carry request details
            _log("relay_alert_failed", reason=reason, error=type(e).__name__)

    def alert(reason: str, fields: dict) -> None:
        t = asyncio.get_running_loop().create_task(post(reason, fields))
        tasks.add(t)
        t.add_done_callback(tasks.discard)
    return alert


class _Relay:
    def __init__(self, bots, http, clock, seen, rate, timeout_s, tripwire=None):
        self.bots, self.http, self.clock, self.seen, self.rate = bots, http, clock, seen, rate
        self.timeout_s = timeout_s
        self.tripwire = tripwire or Tripwire(clock)
        self.rejected = _Counter()
        self._locks: dict[str, list] = {}     # delivery id -> [asyncio.Lock, holders+waiters]
        self._pruned_at = None

    def pending(self, d: str) -> int:
        """Requests holding or waiting for the in-flight lock of delivery `d` (tests use it as a barrier)."""
        return self._locks.get(d, [None, 0])[1]

    def _reject(self, now, bot, reason, status, body=None, **fields):
        self.rejected.add(now)
        _log("relay_rejected", bot=bot, reason=reason, **fields)
        return JSONResponse(body or {"reason": reason}, status_code=status)

    async def wake(self, bot_name: str, request: Request):
        now = self.clock()
        bot = self.bots.get(bot_name)
        if bot is None:
            return self._reject(now, None, "unknown_bot", 404)
        body = await request.body()
        if not verify(bot.hmac_secret, request.headers, body, int(now)):
            resp = self._reject(now, bot.name, _reject_reason(request.headers, int(now)), 401)
            self.tripwire.bad_sig(bot.name)
            return resp
        d = request.headers["x-mmb-delivery"]
        if self._pruned_at is None or now - self._pruned_at >= PRUNE_EVERY_S:
            self.seen.prune(int(now))
            self._pruned_at = now
        entry = self._locks.setdefault(d, [asyncio.Lock(), 0])
        entry[1] += 1
        try:
            async with entry[0]:
                return await self._deliver(bot, d, body, now)
        finally:
            entry[1] -= 1
            if entry[1] == 0:
                self._locks.pop(d, None)

    async def _deliver(self, bot: RelayBot, d: str, body: bytes, now: float):
        if self.seen.has(d):
            return self._reject(now, bot.name, "duplicate", 200, {"status": "duplicate"}, delivery=d)
        if not self.seen.claim(d, int(now)):         # another relay process holds it: let mmbridge retry
            return self._reject(now, bot.name, "in_flight", 503, delivery=d)
        try:
            if not self.rate.allow(bot.name, now):
                resp = self._reject(now, bot.name, "rate_limited", 429, delivery=d)
                self.tripwire.rate_limited(bot.name)
                return resp
            row = self.seen.forward_begin(d, int(now))
            status, err = await self._forward(bot, d, body)
            if status is not None and 200 <= status < 300:
                self.seen.add(d, int(self.clock()))   # only after upstream 2xx (accepted risk A)
                _log("relay_forwarded", bot=bot.name, delivery=d, upstream=status)
                since = int(self.clock()) - SEEN_TTL_S
                if self.seen.forwards_of(d, since) > 1:
                    self.tripwire.double_forward(bot.name, d, self.seen.double_forwards_since(since))
            else:
                if err not in (None, "connect"):
                    _log("relay_delivery_ambiguous", bot=bot.name, delivery=d, error=err)
                else:                                 # an answer, or never reached: the routine did not start
                    self.seen.forward_not_started(row)
                _log("relay_upstream", bot=bot.name, delivery=d, code=err or status)
                if status in (401, 403):
                    self.tripwire.upstream_denied(bot.name, status)
            code, payload = map_upstream(status)
            return JSONResponse(payload, status_code=code)
        finally:
            self.seen.release(d)

    async def _forward(self, bot: RelayBot, d: str, body: bytes) -> tuple[int | None, str | None]:
        headers = {"Authorization": "Bearer " + bot.routine_key, "Content-Type": "application/json",
                   "X-MMB-Delivery": d}
        try:
            r = await asyncio.wait_for(
                self.http.post(bot.routine_url, content=body, headers=headers, timeout=self.timeout_s),
                self.timeout_s)
            return r.status_code, None
        except (httpx.ConnectError, httpx.ConnectTimeout):
            return None, "connect"                    # never reached the routine: not ambiguous
        except (httpx.TimeoutException, asyncio.TimeoutError):
            return None, "timeout"                    # may have started the routine: ambiguous
        except Exception as e:                        # type only: messages may carry request details
            return None, "error_" + type(e).__name__

    def health(self) -> dict:
        now = self.clock()
        return {"ok": True, "bots": len(self.bots), "forwarded_24h": self.seen.count_since(int(now) - SEEN_TTL_S),
                "rejected_24h": self.rejected.since(now),
                "double_forward_24h": self.seen.double_forwards_since(int(now) - SEEN_TTL_S)}


def create_app(env: Mapping[str, str] | None = None, http: httpx.AsyncClient | None = None, clock=time.time,
               seen: Seen | None = None) -> FastAPI:
    """App factory (`uvicorn relay:create_app --factory`). Raises ConfigError on bad bot env (fail fast)."""
    env = os.environ if env is None else env
    _setup_stdout()
    bots = load_bots(env)
    for b in bots.values():
        register_secret(b.hmac_secret)
        register_secret(b.routine_key)
    if seen is None:
        seen = Seen(os.path.join(env.get("RELAY_DATA_DIR", "/data"), "relay.db"))
    rate = RateLimit(float(env.get("RELAY_RATE_PER_MIN", "30")), int(env.get("RELAY_BURST", "10")))
    own_http = http is None
    client = http or httpx.AsyncClient()
    tripwire = Tripwire(clock, alert=_alerter(env, client))
    relay = _Relay(bots, client, clock, seen, rate, float(env.get("RELAY_UPSTREAM_TIMEOUT_S", "5")), tripwire)

    @asynccontextmanager
    async def lifespan(_app):
        _log("relay_start", bots=len(bots))
        yield
        if own_http:
            await client.aclose()

    app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
    app.state.relay = relay

    @app.post("/wake/{bot}")
    async def wake(bot: str, request: Request):
        return await relay.wake(bot, request)

    @app.get("/health")
    async def health():
        return relay.health()

    return app
