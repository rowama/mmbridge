"""Wake relay (ADR-0011, plan Phase 1 / B-s1): env parsing, verify (copy of app.wake.verify, drift guard),
upstream status mapping, byte-identical forward with the Bearer routine key, redaction, replay dedupe,
in-flight guard, per-bot rate limit and the accepted-risk ambiguous outcomes (plan "Delivery guarantee").
B-s2: Tripwire (bad signatures > 5 / 10 min, rate limit hit, upstream 401/403, count drift = double forward)
with the optional Mattermost alert, and /health double_forward_24h."""
import asyncio
import json
import logging

import httpx
import pytest

from app import wake as mm_wake
from relay import relay as rl

SECRET = "s" * 40
KEY = "routine-key-" + "k" * 24
URL = "https://routine.test/eddie"
NOW = 1_800_000_000


class Clock:
    def __init__(self, t=float(NOW)):
        self.t = t

    def __call__(self):
        return self.t


def env(**extra):
    e = {"RELAY_BOT_EDDIE_HMAC_SECRET": SECRET, "RELAY_BOT_EDDIE_ROUTINE_URL": URL,
         "RELAY_BOT_EDDIE_ROUTINE_KEY": KEY}
    e.update(extra)
    return e


def wake_body(delivery="p-1", message="hello", attempt=1):
    return json.dumps({"version": 1, "kind": "post", "delivery_id": delivery, "attempt": attempt,
                       "bot": {"user_id": "u-eddie", "username": "eddie"},
                       "post": {"id": delivery, "message": message}}, separators=(",", ":")).encode()


def signed(body, ts=NOW, secret=SECRET, delivery=None):
    d = delivery if delivery is not None else json.loads(body)["delivery_id"]
    return {"Content-Type": "application/json", "X-MMB-Delivery": d, "X-MMB-Timestamp": str(ts),
            "X-MMB-Signature": mm_wake.sign(secret, ts, body)}


class Upstream:
    """httpx MockTransport routine: records requests; `codes` pops one status per call (last one repeats);
    `exc` raises instead; `gate` (asyncio.Event) holds the response until set."""

    def __init__(self, codes=(200,), exc=None):
        self.codes, self.exc, self.gate = list(codes), exc, None
        self.calls = []
        self.called = asyncio.Event()

    async def handler(self, request):
        self.calls.append({"headers": dict(request.headers), "body": request.content, "url": str(request.url)})
        self.called.set()
        if self.gate is not None:
            await self.gate.wait()
        if self.exc is not None:
            exc, self.exc = self.exc, None
            raise exc
        code = self.codes.pop(0) if len(self.codes) > 1 else self.codes[0]
        return httpx.Response(code, json={"ok": code < 300})


@pytest.fixture
def clk():
    return Clock()


@pytest.fixture
def up():
    return Upstream()


@pytest.fixture
def db(tmp_path):
    return str(tmp_path / "relay.db")


def make(up, clk, db, e=None, seen=None):
    http = httpx.AsyncClient(transport=httpx.MockTransport(up.handler))
    app = rl.create_app(env(**(e or {})), http=http, clock=clk, seen=seen or rl.Seen(db))
    c = httpx.AsyncClient(transport=httpx.ASGITransport(app=app, raise_app_exceptions=False),
                          base_url="http://relay.test")
    c.relay = app.state.relay
    return c


async def until(pred, timeout=5.0):
    """Poll with a deadline (no fixed sleeps, AGENTS.md concurrency rule)."""
    loop = asyncio.get_running_loop()
    end = loop.time() + timeout
    while not pred():
        assert loop.time() < end, "condition not reached"
        await asyncio.sleep(0.001)


async def post(c, body, headers, bot="eddie"):
    return await c.post("/wake/" + bot, content=body, headers=headers)


# --- env parsing ---------------------------------------------------------------------------------------------
def test_load_bots_maps_env_names_to_bot_names():
    e = env(**{"RELAY_BOT_MY_BOT_HMAC_SECRET": "t" * 32, "RELAY_BOT_MY_BOT_ROUTINE_URL": "https://r.test/x",
               "RELAY_BOT_MY_BOT_ROUTINE_KEY": "key2", "OTHER": "x"})
    bots = rl.load_bots(e)
    assert set(bots) == {"eddie", "my-bot"}
    assert bots["eddie"] == rl.RelayBot("eddie", SECRET, URL, KEY)


