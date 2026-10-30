"""Fake Grok Bot routine webhooks (test harness only; ADR-0016). Drivers are not locked; edit freely.

POST /routine/{bot}: records every request (bot, headers, raw body, status). 503 while the bot is `down`;
401 unless `Authorization: Bearer <that bot's routine key>`; else 200 = "run started" (the Grok wake contract,
CP-A). `runs(bot)` are the started runs. B-s2 adds acting as the bot (reply via the MCP bridge).
"""
import contextlib
import json

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
        self.app = Starlette(routes=[Route("/routine/{bot}", self._call, methods=["POST"])])

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
        return JSONResponse({"run": rec["status"] == 200}, status_code=rec["status"])

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
            await _serve.stop(server, task)
