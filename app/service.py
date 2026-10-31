"""Tool logic over the Mattermost client. Identity cache keyed by sha256(token) only."""
import time
from datetime import datetime, timezone

from app.errors import ToolError
from app.mattermost import Client, MMError
from app.validate import segment

IDENTITY_TTL_S = 60.0


class IdentityCache:
    def __init__(self, ttl: float = IDENTITY_TTL_S, clock=time.monotonic):
        self.ttl, self.clock, self._d = ttl, clock, {}

    async def me(self, c: Client, key: str) -> dict:
        hit = self._d.get(key)
        if hit and self.clock() - hit[0] < self.ttl:
            return hit[1]
        me = await c.get("/users/me")
        if len(self._d) > 10000:
            self._d.clear()
        self._d[key] = (self.clock(), {"id": me["id"], "username": me["username"]})
        return self._d[key][1]


async def list_channels(c: Client) -> dict:
    teams = await c.get("/users/me/teams")
    out = []
    for t in teams:
        for ch in await c.get("/users/me/teams/%s/channels" % t["id"]):
            if ch.get("type") in ("O", "P"):
                out.append({"team": t["name"], "name": ch["name"], "display_name": ch.get("display_name", ""),
                            "type": ch["type"]})
    return {"channels": out}


def iso(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


async def _member_channel(c: Client, team: str, channel: str) -> dict:
    """By-name lookup, then membership check (REQ-7). Never joins."""
    try:
        ch = await c.get("/teams/name/%s/channels/name/%s" % (segment(team), segment(channel)))
    except MMError as e:
        if e.status in (403, 404):
            raise ToolError("unknown_channel", "No channel %r in team %r visible to this bot." % (channel, team))
        raise
    try:
        await c.get("/channels/%s/members/me" % segment(ch["id"]))
    except MMError as e:
        if e.status in (403, 404):
            raise ToolError("not_member", "This bot is not a member of %s/%s; ask an admin to add it." % (team, channel))
        raise
    return ch


_BAD_ROOT = "root_id is not a post in this conversation that the bot can see."


async def _root(c: Client, root_id: str) -> dict:
    """Thread root (ADR-0015), fetched with the bot's own token. Mattermost 400/403/404 (bad id, no access,
    gone) -> invalid_root."""
    try:
        root = await c.get("/posts/%s" % segment(root_id))
    except MMError as e:
        if e.status in (400, 403, 404):
            raise ToolError("invalid_root", _BAD_ROOT)
        raise
    return root if isinstance(root, dict) else {}


def _same_channel(root: dict, channel_id: str) -> None:
    if root.get("channel_id") != channel_id:
        raise ToolError("invalid_root", _BAD_ROOT)


async def check_root(c: Client, root_id: str, channel_id: str) -> None:
    """The root must be a post in `channel_id` the bot can see; checked before any write."""
    _same_channel(await _root(c, root_id), channel_id)


def _new_post(channel_id: str, message: str, root_id: str | None) -> dict:
    return {"channel_id": channel_id, "message": message, **({"root_id": root_id} if root_id else {})}


async def post_channel(c: Client, team: str, channel: str, message: str, root_id: str | None = None) -> dict:
    ch = await _member_channel(c, team, channel)
    if root_id:
        await check_root(c, root_id, ch["id"])
    p = await c.post("/posts", _new_post(ch["id"], message, root_id))
    out = {"post_id": p["id"], "channel": channel, "team": team, "create_at": iso(p["create_at"])}
    return {**out, "root_id": root_id} if root_id else out


async def _read_posts(c: Client, channel_id: str, limit: int) -> list:
    data = await c.get("/channels/%s/posts" % segment(channel_id), page=0, per_page=limit)
    posts = sorted((data["posts"][i] for i in data.get("order", [])), key=lambda p: p["create_at"], reverse=True)[:limit]
    ids = sorted({p["user_id"] for p in posts})
    names = {u["id"]: u["username"] for u in (await c.post("/users/ids", ids) if ids else [])}
    return [{"id": p["id"], "author": names.get(p["user_id"], p["user_id"]),
             "create_at": iso(p["create_at"]), "message": p.get("message", "")} for p in posts]


async def read_channel(c: Client, team: str, channel: str, limit: int = 20) -> dict:
    ch = await _member_channel(c, team, channel)
    return {"team": team, "channel": channel, "posts": await _read_posts(c, ch["id"], limit)}


async def _direct_channel(c: Client, username: str, me: dict) -> dict:
    """users/username lookup (404 -> unknown_user, nothing created), then open-or-reuse the direct channel."""
    try:
        user = await c.get("/users/username/%s" % segment(username))
    except MMError as e:
        if e.status == 404:
            raise ToolError("unknown_user", "No Mattermost user named %r." % username)
        raise
    return await c.post("/channels/direct", [me["id"], user["id"]])


async def dm_send(c: Client, username: str, message: str, *, me: dict, root_id: str | None = None) -> dict:
    root = await _root(c, root_id) if root_id else None   # a root the bot cannot see: nothing opened or posted
    ch = await _direct_channel(c, username, me)
    if root is not None:
        _same_channel(root, ch["id"])
    p = await c.post("/posts", _new_post(ch["id"], message, root_id))
    out = {"post_id": p["id"], "channel_id": ch["id"], "create_at": iso(p["create_at"])}
    return {**out, "root_id": root_id} if root_id else out


async def dm_read(c: Client, username: str, limit: int = 20, *, me: dict) -> dict:
    ch = await _direct_channel(c, username, me)
    return {"username": username, "posts": await _read_posts(c, ch["id"], limit)}
