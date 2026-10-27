"""Signed wake dispatcher (ADR-0008, plan Phase 4): sign/verify, delivery classes and backoff, the
signature as the receiver sees it (PR-5), crash recovery and single delivery (PR-1), runtime prune (PR-8),
config read at send time and bot rotation (PR-2), no token in payload/headers/logs (REQ-A7)."""
import asyncio
import hashlib
import hmac
import json
import logging

import httpx
import pytest

from app import store
from app.state import State
from app.store import BotConfig
from app.wake import Dispatcher, sign, token_fp, verify
from drivers.wake_receiver import WakeReceiver

TOKEN = "tok-eddie-" + "x" * 20
SECRET = "k" * 40
URL = "https://receiver.test/wake"


class Clock:
    def __init__(self, t=1_800_000_000.0):
        self.t = t

    def __call__(self):
        return self.t


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.delenv("WAKE_BACKOFF_SCALE", raising=False)
    monkeypatch.delenv("WAKE_MAX_ATTEMPTS", raising=False)


@pytest.fixture
def clk():
    return Clock()


@pytest.fixture
def state(tmp_path, clk):
    return State(str(tmp_path / "state.db"), clock=clk)


@pytest.fixture
def rx(clk):
    return WakeReceiver(SECRET, clock=clk)


def cfg(url=URL, secret=SECRET):
    return BotConfig(token=TOKEN, wake_url=url, wake_secret=secret, channels=["a" * 26])


def payload(post_id="p-1", bot_id="u-eddie"):
    return {"version": 1, "kind": "post", "delivery_id": post_id, "attempt": 1,
            "bot": {"user_id": bot_id, "username": "eddie"},
            "channel": {"id": "c-1", "name": "town-square", "display_name": "Town Square", "type": "O",
                        "team": "main"},
            "sender": {"user_id": "u-rob", "username": "rob"},
            "post": {"id": post_id, "message": "eddie is great", "create_at": "2027-01-15T08:00:00Z",
                     "root_id": None}}


def enqueue(state, post_id="p-1", bot_id="u-eddie"):
    state.enqueue(post_id, "c-1", payload(post_id, bot_id), post_create_at=1_800_000_000_000)


def resolve(state, bot_id="u-eddie", token=TOKEN):
    """What the listener records after users/me for the current token."""
    state.set_meta("bot_user_id", bot_id)
    state.set_meta("bot_token_fp", token_fp(token))


def dispatcher(state, http, c=None, clk=None, **kw):
    if state.get_meta("bot_token_fp") is None:
        resolve(state, state.get_meta("bot_user_id") or "u-eddie")
    return Dispatcher(state, c or cfg(), http, clock=clk or state.clock, **kw)


def client(transport):
    return httpx.AsyncClient(transport=transport)


def mock(status=None, exc=None, seen=None):
    def handler(request):
        if seen is not None:
            seen.append(request)
        if exc:
            raise exc("boom", request=request)
        return httpx.Response(status)
    return httpx.MockTransport(handler)


# --- sign / verify --------------------------------------------------------------------------------------------
def test_sign_known_vector():
    assert sign("k" * 32, 1700000000, b'{"a":1}') == \
        "v1=6935b796c0fec66e5dee52c86c7fd1218a424c32f1adb239ff2893c31e54f033"


def _headers(ts, body, secret=SECRET, **over):
    h = {"X-MMB-Delivery": "p-1", "X-MMB-Timestamp": str(ts), "X-MMB-Signature": sign(secret, ts, body)}
    h.update(over)
    return {k: v for k, v in h.items() if v is not None}


def test_verify_accepts_valid_and_edge_of_window():
    body, ts = b'{"x":1}', 1_800_000_000
    assert verify(SECRET, _headers(ts, body), body, ts)
    assert verify(SECRET, _headers(ts, body), body, ts + 300)
    assert verify(SECRET, _headers(ts, body), body, ts - 300)
    lower = {k.lower(): v for k, v in _headers(ts, body).items()}
    assert verify(SECRET, lower, body, ts)


@pytest.mark.parametrize("case", ["bad_sig", "tampered_body", "tampered_ts", "skew_301", "future_301", "v2",
                                  "no_sig", "no_ts", "bad_ts", "wrong_secret"])
