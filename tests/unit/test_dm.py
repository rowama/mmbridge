"""Slice 3: dm_send / dm_read: unknown_user, direct-channel reuse, DM validation boundaries."""
import pytest

from conftest import call, payload, tok


@pytest.fixture
def rob(mm):
    return mm.add_user("rob")


@pytest.mark.parametrize("tool,args", [
    ("dm_send", {"username": "rob", "message": ""}),
    ("dm_send", {"username": "rob", "message": "   "}),
    ("dm_send", {"username": "rob", "message": "x" * 16384}),
    ("dm_send", {"username": "../users/me", "message": "hi"}),
    ("dm_send", {"username": "Rob", "message": "hi"}),
    ("dm_send", {"username": "rob%2F..", "message": "hi"}),
    ("dm_send", {"username": "x" * 65, "message": "hi"}),
    ("dm_send", {"username": "", "message": "hi"}),
    ("dm_send", {"username": 5, "message": "hi"}),
    ("dm_read", {"username": "rob", "limit": 0}),
    ("dm_read", {"username": "rob", "limit": 101}),
    ("dm_read", {"username": "rob", "limit": True}),
    ("dm_read", {"username": "rob", "limit": "5"}),
    ("dm_read", {"username": "a b"}),
])
async def test_dm_invalid_argument_zero_mm_calls(bridge, mm, rob, tool, args):
    is_err, d = payload(await call(bridge, tool, args, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "invalid_argument" and d["message"]
    assert mm.calls == []


async def test_dm_send_opens_then_reuses_direct_channel(bridge, mm, rob):
    eddie = mm.user_by_name("eddie")
    for msg in ("hello", "x" * 16383):
        is_err, d = payload(await call(bridge, "dm_send", {"username": "rob", "message": msg}, token=tok(mm, "eddie")))
        assert not is_err, d
        assert set(d) == {"post_id", "channel_id", "create_at"} and d["create_at"].endswith("Z")
        assert mm.posts[d["post_id"]]["message"] == msg
        assert mm.posts[d["post_id"]]["user_id"] == eddie["id"]
    chans = mm.direct_channels(eddie["id"], rob["id"])
    assert len(chans) == 1 and chans[0]["id"] == d["channel_id"]
    assert [c for c in mm.changes if c[0] == "direct_channel"] == [("direct_channel", d["channel_id"])]


async def test_dm_send_unknown_user_posts_nothing(bridge, mm):
    is_err, d = payload(await call(bridge, "dm_send", {"username": "nobody", "message": "hi"}, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "unknown_user" and d["message"]
    assert not any(m == "POST" for m, _, _ in mm.calls)
    assert mm.changes == []


async def test_dm_read_unknown_user(bridge, mm):
    is_err, d = payload(await call(bridge, "dm_read", {"username": "nobody"}, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "unknown_user"
    assert mm.changes == []


async def test_dm_read_shape_and_limit(bridge, mm, rob):
    eddie = mm.user_by_name("eddie")
    cid = mm.direct_channel(eddie["id"], rob["id"])["id"]
    for i in range(25):
        mm.add_post(cid, (rob if i % 2 else eddie)["id"], "m%d" % i)
    is_err, d = payload(await call(bridge, "dm_read", {"username": "rob"}, token=tok(mm, "eddie")))
    assert not is_err, d
    assert d["username"] == "rob" and len(d["posts"]) == 20
    assert d["posts"][0] == {"id": d["posts"][0]["id"], "author": "eddie", "create_at": d["posts"][0]["create_at"],
                             "message": "m24"}
    assert [p["create_at"] for p in d["posts"]] == sorted((p["create_at"] for p in d["posts"]), reverse=True)
    is_err, d = payload(await call(bridge, "dm_read", {"username": "rob", "limit": 1}, token=tok(mm, "eddie")))
    assert [p["message"] for p in d["posts"]] == ["m24"]
    assert not any(c[0] == "post" for c in mm.changes)


async def test_dm_send_counts_against_write_bucket(bridge, mm, rob):
    codes = []
    for _ in range(21):
        is_err, d = payload(await call(bridge, "dm_send", {"username": "rob", "message": "hi"}, token=tok(mm, "eddie")))
        codes.append(d.get("code") if is_err else "ok")
    assert codes[:20] == ["ok"] * 20 and codes[20] == "rate_limited"
