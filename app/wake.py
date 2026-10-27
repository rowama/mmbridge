"""Signed wake webhook (ADR-0008): sign/verify and the Dispatcher that delivers queued wakes from state.db.

POST <wake_url> with the wake payload as raw JSON body and headers X-MMB-Delivery (post id, idempotency key),
X-MMB-Timestamp (unix seconds), X-MMB-Signature `v1=<hex HMAC-SHA256(secret, ts + "." + body)>`.
Receivers: `verify(secret, headers, raw_body, now)`; constant-time, rejects |now - ts| > 300 s, an X-MMB-Delivery that is missing or differs from the signed delivery_id, unknown versions
and missing headers.

Dispatcher.tick(): heartbeat the single-owner lease (standby while another owner is fresh), recover_stale,
prune (start + every 6 h), claim_due up to 4 and POST them concurrently (5 s timeout). Config is read at
send time (url/secret rotation applies to queued wakes); wakes of a previous bot user fail `bot_rotated`.
Nothing is claimed until the listener has resolved the identity of the CURRENT token (meta bot_identity =
"<token_fp>:<bot_user_id>", one row, matches the config), so a stale id from a previous token/run never approves old wakes (review P1).
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
from app.state import next_delay

WINDOW_S = 300
TIMEOUT_S = 5
CONCURRENCY = 4
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
        self._waiting = False

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
        cfg = self._cfg()
        # One meta row "<token_fp>:<bot_user_id>", written in one statement by the listener: the id and the
        # token it belongs to are always read as one snapshot (review 3 P2: no split-read race on rotation).
        fp, _, bot_id = (await asyncio.to_thread(st.get_meta, "bot_identity") or "").partition(":")
        if not bot_id or fp != token_fp(cfg.token):
            if not self._waiting:
                _log("dispatcher_waiting_identity", instance=st.instance_id)
                self._waiting = True
            return 0
        self._waiting = False
        due = await asyncio.to_thread(st.claim_due, now, self.concurrency)
        if due:
            await asyncio.gather(*(self._send(w, bot_id, cfg) for w in due))
        return len(due)

    async def _send(self, w, bot_id: str, cfg) -> None:
        st = self.state
        if (w.payload.get("bot") or {}).get("user_id") != bot_id:
            await asyncio.to_thread(st.mark_failed, w.post_id, "bot_rotated")
            _log("wake_failed", post_id=w.post_id, attempt=w.attempts, error="bot_rotated")
            return
        body = json.dumps({**w.payload, "attempt": w.attempts}, separators=(",", ":")).encode()
        ts = int(self.clock())
        headers = {"Content-Type": "application/json", "X-MMB-Delivery": w.post_id,
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
