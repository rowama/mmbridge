"""Live wiring (slice lb5, plan Phase 5): lifespan gating on LIVE_BOTS_ENABLED + store + state, /health listener
and wake_failed_24h (PR-10), supervisor restarts (PR-4), startup delivery of pending wakes, coordinated store
reload (PR-2). The app runs its real lifespan; Mattermost is the fake on a free port, the receiver in-process."""
import asyncio
import contextlib
import json
import logging
import os
import time

import httpx
import pytest
from cryptography.fernet import Fernet

from conftest import call
from app import store
from app.listener import Listener
from app.live import ConfigHolder, LiveRuntime
from app.main import create_app
from app.state import State
from app.store import BotEntry, Store
from app.wake import Dispatcher
from drivers.fake_mattermost import FakeMattermost
from drivers.wake_receiver import WakeReceiver

SECRET = "s" * 40


def D(post_id, bot="eddie"):
    """delivery_id / X-MMB-Delivery of a live wake (B-s3)."""
    return "%s:%s" % (bot, post_id)
URL = "https://receiver.test/wake"


@pytest.fixture
def world():
    m = FakeMattermost(clock=time.time)
    m.add_user("eddie", bot=True)
    m.add_user("eddie2", bot=True)
    m.add_user("rob")
    town = m.add_channel("main", "town-square", ["eddie", "eddie2", "rob"])
    return m, town


@pytest.fixture
async def served(world):
    m, town = world
    async with m.serve() as base:
        yield m, town, base


@pytest.fixture
def key():
    return Fernet.generate_key().decode()


def tok(m, name):
    return m.user_by_name(name)["token"]


def save(tmp_path, key, token, secret=SECRET):
    store.save(str(tmp_path / "bots.enc"), key, Store(bots={"eddie": BotEntry(token, URL, secret, name="eddie")}))


def runtime(tmp_path, key, base, rx=None, flag="true", **kw):
    env = {"MMB_STORE_KEY": key, "MMB_DATA_DIR": str(tmp_path)}
    if flag:
        env["LIVE_BOTS_ENABLED"] = flag
    http = httpx.AsyncClient(transport=(rx or WakeReceiver(SECRET)).transport())
    return LiveRuntime(env=env, base_url=base, http=http, restart_base_s=kw.pop("restart_base_s", 0.3),
                       reload_s=0.05, poll_s=0.02,
                       listener_kw=dict(backoff_s=0.05, max_backoff_s=0.2, ping_s=0.2), **kw)


@contextlib.asynccontextmanager
async def running(live, m):
    app = create_app(mm_transport=m.transport(), live=live)
    started, stop = asyncio.Event(), asyncio.Event()

    async def hold():
        async with app.router.lifespan_context(app):
            started.set()
            await stop.wait()
    task = asyncio.create_task(hold())
    await asyncio.wait_for(started.wait(), 5)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testserver") as c:
        try:
            yield c
        finally:
            stop.set()
            await task


async def health(c):
    r = await c.get("/health")
    assert r.status_code == 200
    return r.json()


async def until(pred, timeout=5.0):
    for _ in range(int(timeout / 0.02)):
        got = pred()
        if asyncio.iscoroutine(got):
            got = await got
        if got:
            return
        await asyncio.sleep(0.02)
    raise AssertionError("condition not met in %.1fs" % timeout)


async def listener_is(c, status):
    return await until(lambda: _status(c, status))


async def _status(c, status):
    return (await health(c))["listener"] == status


async def mcp_works(c, m):
    r = await call(c, token=tok(m, "eddie"))
    assert r.status_code == 200 and "town-square" in r.text


async def test_flag_off_reports_disabled_and_starts_nothing(served, tmp_path, key):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    async with running(runtime(tmp_path, key, base, flag=None), m) as c:
        assert await health(c) == {"ok": True, "listener": "disabled", "wake_failed_24h": 0, "bots_total": 0, "bots_failing": 0}
        await mcp_works(c, m)
    assert not any(x[0] == "WS" for x in m.calls) and not (tmp_path / "state.db").exists()


