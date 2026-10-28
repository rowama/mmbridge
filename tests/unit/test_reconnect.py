"""Listener reconnect, resume and REST catch-up (slice lb5, plan Phase 5 PR-3/PR-4; ADR-0007; architecture
'catch-up channel discovery'). Fake Mattermost on a free port with a real-time post clock."""
import asyncio
import logging
import time

import pytest

from app.listener import Listener
from app.mattermost import Client, MMError
from app.state import State
from app.store import BotConfig
from drivers.fake_mattermost import FakeMattermost

FAST = dict(backoff_s=0.05, max_backoff_s=0.2, ping_s=0.2, idle_s=2.0)


@pytest.fixture
def world():
    m = FakeMattermost(clock=time.time)
    bot = m.add_user("eddie", bot=True)
    rob = m.add_user("rob")
    town = m.add_channel("main", "town-square", ["eddie", "rob"])
    dm = m.direct_channel(bot["id"], rob["id"])["id"]
    return m, {"bot": bot, "rob": rob, "town": town, "dm": dm}


@pytest.fixture
async def served(world):
    m, w = world
    async with m.serve() as base:
        yield m, w, base


async def until(pred, timeout=5.0):
    for _ in range(int(timeout / 0.02)):
        if pred():
            return
        await asyncio.sleep(0.02)
    raise AssertionError("condition not met in %.1fs" % timeout)


class Run:
    """A Listener.run() task on its own state.db, cancelled at teardown."""

    def __init__(self, served, path, client_cls=Client, **kw):
        self.m, self.w, base = served
        cfg = BotConfig(token=self.w["bot"]["token"], wake_url="https://wake.example/hook", wake_secret="s" * 40)
        self.state = State(str(path))
        self.lis = Listener(cfg, self.state, lambda tok: client_cls(tok, base_url=base), base_url=base,
                            **{**FAST, **kw})
        self.task = None

    async def start(self):
        self.task = asyncio.create_task(self.lis.run())
        await until(lambda: self.lis.status == "ok")
        return self

    async def stop(self):
        self.task.cancel()
        await asyncio.gather(self.task, return_exceptions=True)

    def posts_calls(self, cid):
        return [c for c in self.m.calls if c[1] == "/api/v4/channels/%s/posts" % cid]

    def post(self, cid, msg, user="rob", **kw):
        return self.m.add_post(cid, self.m.user_by_name(user)["id"], msg, **kw)

    async def outage(self, during, resumable=False):
        """Drop the socket, refuse reconnects while `during()` runs, then let the listener back in."""
        cid = self.lis.connection_id
        self.m.ws_refuse = True
        self.m.ws_drop(resumable=resumable)
        await until(lambda: self.lis.status != "ok")
        out = during()
        self.m.ws_refuse = False
        await until(lambda: self.lis.status == "ok" and (resumable or self.lis.connection_id != cid))
        return out


@pytest.fixture
async def run(served, tmp_path):
    r = await Run(served, tmp_path / "state.db").start()
    yield r
    await r.stop()


def ids(state):
    return [w.post_id for w in state.wakes()]


async def test_same_connection_id_resumes_without_catchup(run):
    m, w = run.m, run.w
    a = run.post(w["town"], "live one")
    await until(lambda: run.state.wake(a["id"]))
    cid = run.lis.connection_id
    b = await run.outage(lambda: run.post(w["town"], "while dropped"), resumable=True)
    await until(lambda: run.state.wake(b["id"]))
    assert m.ws_resumes == 1 and run.lis.connection_id == cid
    assert ("WS", "/api/v4/websocket", w["bot"]["token"]) in m.calls
    assert run.posts_calls(w["town"]) == []              # resumed: no REST catch-up
    assert ids(run.state) == [a["id"], b["id"]]


async def test_new_connection_id_runs_catchup_and_resets_seq(run, caplog):
    w = run.w
    a = run.post(w["town"], "live one")
    await until(lambda: run.state.wake(a["id"]))
    assert run.lis.last_seq == 1
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        b, c = await run.outage(lambda: (run.post(w["town"], "missed in town"), run.post(w["dm"], "missed dm")))
        await until(lambda: run.state.wake(b["id"]) and run.state.wake(c["id"]))
        assert run.lis.last_seq == 0                         # new connection: expected seq reset (hello is 0)
        d = run.post(w["town"], "live again")
        await until(lambda: run.state.wake(d["id"]))
    assert run.lis.last_seq == 1 and "ws_seq_gap" not in caplog.text
    assert '"event": "ws_reconnect"' in caplog.text and '"event": "catchup"' in caplog.text
    assert ids(run.state) == [a["id"], b["id"], c["id"], d["id"]]
    assert run.state.get_cursor(w["town"]) == (d["create_at"], d["id"])


