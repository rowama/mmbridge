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
        self._db.execute("DELETE FROM in_flight")

    def _q(self, sql: str, args=()):
        with self._lock:
            return self._db.execute(sql, args)

    def has(self, d: str) -> bool:
        return self._q("SELECT 1 FROM seen WHERE delivery_id = ?", (d,)).fetchone() is not None

    def add(self, d: str, now: int) -> None:
        self._q("INSERT OR IGNORE INTO seen (delivery_id, seen_at) VALUES (?, ?)", (d, int(now)))

    def prune(self, now: int) -> int:
        return self._q("DELETE FROM seen WHERE seen_at < ?", (int(now) - SEEN_TTL_S,)).rowcount

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


class _Relay:
    def __init__(self, bots, http, clock, seen, rate, timeout_s):
        self.bots, self.http, self.clock, self.seen, self.rate = bots, http, clock, seen, rate
        self.timeout_s = timeout_s
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
            return self._reject(now, bot.name, _reject_reason(request.headers, int(now)), 401)
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
                return self._reject(now, bot.name, "rate_limited", 429, delivery=d)
            status, err = await self._forward(bot, d, body)
            if status is not None and 200 <= status < 300:
                self.seen.add(d, int(self.clock()))   # only after upstream 2xx (accepted risk A)
                _log("relay_forwarded", bot=bot.name, delivery=d, upstream=status)
            else:
                if err not in (None, "connect"):
                    _log("relay_delivery_ambiguous", bot=bot.name, delivery=d, error=err)
                _log("relay_upstream", bot=bot.name, delivery=d, code=err or status)
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
                "rejected_24h": self.rejected.since(now)}


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
    relay = _Relay(bots, client, clock, seen, rate, float(env.get("RELAY_UPSTREAM_TIMEOUT_S", "5")))

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
