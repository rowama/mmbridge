"""Mattermost websocket listener for the ONE live bot (ADR-0007).

run(): GET /users/me -> WS /api/v4/websocket with `Authorization: Bearer` -> hello{connection_id} -> for each
`posted` event, live_filter.decide -> wake payload (ADR-0008 schema, no token; channel/team/sender lookups
cached) -> state.enqueue_and_advance (dedupe gate + forward-only cursor, PR-3). Tracks seq (gaps logged as
ws_seq_gap); sends the Mattermost `ping` action every PING_S and treats IDLE_S without any frame as dead.
One connection per run(): reconnect, resume and catch-up are slice 5. Never joins channels or posts.
"""
import asyncio
import itertools
import json
import logging
import time
from datetime import datetime, timezone

import websockets
from websockets.exceptions import ConnectionClosed

from app import logging as mlog
from app.live_filter import WakeIntent, decide
from app.mattermost import MATTERMOST_URL, MMError
from app.wake import token_fp

PING_S = 30
IDLE_S = 60

# websockets logs handshake headers (incl. Authorization) and frames at DEBUG: own logger, redacted, INFO.
_ws_log = logging.getLogger("mmbridge.ws")
_ws_log.setLevel(logging.INFO)
_ws_log.addFilter(mlog.RedactFilter())


def ws_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    return ("wss://" + base[8:] if base.startswith("https://") else "ws://" + base.removeprefix("http://")) \
        + "/api/v4/websocket"


def connect(url: str, headers: dict):
    """Default ws_connect: protocol-level keepalive off (the listener pings at application level)."""
    return websockets.connect(url, additional_headers=headers, ping_interval=None, open_timeout=10, logger=_ws_log)


def _log(event: str, **fields) -> None:
    mlog.log.info(json.dumps({"event": event, **fields}))


def _iso(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Listener:
    def __init__(self, cfg, state, client_factory, ws_connect=connect, clock=time.time,
                 base_url: str = MATTERMOST_URL, ping_s: float = PING_S, idle_s: float = IDLE_S):
        self.cfg, self.state, self.client_factory, self.ws_connect = cfg, state, client_factory, ws_connect
        self.clock, self.base_url, self.ping_s, self.idle_s = clock, base_url, ping_s, idle_s
        self.status = "off"                   # off | connecting | ok
        self.bot_user_id = self.connection_id = self.last_seq = None
        self._bot: dict = {}
        self._channels: dict = {}
        self._teams: dict = {}
        self._users: dict = {}

    async def run(self) -> None:
        mlog.register_secret(self.cfg.token)
        client = self.client_factory(self.cfg.token)
        self.status = "connecting"
        try:
            me = await client.get("/users/me")
            self.bot_user_id, self._bot = me["id"], {"user_id": me["id"], "username": me["username"]}
            await asyncio.to_thread(self.state.set_meta, "bot_user_id", me["id"])   # dispatcher: bot_rotated
            await asyncio.to_thread(self.state.set_meta, "bot_identity",              # id + token as one row
                                    token_fp(self.cfg.token) + ":" + me["id"])
            async with self.ws_connect(ws_url(self.base_url), {"Authorization": "Bearer " + self.cfg.token}) as ws:
                pinger = asyncio.create_task(self._ping(ws))
                try:
                    await self._read(ws, client)
                finally:
                    pinger.cancel()
        finally:
            self.status = "off"

    async def _read(self, ws, client) -> None:
        while True:
            try:
                raw = await asyncio.wait_for(ws.recv(), self.idle_s)
            except TimeoutError:
                _log("ws_idle", seconds=self.idle_s)
                return
            except ConnectionClosed:
                _log("ws_closed", connection_id=self.connection_id)
                return
            try:
                ev = json.loads(raw)
            except ValueError:
                mlog.log.warning(json.dumps({"event": "event_invalid", "reason": "json"}))
                continue
            if not isinstance(ev, dict) or "event" not in ev:
                continue                      # ping replies ({"status","seq_reply"}) and other non-events
            self._track_seq(ev)
            if ev["event"] == "hello":
                self.connection_id = (ev.get("data") or {}).get("connection_id")
                await asyncio.to_thread(self.state.set_meta, "ws_connection_id", self.connection_id or "")
                self.status = "ok"
                _log("ws_connected", connection_id=self.connection_id,
                     server_version=(ev.get("data") or {}).get("server_version"))
                continue
            intent = decide(ev, self.bot_user_id)
            if intent:
                payload = await self._payload(intent, client)
                new = await asyncio.to_thread(self.state.enqueue_and_advance, intent.post_id, intent.channel_id,
                                              payload, intent.create_at)
                _log("wake_queued", post_id=intent.post_id, channel_id=intent.channel_id, new=new)

    def _track_seq(self, ev: dict) -> None:
        seq = ev.get("seq")
        if not isinstance(seq, int):
            return
        if ev["event"] != "hello" and self.last_seq is not None and seq != self.last_seq + 1:
            _log("ws_seq_gap", expected=self.last_seq + 1, got=seq)
        self.last_seq = seq

    async def _ping(self, ws) -> None:
        for n in itertools.count(1):
            await asyncio.sleep(self.ping_s)
            try:
                await ws.send(json.dumps({"action": "ping", "seq": n}))
            except ConnectionClosed:
                return

    async def _get(self, client, cache: dict, key: str, path: str) -> dict | None:
        """Cached REST lookup; None (not cached) on Mattermost errors so the event hints are used instead."""
        if key not in cache:
            try:
                cache[key] = await client.get(path)
            except MMError as e:
                _log("lookup_failed", path=path.split("/")[1], code=e.code)
                return None
        return cache[key]

    async def _payload(self, w: WakeIntent, client) -> dict:
        h = w.hints
        ch = await self._get(client, self._channels, w.channel_id, "/channels/" + w.channel_id) or {}
        team_id = ch.get("team_id", h.get("team_id")) or ""
        team = await self._get(client, self._teams, team_id, "/teams/" + team_id) if team_id else None
        user = await self._get(client, self._users, w.user_id, "/users/" + w.user_id) or {}
        return {
            "version": 1, "kind": "post", "delivery_id": w.post_id, "attempt": 1,
            "bot": dict(self._bot),
            "channel": {"id": w.channel_id, "name": ch.get("name", h.get("channel_name")),
                        "display_name": ch.get("display_name", h.get("channel_display_name")),
                        "type": w.channel_type, "team": (team or {}).get("name")},
            "sender": {"user_id": w.user_id,
                       "username": user.get("username") or (h.get("sender_name") or "").lstrip("@") or None},
            "post": {"id": w.post_id, "message": w.message, "create_at": _iso(w.create_at), "root_id": w.root_id},
        }