@pytest.mark.parametrize("drop", ["HMAC_SECRET", "ROUTINE_URL", "ROUTINE_KEY"])
def test_load_bots_fails_on_missing_field(drop):
    e = env()
    del e["RELAY_BOT_EDDIE_" + drop]
    with pytest.raises(rl.ConfigError, match=drop.lower()):
        rl.load_bots(e)


def test_load_bots_fails_on_short_secret_without_echoing_it():
    with pytest.raises(rl.ConfigError) as ei:
        rl.load_bots(env(RELAY_BOT_EDDIE_HMAC_SECRET="short-secret-value"))
    assert "32" in str(ei.value) and "short-secret-value" not in str(ei.value)


def test_load_bots_requires_https_unless_test_flag():
    with pytest.raises(rl.ConfigError, match="https"):
        rl.load_bots(env(RELAY_BOT_EDDIE_ROUTINE_URL="http://routine.test/eddie"))
    bots = rl.load_bots(env(RELAY_BOT_EDDIE_ROUTINE_URL="http://routine.test/eddie", RELAY_ALLOW_HTTP_UPSTREAM="true"))
    assert bots["eddie"].routine_url == "http://routine.test/eddie"


# --- verify: copy of app.wake.verify (drift guard) -----------------------------------------------------------
def test_verify_accepts_wake_signed_by_mmbridge_sign():
    body = wake_body()
    assert rl.verify(SECRET, signed(body), body, NOW)


@pytest.mark.parametrize("case", ["ok", "tampered", "wrong_secret", "stale", "future", "no_sig", "no_ts",
                                  "bad_ts", "no_v1", "delivery_mismatch", "no_delivery", "not_json"])
def test_verify_matches_app_wake_verify(case):
    body = wake_body()
    h = signed(body)
    if case == "tampered":
        body = wake_body(message="evil")
    elif case == "wrong_secret":
        h = signed(body, secret="x" * 40)
    elif case == "stale":
        h = signed(body, ts=NOW - 301)
    elif case == "future":
        h = signed(body, ts=NOW + 301)
    elif case == "no_sig":
        del h["X-MMB-Signature"]
    elif case == "no_ts":
        del h["X-MMB-Timestamp"]
    elif case == "bad_ts":
        h["X-MMB-Timestamp"] = "abc"
    elif case == "no_v1":
        h["X-MMB-Signature"] = h["X-MMB-Signature"][3:]
    elif case == "delivery_mismatch":
        h["X-MMB-Delivery"] = "other"
    elif case == "no_delivery":
        del h["X-MMB-Delivery"]
    elif case == "not_json":
        body = b"not json"
        h = signed(body, delivery="p-1")
    assert rl.verify(SECRET, h, body, NOW) == mm_wake.verify(SECRET, h, body, NOW)
    assert rl.verify(SECRET, h, body, NOW) is (case == "ok")


# --- mapping table -------------------------------------------------------------------------------------------
@pytest.mark.parametrize("status,code", [(200, 200), (202, 200), (204, 200), (408, 503), (429, 503), (500, 503),
                                         (502, 503), (503, 503), (None, 503), (400, 424), (401, 424), (403, 424),
                                         (404, 424), (302, 424)])
def test_map_upstream(status, code):
    got, body = rl.map_upstream(status)
    assert got == code
    if code == 424:
        assert body == {"upstream": status}


# --- POST /wake/{bot} ----------------------------------------------------------------------------------------
async def test_valid_wake_forwarded_byte_identical_with_bearer(up, clk, db):
    body = wake_body()
    async with make(up, clk, db) as c:
        r = await post(c, body, signed(body))
    assert r.status_code == 200 and r.json() == {"status": "forwarded"}
    assert len(up.calls) == 1
    call = up.calls[0]
    assert call["url"] == URL and call["body"] == body
    assert call["headers"]["authorization"] == "Bearer " + KEY
    assert call["headers"]["content-type"] == "application/json"
    assert call["headers"]["x-mmb-delivery"] == "p-1"
    assert "x-mmb-signature" not in call["headers"]