async def test_bad_store_key_reports_off_and_mcp_still_works(served, tmp_path, key, caplog):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    wrong = Fernet.generate_key().decode()
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with running(runtime(tmp_path, wrong, base), m) as c:
            assert await health(c) == {"ok": True, "listener": "off", "wake_failed_24h": 0, "bots_total": 0, "bots_failing": 0}
            await mcp_works(c, m)
    assert '"event": "store_unreadable"' in caplog.text and wrong not in caplog.text and key not in caplog.text
    assert not any(x[0] == "WS" for x in m.calls)


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory permissions")
async def test_readonly_data_dir_reports_off(served, tmp_path, key, caplog):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    tmp_path.chmod(0o500)
    try:
        with caplog.at_level(logging.INFO, logger="mmbridge"):
            async with running(runtime(tmp_path, key, base), m) as c:
                assert (await health(c))["listener"] == "off"
                await mcp_works(c, m)
    finally:
        tmp_path.chmod(0o700)
    assert '"event": "state_unwritable"' in caplog.text


async def test_health_connecting_before_hello_then_ok(served, tmp_path, key):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    m.ws_refuse = True
    async with running(runtime(tmp_path, key, base), m) as c:
        await listener_is(c, "connecting")
        m.ws_refuse = False
        await listener_is(c, "ok")
        h = await health(c)
    assert set(h) == {"ok", "listener", "wake_failed_24h", "bots_total", "bots_failing"} and tok(m, "eddie") not in json.dumps(h)


async def test_wake_failed_24h_counts_failed_rows_of_the_last_24h_only(served, tmp_path, key):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    t = [time.time() - 2 * 86400]
    s = State(str(tmp_path / "state.db"), clock=lambda: t[0])
    for pid, at, mark in (("old", time.time() - 2 * 86400, "failed"), ("recent", time.time() - 3600, "failed"),
                          ("ok", time.time() - 60, "delivered")):
        t[0] = at
        s.enqueue("eddie", pid, town, {"bot": {"user_id": "u-eddie"}})
        s.claim_due(int(at))
        s.mark_failed("eddie", pid, "http_410") if mark == "failed" else s.mark_delivered("eddie", pid)
    s.close()
    async with running(runtime(tmp_path, key, base), m) as c:
        assert (await health(c))["wake_failed_24h"] == 1


def _crash_once(monkeypatch, cls):
    real, calls = cls.run, []

    async def flaky(self):
        calls.append(1)
        if len(calls) == 1:
            raise RuntimeError("boom")
        return await real(self)
    monkeypatch.setattr(cls, "run", flaky)
    return calls


async def test_crashed_listener_is_restarted_health_degraded_then_ok(served, tmp_path, key, monkeypatch, caplog):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    calls = _crash_once(monkeypatch, Listener)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with running(runtime(tmp_path, key, base, restart_base_s=0.5), m) as c:
            await listener_is(c, "degraded")
            await mcp_works(c, m)                      # MCP keeps serving while the listener restarts
            await listener_is(c, "ok")
    assert len(calls) == 2 and '"event": "task_crashed"' in caplog.text and '"task": "listener:eddie"' in caplog.text


async def test_crashed_dispatcher_is_restarted_and_delivers(served, tmp_path, key, monkeypatch):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    calls = _crash_once(monkeypatch, Dispatcher)
    rx = WakeReceiver(SECRET)
    async with running(runtime(tmp_path, key, base, rx=rx), m) as c:
        await listener_is(c, "degraded")
        await listener_is(c, "ok")
        p = m.add_post(town, "u-rob", "after the restart")
        await until(lambda: D(p["id"]) in rx.accepted)
    assert len(calls) == 2


async def test_startup_delivers_pending_and_stale_in_flight_wakes_exactly_once(served, tmp_path, key):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    old = time.time() - 120
    s = State(str(tmp_path / "state.db"), instance_id="crashed-run", clock=lambda: old)
    payload = lambda pid: {"version": 1, "delivery_id": pid, "bot": {"user_id": "u-eddie"}, "post": {"id": pid}}
    s.enqueue("eddie", "stale", town, payload("stale"))
    assert [w.post_id for w in s.claim_due(int(old))] == ["stale"]       # lease long expired
    s.enqueue("eddie", "queued", town, payload("queued"))
    s.close()
    rx = WakeReceiver(SECRET)
    async with running(runtime(tmp_path, key, base, rx=rx), m) as c:
        await until(lambda: {"stale", "queued"} <= set(rx.accepted))
        await asyncio.sleep(0.3)
    assert [r["status"] for r in rx.attempts("stale")] == [204]
    assert [r["status"] for r in rx.attempts("queued")] == [204]