def test_verify_rejects(case):
    body, ts = b'{"x":1}', 1_800_000_000
    h, b, now, secret = _headers(ts, body), body, ts, SECRET
    if case == "bad_sig":
        h["X-MMB-Signature"] = "v1=" + "0" * 64
    elif case == "tampered_body":
        b = b'{"x":2}'
    elif case == "tampered_ts":
        h["X-MMB-Timestamp"] = str(ts + 1)
    elif case == "skew_301":
        now = ts + 301
    elif case == "future_301":
        now = ts - 301
    elif case == "v2":
        h["X-MMB-Signature"] = "v2=" + h["X-MMB-Signature"][3:]
    elif case == "no_sig":
        del h["X-MMB-Signature"]
    elif case == "no_ts":
        del h["X-MMB-Timestamp"]
    elif case == "bad_ts":
        h["X-MMB-Timestamp"] = "soon"
    else:
        secret = "z" * 40
    assert not verify(secret, h, b, now)


# --- delivery ---------------------------------------------------------------------------------------------------
async def test_delivered_request_is_signed_as_receiver_recomputes(state, rx, clk):
    enqueue(state)
    async with client(rx.transport()) as http:
        assert await dispatcher(state, http).tick() == 1
    assert state.wake("p-1").status == "delivered"
    [req] = rx.requests
    h, body = req["headers"], req["body"]
    assert req["status"] == 204 and h["x-mmb-delivery"] == "p-1"
    assert h["content-type"] == "application/json"
    ts = int(h["x-mmb-timestamp"])
    assert abs(ts - clk()) <= 5
    expected = hmac.new(SECRET.encode(), h["x-mmb-timestamp"].encode() + b"." + body, hashlib.sha256).hexdigest()
    assert h["x-mmb-signature"] == "v1=" + expected          # body as received == the signed bytes
    sent = json.loads(body)
    assert sent["delivery_id"] == "p-1" and sent["attempt"] == 1 and sent["post"]["message"] == "eddie is great"


async def test_request_uses_5s_timeout(state):
    seen = []
    enqueue(state)
    async with client(mock(204, seen=seen)) as http:
        await dispatcher(state, http).tick()
    assert seen[0].extensions["timeout"] == {"connect": 5, "read": 5, "write": 5, "pool": 5}


@pytest.mark.parametrize("status", [200, 201, 202, 204])
async def test_2xx_is_delivered(state, status):
    enqueue(state)
    async with client(mock(status)) as http:
        await dispatcher(state, http).tick()
    w = state.wake("p-1")
    assert w.status == "delivered" and w.delivered_at is not None


@pytest.mark.parametrize("status,exc,err", [(503, None, "http_503"), (500, None, "http_500"),
                                            (429, None, "http_429"), (408, None, "http_408"),
                                            (None, httpx.ReadTimeout, "timeout"),
                                            (None, httpx.ConnectError, "connect")])
async def test_retryable_backs_off_2_4_8_16_32_then_fails(state, clk, caplog, status, exc, err):
    enqueue(state)
    t0 = clk.t
    async with client(mock(status, exc)) as http:
        d = dispatcher(state, http)
        for delay in (2, 4, 8, 16):
            assert await d.tick() == 1
            w = state.wake("p-1")
            assert (w.status, w.last_error, w.next_at) == ("retry", err, clk.t + delay)
            clk.t += delay - 1
            assert await d.tick() == 0                   # not due yet
            clk.t += 1
        with caplog.at_level(logging.INFO, logger="mmbridge"):
            assert await d.tick() == 1
    w = state.wake("p-1")
    assert (w.status, w.attempts, w.last_error) == ("failed", 5, err)
    assert clk.t - t0 == 2 + 4 + 8 + 16
    failed = [json.loads(r.getMessage()) for r in caplog.records if "wake_failed" in r.getMessage()]
    assert failed == [{"event": "wake_failed", "post_id": "p-1", "attempt": 5, "error": err}]


@pytest.mark.parametrize("status", [400, 401, 403, 404, 410])
async def test_other_4xx_is_permanent(state, status, caplog):
    enqueue(state)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with client(mock(status)) as http:
            await dispatcher(state, http).tick()
    w = state.wake("p-1")
    assert (w.status, w.attempts, w.last_error) == ("failed", 1, "http_%d" % status)
    assert any("wake_failed" in r.getMessage() for r in caplog.records)


async def test_receiver_rejecting_signature_is_permanent_failure(state, rx):
    enqueue(state)
    async with client(rx.transport()) as http:
        await dispatcher(state, http, c=cfg(secret="w" * 40)).tick()
    assert rx.requests[0]["status"] == 401
    w = state.wake("p-1")
    assert (w.status, w.last_error) == ("failed", "http_401")


async def test_attempt_number_is_sent_and_signed(state, rx, clk):
    enqueue(state)
    rx.down = True
    async with client(rx.transport()) as http:
        d = dispatcher(state, http)
        await d.tick()
        rx.down = False
        clk.t += 2
        await d.tick()
    bodies = [json.loads(r["body"]) for r in rx.requests]
    assert [b["attempt"] for b in bodies] == [1, 2]
    assert rx.requests[1]["status"] == 204


