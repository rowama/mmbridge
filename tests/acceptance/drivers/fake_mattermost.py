"""Recording fake of the Mattermost /api/v4 endpoints the bridge uses (test harness only).

Injected into the bridge via httpx.ASGITransport. Records every call as (method, path, auth_token).
Slice 1: users/me, users/me/teams, users/me/teams/{id}/channels.
Slice 2: channel by name, members/me, POST /posts, channel posts, POST /users/ids.
Slice 3: users/username/{u}, POST /channels/direct (idempotent; creating one is a world change).
"""
import itertools

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
        self.posts = {}      # id -> {"id","channel_id","user_id","message","create_at"}
        self.calls = []      # (method, path, token)
        self.changes = []    # world changes made through the API (seeding is not a change)
        self._clock = itertools.count(1_700_000_000_000, 1000)
        self._ids = itertools.count(1)
        self.down = False
        self.fail_status = None   # force every response to this HTTP status
        self.app = Starlette(routes=[
            Route("/api/v4/users/me", self._me),
            Route("/api/v4/users/me/teams", self._teams),
            Route("/api/v4/users/me/teams/{team_id}/channels", self._team_channels),
            Route("/api/v4/teams/name/{team}/channels/name/{channel}", self._channel_by_name),
            Route("/api/v4/channels/{channel_id}/members/me", self._member_me),
            Route("/api/v4/channels/{channel_id}/posts", self._channel_posts),
            Route("/api/v4/posts", self._create_post, methods=["POST"]),
            Route("/api/v4/users/ids", self._users_by_ids, methods=["POST"]),
            Route("/api/v4/users/username/{username}", self._user_by_username),
            Route("/api/v4/channels/direct", self._direct, methods=["POST"]),
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

    def channel_by_name(self, name, team=None):
        return next(c for c in self.channels.values()
                    if c["name"] == name and (team is None or self.teams[c["team_id"]]["name"] == team))

    def direct_channel(self, user_a, user_b):
        """Get or create the direct channel between two user ids (MM name: sorted ids joined by '__')."""
        cid = "d-" + "__".join(sorted((user_a, user_b)))
        if cid not in self.channels:
            self.channels[cid] = {"id": cid, "team_id": "", "name": cid[2:], "display_name": "",
                                  "type": "D", "members": {user_a, user_b}}
        return self.channels[cid]

    def direct_channels(self, user_a, user_b):
        return [c for c in self.channels.values() if c["type"] == "D" and c["members"] == {user_a, user_b}]

    def add_post(self, channel_id, user_id, message):
        pid = "p-%d" % next(self._ids)
        self.posts[pid] = {"id": pid, "channel_id": channel_id, "user_id": user_id, "message": message,
                           "create_at": next(self._clock)}
        return self.posts[pid]

    def channel_posts(self, channel_id):
        """Posts of a channel, oldest first."""
        return sorted((p for p in self.posts.values() if p["channel_id"] == channel_id), key=lambda p: p["create_at"])

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
        tids = {c["team_id"] for c in self.channels.values() if u["id"] in c["members"] and c["team_id"]}
        return JSONResponse([self.teams[t] for t in sorted(tids)])

    async def _team_channels(self, request):
        u, err = self._auth(request)
        if err:
            return err
        tid = request.path_params["team_id"]
        return JSONResponse([{k: v for k, v in c.items() if k != "members"}
                             for c in self.channels.values() if c["team_id"] == tid and u["id"] in c["members"]])

    def _member_channel(self, u, cid):
        c = self.channels.get(cid)
        if not c:
            return None, JSONResponse({"message": "not found"}, status_code=404)
        if u["id"] not in c["members"]:
            return None, JSONResponse({"message": "no permission"}, status_code=403)
        return c, None

    async def _channel_by_name(self, request):
        u, err = self._auth(request)
        if err:
            return err
        p = request.path_params
        c = next((c for c in self.channels.values() if c["name"] == p["channel"] and c["team_id"]
                  and self.teams[c["team_id"]]["name"] == p["team"]), None)
        if not c:
            return JSONResponse({"message": "not found"}, status_code=404)
        return JSONResponse({k: v for k, v in c.items() if k != "members"})

    async def _member_me(self, request):
        u, err = self._auth(request)
        if err:
            return err
        c = self.channels.get(request.path_params["channel_id"])
        if not c or u["id"] not in c["members"]:
            return JSONResponse({"message": "not found"}, status_code=404)
        return JSONResponse({"channel_id": c["id"], "user_id": u["id"]})

    async def _channel_posts(self, request):
        u, err = self._auth(request)
        if err:
            return err
        c, err = self._member_channel(u, request.path_params["channel_id"])
        if err:
            return err
        page, per_page = int(request.query_params.get("page", 0)), int(request.query_params.get("per_page", 60))
        newest = list(reversed(self.channel_posts(c["id"])))[page * per_page:(page + 1) * per_page]
        return JSONResponse({"order": [p["id"] for p in newest], "posts": {p["id"]: p for p in newest}})

    async def _create_post(self, request):
        u, err = self._auth(request)
        if err:
            return err
        body = await request.json()
        c, err = self._member_channel(u, body.get("channel_id"))
        if err:
            return err
        p = self.add_post(c["id"], u["id"], body["message"])
        self.changes.append(("post", c["id"], p["id"]))
        return JSONResponse(p, status_code=201)

    async def _users_by_ids(self, request):
        u, err = self._auth(request)
        if err:
            return err
        ids = await request.json()
        return JSONResponse([{"id": x["id"], "username": x["username"]} for i in ids if (x := self.users.get(i))])

    async def _user_by_username(self, request):
        u, err = self._auth(request)
        if err:
            return err
        x = next((x for x in self.users.values() if x["username"] == request.path_params["username"]), None)
        if not x:
            return JSONResponse({"message": "not found"}, status_code=404)
        return JSONResponse({"id": x["id"], "username": x["username"], "is_bot": x["is_bot"]})

    async def _direct(self, request):
        u, err = self._auth(request)
        if err:
            return err
        ids = await request.json()
        if not isinstance(ids, list) or len(ids) != 2 or u["id"] not in ids or not all(i in self.users for i in ids):
            return JSONResponse({"message": "bad request"}, status_code=400)
        existed = bool(self.direct_channels(*ids))
        c = self.direct_channel(*ids)
        if not existed:
            self.changes.append(("direct_channel", c["id"]))
        return JSONResponse({k: v for k, v in c.items() if k != "members"}, status_code=200 if existed else 201)


def _tok(headers):
    a = headers.get("authorization", "")
    return a[7:] if a.startswith("Bearer ") else None
