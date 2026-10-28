"""Recording fake of the Mattermost /api/v4 endpoints the bridge uses (test harness only).

Injected into the bridge via httpx.ASGITransport. Records every call as (method, path, auth_token).
Slice 1: users/me, users/me/teams, users/me/teams/{id}/channels.
Slice 2: channel by name, members/me, POST /posts, channel posts, POST /users/ids.
Slice 3: users/username/{u}, POST /channels/direct (idempotent; creating one is a world change).
Live bots lb3: GET channels/{id}, teams/{id}, users/{id}; websocket /api/v4/websocket (Bearer handshake,
hello{connection_id}, per-connection seq, `posted` broadcast to channel members, ping action -> pong reply,
drop/raw/seq-skip controls). `serve()` runs the app on a free localhost port for real HTTP/WS clients.
Live bots lb4: `mm_ids=True` gives channels Mattermost-shaped 26-char ids (the bot store validates them).
Live bots lb5: `clock` (seconds callable, e.g. time.time) stamps posts with real ms (catch-up windows); channel
posts: `since` as Mattermost (paging ignored, capped at `since_cap`), else newest-first pages with `before`/`after`
post-id anchors (fix cycle: catch-up pages by id); GET /users/{id}/channels (all, D included); /users/me/teams and team channels page (`page`/`per_page`) and team channel lists include
the user's D/G channels (as Mattermost does); `ws_refuse` (REST 503 + websocket handshake 503, an MM restart);
resume: a dropped session stays resumable (`ws_drop(resumable=True)`), keeps receiving its events in a dead
queue, and a reconnect with `?connection_id&sequence_number` gets hello (same id, no seq) + the missed events.
"""
import asyncio
import contextlib
import hashlib
import itertools
import json
from urllib.parse import parse_qs

import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route, WebSocketRoute
from starlette.websockets import WebSocket


