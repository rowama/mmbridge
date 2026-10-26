"""Recording fake of the Mattermost /api/v4 endpoints the bridge uses (test harness only).

Injected into the bridge via httpx.ASGITransport. Records every call as (method, path, auth_token).
Slice 1: users/me, users/me/teams, users/me/teams/{id}/channels. Extended in slices 2-3.
"""
import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


class FakeMattermost:
    def __init__(self):
        self.users = {}      # id -> {"id","username","token"|None,"is_bot"}
        self.teams = {}      # id -> {"id","name","display_name"}
        self.channels = {}   # id -> {"id","team_id","name","display_name","type","members":set}
        self.calls = []      # (method, path, token)
        self.changes = []
        self.down = False
        self.fail_status = None   # force every response to this HTTP status
        self.app = Starlette(routes=[
            Route("/api/v4/users/me", self._me),
            Route("/api/v4/users/me/teams", self._teams),
            Route("/api/v4/users/me/teams/{team_id}/channels", self._team_channels),
        ])

    # --- world setup -------------------------------------------------------------
    def add_user(self, username, bot=False):
        uid = "u-" + username
        self.users[uid] = {"id": uid, "username": username, "is_bot": bot,
                           "token": ("tok-%s-%s" % (username, "x" * 20)) if bot else None}
        return self.users[uid]

    def user_by_name(self, username):
        return next(u for u in self.users.values() if u["username"] == username)

    def add_team(self, name):
        tid = "t-" + name
        self.teams.setdefault(tid, {"id": tid, "name": name, "display_name": name.title()})
        return tid

    def add_channel(self, team, name, members=(), ctype="O"):
        tid = self.add_team(team)
        cid = "c-%s-%s" % (team, name)
        self.channels[cid] = {"id": cid, "team_id": tid, "name": name, "display_name": name.title(),
                              "type": ctype, "members": {self.user_by_name(m)["id"] for m in members}}
        return cid

    def transport(self):
        fake = self

        class _T(httpx.AsyncBaseTransport):
            def __init__(self):
                self._inner = httpx.ASGITransport(app=fake.app)

            async def handle_async_request(self, request):
                if fake.down:
                    fake.calls.append((request.method, request.url.path, _tok(request.headers)))
                    raise httpx.ConnectError("connection refused", request=request)
                return await self._inner.handle_async_request(request)

        return _T()

    # --- endpoints ---------------------------------------------------------------
    def _auth(self, request: Request):
        tok = _tok(request.headers)
        self.calls.append((request.method, request.url.path, tok))
        if self.fail_status:
            return None, JSONResponse({"message": "forced"}, status_code=self.fail_status)
        user = next((u for u in self.users.values() if tok and u["token"] == tok), None)
        if not user:
            return None, JSONResponse({"message": "Invalid or expired session"}, status_code=401)
        return user, None

    async def _me(self, request):
        u, err = self._auth(request)
        if err:
            return err
        return JSONResponse({"id": u["id"], "username": u["username"], "is_bot": u["is_bot"]})

    async def _teams(self, request):
        u, err = self._auth(request)
        if err:
            return err
        tids = {c["team_id"] for c in self.channels.values() if u["id"] in c["members"]}
        return JSONResponse([self.teams[t] for t in sorted(tids)])

    async def _team_channels(self, request):
        u, err = self._auth(request)
        if err:
            return err
        tid = request.path_params["team_id"]
        return JSONResponse([{k: v for k, v in c.items() if k != "members"}
                             for c in self.channels.values() if c["team_id"] == tid and u["id"] in c["members"]])


def _tok(headers):
    a = headers.get("authorization", "")
    return a[7:] if a.startswith("Bearer ") else None