async def test_unknown_bot_404_and_not_forwarded(up, clk, db):
    body = wake_body()
    async with make(up, clk, db) as c:
        r = await post(c, body, signed(body), bot="ghost")
    assert r.status_code == 404 and up.calls == []


@pytest.mark.parametrize("case,reason", [("forged", "bad_sig"), ("tampered", "bad_sig"), ("stale", "stale"),
                                         ("no_headers", "bad_sig")])
async def test_bad_wakes_401_and_upstream_not_called(up, clk, db, case, reason):
    body = wake_body()
    h = signed(body)
    if case == "forged":
        h = signed(body, secret="f" * 40)
    elif case == "tampered":
        body = wake_body(message="deploy now")
    elif case == "stale":
        clk.t = NOW + 600
    elif case == "no_headers":
        h = {"Content-Type": "application/json"}
    async with make(up, clk, db) as c:
        r = await post(c, body, h)
    assert r.status_code == 401 and r.json() == {"reason": reason}
    assert up.calls == []


@pytest.mark.parametrize("codes,exc,status", [((500,), None, 503), ((429,), None, 503), ((404,), None, 424),
                                              ((401,), None, 424), ((200,), httpx.ConnectError("x"), 503)])
async def test_upstream_status_mapped_back(clk, db, codes, exc, status):
    up = Upstream(codes, exc)
    body = wake_body()
    async with make(up, clk, db) as c:
        r = await post(c, body, signed(body))
    assert r.status_code == status


async def test_no_key_or_secret_in_logs_or_responses(up, clk, db, caplog):
    caplog.set_level(logging.INFO)
    body = wake_body()
    up.codes = [401, 500, 200]
    async with make(up, clk, db) as c:
        rs = [await post(c, body, signed(body)) for _ in range(3)]
        rs.append(await post(c, body, signed(body, secret="f" * 40)))
        rs.append(await c.get("/health"))
    text = caplog.text + "".join(r.text + json.dumps(dict(r.headers)) for r in rs)
    assert "relay_forwarded" in caplog.text and "relay_upstream" in caplog.text
    assert KEY not in text and SECRET not in text
    rl.log.info("leak check Authorization: Bearer %s secret %s", KEY, SECRET)
    assert KEY not in caplog.text and SECRET not in caplog.text


async def test_health_counts_only(up, clk, db):
    body = wake_body()
    async with make(up, clk, db) as c:
        await post(c, body, signed(body))
        await post(c, body, signed(body, secret="f" * 40))
        h = (await c.get("/health")).json()
    assert h == {"ok": True, "bots": 1, "forwarded_24h": 1, "rejected_24h": 1, "double_forward_24h": 0}


# --- replay / dedupe (required green before the B-s1 live demo) --------------------------------------------
async def test_replay_within_window_is_duplicate_not_forwarded(up, clk, db):
    body = wake_body()
    h = signed(body)
    async with make(up, clk, db) as c:
        r1 = await post(c, body, h)
        clk.t += 5
        r2 = await post(c, body, h)
    assert r1.json() == {"status": "forwarded"}
    assert r2.status_code == 200 and r2.json() == {"status": "duplicate"}
    assert len(up.calls) == 1


async def test_concurrent_identical_deliveries_forward_once(clk, db):
    up = Upstream()
    up.gate = asyncio.Event()
    body = wake_body()
    h = signed(body)
    async with make(up, clk, db) as c:
        t1 = asyncio.create_task(post(c, body, h))
        await asyncio.wait_for(up.called.wait(), 5)
        t2 = asyncio.create_task(post(c, body, h))
        await until(lambda: c.relay.pending("p-1") == 2)    # t2 waits on the in-flight guard, t1 is upstream
        up.gate.set()
        r1, r2 = await asyncio.wait_for(asyncio.gather(t1, t2), 5)
    assert sorted(r.json()["status"] for r in (r1, r2)) == ["duplicate", "forwarded"]
    assert len(up.calls) == 1


