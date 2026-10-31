"""Signed wake webhook (ADR-0008): sign/verify and the Dispatcher that delivers queued wakes from state.db.

POST <wake_url> with the wake payload as raw JSON body and headers X-MMB-Delivery (delivery id, idempotency key),
X-MMB-Timestamp (unix seconds), X-MMB-Signature `v1=<hex HMAC-SHA256(secret, ts + "." + body)>`.
Receivers: `verify(secret, headers, raw_body, now)`; constant-time, rejects |now - ts| > 300 s, an X-MMB-Delivery that is missing or differs from the signed delivery_id, unknown versions
and missing headers.

Dispatcher (B-s3: ONE shared dispatcher for every bot, ADR-0014): each pass heartbeats the single-owner lease
(standby while another owner is fresh), recover_stale, prune (start + every 6 h), then per bot with due rows
(round robin) claims up to its free in-flight slots (per-bot cap 2, total cap 4) and POSTs them as background
tasks (5 s timeout), so a dead target holds at most its own 2 slots and never delays other bots (B8 fairness).
`tick()` is one pass that also waits for its sends (tests). Config is read per row at send time from the current
Store (url/secret rotation applies to queued wakes); rows of a bot no longer in the store fail `bot_removed`;
wakes of a previous bot user fail `bot_rotated`. Nothing of a bot is claimed until its listener has resolved the
identity of the CURRENT token (meta bot:<name>:identity = "<token_fp>:<bot_user_id>", one row, matches the
config), so a stale id from a previous token/run never approves old wakes (review P1).
X-MMB-Delivery = the signed payload's delivery_id ("<bot>:<post_id>").
Each POST has an overall deadline of TIMEOUT_S (not only per network step), so a slow-drip receiver cannot
stall the loop and the owner heartbeat (review P2).
2xx delivered; 408/429/5xx/timeout/connect retry (state.next_delay; failed after max attempts); other 4xx
failed. Logs carry post id, attempt and error class only: never token, secret, signature or message text.
"""
import asyncio
import hashlib
import hmac
import json
import time
from collections.abc import Mapping

import httpx

from app import logging as mlog
from app.state import meta_key, next_delay

WINDOW_S = 300
TIMEOUT_S = 5
CONCURRENCY = 4          # total in flight
PER_BOT_IN_FLIGHT = 2    # per bot (fairness: one dead target cannot take every slot)
PRUNE_EVERY_S = 6 * 3600
POLL_S = 0.5


def token_fp(token: str) -> str:
    """Non-secret fingerprint of the bot token, stored with bot_user_id in meta bot_identity by the listener."""
    return hashlib.sha256(("mmb-token-fp:" + token).encode()).hexdigest()[:16]


def _mac(secret: str, ts: str, body: bytes) -> str:
    return hmac.new(secret.encode(), ts.encode() + b"." + body, hashlib.sha256).hexdigest()


def sign(secret: str, ts: int, body: bytes) -> str:
    return "v1=" + _mac(secret, str(ts), body)


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


def _log(event: str, **fields) -> None:
    mlog.log.info(json.dumps({"event": event, **fields}))