async def test_concurrency_4(state):
    for i in range(6):
        enqueue(state, "p-%d" % i)
    inflight, peak, gate = [0], [0], asyncio.Event()

    async def handler(request):
        inflight[0] += 1
        peak[0] = max(peak[0], inflight[0])
        await gate.wait()
        inflight[0] -= 1
        return httpx.Response(204)
    async with client(httpx.MockTransport(handler)) as http:
        t = asyncio.create_task(dispatcher(state, http).tick())
        for _ in range(200):
            if inflight[0] >= 4:
                break
            await asyncio.sleep(0.01)
        await asyncio.sleep(0.05)                        # a 5th request would arrive now
        gate.set()
        assert await t == 4
    assert peak[0] == 4


async def test_token_never_in_payload_headers_or_logs(state, rx, caplog):
    enqueue(state)
    enqueue(state, "p-2")
    rx.down = True
    with caplog.at_level(logging.DEBUG):
        async with client(rx.transport()) as http:
            d = dispatcher(state, http)
            await d.tick()
            rx.down = False
            state.clock.t += 2
            await d.tick()
    assert len(rx.requests) == 4
    for r in rx.requests:
        assert TOKEN not in r["body"].decode() and TOKEN not in json.dumps(r["headers"])
    text = "\n".join(r.getMessage() for r in caplog.records)
    assert TOKEN not in text and SECRET not in text and "eddie is great" not in text


# --- PR-1: crash recovery, single owner -----------------------------------------------------------------------
async def test_crash_mid_post_redelivers_exactly_once_after_restart(tmp_path, clk, rx):
    path = str(tmp_path / "state.db")
    s1 = State(path, instance_id="d1", clock=clk)
    enqueue(s1)
    rx.hang = asyncio.Event()
    async with client(rx.transport()) as http:
        t = asyncio.create_task(dispatcher(s1, http).tick())
        for _ in range(100):
            if rx.requests:
                break
            await asyncio.sleep(0.01)
        t.cancel()
        with pytest.raises(asyncio.CancelledError):
            await t
        assert s1.wake("p-1").status == "in_flight"
        rx.hang = None
        clk.t += 61                                     # lease (30 s) and owner heartbeat (60 s) expired
        s2 = State(path, instance_id="d2", clock=clk)
        d2 = dispatcher(s2, http)
        assert await d2.tick() == 1
        assert await d2.tick() == 0
    assert s2.wake("p-1").status == "delivered"
    assert list(rx.accepted) == ["p-1"]
    assert [r["status"] for r in rx.requests] == [None, 204]  # the cancelled one never answered


async def test_two_dispatchers_never_double_send(tmp_path, clk, rx):
    path = str(tmp_path / "state.db")
    s1, s2 = State(path, instance_id="d1", clock=clk), State(path, instance_id="d2", clock=clk)
    for i in range(10):
        enqueue(s1, "p-%d" % i)
    async with client(rx.transport()) as http:
        d1, d2 = dispatcher(s1, http), dispatcher(s2, http)
        for _ in range(4):
            await asyncio.gather(d1.tick(), d2.tick())
    assert len(rx.requests) == 10 and len(rx.accepted) == 10
    assert sorted([d1.owner, d2.owner]) == [False, True]  # one owner; the other stands by


async def test_standby_takes_over_after_owner_heartbeat_expires(tmp_path, clk, rx):
    path = str(tmp_path / "state.db")
    s1, s2 = State(path, instance_id="d1", clock=clk), State(path, instance_id="d2", clock=clk)
    async with client(rx.transport()) as http:
        d1, d2 = dispatcher(s1, http), dispatcher(s2, http)
        await d1.tick()
        enqueue(s1)
        assert await d2.tick() == 0
        clk.t += 61
        assert await d2.tick() == 1
    assert d2.owner is True and list(rx.accepted) == ["p-1"]


async def test_run_loop_recovers_stale_and_delivers(tmp_path, clk, rx):
    path = str(tmp_path / "state.db")
    s1 = State(path, instance_id="dead", clock=clk)
    enqueue(s1)
    s1.claim_due(clk())                                  # crashed holder: in_flight with a lease
    clk.t += 31
    s2 = State(path, instance_id="new", clock=clk)
    async with client(rx.transport()) as http:
        task = asyncio.create_task(dispatcher(s2, http, poll_s=0.01).run())
        for _ in range(200):
            if rx.accepted:
                break
            await asyncio.sleep(0.01)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
    assert list(rx.accepted) == ["p-1"] and s2.wake("p-1").status == "delivered"


