"""B-s2 (ADR-0015, plan Phase 2): optional root_id on post_channel / dm_send. The root is fetched with the bot's
own token before posting and must belong to the target channel (post_channel) or the bot<->user DM (dm_send);
anything else is `invalid_root` and no post is created."""
import pytest

from conftest import call, payload, tok
from app import service, validate
from app.errors import ToolError
from app.mattermost import MMError
from drivers.fake_mattermost import FakeMattermost


@pytest.fixture
def mm():
    """Mattermost-shaped 26-char ids (root_id is validated as a Mattermost id)."""
    m = FakeMattermost(mm_ids=True)
    eddie, rob, ulrik = m.add_user("eddie", bot=True), m.add_user("rob"), m.add_user("ulrik")
    m.add_channel("rmlab", "dev", ["eddie", "rob"])
    m.add_channel("rmlab", "ops", ["eddie", "rob"])
    m.add_channel("rmlab", "hr", ["rob"], ctype="P")                      # bot is not a member
    m.dm_rob = m.direct_channel(eddie["id"], rob["id"])["id"]
    m.dm_ulrik = m.direct_channel(eddie["id"], ulrik["id"])["id"]
    m.dm_others = m.direct_channel(rob["id"], ulrik["id"])["id"]           # bot is not in it
    return m


def root(mm, where, author="rob", message="root post"):
    cid = mm.channel_by_name(where, "rmlab")["id"] if not where.startswith("dm") else getattr(mm, where)
    return mm.add_post(cid, mm.user_by_name(author)["id"], message)["id"]


def posts_created(mm):
    return [c for c in mm.changes if c[0] == "post"]


def no_post_call(mm):
    return not [c for c in mm.calls if c[0] == "POST" and c[1].endswith("/posts")]


def test_post_id_validator():
    assert validate.post_id(None) is None
    assert validate.post_id("a" * 26) == "a" * 26
    assert validate.post_id("p0000000000000000000000001") == "p0000000000000000000000001"
    for bad in ("a" * 25, "a" * 27, "A" * 26, "p-1", "", "a" * 25 + "/", "a" * 25 + "\n", 26, ["a" * 26]):
        with pytest.raises(ToolError) as e:
            validate.post_id(bad)
        assert e.value.code == "invalid_argument" and e.value.message


async def test_post_channel_root_id_replies_in_thread(bridge, mm):
    r = root(mm, "dev")
    is_err, d = payload(await call(bridge, "post_channel", {"team": "rmlab", "channel": "dev", "message": "on it",
                                                            "root_id": r}, token=tok(mm, "eddie")))
    assert not is_err, d
    assert mm.posts[d["post_id"]]["root_id"] == r and d["root_id"] == r
    assert ("GET", "/api/v4/posts/" + r, tok(mm, "eddie")) in mm.calls       # fetched with the bot's token


async def test_post_channel_without_root_id_unchanged(bridge, mm):
    is_err, d = payload(await call(bridge, "post_channel", {"team": "rmlab", "channel": "dev", "message": "hi"},
                                   token=tok(mm, "eddie")))
    assert not is_err and set(d) == {"post_id", "channel", "team", "create_at"}
    assert mm.posts[d["post_id"]]["root_id"] == ""
    assert not [c for c in mm.calls if c[1].startswith("/api/v4/posts/")]


