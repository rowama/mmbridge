"""live_filter.decide: architecture Filter rules (REQ-A1 chosen channels, A2 DMs, A3 own posts)."""
import json
import logging

import pytest

from app.live_filter import WakeIntent, decide

BOT = "u-eddie"
CHOSEN = {"c-main-town-square"}


def posted(channel_id="c-main-town-square", ctype="O", user_id="u-rob", ptype="", root_id="", message="hi",
           post_as_str=True, **post_extra):
    post = {"id": "p-1", "channel_id": channel_id, "user_id": user_id, "message": message, "type": ptype,
            "create_at": 1_700_000_000_000, "root_id": root_id, **post_extra}
    return {"event": "posted", "seq": 3,
            "data": {"channel_type": ctype, "channel_name": "town-square", "channel_display_name": "Town Square",
                     "sender_name": "@rob", "team_id": "t-main", "post": json.dumps(post) if post_as_str else post},
            "broadcast": {"channel_id": channel_id}}


def test_chosen_channel_wakes():
    w = decide(posted(), BOT, CHOSEN)
    assert isinstance(w, WakeIntent)
    assert (w.post_id, w.channel_id, w.channel_type, w.user_id, w.message, w.create_at, w.root_id) == (
        "p-1", "c-main-town-square", "O", "u-rob", "hi", 1_700_000_000_000, None)


@pytest.mark.parametrize("ctype", ["O", "P"])
def test_non_chosen_open_or_private_channel_drops(ctype):
    assert decide(posted(channel_id="c-main-other", ctype=ctype), BOT, CHOSEN) is None


def test_chosen_private_channel_wakes():
    assert decide(posted(ctype="P"), BOT, CHOSEN) is not None


def test_dm_wakes_without_being_chosen():
    w = decide(posted(channel_id="d-u-eddie__u-rob", ctype="D"), BOT, CHOSEN)
    assert w is not None and w.channel_type == "D"


def test_group_dm_drops_even_if_chosen():
    assert decide(posted(ctype="G"), BOT, CHOSEN) is None


@pytest.mark.parametrize("ctype", ["O", "D"])
def test_own_post_drops(ctype):
    assert decide(posted(ctype=ctype, user_id=BOT), BOT, CHOSEN) is None


@pytest.mark.parametrize("ptype", ["system_join_channel", "system_add_to_channel", "system_header_change"])
def test_system_post_drops(ptype):
    assert decide(posted(ptype=ptype), BOT, CHOSEN) is None


def test_thread_reply_wakes_with_root_id():
    w = decide(posted(root_id="p-root"), BOT, CHOSEN)
    assert w is not None and w.root_id == "p-root"


def test_post_given_as_dict_is_accepted():
    assert decide(posted(post_as_str=False), BOT, CHOSEN) is not None


def test_non_posted_event_is_ignored_silently(caplog):
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        assert decide({"event": "typing", "data": {}, "seq": 2}, BOT, CHOSEN) is None
    assert "event_invalid" not in caplog.text


def _broken():
    e = posted(message="m-private-text")
    yield "no data", {"event": "posted", "seq": 1}
    yield "post not json", {**e, "data": {**e["data"], "post": "{not json"}}
    yield "post not object", {**e, "data": {**e["data"], "post": "[1, 2]"}}
    p = json.loads(e["data"]["post"])
    for field in ("id", "channel_id", "user_id", "create_at"):
        q = {k: v for k, v in p.items() if k != field}
        yield "missing " + field, {**e, "data": {**e["data"], "post": json.dumps(q)}}
    yield "create_at not int", {**e, "data": {**e["data"], "post": json.dumps({**p, "create_at": "x"})}}
    yield "message not str", {**e, "data": {**e["data"], "post": json.dumps({**p, "message": None})}}
    yield "no channel_type", {**e, "data": {k: v for k, v in e["data"].items() if k != "channel_type"}}
    yield "not a dict", ["posted"]


@pytest.mark.parametrize("label,event", list(_broken()), ids=[x[0] for x in _broken()])
def test_malformed_event_drops_and_logs_event_invalid(label, event, caplog):
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        assert decide(event, BOT, CHOSEN) is None
    assert "event_invalid" in caplog.text
    assert "m-private-text" not in caplog.text   # message text never logged
