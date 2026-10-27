"""Signed wake webhook (ADR-0008): sign/verify and the Dispatcher that delivers queued wakes from state.db.

POST <wake_url> with the wake payload as raw JSON body and headers X-MMB-Delivery (post id, idempotency key),
X-MMB-Timestamp (unix seconds), X-MMB-Signature `v1=<hex HMAC-SHA256(secret, ts + "." + body)>`.
Receivers: `verify(secret, headers, raw_body, now)`; constant-time, rejects |now - ts| > 300 s, unknown versions
and missing headers.

Dispatcher.tick(): heartbeat the single-owner lease (standby while another owner is fresh), recover_stale,
prune (start + every 6 h), claim_due up to 4 and POST them concurrently (5 s timeout). Config is read at
send time (url/secret rotation applies to queued wakes); wakes of a previous bot user fail `bot_rotated`.
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
from app.state import next_delay

WINDOW_S = 300
TIMEOUT_S = 5
CONCURRENCY = 4
PRUNE_EVERY_S = 6 * 3600
POLL_S = 0.5


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
    return hmac.compare_digest(sig[3:].encode(), _mac(secret, ts, body).encode())


def _log(event: str, **fields) -> None:
    mlog.log.info(json.dumps({"event": event, **fields}))


class Dispatcher:
    def __init__(self, state, cfg, http: httpx.AsyncClient, max_attempts: int | None = None, clock=None,
                 poll_s: float = POLL_S, concurrency: int = CONCURRENCY):
        """cfg: BotConfig or a zero-arg callable returning the current one (read at every send, PR-2)."""
        self.state, self.http = state, http
        self._cfg = cfg if callable(cfg) else (lambda: cfg)
        if max_attempts:
            state.max_attempts = max_attempts
        self.clock = clock or state.clock
        self.poll_s, self.concurrency = poll_s, concurrency
        self.owner = None
        self._pruned_at = None

    async def run(self) -> None:
        while True:
            if not await self.tick():
                await asyncio.sleep(self.poll_s)

    async def tick(self) -> int:
        """One loop pass; returns the number of wakes attempted."""
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
        due = await asyncio.to_thread(st.claim_due, now, self.concurrency)
        if due:
            bot_id = await asyncio.to_thread(st.get_meta, "bot_user_id")
            await asyncio.gather(*(self._send(w, bot_id) for w in due))
        return len(due)

    async def _send(self, w, bot_id: str | None) -> None:
        st = self.state
        if bot_id and (w.payload.get("bot") or {}).get("user_id") != bot_id:
            await asyncio.to_thread(st.mark_failed, w.post_id, "bot_rotated")
            _log("wake_failed", post_id=w.post_id, attempt=w.attempts, error="bot_rotated")
            return
        cfg = self._cfg()
        body = json.dumps({**w.payload, "attempt": w.attempts}, separators=(",", ":")).encode()
        ts = int(self.clock())
        headers = {"Content-Type": "application/json", "X-MMB-Delivery": w.post_id,
                   "X-MMB-Timestamp": str(ts), "X-MMB-Signature": sign(cfg.wake_secret, ts, body)}
        try:
            r = await self.http.post(cfg.wake_url, content=body, headers=headers, timeout=TIMEOUT_S)
            status, err = r.status_code, "http_%d" % r.status_code
        except httpx.TimeoutException:
            status, err = None, "timeout"
        except httpx.TransportError:
            status, err = None, "connect"
        if status is not None and 200 <= status < 300:
            await asyncio.to_thread(st.mark_delivered, w.post_id)
            fields = {"post_id": w.post_id, "attempt": w.attempts}
            if w.post_create_at:
                fields["latency_ms"] = int(self.clock() * 1000) - w.post_create_at
            _log("wake_delivered", **fields)
        elif status is None or status in (408, 429) or status >= 500:
            res = await asyncio.to_thread(st.mark_retry, w.post_id, err, self.clock() + next_delay(w.attempts))
            _log("wake_failed" if res == "failed" else "wake_retry", post_id=w.post_id, attempt=w.attempts,
                 error=err)
        else:
            await asyncio.to_thread(st.mark_failed, w.post_id, err)
            _log("wake_failed", post_id=w.post_id, attempt=w.attempts, error=err)