class FakeMattermost:
    def __init__(self, mm_ids=False, clock=None):
        self.mm_ids, self.clock = mm_ids, clock
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
        self.server_version = "10.11.0"
        self.ws_sessions = []     # open websocket sessions (_WsSession)
        self.ws_answer_pings = True
        self.ws_pings = 0
        self.ws_refuse = False    # Mattermost unreachable: REST 503, websocket handshake 503
        self.ws_dead = {}         # connection_id -> resumable dropped _WsSession (dead queue)
        self.ws_resumes = 0
        self.since_cap = 1000     # Mattermost caps `GET /channels/{id}/posts?since=` (and ignores paging there)
        self.posts_queries = []   # (channel_id, query dict) of every channel posts call
        self._ws_ids = itertools.count(1)
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
            Route("/api/v4/channels/{channel_id}", self._channel),
            Route("/api/v4/teams/{team_id}", self._team),
            Route("/api/v4/users/{user_id}/channels", self._user_channels),
            Route("/api/v4/users/{user_id}", self._user),
            WebSocketRoute("/api/v4/websocket", self._ws),
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
        if self.mm_ids:
            cid = hashlib.sha1(cid.encode()).hexdigest()[:26]
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

    def _now_ms(self):
        if self.clock is None:
            return next(self._clock)
        self._last_ms = max(int(self.clock() * 1000), getattr(self, "_last_ms", 0) + 1)
        return self._last_ms

    def add_post(self, channel_id, user_id, message, type="", root_id="", create_at=None):
        """Create a post and broadcast `posted` to the channel members' websocket sessions (as Mattermost does,
        including the author's own sessions; dead resumable sessions queue it)."""
        pid = "p-%d" % next(self._ids)
        self.posts[pid] = p = {"id": pid, "channel_id": channel_id, "user_id": user_id, "message": message,
                               "create_at": self._now_ms() if create_at is None else create_at, "type": type,
                               "root_id": root_id}
        c = self.channels[channel_id]
        event = {"event": "posted", "broadcast": {"channel_id": channel_id, "team_id": "", "user_id": ""},
                 "data": {"channel_display_name": c["display_name"], "channel_name": c["name"],
                          "channel_type": c["type"], "sender_name": "@" + self.users[user_id]["username"],
                          "team_id": c["team_id"], "post": json.dumps(p)}}
        for s in self.ws_sessions + list(self.ws_dead.values()):
            if s.user_id in c["members"]:
                s.push(event)
        return p

    def ws_event(self, user_id, event, data, broadcast=None):
        """Send a non-post event (user_added, added_to_team, user_removed, ...) to the user's sessions."""
        for s in self.ws_sessions:
            if s.user_id == user_id:
                s.push({"event": event, "data": data, "broadcast": broadcast or {"user_id": user_id}})

    # --- websocket controls -------------------------------------------------------
    def ws_send_raw(self, event):
        """Send a raw frame (dict -> JSON with the session seq; str -> as is) to every open session."""
        for s in self.ws_sessions:
            s.push(event) if isinstance(event, dict) else s.q.put_nowait(event)

    def ws_resend_last(self):
        """Re-send each session's last event with a fresh seq (duplicate delivery)."""
        for s in self.ws_sessions:
            s.push({k: v for k, v in s.last.items() if k != "seq"})

    def ws_skip_seq(self, n=1):
        for s in self.ws_sessions + list(self.ws_dead.values()):
            s.seq += n

    def ws_drop(self, resumable=False):
        """Close every open websocket session (connection drop). resumable: the server keeps each session's
        dead queue so a reconnect with its connection_id resumes; otherwise reconnects get a new id."""
        for s in self.ws_sessions:
            s.resumable = resumable
            s.q.put_nowait(None)
        if not resumable:
            self.ws_dead.clear()

    @contextlib.asynccontextmanager
    async def serve(self):
        """Serve REST + websocket on 127.0.0.1:<free port>; yields the base URL (http://127.0.0.1:<port>)."""
        import uvicorn
        server = uvicorn.Server(uvicorn.Config(self.app, host="127.0.0.1", port=0, log_level="warning",
                                               lifespan="off", ws="websockets"))
        task = asyncio.create_task(server.serve())
        while not server.started:
            if task.done():
                task.result()
            await asyncio.sleep(0.01)
        port = server.servers[0].sockets[0].getsockname()[1]
        try:
            yield "http://127.0.0.1:%d" % port
        finally:
            self.ws_drop()
            server.should_exit = True
            await task

    def channel_posts(self, channel_id):
        """Posts of a channel, oldest first (create_at, then creation order)."""
        return sorted((p for p in self.posts.values() if p["channel_id"] == channel_id),
                      key=lambda p: (p["create_at"], int(p["id"][2:])))

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
        if self.ws_refuse:
            return None, JSONResponse({"message": "unavailable"}, status_code=503)
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
        return JSONResponse(_page(request, [self.teams[t] for t in sorted(tids)]))

    async def _team_channels(self, request):
        u, err = self._auth(request)
        if err:
            return err
        tid = request.path_params["team_id"]
        return JSONResponse(_page(request, [{k: v for k, v in c.items() if k != "members"}
                                            for c in self.channels.values()
                                            if c["team_id"] in (tid, "") and u["id"] in c["members"]]))

    async def _user_channels(self, request):
        """GET /users/{id}/channels: every channel of the user across teams, D/G included (no paging)."""
        u, err = self._auth(request)
        if err:
            return err
        if request.path_params["user_id"] != u["id"]:
            return JSONResponse({"message": "no permission"}, status_code=403)
        return JSONResponse([{k: v for k, v in c.items() if k != "members"}
                             for c in self.channels.values() if u["id"] in c["members"]])

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
        q = request.query_params
        self.posts_queries.append((c["id"], dict(q)))
        page, per_page = int(q.get("page", 0)), int(q.get("per_page", 60))
        newest = list(reversed(self.channel_posts(c["id"])))
        if "since" in q:                      # as Mattermost: page/per_page ignored, result capped
            since = int(q["since"])
            newest = [p for p in newest if p["create_at"] > since][:self.since_cap]
        else:
            ids = [p["id"] for p in newest]
            if q.get("before"):
                newest = newest[ids.index(q["before"]) + 1:] if q["before"] in ids else []
            elif q.get("after"):          # the per_page posts right after the anchor, still newest first
                later = list(reversed(newest[:ids.index(q["after"])])) if q["after"] in ids else []
                newest = list(reversed(later[page * per_page:(page + 1) * per_page]))
            if not q.get("after"):
                newest = newest[page * per_page:(page + 1) * per_page]
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

    async def _channel(self, request):
        u, err = self._auth(request)
        if err:
            return err
        c, err = self._member_channel(u, request.path_params["channel_id"])
        if err:
            return err
        return JSONResponse({k: v for k, v in c.items() if k != "members"})

    async def _team(self, request):
        u, err = self._auth(request)
        if err:
            return err
        t = self.teams.get(request.path_params["team_id"])
        return JSONResponse(t) if t else JSONResponse({"message": "not found"}, status_code=404)

    async def _user(self, request):
        u, err = self._auth(request)
        if err:
            return err
        x = self.users.get(request.path_params["user_id"])
        if not x:
            return JSONResponse({"message": "not found"}, status_code=404)
        return JSONResponse({"id": x["id"], "username": x["username"], "is_bot": x["is_bot"]})

    async def _ws(self, ws: WebSocket):
        tok = _tok(ws.headers)
        self.calls.append(("WS", ws.url.path, tok))
        user = next((u for u in self.users.values() if tok and u["token"] == tok), None)
        if self.ws_refuse:
            await ws.send_denial_response(JSONResponse({"message": "unavailable"}, status_code=503))
            return
        if not user or self.fail_status:
            await ws.close(code=1008)          # before accept: the handshake is refused (HTTP 403)
            return
        await ws.accept()
        q = parse_qs(ws.url.query)
        cid, seq = (q.get("connection_id") or [""])[0], (q.get("sequence_number") or [""])[0]
        dead = self.ws_dead.pop(cid, None)
        if dead is not None and dead.user_id == user["id"] and seq.isdigit():
            s, self.ws_resumes = dead, self.ws_resumes + 1
            s.q, s.resumable = asyncio.Queue(), False
            s.q.put_nowait({"event": "hello", "data": {"connection_id": cid, "server_version": self.server_version},
                            "broadcast": {"user_id": user["id"]}})
            for ev in s.history:
                if ev["seq"] >= int(seq):
                    s.q.put_nowait(ev)
        else:
            s = _WsSession(user["id"], "conn-%d" % next(self._ws_ids))
            s.push({"event": "hello", "data": {"connection_id": s.connection_id,
                                               "server_version": self.server_version},
                    "broadcast": {"user_id": user["id"]}})
        self.ws_sessions.append(s)

        async def writer():
            while (m := await s.q.get()) is not None:
                await ws.send_text(m if isinstance(m, str) else json.dumps(m))

        async def reader():
            while True:
                msg = json.loads(await ws.receive_text())
                if msg.get("action") == "ping":
                    self.ws_pings += 1
                    if self.ws_answer_pings:
                        s.q.put_nowait({"status": "OK", "seq_reply": msg.get("seq"),
                                        "data": {"text": "pong", "version": self.server_version}})
        tasks = [asyncio.create_task(writer()), asyncio.create_task(reader())]
        try:
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        finally:
            for t in tasks:
                t.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            self.ws_sessions.remove(s)
            if s.resumable:
                self.ws_dead[s.connection_id] = s
            with contextlib.suppress(Exception):
                await ws.close()

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


class _WsSession:
    """One websocket connection: outgoing queue (None closes it) and the per-connection seq (hello is 0)."""

    def __init__(self, user_id, connection_id):
        self.user_id, self.connection_id = user_id, connection_id
        self.q = asyncio.Queue()
        self.seq, self.last = 0, None
        self.history = []          # every event sent (replayed from sequence_number on resume)
        self.resumable = False

    def push(self, event):
        self.last = {**event, "seq": self.seq}
        self.seq += 1
        self.history.append(self.last)
        self.q.put_nowait(self.last)


def _page(request, items):
    q = request.query_params
    if "per_page" not in q:
        return items
    page, per_page = int(q.get("page", 0)), int(q["per_page"])
    return items[page * per_page:(page + 1) * per_page]


def _tok(headers):
    a = headers.get("authorization", "")
    return a[7:] if a.startswith("Bearer ") else None
