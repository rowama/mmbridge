"""Slice 2: shared validators, write bucket, post_channel / read_channel paths."""
import pytest

from conftest import call, payload, tok
from app import validate
from app.errors import ToolError
from app.ratelimit import RateLimiter


def _invalid(fn, *a):
    with pytest.raises(ToolError) as e:
        fn(*a)
    assert e.value.code == "invalid_argument" and e.value.message


def test_limit_boundaries():
    assert validate.limit(None) == 20
    assert validate.limit(1) == 1 and validate.limit(100) == 100
    for bad in (0, 101, -1, True, False, "5", 5.0, [5]):
        _invalid(validate.limit, bad)


def test_message_boundaries():
    assert validate.message("x" * 16383) == "x" * 16383
    assert validate.message("  hi  ") == "hi"
    for bad in ("", "   ", "x" * 16384, None, 5):
        _invalid(validate.message, bad)


def test_identifier_rules():
    for ok in ("dev", "town-square", "a", "my_team.1", "x" * 64):
        assert validate.identifier("channel", ok) == ok
    for bad in ("a/b", "..", "a..b", "%2F", "dev%2Fx", "my channel", "Dev", "x" * 65, "", "-dev", "dev\n", None, 3):
        _invalid(validate.identifier, "channel", bad)


def test_segment_url_encodes():
    assert validate.segment("a/b c") == "a%2Fb%20c"


def test_write_bucket_independent_of_calls():
    rl = RateLimiter(calls_per_min=100, writes_per_min=2, anon_per_min=1, clock=lambda: 0.0)
    assert rl.check_write("a") == 0 and rl.check_write("a") == 0 and rl.check_write("a") > 0
    assert rl.check_write("b") == 0
    assert rl.check_call("a") == 0


def test_write_bucket_default_20():
    assert RateLimiter().writes_per_min == 20


@pytest.mark.parametrize("tool,args", [
    ("post_channel", {"team": "rmlab", "channel": "dev", "message": ""}),
    ("post_channel", {"team": "rmlab", "channel": "dev", "message": "x" * 16384}),
    ("post_channel", {"team": "rmlab", "channel": "../users", "message": "hi"}),
    ("post_channel", {"team": "RMLAB", "channel": "dev", "message": "hi"}),
    ("post_channel", {"team": "rmlab", "channel": "dev%2F..", "message": "hi"}),
    ("read_channel", {"team": "rmlab", "channel": "dev", "limit": 0}),
    ("read_channel", {"team": "rmlab", "channel": "dev", "limit": 101}),
    ("read_channel", {"team": "rmlab", "channel": "dev", "limit": True}),
    ("read_channel", {"team": "rmlab", "channel": "dev", "limit": "5"}),
    ("read_channel", {"team": "rmlab", "channel": "a b", "limit": 5}),
])
async def test_invalid_argument_zero_mm_calls(bridge, mm, tool, args):
    is_err, d = payload(await call(bridge, tool, args, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "invalid_argument" and d["message"]
    assert mm.calls == []


async def test_post_channel_ok(bridge, mm):
    is_err, d = payload(await call(bridge, "post_channel", {"team": "rmlab", "channel": "dev", "message": "hi"},
                                   token=tok(mm, "eddie")))
    assert not is_err
    assert set(d) == {"post_id", "channel", "team", "create_at"}
    assert d["channel"] == "dev" and d["team"] == "rmlab" and d["create_at"].endswith("Z")
    assert mm.posts[d["post_id"]]["message"] == "hi"


@pytest.mark.parametrize("tool,args", [
    ("post_channel", {"team": "rmlab", "channel": "ops", "message": "hi"}),
    ("read_channel", {"team": "rmlab", "channel": "ops"}),
])
async def test_not_member_no_post_no_posts_get(bridge, mm, tool, args):
    is_err, d = payload(await call(bridge, tool, args, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "not_member" and d["message"]
    assert not [c for c in mm.calls if c[0] == "POST" or c[1].endswith("/posts")]
    assert mm.changes == []


@pytest.mark.parametrize("tool", ["post_channel", "read_channel"])
async def test_unknown_channel(bridge, mm, tool):
    args = {"team": "rmlab", "channel": "ghost"} | ({"message": "hi"} if tool == "post_channel" else {})
    is_err, d = payload(await call(bridge, tool, args, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "unknown_channel" and d["message"]
    assert not [c for c in mm.calls if "/members" in c[1] or c[1].endswith("/posts")]


async def test_read_channel_format_newest_first(bridge, mm):
    cid = mm.channel_by_name("dev")["id"]
    rob = mm.add_user("rob")
    for i in range(3):
        mm.add_post(cid, rob["id"], "m%d" % i)
    is_err, d = payload(await call(bridge, "read_channel", {"team": "rmlab", "channel": "dev", "limit": 2},
                                   token=tok(mm, "eddie")))
    assert not is_err
    assert [p["message"] for p in d["posts"]] == ["m2", "m1"]
    p = d["posts"][0]
    assert set(p) == {"id", "author", "create_at", "message"}
    assert p["author"] == "rob" and p["create_at"] == "2023-11-14T22:13:22.000Z"


async def test_write_rate_limit_21st_post(bridge, mm):
    t = tok(mm, "eddie")
    args = {"team": "rmlab", "channel": "dev", "message": "hi"}
    for _ in range(20):
        assert not payload(await call(bridge, "post_channel", args, token=t))[0]
    n = len(mm.calls)
    is_err, d = payload(await call(bridge, "post_channel", args, token=t))
    assert is_err and d["code"] == "rate_limited" and d["retry_after_s"] > 0
    assert len(mm.calls) == n
    # reads are not write-limited
    assert not payload(await call(bridge, "read_channel", {"team": "rmlab", "channel": "dev"}, token=t))[0]