# --- PR-8: prune schedule -------------------------------------------------------------------------------------
def age(state, post_id, days):
    state._conn.execute("UPDATE wakes SET updated_at=updated_at-? WHERE post_id=?", (days * 86400, post_id))


async def test_prune_runs_at_start_and_every_6h(state, clk, rx):
    enqueue(state, "a")
    state.claim_due(clk())
    state.mark_failed("a", "http_404")
    age(state, "a", 8)
    async with client(rx.transport()) as http:
        d = dispatcher(state, http)
        enqueue(state, "b")
        await d.tick()                                   # start: prunes 8-day-old "a", delivers "b"
        assert state.wake("a") is None and state.wake("b").status == "delivered"
        age(state, "b", 8)
        clk.t += 6 * 3600 - 1
        await d.tick()
        assert state.wake("b") is not None               # next prune not due yet
        clk.t += 1
        await d.tick()                                   # 6 h after the start prune
    assert state.wake("b") is None


# --- PR-2: config at send time, bot rotation -----------------------------------------------------------------
async def test_secret_and_url_rotated_after_enqueue_use_new_values(tmp_path, state, clk, monkeypatch):
    from cryptography.fernet import Fernet
    monkeypatch.setenv("LIVE_ALLOW_HTTP_WAKE", "false")
    key, path = Fernet.generate_key().decode(), str(tmp_path / "bots.enc")
    store.save(path, key, cfg())
    new_rx = WakeReceiver("n" * 40, clock=clk)
    old_rx = WakeReceiver(SECRET, clock=clk)

    def route(request):
        rx = new_rx if request.url.host == "new.test" else old_rx
        return rx
    enqueue(state)

    class T(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return await route(request).transport().handle_async_request(request)
    async with client(T()) as http:
        d = dispatcher(state, http, c=lambda: store.load(path, key))
        store.save(path, key, cfg(url="https://new.test/wake", secret="n" * 40))
        await d.tick()
    assert old_rx.requests == [] and list(new_rx.accepted) == ["p-1"]
    assert state.wake("p-1").status == "delivered"


async def test_bot_rotated_fails_old_wakes(state, rx, caplog):
    enqueue(state, "p-old", bot_id="u-eddie")
    enqueue(state, "p-new", bot_id="u-ada")
    state.set_meta("bot_user_id", "u-ada")               # listener resolved a different bot (token changed)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with client(rx.transport()) as http:
            await dispatcher(state, http).tick()
    assert (state.wake("p-old").status, state.wake("p-old").last_error) == ("failed", "bot_rotated")
    assert state.wake("p-new").status == "delivered"
    assert list(rx.accepted) == ["p-new"]
    assert any("bot_rotated" in r.getMessage() for r in caplog.records)


# --- review P1: identity of the CURRENT token gates dispatch -------------------------------------------------------
async def test_no_identity_sends_nothing(state, rx):
    enqueue(state)
    async with client(rx.transport()) as http:
        assert await Dispatcher(state, cfg(), http, clock=state.clock).tick() == 0
    assert rx.requests == [] and state.wake("p-1").status != "delivered" and state.wake("p-1").attempts == 0


async def test_restart_after_token_swap_waits_then_fails_old_wakes(state, rx):
    enqueue(state, "p-old", bot_id="u-eddie")
    resolve(state, "u-eddie", token="tok-old-" + "y" * 20)   # stored by the previous run, previous token
    async with client(rx.transport()) as http:
        d = Dispatcher(state, cfg(), http, clock=state.clock)  # cfg now holds the NEW token (u-ada)
        assert await d.tick() == 0                             # stale id must not approve old wakes
        assert rx.requests == []
        resolve(state, "u-ada")                                # listener resolved users/me for the new token
        await d.tick()
    assert (state.wake("p-old").status, state.wake("p-old").last_error) == ("failed", "bot_rotated")
    assert rx.requests == []


# --- review P2: overall deadline per POST ------------------------------------------------------------------------
async def test_drip_response_hits_overall_deadline(state, monkeypatch):
    import time
    from app import wake
    monkeypatch.setattr(wake, "TIMEOUT_S", 0.3)

    class Drip(httpx.AsyncByteStream):
        async def __aiter__(self):
            for _ in range(40):                                # each chunk well inside the per-read timeout
                await asyncio.sleep(0.05)
                yield b"x"

    enqueue(state)
    async with client(httpx.MockTransport(lambda r: httpx.Response(200, stream=Drip()))) as http:
        t0 = time.monotonic()
        await dispatcher(state, http).tick()
        assert time.monotonic() - t0 < 1.5
    w = state.wake("p-1")
    assert w.status != "delivered" and w.last_error == "timeout"

