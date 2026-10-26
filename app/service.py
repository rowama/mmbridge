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


async def post_channel(c: Client, team: str, channel: str, message: str) -> dict:
    ch = await _member_channel(c, team, channel)
    p = await c.post("/posts", {"channel_id": ch["id"], "message": message})
    return {"post_id": p["id"], "channel": channel, "team": team, "create_at": iso(p["create_at"])}


async def read_channel(c: Client, team: str, channel: str, limit: int = 20) -> dict:
    ch = await _member_channel(c, team, channel)
    data = await c.get("/channels/%s/posts" % segment(ch["id"]), page=0, per_page=limit)
    posts = sorted((data["posts"][i] for i in data.get("order", [])), key=lambda p: p["create_at"], reverse=True)[:limit]
    ids = sorted({p["user_id"] for p in posts})
    names = {u["id"]: u["username"] for u in (await c.post("/users/ids", ids) if ids else [])}
    return {"team": team, "channel": channel,
            "posts": [{"id": p["id"], "author": names.get(p["user_id"], p["user_id"]),
                       "create_at": iso(p["create_at"]), "message": p.get("message", "")} for p in posts]}
