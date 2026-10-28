"""Listener against the fake Mattermost REST + websocket (served by uvicorn on a free port): users/me,
Bearer handshake, hello/seq, ping/idle, posted -> filter -> state.db (enqueue_and_advance)."""
import asyncio
import json
import logging

import pytest

from app.listener import Listener, ws_url
from app.mattermost import Client
from app.state import State
from app.store import BotConfig
from drivers.fake_mattermost import FakeMattermost


@pytest.fixture
def world():
    m = FakeMattermost()
    bot = m.add_user("eddie", bot=True)
    rob = m.add_user("rob")
    m.add_team("main")
    chosen = m.add_channel("main", "town-square", ["eddie", "rob"])
    other = m.add_channel("main", "off-topic", ["eddie", "rob"])
    hr = m.add_channel("main", "hr", ["rob"], ctype="P")          # bot is not a member
    group = m.add_channel("main", "gdm", ["eddie", "rob"], ctype="G")
    dm = m.direct_channel(bot["id"], rob["id"])["id"]
    return m, {"bot": bot, "rob": rob, "chosen": chosen, "other": other, "hr": hr, "group": group, "dm": dm}


@pytest.fixture
async def served(world):
    m, w = world
    async with m.serve() as base_url:
        yield m, w, base_url


def make(served, tmp_path, **kw):
    m, w, base = served
    cfg = BotConfig(token=w["bot"]["token"], wake_url="https://wake.example/hook", wake_secret="s" * 40)
    state = State(str(tmp_path / "state.db"))
    lis = Listener(cfg, state, lambda tok: Client(tok, base_url=base), base_url=base, **kw)
    return lis, state


async def until(pred, timeout=5.0):
    for _ in range(int(timeout / 0.02)):
        if pred():
            return
        await asyncio.sleep(0.02)
    raise AssertionError("condition not met in %.1fs" % timeout)


@pytest.fixture
async def running(served, tmp_path):
    lis, state = make(served, tmp_path)
    task = asyncio.create_task(lis.run())
    await until(lambda: lis.status == "ok")
    yield served[0], served[1], lis, state
    served[0].ws_drop()
    await asyncio.wait_for(task, 5)


def test_ws_url():
    assert ws_url("http://mattermost:8065") == "ws://mattermost:8065/api/v4/websocket"
    assert ws_url("https://chat.example/") == "wss://chat.example/api/v4/websocket"


async def test_qualifying_posts_land_once_in_state(running):
    m, w, lis, state = running
    rob, bot = w["rob"]["id"], w["bot"]["id"]
    wake1 = m.add_post(w["chosen"], rob, "eddie is great")
    other = m.add_post(w["other"], rob, "@channel any member channel wakes")
    m.add_post(w["hr"], rob, "salary review")             # non-member: Mattermost never sends it to the bot
    m.add_post(w["chosen"], bot, "my own post")
    m.add_post(w["chosen"], rob, "rob joined", type="system_join_channel")
    m.add_post(w["group"], rob, "group dm")
    wake2 = m.add_post(w["dm"], rob, "ping")
    reply = m.add_post(w["chosen"], rob, "a reply", root_id=wake1["id"])
    m.ws_resend_last()                      # duplicate delivery of the reply event: dedupe gate
    marker = m.add_post(w["dm"], rob, "marker")
    await until(lambda: state.wake(marker["id"]) is not None)
    assert [x.post_id for x in state.wakes()] == [wake1["id"], other["id"], wake2["id"], reply["id"],
                                                  marker["id"]]
    assert all(x.status == "queued" for x in state.wakes())
    assert state.get_cursor(w["chosen"]) == (reply["create_at"], reply["id"])
    assert state.get_cursor(w["hr"]) is None
    assert state.get_cursor(w["dm"]) == (marker["create_at"], marker["id"])
    assert state.wake(reply["id"]).payload["post"]["root_id"] == wake1["id"]
    assert state.wake(wake1["id"]).post_create_at == wake1["create_at"]


async def test_payload_matches_wake_contract(running):
    m, w, lis, state = running
    p = m.add_post(w["chosen"], w["rob"]["id"], "eddie is great")
    d = m.add_post(w["dm"], w["rob"]["id"], "ping")
    await until(lambda: state.wake(d["id"]) is not None)
    assert state.wake(p["id"]).payload == {
        "version": 1, "kind": "post", "delivery_id": p["id"], "attempt": 1,
        "bot": {"user_id": w["bot"]["id"], "username": "eddie"},
        "channel": {"id": w["chosen"], "name": "town-square", "display_name": "Town-Square", "type": "O",
                    "team": "main"},
        "sender": {"user_id": w["rob"]["id"], "username": "rob"},
        "post": {"id": p["id"], "message": "eddie is great", "create_at": "2023-11-14T22:13:20Z", "root_id": None}}
    dm = state.wake(d["id"]).payload
    assert dm["channel"]["type"] == "D" and dm["channel"]["team"] is None and dm["sender"]["username"] == "rob"