async def test_store_token_change_reconnects_listener_with_new_bearer(served, tmp_path, key, caplog):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    rx = WakeReceiver(SECRET)
    live = runtime(tmp_path, key, base, rx=rx)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with running(live, m) as c:
            await listener_is(c, "ok")
            save(tmp_path, key, tok(m, "eddie2"))
            await until(lambda: ("WS", "/api/v4/websocket", tok(m, "eddie2")) in m.calls)
            await until(lambda: live.supervisor.listeners["eddie"].status == "ok" and live.supervisor.listeners["eddie"].bot_user_id == "u-eddie2")
            p = m.add_post(town, "u-rob", "hello new bot")
            await until(lambda: D(p["id"]) in rx.accepted)
    assert rx.accepted[D(p["id"])]["bot"]["username"] == "eddie2"
    assert '"event": "store_updated"' in caplog.text and '"eddie.token"' in caplog.text
    assert tok(m, "eddie2") not in caplog.text and tok(m, "eddie") not in caplog.text


async def test_wake_secret_rotation_applies_to_the_next_send(served, tmp_path, key):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    rx = WakeReceiver(SECRET)
    live = runtime(tmp_path, key, base, rx=rx)
    async with running(live, m) as c:
        await listener_is(c, "ok")
        new = "n" * 40
        save(tmp_path, key, tok(m, "eddie"), secret=new)
        await until(lambda: live.holder.get().bots["eddie"].wake_secret == new)
        rx.secret = new
        p = m.add_post(town, "u-rob", "signed with the new secret")
        await until(lambda: D(p["id"]) in rx.accepted)
    assert [r["status"] for r in rx.attempts(D(p["id"]))] == [204]


async def test_invalid_store_edit_keeps_old_config(served, tmp_path, key, caplog):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    rx = WakeReceiver(SECRET)
    live = runtime(tmp_path, key, base, rx=rx)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with running(live, m) as c:
            await listener_is(c, "ok")
            (tmp_path / "bots.enc").write_bytes(b"not a fernet token")
            await until(lambda: "store_reload_failed" in caplog.text)
            assert live.holder.get().bots["eddie"].token == tok(m, "eddie")
            p = m.add_post(town, "u-rob", "still served")
            await until(lambda: D(p["id"]) in rx.accepted)


def test_config_holder_only_notifies_on_a_real_change(tmp_path, key):
    save(tmp_path, key, "t" * 26)
    path = str(tmp_path / "bots.enc")
    h = ConfigHolder(path, key, store.load(path, key))
    seen = []
    h.subscribe(lambda old, new: seen.append((old.bots["eddie"].token, new.bots["eddie"].token)))
    assert h.check() is False
    save(tmp_path, key, "t" * 26)                         # rewritten, same values: no notification
    assert h.check() is False and seen == []
    save(tmp_path, key, "u" * 26)
    assert h.check() is True and seen == [("t" * 26, "u" * 26)] and h.generation == 1


async def test_boot_without_store_then_set_bot_starts_listener_without_restart(served, tmp_path, key, caplog):
    """Ops fix (Rob 2026-10-30): boot before bots.enc exists -> `off`; the first set-bot writes the store and the
    runtime picks it up on its reload poll and starts the listener (no container restart)."""
    m, town, base = served
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with running(runtime(tmp_path, key, base), m) as c:
            assert (await health(c))["listener"] == "off"
            await asyncio.sleep(0.15)
            assert not any(x[0] == "WS" for x in m.calls)
            save(tmp_path, key, tok(m, "eddie"))
            await listener_is(c, "ok")
            await until(lambda: any(x[0] == "WS" for x in m.calls))
            await mcp_works(c, m)
    assert caplog.text.count('"event": "store_unreadable"') == 1
    assert '"event": "store_appeared"' in caplog.text


# --- B-s3: several bots (ADR-0014): supervisor, isolation, routing, health counts, migrations ---------------------
def save_bots(tmp_path, key, m, *names):
    store.save(str(tmp_path / "bots.enc"), key, Store(bots={
        n: BotEntry(tok(m, n), URL, SECRET, name=n, user_id="u-" + n, username=n) for n in names}))


def bot_ok(live, *names):
    return lambda: all(live.bot_status().get(n, ("off",))[0] == "ok" for n in names)


