"""MCP protocol driver (layer 3): drives the bridge app over Streamable HTTP (/mcp) in-process,
with Mattermost replaced by a recording fake (/api/v4). Slice 1: list_channels + auth.
Slice 2: channel posts (post/read). Slice 3: DMs (direct channels in the fake, DM world/inspection helpers)."""
import io
import json
import logging

import anyio
import httpx
from anyio.from_thread import start_blocking_portal

from drivers.fake_mattermost import FakeMattermost

INVALID_TOKEN = "invalidtokenAAAAAAAAAAAAAAAAAAAA"


class McpDriver:
    def __init__(self):
        from app.main import create_app
        self.mm = FakeMattermost()
        self.app = create_app(mm_transport=self.mm.transport())
        self._bot = None
        self._last_token = None
        self._log = io.StringIO()
        self._handler = logging.StreamHandler(self._log)
        logging.getLogger("mmbridge").addHandler(self._handler)
        self._portal_cm = start_blocking_portal()
        self._portal = self._portal_cm.__enter__()
        self._stop = self._portal.call(anyio.Event)
        started = self._portal.call(anyio.Event)
        self._held = self._portal.start_task_soon(self._hold, started)
        self._portal.call(started.wait)
        self._id = 0
        self._seeded = None   # channel id of the last given_channel_posts

    async def _hold(self, started):  # lifespan enter/exit in one task (anyio cancel scopes)
        async with self.app.router.lifespan_context(self.app):
            started.set()
            await self._stop.wait()

    # --- given -------------------------------------------------------------------
    def given_bot(self, name):
        self.mm.add_user(name, bot=True)
        if self._bot is None:
            self._bot = name

    def given_user(self, username):
        self.mm.add_user(username)

    def given_channel(self, team, channel, members):
        self.mm.add_channel(team, channel, members)

    def given_channel_posts(self, team, channel, count):
        cid = self.mm.channel_by_name(channel, team)["id"]
        author = next((u for u in self.mm.users.values() if u["username"] == "seed-author"), None) \
            or self.mm.add_user("seed-author")
        for i in range(count):
            self.mm.add_post(cid, author["id"], "seeded post %d" % (i + 1))
        self._seeded = cid

    def given_no_channel(self, team, channel):
        self.mm.add_team(team)
        assert not any(c["name"] == channel and c["team_id"] == "t-" + team for c in self.mm.channels.values())

    def given_dm_post(self, author, bot, message):
        a, b = self.mm.user_by_name(author), self.mm.user_by_name(bot)
        self.mm.add_post(self.mm.direct_channel(a["id"], b["id"])["id"], a["id"], message)

    def given_no_user(self, username):
        assert not any(u["username"] == username for u in self.mm.users.values())

    def given_mattermost_down(self):
        self.mm.down = True

    def as_bot(self, name):
        self._bot = name

    # --- when --------------------------------------------------------------------
    def call(self, tool, args, credential="valid"):
        headers = {"accept": "application/json, text/event-stream", "content-type": "application/json"}
        if credential == "valid":
            tok = self.mm.user_by_name(self._bot)["token"]
        elif credential == "invalid":
            tok = INVALID_TOKEN
        else:
            tok = None
        self._last_token = tok or self.mm.user_by_name(self._bot)["token"]
        if tok:
            headers["authorization"] = "Bearer " + tok
        self._id += 1
        body = {"jsonrpc": "2.0", "id": self._id, "method": "tools/call",
                "params": {"name": tool, "arguments": args}}
        return self._portal.call(self._post, headers, body)

    async def _post(self, headers, body):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app),
                                     base_url="http://testserver") as c:
            r = await c.post("/mcp", headers=headers, json=body)
        out = {"http_status": r.status_code, "result": None, "error": None, "raw": r.text}
        if r.status_code != 200:
            return out
        res = r.json().get("result", {})
        data = res.get("structuredContent")
        if data is None:
            text = "".join(c.get("text", "") for c in res.get("content", []))
            try:
                data = json.loads(text) if text else {}
            except ValueError:  # SDK-level error text (e.g. unknown tool)
                data = {"code": "tool_error", "message": text}
        if "result" in data and len(data) == 1:
            data = data["result"]
        if res.get("isError"):
            out["error"] = data
        else:
            out["result"] = data
        return out

    # --- inspection --------------------------------------------------------------
    def mattermost_calls(self):
        return [(m, p) for m, p, _ in self.mm.calls]

    def channel_posts(self, channel):
        cid = self.mm.channel_by_name(channel)["id"]
        return [(self.mm.users[p["user_id"]]["username"], p["message"]) for p in self.mm.channel_posts(cid)]

    def _dm_pair(self, bot, username):
        return self.mm.user_by_name(bot)["id"], self.mm.user_by_name(username)["id"]

    def dm_posts(self, bot, username):
        return [(self.mm.users[p["user_id"]]["username"], p["message"])
                for c in self.mm.direct_channels(*self._dm_pair(bot, username)) for p in self.mm.channel_posts(c["id"])]

    def dm_channel_count(self, bot, username):
        return len(self.mm.direct_channels(*self._dm_pair(bot, username)))

    def newest_posts(self, count):
        return [(p["id"], p["message"]) for p in reversed(self.mm.channel_posts(self._seeded))][:count]

    def world_changes(self):
        return list(self.mm.changes)

    def current_token(self):
        return self._last_token

    def bridge_logs(self):
        return self._log.getvalue()

    def __getattr__(self, name):
        raise NotImplementedError("McpDriver.%s: implement in the slice that needs it" % name)

    def close(self):
        logging.getLogger("mmbridge").removeHandler(self._handler)
        self._portal.call(self._stop.set)
        self._held.result()
        self._portal_cm.__exit__(None, None, None)