@pytest.mark.parametrize("where", ["ops", "hr", "dm_rob"])
async def test_post_channel_root_from_another_channel_is_invalid_root(bridge, mm, where):
    """A valid root id of a post in another channel (member or not, or a DM) never posts (plan review #8)."""
    r = root(mm, where)
    is_err, d = payload(await call(bridge, "post_channel", {"team": "rmlab", "channel": "dev", "message": "x",
                                                            "root_id": r}, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "invalid_root" and d["message"]
    assert posts_created(mm) == [] and no_post_call(mm)


async def test_post_channel_unknown_root_is_invalid_root(bridge, mm):
    is_err, d = payload(await call(bridge, "post_channel", {"team": "rmlab", "channel": "dev", "message": "x",
                                                            "root_id": "z" * 26}, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "invalid_root"
    assert posts_created(mm) == [] and no_post_call(mm)


async def test_post_channel_not_member_wins_over_root(bridge, mm):
    r = root(mm, "hr")
    is_err, d = payload(await call(bridge, "post_channel", {"team": "rmlab", "channel": "hr", "message": "x",
                                                            "root_id": r}, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "not_member" and posts_created(mm) == []


@pytest.mark.parametrize("tool,args", [
    ("post_channel", {"team": "rmlab", "channel": "dev", "message": "x"}),
    ("dm_send", {"username": "rob", "message": "x"}),
])
@pytest.mark.parametrize("bad", ["p-1", "A" * 26, "a" * 25, "a" * 27, "../../users/me" + "a" * 12, 7])
async def test_bad_root_id_format_is_invalid_argument_zero_mm_calls(bridge, mm, tool, args, bad):
    is_err, d = payload(await call(bridge, tool, {**args, "root_id": bad}, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "invalid_argument"
    assert mm.calls == []


async def test_dm_send_root_id_replies_in_dm_thread(bridge, mm):
    r = root(mm, "dm_rob")
    is_err, d = payload(await call(bridge, "dm_send", {"username": "rob", "message": "hello Rob", "root_id": r},
                                   token=tok(mm, "eddie")))
    assert not is_err, d
    p = mm.posts[d["post_id"]]
    assert p["root_id"] == r and p["channel_id"] == mm.dm_rob and d["root_id"] == r


@pytest.mark.parametrize("where", ["dm_ulrik", "dm_others", "dev"])
async def test_dm_send_root_from_another_conversation_is_invalid_root(bridge, mm, where):
    """Root of the bot's DM with someone else, of another users' DM (bot not in it) or of a channel post."""
    r = root(mm, where, author="ulrik" if where != "dev" else "rob")
    is_err, d = payload(await call(bridge, "dm_send", {"username": "rob", "message": "x", "root_id": r},
                                   token=tok(mm, "eddie")))
    assert is_err and d["code"] == "invalid_root" and d["message"]
    assert posts_created(mm) == [] and no_post_call(mm)


async def test_dm_send_unknown_root_creates_nothing(bridge, mm):
    is_err, d = payload(await call(bridge, "dm_send", {"username": "rob", "message": "x", "root_id": "z" * 26},
                                   token=tok(mm, "eddie")))
    assert is_err and d["code"] == "invalid_root"
    assert mm.changes == []                    # no post and no new DM conversation


class _Stub:
    def __init__(self, exc=None, post=None):
        self.exc, self.post_ = exc, post

    async def get(self, path, **_):
        if self.exc:
            raise self.exc
        return self.post_


@pytest.mark.parametrize("status", [400, 403, 404])
async def test_root_lookup_mattermost_4xx_is_invalid_root(status):
    code = {404: "not_found"}.get(status, "mattermost_error")
    with pytest.raises(ToolError) as e:
        await service.check_root(_Stub(MMError(code, status)), "a" * 26, "c" * 26)
    assert e.value.code == "invalid_root"


async def test_root_lookup_other_errors_propagate():
    with pytest.raises(MMError):
        await service.check_root(_Stub(MMError("mattermost_unavailable")), "a" * 26, "c" * 26)


async def test_root_lookup_compares_channel():
    await service.check_root(_Stub(post={"id": "a" * 26, "channel_id": "c" * 26}), "a" * 26, "c" * 26)
    with pytest.raises(ToolError):
        await service.check_root(_Stub(post={"id": "a" * 26, "channel_id": "d" * 26}), "a" * 26, "c" * 26)
    with pytest.raises(ToolError):
        await service.check_root(_Stub(post={"id": "a" * 26}), "a" * 26, "c" * 26)


async def test_tool_schema_documents_root_id(bridge, mm):
    r = await bridge.post("/mcp", headers={"accept": "application/json, text/event-stream",
                                           "content-type": "application/json",
                                           "authorization": "Bearer " + tok(mm, "eddie")},
                          json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    tools = {t["name"]: t for t in r.json()["result"]["tools"]}
    for name in ("post_channel", "dm_send"):
        prop = tools[name]["inputSchema"]["properties"]["root_id"]
        assert "thread" in prop["description"].lower()
        assert "root_id" not in tools[name]["inputSchema"].get("required", [])


@pytest.mark.parametrize("tool,where,args", [
    ("post_channel", "dev", {"team": "rmlab", "channel": "dev"}),
    ("dm_send", "dm_rob", {"username": "rob"}),
])
async def test_root_that_is_itself_a_reply_is_invalid_root(bridge, mm, tool, where, args):
    """Mattermost threads have one level: a reply inside the conversation is not a thread root (review F1)."""
    r = root(mm, where)
    cid = mm.posts[r]["channel_id"]
    reply = mm.add_post(cid, mm.user_by_name("rob")["id"], "a reply", root_id=r)["id"]
    is_err, d = payload(await call(bridge, tool, {**args, "message": "x", "root_id": reply}, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "invalid_root"
    assert posts_created(mm) == [] and no_post_call(mm)