async def test_lookups_are_cached(running):
    m, w, lis, state = running
    for i in range(3):
        last = m.add_post(w["chosen"], w["rob"]["id"], "msg %d" % i)
    await until(lambda: state.wake(last["id"]) is not None)
    paths = [c[1] for c in m.calls]
    assert paths.count("/api/v4/channels/%s" % w["chosen"]) == 1
    assert paths.count("/api/v4/users/%s" % w["rob"]["id"]) == 1
    assert paths.count("/api/v4/teams/t-main") == 1


async def test_bearer_header_on_handshake_and_rest(running):
    m, w, lis, state = running
    tok = w["bot"]["token"]
    assert ("GET", "/api/v4/users/me", tok) in m.calls
    assert ("WS", "/api/v4/websocket", tok) in m.calls
    assert lis.connection_id and state.get_meta("ws_connection_id") == lis.connection_id
    assert lis.bot_user_id == w["bot"]["id"]
    assert state.get_meta("bot_user_id") == w["bot"]["id"]      # dispatcher fails wakes of a rotated bot (PR-2)
    from app.wake import token_fp
    assert state.get_meta("bot_identity") == token_fp(lis.cfg.token) + ":" + w["bot"]["id"]   # identity of the current token (review P1)


@pytest.mark.parametrize("ws_level", [None, logging.DEBUG], ids=["default", "ws-debug"])
async def test_token_absent_from_logs_and_state(served, tmp_path, caplog, ws_level):
    m, w, _ = served
    with caplog.at_level(logging.DEBUG), caplog.at_level(ws_level or logging.INFO, logger="mmbridge.ws"):
        lis, state = make(served, tmp_path)
        task = asyncio.create_task(lis.run())
        await until(lambda: lis.status == "ok")
        p = m.add_post(w["chosen"], w["rob"]["id"], "hello")
        await until(lambda: state.wake(p["id"]) is not None)
        m.ws_drop()
        await asyncio.wait_for(task, 5)
    tok = w["bot"]["token"]
    assert "wake_queued" in caplog.text and "ws_connected" in caplog.text
    assert tok not in caplog.text
    assert tok not in json.dumps([x.payload for x in state.wakes()])
    state.close()
    for f in tmp_path.iterdir():
        assert tok.encode() not in f.read_bytes()


async def test_malformed_event_is_skipped_and_listener_keeps_going(running, caplog):
    m, w, lis, state = running
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        m.ws_send_raw("{not json")
        m.ws_send_raw({"event": "posted", "data": {"channel_type": "O", "post": "{broken"}})
        p = m.add_post(w["chosen"], w["rob"]["id"], "still listening")
        await until(lambda: state.wake(p["id"]) is not None)
    assert caplog.text.count("event_invalid") == 2
    assert [x.post_id for x in state.wakes()] == [p["id"]]


async def test_seq_is_tracked_and_gap_logged(running, caplog):
    m, w, lis, state = running
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        a = m.add_post(w["chosen"], w["rob"]["id"], "one")
        await until(lambda: state.wake(a["id"]) is not None)
        assert lis.last_seq == 1
        m.ws_skip_seq(2)
        b = m.add_post(w["chosen"], w["rob"]["id"], "two")
        await until(lambda: state.wake(b["id"]) is not None)
    assert lis.last_seq == 4
    assert '"event": "ws_seq_gap"' in caplog.text and '"expected": 2' in caplog.text


async def test_pings_keep_a_quiet_connection_alive(served, tmp_path):
    m, w, _ = served
    lis, state = make(served, tmp_path, ping_s=0.05, idle_s=0.3)
    task = asyncio.create_task(lis.run())
    await until(lambda: lis.status == "ok")
    await asyncio.sleep(1.0)
    assert not task.done() and m.ws_pings >= 5
    m.ws_drop()
    await asyncio.wait_for(task, 5)
    assert lis.status == "off"


async def test_idle_connection_is_treated_as_dead(served, tmp_path, caplog):
    m, w, _ = served
    m.ws_answer_pings = False
    lis, state = make(served, tmp_path, ping_s=0.05, idle_s=0.3)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        await asyncio.wait_for(lis.run(), 5)
    assert lis.status == "off" and "ws_idle" in caplog.text


async def test_listener_never_joins_or_posts(running):
    m, w, lis, state = running
    p = m.add_post(w["chosen"], w["rob"]["id"], "hi")
    await until(lambda: state.wake(p["id"]) is not None)
    assert m.changes == []
    assert all(c[0] in ("GET", "WS") for c in m.calls)


async def test_ws_spike_prints_shapes_without_token_or_text(served):
    from app.ws_spike import spike
    m, w, base = served
    lines = []

    async def post_soon():
        await until(lambda: m.ws_pings)   # ping reply is queued before the posted event
        m.add_post(w["chosen"], w["rob"]["id"], "m-private-text")
    poster = asyncio.create_task(post_soon())
    assert await spike(w["bot"]["token"], base, 5, out=lines.append) == 0
    await poster
    text = "\n".join(lines)
    assert "hello: event=hello seq=0 connection_id=True" in text
    assert "ping reply shape" in text and "posted: seq=1 channel_type=O" in text
    assert w["bot"]["token"] not in text and "m-private-text" not in text