async def test_two_bots_each_woken_once_per_post_and_registered_bot_posts_wake_nobody(served, tmp_path, key):
    m, town, base = served
    save_bots(tmp_path, key, m, "eddie", "eddie2")
    rx = WakeReceiver(SECRET)
    live = runtime(tmp_path, key, base, rx=rx)
    async with running(live, m) as c:
        await until(bot_ok(live, "eddie", "eddie2"))
        h = await health(c)
        assert (h["listener"], h["bots_total"], h["bots_failing"]) == ("ok", 2, 0)
        p = m.add_post(town, "u-rob", "standup")
        await until(lambda: {D(p["id"]), D(p["id"], "eddie2")} <= set(rx.accepted))
        assert rx.accepted[D(p["id"], "eddie2")]["bot"] == {"name": "eddie2", "user_id": "u-eddie2",
                                                           "username": "eddie2"}
        by_bot = m.add_post(town, "u-eddie", "@eddie2 hi")             # B7: a registered bot's post
        q = m.add_post(town, "u-rob", "barrier")
        await until(lambda: {D(q["id"]), D(q["id"], "eddie2")} <= set(rx.accepted))
        await asyncio.sleep(0.1)
    assert [d for d in rx.accepted if by_bot["id"] in d] == []
    assert [r["status"] for r in rx.attempts(D(p["id"]))] == [204]
    assert [r["status"] for r in rx.attempts(D(p["id"], "eddie2"))] == [204]


async def test_reload_adds_rotates_and_removes_bots_without_restart(served, tmp_path, key, caplog):
    m, town, base = served
    save_bots(tmp_path, key, m, "eddie")
    rx = WakeReceiver(SECRET)
    live = runtime(tmp_path, key, base, rx=rx)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with running(live, m) as c:
            await until(bot_ok(live, "eddie"))
            first = live.supervisor.listeners["eddie"]
            save_bots(tmp_path, key, m, "eddie", "eddie2")             # add
            await until(bot_ok(live, "eddie", "eddie2"))
            assert live.supervisor.listeners["eddie"] is first         # untouched bot keeps its listener
            assert (await health(c))["bots_total"] == 2
            p = m.add_post(town, "u-rob", "both now")
            await until(lambda: D(p["id"], "eddie2") in rx.accepted and D(p["id"]) in rx.accepted)
            save_bots(tmp_path, key, m, "eddie2")                      # remove eddie
            await until(lambda: list(live.supervisor.listeners) == ["eddie2"])
            await until(lambda: not any(s.user_id == "u-eddie" for s in m.ws_sessions))
            q = m.add_post(town, "u-rob", "only eddie2")
            await until(lambda: D(q["id"], "eddie2") in rx.accepted)
            await asyncio.sleep(0.2)
            assert D(q["id"]) not in rx.accepted
            assert (await health(c))["bots_total"] == 1
    assert '"event": "bot_started", "bot": "eddie2"' in caplog.text
    assert '"event": "bot_stopped", "bot": "eddie"' in caplog.text
    assert '"+eddie2"' in caplog.text and '"-eddie"' in caplog.text


async def test_one_bot_revoked_others_unaffected_and_counted_failing(served, tmp_path, key, caplog):
    m, town, base = served
    save_bots(tmp_path, key, m, "eddie", "eddie2")
    rx = WakeReceiver(SECRET)
    live = runtime(tmp_path, key, base, rx=rx)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with running(live, m) as c:
            await until(bot_ok(live, "eddie", "eddie2"))
            m.revoke_token("u-eddie2")
            await until(lambda: live.bot_status()["eddie2"] == ("degraded", "mm_unauthorized"))
            h = await health(c)
            assert (h["listener"], h["bots_total"], h["bots_failing"]) == ("degraded", 2, 1)
            assert live.bot_status()["eddie"] == ("ok", None)
            p = m.add_post(town, "u-rob", "who is alive?")
            await until(lambda: D(p["id"]) in rx.accepted)
            await until(lambda: live.state.get_meta("bot:eddie2:status") and json.loads(
                live.state.get_meta("bot:eddie2:status"))["status"] == "degraded")
            rep = json.loads(live.state.get_meta("bot:eddie2:status"))
            assert rep["error"] == "mm_unauthorized" and json.loads(live.state.get_meta("bot:eddie:status"))[
                "status"] == "ok"
            await mcp_works(c, m)
    assert '"event": "mm_unauthorized", "bot": "eddie2"' in caplog.text


