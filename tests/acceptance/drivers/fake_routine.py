"""Fake Grok Bot routines (test harness only; ADR-0016). Drivers are not locked; edit freely.

POST /routine/{bot}: records every request (bot, headers, raw body, status). 503 while the bot is `down`;
401 unless `Authorization: Bearer <that bot's routine key>`; else 200 = "run started" (the Grok wake contract,
CP-A). `runs(bot)` are the started runs.
B-s2: a started run of a bot with an answer (`answer(bot, text, token, mcp_url)`) acts as that bot: it reads the
wake's `reply` hints (tool, team + channel | username, root_id) and calls that tool on the real MCP bridge with the
bot's own Mattermost token, after answering 200 (as a real routine runs after accepting the webhook). Each call and
its tool result land in `replies`.
"""
import asyncio
import contextlib
import json

import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from drivers import _serve


class FakeRoutine:
    def __init__(self):
        self.keys = {}            # bot -> routine key
        self.down = set()         # bots whose routine fails with 503
        self.requests = []        # {"bot", "headers", "body", "status"}
        self.answers = {}         # bot -> (text, mm token, mcp url)
        self.replies = []         # {"bot", "tool", "args", "status", "result"}
        self._tasks = set()
        self.app = Starlette(routes=[Route("/routine/{bot}", self._call, methods=["POST"])])

    def answer(self, bot: str, text: str, token: str, mcp_url: str) -> None:
        self.answers[bot] = (text, token, mcp_url)

    async def _call(self, request: Request):
        bot = request.path_params["bot"]
        body = await request.body()
        rec = {"bot": bot, "headers": dict(request.headers), "body": body, "status": None}
        self.requests.append(rec)
        if bot in self.down:
            rec["status"] = 503
        elif bot not in self.keys or request.headers.get("authorization") != "Bearer " + self.keys[bot]:
            rec["status"] = 401
        else:
            rec["status"] = 200
            if bot in self.answers:
                t = asyncio.get_running_loop().create_task(self._act(bot, body))
                self._tasks.add(t)
                t.add_done_callback(self._tasks.discard)
        return JSONResponse({"run": rec["status"] == 200}, status_code=rec["status"])

    async def _act(self, bot: str, body: bytes) -> None:
        """The bot's run: answer through the MCP bridge using only what the wake body says."""
        text, token, mcp_url = self.answers[bot]
        hint = json.loads(body).get("reply") or {}
        tool = hint.get("tool")
        keys = ("team", "channel") if tool == "post_channel" else ("username",)
        args = {k: hint.get(k) for k in keys} | {"message": text}
        if hint.get("root_id"):
            args["root_id"] = hint["root_id"]
        rec = {"bot": bot, "tool": tool, "args": args, "status": None, "result": None}
        self.replies.append(rec)
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.post(mcp_url, headers={"accept": "application/json, text/event-stream",
                                                   "content-type": "application/json",
                                                   "authorization": "Bearer " + token},
                                 json={"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                       "params": {"name": tool, "arguments": args}})
            rec["status"] = r.status_code
            rec["result"] = r.json().get("result") if r.status_code == 200 else r.text
        except Exception as e:      # recorded for the assertion message; never kills the server
            rec["result"] = "error: %s" % type(e).__name__

    @staticmethod
    def post_id(rec) -> str | None:
        try:
            return json.loads(rec["body"])["post"]["id"]
        except (ValueError, KeyError, TypeError):
            return None

    def reached(self, bot: str, post_id: str) -> list[dict]:
        """Every request for this post that reached the bot's routine (any status)."""
        return [r for r in self.requests if r["bot"] == bot and self.post_id(r) == post_id]

    def runs(self, bot: str) -> list[dict]:
        return [r for r in self.requests if r["bot"] == bot and r["status"] == 200]

    @contextlib.asynccontextmanager
    async def serve(self):
        """Yields the base URL http://127.0.0.1:<port>/routine (append /<bot>)."""
        server, task, port = await _serve.start(self.app)
        try:
            yield "http://127.0.0.1:%d/routine" % port
        finally:
            for t in list(self._tasks):
                t.cancel()
            await asyncio.gather(*self._tasks, return_exceptions=True)
            await _serve.stop(server, task)