async def test_seq_gap_on_resume_triggers_catchup(run, caplog):
    m, w = run.m, run.w
    a = run.post(w["town"], "live one")
    await until(lambda: run.state.wake(a["id"]))

    def lose_one():
        lost = run.post(w["town"], "lost by the server")
        dead = next(iter(m.ws_dead.values()))
        dead.history = [e for e in dead.history if lost["id"] not in str(e)]   # never replayed: a seq gap
        return lost, run.post(w["town"], "replayed")
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        lost, replayed = await run.outage(lose_one, resumable=True)
        await until(lambda: run.state.wake(lost["id"]) and run.state.wake(replayed["id"]))
    assert m.ws_resumes == 1 and "ws_seq_gap" in caplog.text and run.posts_calls(w["town"])
    assert ids(run.state) == [a["id"], lost["id"], replayed["id"]]


async def test_outage_longer_than_window_skips_old_posts(served, tmp_path, caplog):
    now = [time.time()]
    r = await Run(served, tmp_path / "state.db", clock=lambda: now[0], catchup_minutes=15).start()
    w = r.w
    t0 = int(now[0] * 1000)

    def during():
        old = r.post(w["town"], "too old", create_at=t0 + 1000)
        now[0] += 20 * 60
        return old, r.post(w["town"], "recent", create_at=int(now[0] * 1000) - 1000)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        old, recent = await r.outage(during)
        await until(lambda: r.state.wake(recent["id"]))
    await r.stop()
    assert r.state.wake(old["id"]) is None
    assert '"event": "catchup_skipped"' in caplog.text and '"n": 1' in caplog.text


async def test_catchup_paginates_450_posts_each_enqueued_once(run):
    w = run.w
    posts = await run.outage(lambda: [run.post(w["town"], "bulk %d" % i) for i in range(450)])
    await until(lambda: len(run.state.wakes()) == 450)
    assert len(run.posts_calls(w["town"])) == 3                      # 200 + 200 + 50
    assert ids(run.state) == [p["id"] for p in posts]               # ascending (create_at, post_id)


async def test_equal_create_at_straddling_a_page_boundary_both_enqueued_once(served, tmp_path):
    r = await Run(served, tmp_path / "state.db", per_page=2).start()
    w = r.w
    ts = int(time.time() * 1000) + 5000

    def during():
        return [r.post(w["town"], "same ts %d" % i, create_at=ts) for i in range(3)] + \
            [r.post(w["town"], "later", create_at=ts + 1)]
    posts = await r.outage(during)
    await until(lambda: len(r.state.wakes()) == 4)
    await asyncio.sleep(0.2)
    await r.stop()
    assert sorted(ids(r.state)) == sorted(p["id"] for p in posts)
    assert len(r.posts_calls(w["town"])) >= 2


async def test_dm_created_during_outage_is_discovered_and_caught_up(run):
    m, w = run.m, run.w
    ann = m.add_user("ann")

    def during():
        c = m.direct_channel(w["bot"]["id"], ann["id"])
        return run.post(c["id"], "first dm from ann", user="ann")
    p = await run.outage(during)
    await until(lambda: run.state.wake(p["id"]))
    assert run.state.wake(p["id"]).payload["channel"]["type"] == "D"


async def test_two_teams_and_channel_joined_during_outage_are_caught_up(served, tmp_path):
    m, w, _ = served
    ops = m.add_channel("lab2", "ops", ["eddie", "rob"])
    r = await Run(served, tmp_path / "state.db").start()

    def during():
        new = m.add_channel("lab3", "fresh", ["eddie", "rob"])     # bot added on a third team meanwhile
        return r.post(ops, "disk at 90%"), r.post(new, "welcome eddie")
    a, b = await r.outage(during)
    await until(lambda: r.state.wake(a["id"]) and r.state.wake(b["id"]))
    await r.stop()
    assert [x.payload["channel"]["team"] for x in r.state.wakes()] == ["lab2", "lab3"]


