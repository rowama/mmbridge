"""Tool logic over the Mattermost client. Identity cache keyed by sha256(token) only."""
import time

from app.mattermost import Client

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