async def test_upstream_503_then_retry_forwarded_once_and_recorded(clk, db):
    up = Upstream(codes=(503, 200))
    body = wake_body()
    async with make(up, clk, db) as c:
        r1 = await post(c, body, signed(body))
        r2 = await post(c, body, signed(body, ts=NOW + 1))
        r3 = await post(c, body, signed(body, ts=NOW + 2))
    assert [r1.status_code, r2.status_code, r3.status_code] == [503, 200, 200]
    assert r3.json() == {"status": "duplicate"}
    assert len(up.calls) == 2
    assert rl.Seen(db).has("p-1")


async def test_seen_survives_restart(up, clk, db):
    body = wake_body()
    async with make(up, clk, db) as c:
        await post(c, body, signed(body))
    async with make(up, clk, db) as c:
        r = await post(c, body, signed(body))
    assert r.json() == {"status": "duplicate"} and len(up.calls) == 1


def test_seen_prunes_after_24h(db):
    s = rl.Seen(db)
    s.add("old", NOW)
    s.add("new", NOW + 3600)
    assert s.prune(NOW + 86400 + 1) == 1
    assert not s.has("old") and s.has("new")


async def test_rate_limit_eleventh_burst_request_429_not_forwarded(up, clk, db):
    async with make(up, clk, db) as c:
        rs = []
        for i in range(11):
            body = wake_body(delivery="p-%d" % i)
            rs.append(await post(c, body, signed(body)))
    assert [r.status_code for r in rs] == [200] * 10 + [429]
    assert rs[-1].json() == {"reason": "rate_limited"}
    assert len(up.calls) == 10


def test_rate_limit_refills_with_fake_clock():
    r = rl.RateLimit(per_min=30, burst=10)
    assert all(r.allow("eddie", 0.0) for _ in range(10))
    assert not r.allow("eddie", 0.0)
    assert r.allow("eddie", 2.0)               # 30/min = one token every 2 s
    assert not r.allow("eddie", 2.0)
    assert r.allow("other", 2.0)               # per bot
    assert not r.allow("eddie", 1.0)           # clock going backwards never adds tokens


# --- ambiguous outcomes (accepted risk A, Rob 2026-10-28): documented double wake ---------------------------
async def test_upstream_2xx_but_response_lost_retry_forwards_again(clk, db, caplog):
    caplog.set_level(logging.INFO)
    up = Upstream(exc=httpx.ReadTimeout("response lost"))   # routine started, its 200 never reached us
    body = wake_body()
    async with make(up, clk, db) as c:
        r1 = await post(c, body, signed(body))
        r2 = await post(c, body, signed(body, ts=NOW + 1))
    assert r1.status_code == 503 and r2.status_code == 200
    assert len(up.calls) == 2                                # double wake: accepted, not hidden
    assert "relay_delivery_ambiguous" in caplog.text


async def test_crash_between_upstream_2xx_and_seen_add_retry_forwards_again(up, clk, db):
    class CrashingSeen(rl.Seen):
        def add(self, d, now):
            raise RuntimeError("crash injected after upstream 2xx")

    body = wake_body()
    async with make(up, clk, db, seen=CrashingSeen(db)) as c:
        r1 = await post(c, body, signed(body))
    assert r1.status_code == 500
    async with make(up, clk, db) as c:                       # restarted relay, same db file
        r2 = await post(c, body, signed(body, ts=NOW + 1))
    assert r2.json() == {"status": "forwarded"}
    assert len(up.calls) == 2


# --- tripwire (B-s2): relay_tripwire{reason} + optional Mattermost alert --------------------------------------
def trips(caplog, reason=None):
    out = []
    for r in caplog.records:
        if r.name == "relay" and "relay_tripwire" in r.getMessage():
            ev = json.loads(r.getMessage())
            if reason is None or ev["reason"] == reason:
                out.append(ev)
    return out