class Dispatcher:
    def __init__(self, state, cfg, http: httpx.AsyncClient, max_attempts: int | None = None, clock=None,
                 poll_s: float = POLL_S, concurrency: int = CONCURRENCY, per_bot_in_flight: int = PER_BOT_IN_FLIGHT):
        """state: State (all bots). cfg: Store or a zero-arg callable returning the current one (read per send, PR-2)."""
        self.state, self.http = state, http
        self._cfg = cfg if callable(cfg) else (lambda: cfg)
        if max_attempts:
            state.max_attempts = max_attempts
        self.clock = clock or state.clock
        self.poll_s, self.concurrency, self.per_bot = poll_s, concurrency, per_bot_in_flight
        self.owner = None
        self._pruned_at = None
        self._waiting: set = set()
        self._inflight: dict = {}          # bot -> set of send tasks
        self._rr = 0

    def in_flight(self, bot: str | None = None) -> int:
        if bot is not None:
            return len(self._inflight.get(bot, ()))
        return sum(len(t) for t in self._inflight.values())

    def _tasks(self) -> list:
        return [t for ts in self._inflight.values() for t in ts]

    async def run(self) -> None:
        try:
            while True:
                if not await self._pass():
                    await asyncio.sleep(self.poll_s)
        finally:
            tasks = self._tasks()
            for t in tasks:
                t.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)   # claims stay in_flight: lease recovery

    async def tick(self) -> int:
        """One pass that also waits for the sends it started; returns the number of wakes attempted."""
        n = await self._pass()
        await self.drain()
        return n

    async def drain(self) -> None:
        tasks = self._tasks()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _pass(self) -> int:
        st, now = self.state, self.clock()
        owner = await asyncio.to_thread(st.claim_owner, now)
        if owner != self.owner:
            _log("dispatcher_owner" if owner else "dispatcher_standby", instance=st.instance_id)
            self.owner = owner
        if not owner:
            return 0
        await asyncio.to_thread(st.recover_stale, now)
        if self._pruned_at is None or now - self._pruned_at >= PRUNE_EVERY_S:
            n = await asyncio.to_thread(st.prune, 7)
            self._pruned_at = now
            _log("wakes_pruned", count=n)
        bots = self._cfg().bots
        due = await asyncio.to_thread(st.due_bots, now)
        if due:                                   # round robin: a different bot goes first each pass
            k = self._rr % len(due)
            due, self._rr = due[k:] + due[:k], self._rr + 1
        started = 0
        for name in due:
            if name not in bots:
                for w in await asyncio.to_thread(st.claim_due, now, 50, name):
                    await asyncio.to_thread(st.mark_failed, w.bot, w.post_id, "bot_removed")
                    _log("wake_failed", bot=w.bot, post_id=w.post_id, attempt=w.attempts, error="bot_removed")
                    started += 1
                continue
            free = min(self.per_bot - self.in_flight(name), self.concurrency - self.in_flight())
            if free <= 0:
                continue
            bot_id = await self._identity(name, bots[name])
            if not bot_id:
                continue
            for w in await asyncio.to_thread(st.claim_due, now, free, name):
                t = asyncio.create_task(self._send(w, bot_id, bots[name]))
                ts = self._inflight.setdefault(name, set())
                ts.add(t)
                t.add_done_callback(ts.discard)
                t.add_done_callback(lambda t, w=w: self._crashed(t, w))
                started += 1
        return started

    @staticmethod
    def _crashed(t: asyncio.Task, w) -> None:
        """A send that raised (e.g. state.db error marking the result): log it; the row stays in_flight and
        recover_stale retries it after the lease (was a dispatcher crash before sends ran in the background)."""
        if not t.cancelled() and t.exception() is not None:
            mlog.log.error(json.dumps({"event": "wake_send_crashed", "bot": w.bot, "post_id": w.post_id,
                                       "error": type(t.exception()).__name__}))

    async def _identity(self, name: str, entry) -> str | None:
        # One meta row "<token_fp>:<bot_user_id>" per bot, written in one statement by its listener: the id and the
        # token it belongs to are always read as one snapshot (review 3 P2: no split-read race on rotation).
        fp, _, bot_id = (await asyncio.to_thread(self.state.get_meta, meta_key(name, "identity")) or "").partition(":")
        if not bot_id or fp != token_fp(entry.token):
            if name not in self._waiting:
                _log("dispatcher_waiting_identity", bot=name, instance=self.state.instance_id)
                self._waiting.add(name)
            return None
        self._waiting.discard(name)
        return bot_id

    async def _send(self, w, bot_id: str, cfg) -> None:
        st, ids = self.state, {"bot": w.bot, "post_id": w.post_id}
        if (w.payload.get("bot") or {}).get("user_id") != bot_id:
            await asyncio.to_thread(st.mark_failed, w.bot, w.post_id, "bot_rotated")
            _log("wake_failed", **ids, attempt=w.attempts, error="bot_rotated")
            return
        body = json.dumps({**w.payload, "attempt": w.attempts}, separators=(",", ":")).encode()
        ts = int(self.clock())
        headers = {"Content-Type": "application/json", "X-MMB-Delivery": w.payload.get("delivery_id") or w.post_id,
                   "X-MMB-Timestamp": str(ts), "X-MMB-Signature": sign(cfg.wake_secret, ts, body)}
        try:
            r = await asyncio.wait_for(
                self.http.post(cfg.wake_url, content=body, headers=headers, timeout=TIMEOUT_S), TIMEOUT_S)
            status, err = r.status_code, "http_%d" % r.status_code
        except (httpx.TimeoutException, asyncio.TimeoutError):
            status, err = None, "timeout"
        except httpx.TransportError:
            status, err = None, "connect"
        except (httpx.InvalidURL, ValueError):   # malformed wake_url: permanent, never kills the loop (review 4 P2)
            status, err = 0, "invalid_url"
        except httpx.HTTPError:                  # e.g. DecodingError on a bad gzip body: retryable (review 5 P2)
            status, err = None, "http_error"
        except Exception as e:                   # last line: no send error may stop the dispatcher or strand a claim
            status, err = None, "error_" + type(e).__name__
        if status is not None and 200 <= status < 300:
            await asyncio.to_thread(st.mark_delivered, w.bot, w.post_id)
            fields = {**ids, "attempt": w.attempts}
            if w.post_create_at:
                fields["latency_ms"] = int(self.clock() * 1000) - w.post_create_at
            _log("wake_delivered", **fields)
        elif status is None or status in (408, 429) or status >= 500:
            res = await asyncio.to_thread(st.mark_retry, w.bot, w.post_id, err, self.clock() + next_delay(w.attempts))
            _log("wake_failed" if res == "failed" else "wake_retry", **ids, attempt=w.attempts, error=err)
        else:
            await asyncio.to_thread(st.mark_failed, w.bot, w.post_id, err)
            _log("wake_failed", **ids, attempt=w.attempts, error=err)