async def test_dead_wake_target_of_one_bot_counted_failing_other_still_delivered(served, tmp_path, key, monkeypatch):
    monkeypatch.setenv("WAKE_MAX_ATTEMPTS", "1")
    m, town, base = served
    store.save(str(tmp_path / "bots.enc"), key, Store(bots={
        "eddie": BotEntry(tok(m, "eddie"), URL, SECRET, name="eddie"),
        "eddie2": BotEntry(tok(m, "eddie2"), "https://dead.test/wake", SECRET, name="eddie2")}))
    rx = WakeReceiver(SECRET)

    async def route(request):
        if request.url.host == "dead.test":
            return httpx.Response(503)
        return await rx.transport().handle_async_request(request)
    live = runtime(tmp_path, key, base)
    live._http = httpx.AsyncClient(transport=httpx.MockTransport(route))
    async with running(live, m) as c:
        await until(bot_ok(live, "eddie", "eddie2"))
        p = m.add_post(town, "u-rob", "who is up?")
        await until(lambda: D(p["id"]) in rx.accepted)
        await until(lambda: live.state.wake("eddie2", p["id"]).status == "failed")
        h = await health(c)
        assert (h["listener"], h["bots_failing"], h["wake_failed_24h"]) == ("ok", 1, 1)


async def test_v1_store_and_state_migrated_at_boot(served, tmp_path, key, caplog):
    m, town, base = served
    import sqlite3
    v1 = Fernet(key.encode()).encrypt(json.dumps({"version": 1, "bot": {
        "token": tok(m, "eddie"), "wake_url": URL, "wake_secret": SECRET}}).encode())
    (tmp_path / "bots.enc").write_bytes(v1)
    con = sqlite3.connect(str(tmp_path / "state.db"))
    con.executescript(
        "CREATE TABLE wakes (post_id TEXT PRIMARY KEY, channel_id TEXT NOT NULL, payload_json TEXT NOT NULL, "
        "status TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0, next_at INTEGER NOT NULL, last_error TEXT, "
        "claimed_by TEXT, lease_until INTEGER, post_create_at INTEGER, delivered_at INTEGER, "
        "created_at INTEGER NOT NULL, updated_at INTEGER NOT NULL);"
        "CREATE TABLE cursors (channel_id TEXT PRIMARY KEY, last_create_at INTEGER NOT NULL, last_post_id TEXT NOT NULL);"
        "CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);"
        "INSERT INTO wakes VALUES ('old', 'c', '{}', 'failed', 5, 0, 'http_410', NULL, NULL, 1, NULL, %d, %d);"
        "INSERT INTO meta VALUES ('bot_user_id', 'u-eddie');" % ((int(time.time()),) * 2))   # recent: not pruned
    con.commit()
    con.close()
    rx = WakeReceiver(SECRET)
    live = runtime(tmp_path, key, base, rx=rx)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with running(live, m) as c:
            await until(bot_ok(live, "eddie"))
            p = m.add_post(town, "u-rob", "after upgrade")
            await until(lambda: D(p["id"]) in rx.accepted)
            assert live.state.wake("eddie", "old").last_error == "http_410"
    st = store.load(str(tmp_path / "bots.enc"), key)
    assert st.migrated_from is None and list(st.bots) == ["eddie"] and st.bots["eddie"].user_id == "u-eddie"
    assert (tmp_path / "bots.enc.v1.bak").read_bytes() == v1 and (tmp_path / "state.db.v1.bak").exists()
    assert '"event": "store_migrated", "bot": "eddie"' in caplog.text and "live_migration_done" in caplog.text


async def test_state_migration_failure_turns_live_off_mcp_stays_up(served, tmp_path, key, caplog, monkeypatch):
    m, town, base = served
    save_bots(tmp_path, key, m, "eddie")
    from app import state as state_mod

    def broken(*a, **k):
        raise state_mod.StateError("live_migration_failed", "injected")
    monkeypatch.setattr("app.live.State", broken)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with running(runtime(tmp_path, key, base), m) as c:
            assert (await health(c))["listener"] == "degraded"
            await mcp_works(c, m)
            await asyncio.sleep(0.1)
            assert not any(x[0] == "WS" for x in m.calls)
    assert '"event": "live_runtime_off", "reason": "live_migration_failed"' in caplog.text