async def test_tripwire_bad_sig_over_five_in_ten_minutes(up, clk, db, caplog):
    caplog.set_level(logging.INFO)
    body = wake_body()
    bad = signed(body, secret="f" * 40)
    async with make(up, clk, db) as c:
        for _ in range(5):
            await post(c, body, bad)
        assert trips(caplog) == []
        await post(c, body, bad)                              # 6th within 10 min
        assert [t["reason"] for t in trips(caplog)] == ["bad_sig"]
        clk.t += 601                                          # window slides: the old failures no longer count
        for _ in range(5):
            await post(c, body, signed(body, ts=int(clk.t), secret="f" * 40))
    assert len(trips(caplog)) == 1 and up.calls == []


async def test_tripwire_counts_stale_timestamps_as_hmac_failures(up, clk, db, caplog):
    caplog.set_level(logging.INFO)
    body = wake_body()
    async with make(up, clk, db) as c:
        for _ in range(6):
            await post(c, body, signed(body, ts=NOW - 600))
    assert [t["reason"] for t in trips(caplog)] == ["bad_sig"]


async def test_tripwire_on_rate_limit_hit(up, clk, db, caplog):
    caplog.set_level(logging.INFO)
    async with make(up, clk, db, e={"RELAY_BURST": "1"}) as c:
        for i in range(2):
            body = wake_body(delivery="p-%d" % i)
            await post(c, body, signed(body))
    assert [(t["reason"], t["bot"]) for t in trips(caplog)] == [("rate_limited", "eddie")]


@pytest.mark.parametrize("code,reason", [(401, "upstream_http_401"), (403, "upstream_http_403"), (404, None),
                                         (500, None)])
async def test_tripwire_on_upstream_401_403_only(clk, db, caplog, code, reason):
    caplog.set_level(logging.INFO)
    body = wake_body()
    async with make(Upstream(codes=(code,)), clk, db) as c:
        await post(c, body, signed(body))
    assert [t["reason"] for t in trips(caplog)] == ([reason] if reason else [])


async def test_double_forward_after_lost_response_trips_and_shows_in_health(clk, db, caplog):
    caplog.set_level(logging.INFO)
    up = Upstream(exc=httpx.ReadTimeout("response lost"))
    body = wake_body()
    async with make(up, clk, db) as c:
        await post(c, body, signed(body))
        assert trips(caplog) == []
        await post(c, body, signed(body, ts=NOW + 1))
        h = (await c.get("/health")).json()
    assert [(t["reason"], t["delivery"]) for t in trips(caplog)] == [("double_forward", "p-1")]
    assert h["double_forward_24h"] == 1


async def test_double_forward_after_crash_is_counted_after_restart(up, clk, db, caplog):
    caplog.set_level(logging.INFO)

    class CrashingSeen(rl.Seen):
        def add(self, d, now):
            raise RuntimeError("crash injected after upstream 2xx")

    body = wake_body()
    async with make(up, clk, db, seen=CrashingSeen(db)) as c:
        await post(c, body, signed(body))
    async with make(up, clk, db) as c:
        await post(c, body, signed(body, ts=NOW + 1))
        h = (await c.get("/health")).json()
    assert [t["reason"] for t in trips(caplog)] == ["double_forward"] and h["double_forward_24h"] == 1


async def test_retry_after_definite_failure_is_not_drift(clk, db, caplog):
    caplog.set_level(logging.INFO)
    up = Upstream(codes=(503, 200))
    body = wake_body()
    async with make(up, clk, db) as c:
        await post(c, body, signed(body))
        await post(c, body, signed(body, ts=NOW + 1))
        h = (await c.get("/health")).json()
    assert len(up.calls) == 2 and trips(caplog) == [] and h["double_forward_24h"] == 0


async def test_connect_error_then_retry_is_not_drift(clk, db, caplog):
    caplog.set_level(logging.INFO)
    up = Upstream(exc=httpx.ConnectError("refused"))
    body = wake_body()
    async with make(up, clk, db) as c:
        await post(c, body, signed(body))
        await post(c, body, signed(body, ts=NOW + 1))
        assert (await c.get("/health")).json()["double_forward_24h"] == 0
    assert trips(caplog) == []


def test_double_forward_count_expires_after_24h(db):
    s = rl.Seen(db)
    for d in ("a", "a", "b"):
        s.forward_begin(d, NOW)
    assert s.double_forwards_since(NOW - 86400) == 1
    s.prune(NOW + 86400 + 1)
    assert s.double_forwards_since(NOW + 1) == 0