async def test_membership_events_refresh_and_user_removed_drops_cursor(run):
    m, w = run.m, run.w
    p = run.post(w["town"], "set a cursor")
    await until(lambda: run.state.wake(p["id"]))
    before = sum(c[1] == "/api/v4/users/me/teams" for c in m.calls)
    m.ws_event(w["bot"]["id"], "added_to_team", {"team_id": "t-lab2", "user_id": w["bot"]["id"]})
    await until(lambda: sum(c[1] == "/api/v4/users/me/teams" for c in m.calls) > before)
    m.channels[w["town"]]["members"].discard(w["bot"]["id"])
    m.ws_event(w["bot"]["id"], "user_removed", {"channel_id": w["town"], "remover_id": w["rob"]["id"]})
    await until(lambda: run.state.get_cursor(w["town"]) is None)
    assert w["town"] not in run.lis.members


class _FlakyClient(Client):
    """Fails the first catch-up GET of page 1 (crash between pages)."""
    failed = False

    async def get(self, path, **params):
        if path.endswith("/posts") and params.get("page") == 1 and not _FlakyClient.failed:
            _FlakyClient.failed = True
            raise MMError("mattermost_unavailable", 503)
        return await super().get(path, **params)


async def test_crash_between_pages_recovers_with_no_loss_or_duplicate(served, tmp_path):
    _FlakyClient.failed = False
    r = await Run(served, tmp_path / "state.db", client_cls=_FlakyClient).start()
    posts = await r.outage(lambda: [r.post(r.w["town"], "bulk %d" % i) for i in range(250)])
    await until(lambda: len(r.state.wakes()) == 250)
    await asyncio.sleep(0.2)
    await r.stop()
    assert _FlakyClient.failed and ids(r.state) == [p["id"] for p in posts]


async def test_crash_mid_enqueue_resumes_from_last_committed_cursor(run, monkeypatch):
    w = run.w
    real, n, cursor_at_crash = run.state.enqueue_and_advance, [0], []

    def flaky(*a):
        n[0] += 1
        if n[0] == 101:
            cursor_at_crash.append(run.state.get_cursor(w["town"]))
            raise RuntimeError("disk hiccup")
        return real(*a)
    monkeypatch.setattr(run.state, "enqueue_and_advance", flaky)

    async def supervised():                  # stands in for app.live.supervise: restart the crashed task
        while True:
            try:
                await run.lis.run()
            except RuntimeError:
                await asyncio.sleep(0.05)
    await run.stop()
    run.task = asyncio.create_task(supervised())
    await until(lambda: run.lis.status == "ok")
    posts = await run.outage(lambda: [run.post(w["town"], "bulk %d" % i) for i in range(150)])
    await until(lambda: len(run.state.wakes()) == 150)
    assert cursor_at_crash == [(posts[99]["create_at"], posts[99]["id"])]   # 100 committed before the crash
    assert n[0] > 150 and ids(run.state) == [p["id"] for p in posts]


async def test_unauthorized_token_degrades_then_retries(served, tmp_path, caplog):
    m, w, _ = served
    good = w["bot"]["token"]
    w["bot"]["token"] = "revoked-token-value"
    r = Run(served, tmp_path / "state.db", auth_retry_s=0.3)
    r.lis._cfg = lambda: BotConfig(token=good, wake_url="https://wake.example/hook", wake_secret="s" * 40)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        r.task = asyncio.create_task(r.lis.run())
        await until(lambda: r.lis.status == "degraded")
        w["bot"]["token"] = good                         # token fixed in Mattermost: next retry succeeds
        await until(lambda: r.lis.status == "ok")
    await r.stop()
    assert "mm_unauthorized" in caplog.text and good not in caplog.text


async def test_second_listener_cannot_take_the_lease(served, tmp_path, caplog):
    m = served[0]
    a = await Run(served, tmp_path / "state.db").start()
    b = Run(served, tmp_path / "state.db", lease_retry_s=0.1)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        b.task = asyncio.create_task(b.lis.run())
        await until(lambda: "listener_lease_held" in caplog.text)
    assert b.lis.status == "off"
    assert sum(c[0] == "WS" for c in m.calls) == 1
    await b.stop()
    await a.stop()


def test_reconnect_backoff_doubles_with_jitter_and_caps(tmp_path):
    lis = Listener(BotConfig("t" * 26, "https://x.example/h", "s" * 40), State(str(tmp_path / "s.db")),
                   lambda t: None, rand=lambda: 1.0)
    assert [lis._backoff(n) for n in range(1, 9)] == [1, 2, 4, 8, 16, 32, 60, 60]
    lis.rand = lambda: 0.0
    assert lis._backoff(3) == 2.0                       # jitter: between half and full delay