def test_tripwire_alerts_throttled_and_drift_alerts_from_three():
    clk, alerts = Clock(), []
    tw = rl.Tripwire(clk, alert=lambda reason, fields: alerts.append(reason))
    tw.upstream_denied("eddie", 401)
    tw.upstream_denied("eddie", 401)                    # same reason within 10 min: logged, not alerted again
    assert alerts == ["upstream_http_401"]
    clk.t += 601
    tw.upstream_denied("eddie", 401)
    assert alerts == ["upstream_http_401"] * 2
    tw.double_forward("eddie", "p-1", count_24h=1)
    tw.double_forward("eddie", "p-2", count_24h=2)
    assert alerts == ["upstream_http_401"] * 2          # below 3 in 24 h: log only
    tw.double_forward("eddie", "p-3", count_24h=3)
    assert alerts[-1] == "double_forward"


def test_alert_config_must_be_complete():
    with pytest.raises(rl.ConfigError, match="RELAY_ALERT"):
        rl.create_app(env(RELAY_ALERT_URL="http://mattermost:8065"), http=httpx.AsyncClient(),
                      seen=rl.Seen(":memory:"))


async def test_alert_posts_to_mattermost_with_alert_token_and_no_secrets(clk, db):
    alert_tok, chan = "alert-token-" + "a" * 20, "c" * 26
    calls = []

    async def handler(request):
        calls.append({"url": str(request.url), "headers": dict(request.headers), "body": request.content})
        if request.url.host == "mattermost":
            return httpx.Response(201, json={"id": "x"})
        return httpx.Response(401, json={})                # routine key revoked -> tripwire

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    app = rl.create_app(env(RELAY_ALERT_URL="http://mattermost:8065", RELAY_ALERT_TOKEN=alert_tok,
                            RELAY_ALERT_CHANNEL=chan), http=http, clock=clk, seen=rl.Seen(db))
    body = wake_body()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://relay.test") as c:
        r = await post(c, body, signed(body))
        await until(lambda: any(x["url"].startswith("http://mattermost") for x in calls))
    assert r.status_code == 424
    mm = next(x for x in calls if x["url"].startswith("http://mattermost"))
    assert mm["url"] == "http://mattermost:8065/api/v4/posts"
    assert mm["headers"]["authorization"] == "Bearer " + alert_tok
    sent = json.loads(mm["body"])
    assert sent["channel_id"] == chan and "upstream_http_401" in sent["message"] and "eddie" in sent["message"]
    assert KEY not in mm["body"].decode() and SECRET not in mm["body"].decode()


async def test_alert_failure_is_logged_and_never_breaks_the_wake(clk, db, caplog):
    caplog.set_level(logging.INFO)
    alert_tok = "alert-token-" + "a" * 20

    async def handler(request):
        if request.url.host == "mattermost":
            raise httpx.ConnectError("down")
        return httpx.Response(403, json={})

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    app = rl.create_app(env(RELAY_ALERT_URL="http://mattermost:8065", RELAY_ALERT_TOKEN=alert_tok,
                            RELAY_ALERT_CHANNEL="c" * 26), http=http, clock=clk, seen=rl.Seen(db))
    body = wake_body()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://relay.test") as c:
        r = await post(c, body, signed(body))
        await until(lambda: "relay_alert_failed" in caplog.text)
    assert r.status_code == 424 and alert_tok not in caplog.text


def test_bad_sig_tracking_is_bounded_under_a_flood():
    """Forged wakes bypass the rate limiter: the failure window keeps bounded state, not one entry per request
    (review F2), and still trips on > 5 in 10 min."""
    clk = Clock()
    tw = rl.Tripwire(clk)
    for i in range(5000):
        clk.t = NOW + i * 0.1                       # 5000 failures over ~8 min
        tw.bad_sig("eddie")
    assert len(tw._bad) <= rl.TRIP_WINDOW_S // rl.BAD_SIG_BUCKET_S + 1
    clk.t += rl.TRIP_WINDOW_S + rl.BAD_SIG_BUCKET_S  # all failures out of the window
    assert tw.bad_sig_count() == 0
