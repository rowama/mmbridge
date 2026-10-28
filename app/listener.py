"""Mattermost websocket listener for the ONE live bot (ADR-0007).

run(): GET /users/me -> WS /api/v4/websocket with `Authorization: Bearer` -> hello{connection_id} -> for each
`posted` event, live_filter.decide -> wake payload (ADR-0008 schema, no token; channel/team/sender lookups
cached) -> state.enqueue_and_advance (dedupe gate + forward-only cursor, PR-3). Tracks seq; sends the
Mattermost `ping` action every PING_S and treats IDLE_S without any frame as dead. Never joins channels or posts.

lb5: run() reconnects forever (backoff 1->60 s with jitter) and asks to resume with
`?connection_id&sequence_number`. Same connection_id in hello = resumed (missed events are replayed). A new id,
or a seq gap, runs REST catch-up: membership across all teams (+ D channels, channels with a cursor, channels
seen on the socket), then per channel `GET /channels/{id}/posts` paged back by post id (`before=`; never
`since`, which Mattermost does not page), ascending (create_at, post_id),
each post through decide() and enqueue_and_advance (the ledger dedupes). Channels without a cursor start at meta
`last_event_at` (last alive); posts older than LIVE_CATCHUP_MINUTES are skipped (`catchup_skipped`). 401 ->
`degraded`, retry every 5 min or on a config change. One listener per state.db (meta lease `listener_owner`).
"""
import asyncio
import itertools
import json
import logging
import os
import random
import time
from datetime import datetime, timezone

import websockets
from websockets.exceptions import ConnectionClosed, InvalidHandshake, InvalidStatus

from app import logging as mlog
from app.live_filter import WakeIntent, decide
from app.mattermost import MATTERMOST_URL, MMError
from app.wake import token_fp

PING_S = 30
IDLE_S = 60
BACKOFF_S, MAX_BACKOFF_S = 1.0, 60.0
AUTH_RETRY_S = 300
LEASE_TTL_S = 60
PER_PAGE = 200
MAX_PAGES = 50
ALIVE_EVERY_S = 5

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


class Unauthorized(Exception):
    """users/me or the websocket handshake refused the bot token."""


class LeaseHeld(Exception):
    """Another listener holds the state.db lease."""


class Listener:
    def __init__(self, cfg, state, client_factory, ws_connect=connect, clock=time.time,
                 base_url: str = MATTERMOST_URL, ping_s: float = PING_S, idle_s: float = IDLE_S,
                 backoff_s: float = BACKOFF_S, max_backoff_s: float = MAX_BACKOFF_S,
                 auth_retry_s: float = AUTH_RETRY_S, lease_retry_s: float = LEASE_TTL_S / 2,
                 catchup_minutes: float | None = None, refresh_s: float | None = None, per_page: int = PER_PAGE,
                 rand=random.random):
        """cfg: BotConfig or a zero-arg callable returning the current one (ConfigHolder.get, PR-2)."""
        self._cfg = cfg if callable(cfg) else (lambda: cfg)
        self.state, self.client_factory, self.ws_connect = state, client_factory, ws_connect
        self.clock, self.base_url, self.ping_s, self.idle_s = clock, base_url, ping_s, idle_s
        self.backoff_s, self.max_backoff_s, self.rand = backoff_s, max_backoff_s, rand
        self.auth_retry_s, self.lease_retry_s, self.per_page = auth_retry_s, lease_retry_s, per_page
        self.window_ms = int(60_000 * (catchup_minutes if catchup_minutes is not None
                                       else float(os.getenv("LIVE_CATCHUP_MINUTES", "15"))))
        self.refresh_s = refresh_s if refresh_s is not None else float(os.getenv("LIVE_MEMBERSHIP_REFRESH_S", "300"))
        self.status = "off"                   # off | connecting | ok | degraded (401)
        self.bot_user_id = self.connection_id = self.last_seq = None
        self.members: dict = {}               # channel id -> channel (O/P/D), catch-up set
        self._seen: dict = {}                 # channel id -> type, seen on the socket since start
        self._bot: dict = {}
        self._channels: dict = {}
        self._teams: dict = {}
        self._users: dict = {}
        self._alive_at = None                 # ms, last frame received (meta last_event_at)
        self._alive_written = 0.0
        self._refreshed_at = 0.0
        self._catchup_pending = False
        self._catchup_from = None
        self._resume_id = None
        self._ws = None
        self._wake = asyncio.Event()

    @property
    def cfg(self):
        return self._cfg()

    def config_changed(self, old, new) -> None:
        """ConfigHolder subscriber: a new token reconnects at once (no resume across tokens, fresh lookups)."""
        if new.token == old.token:
            return
        mlog.register_secret(new.token)
        self.connection_id = None
        self._channels, self._teams, self._users = {}, {}, {}
        self._wake.set()
        if self._ws is not None:
            asyncio.ensure_future(self._ws.close())

    def _backoff(self, attempt: int) -> float:
        d = min(self.max_backoff_s, self.backoff_s * 2 ** (max(attempt, 1) - 1))
        return d * (0.5 + 0.5 * self.rand())

    async def _pause(self, seconds: float) -> None:
        """Sleep, cut short by a config change."""
        self._wake.clear()
        try:
            await asyncio.wait_for(self._wake.wait(), seconds)
        except TimeoutError:
            pass

    async def run(self) -> None:
        """Reconnect forever (cancel to stop)."""
        attempt = 0
        try:
            while True:
                try:
                    ok = await self.connect_once()
                    attempt = 0 if ok else attempt + 1
                except Unauthorized:
                    self.status = "degraded"
                    mlog.log.warning(json.dumps({"event": "mm_unauthorized", "retry_s": self.auth_retry_s}))
                    await self._pause(self.auth_retry_s)
                    continue
                except LeaseHeld:
                    _log("listener_lease_held", instance=self.state.instance_id)
                    await self._pause(self.lease_retry_s)
                    continue
                except (OSError, TimeoutError, MMError, InvalidHandshake, ConnectionClosed) as e:
                    attempt += 1
                    _log("ws_connect_failed", error=getattr(e, "code", None) or type(e).__name__)
                delay = self._backoff(attempt)
                self.status = "connecting"
                _log("ws_reconnect", attempt=attempt, delay=round(delay, 2))
                await self._pause(delay)
        finally:
            self.status = "off"
            await asyncio.to_thread(self.state.release_owner, "listener_owner")

    async def connect_once(self) -> bool:
        """One connection; True if it reached hello (then dropped/idled). Raises Unauthorized / LeaseHeld."""
        cfg = self.cfg
        mlog.register_secret(cfg.token)
        client = self.client_factory(cfg.token)
        self.status = "connecting"
        reached = False
        try:
            if not await asyncio.to_thread(self.state.claim_owner, self.clock(), LEASE_TTL_S, "listener_owner"):
                self.status = "off"
                raise LeaseHeld()
            if self._alive_at is None:
                v = await asyncio.to_thread(self.state.get_meta, "last_event_at")
                self._alive_at = int(v) if v else None
            try:
                me = await client.get("/users/me")
            except MMError as e:
                if e.code == "unauthorized":
                    raise Unauthorized() from None
                raise
            if me["id"] != self.bot_user_id:
                self.connection_id, self.members, self._seen = None, {}, {}
            self.bot_user_id, self._bot = me["id"], {"user_id": me["id"], "username": me["username"]}
            await asyncio.to_thread(self.state.set_meta, "bot_user_id", me["id"])   # dispatcher: bot_rotated
            await asyncio.to_thread(self.state.set_meta, "bot_identity",              # id + token as one row
                                    token_fp(cfg.token) + ":" + me["id"])
            url = ws_url(self.base_url)
            self._resume_id = self.connection_id
            if self.connection_id and self.last_seq is not None:
                url += "?connection_id=%s&sequence_number=%d" % (self.connection_id, self.last_seq + 1)
            try:
                conn = self.ws_connect(url, {"Authorization": "Bearer " + cfg.token})
                ws = await conn.__aenter__()
            except InvalidStatus as e:
                if e.response.status_code in (401, 403):
                    raise Unauthorized() from None
                raise
            self._ws = ws
            try:
                pinger = asyncio.create_task(self._ping(ws))
                try:
                    reached = await self._read(ws, client)
                finally:
                    pinger.cancel()
            finally:
                self._ws = None
                await conn.__aexit__(None, None, None)
        finally:
            if self.status != "degraded":
                self.status = "off"
        return reached

    async def _read(self, ws, client) -> bool:
        reached = False
        while True:
            try:
                raw = await asyncio.wait_for(ws.recv(), self.idle_s)
            except TimeoutError:
                _log("ws_idle", seconds=self.idle_s)
                return reached
            except ConnectionClosed:
                _log("ws_closed", connection_id=self.connection_id)
                return reached
            prev_alive = self._alive_at
            self._alive_at = int(self.clock() * 1000)   # in memory now; persisted only once the frame is handled
            if await self._frame(raw, client, prev_alive):
                reached = True
            await self._mark_alive()

    async def _frame(self, raw, client, prev_alive: int | None) -> bool:
        """Handle one frame; True when it was a hello (connection established). Raises leave last_seq and
        meta last_event_at untouched, so a reconnect resumes/catches up from before this frame."""
        try:
            ev = json.loads(raw)
        except ValueError:
            mlog.log.warning(json.dumps({"event": "event_invalid", "reason": "json"}))
            return False
        if not isinstance(ev, dict) or "event" not in ev:
            return False                      # ping replies ({"status","seq_reply"}) and other non-events
        if ev["event"] == "hello":
            cid = (ev.get("data") or {}).get("connection_id")
            resumed = bool(cid) and cid == self._resume_id
            self.connection_id = cid
            await asyncio.to_thread(self.state.set_meta, "ws_connection_id", cid or "")
            if not resumed:
                self.last_seq = ev.get("seq") if isinstance(ev.get("seq"), int) else 0
            _log("ws_connected", connection_id=cid, resumed=resumed,
                 server_version=(ev.get("data") or {}).get("server_version"))
            if not resumed or self._catchup_pending:
                await self._catch_up(client, "new_connection" if not resumed else "pending", prev_alive)
            elif time.monotonic() - self._refreshed_at >= self.refresh_s:
                await self._refresh_soft(client)
            self.status = "ok"
            return True
        seq = ev.get("seq")
        if self._seq_gap(ev):
            await self._catch_up(client, "seq_gap", prev_alive)
        if time.monotonic() - self._refreshed_at >= self.refresh_s:
            await self._refresh_soft(client)
        await self._membership_event(ev, client)
        intent = decide(ev, self.bot_user_id)
        if intent:
            self._seen.setdefault(intent.channel_id, {"id": intent.channel_id, "type": intent.channel_type})
            await self._enqueue(intent, client)
        if isinstance(seq, int):
            self.last_seq = seq           # only after the event is committed (a raise above replays it)
        return False

    async def _enqueue(self, intent: WakeIntent, client) -> bool:
        payload = await self._payload(intent, client)
        new = await asyncio.to_thread(self.state.enqueue_and_advance, intent.post_id, intent.channel_id,
                                      payload, intent.create_at)
        _log("wake_queued", post_id=intent.post_id, channel_id=intent.channel_id, new=new)
        return new

    def _seq_gap(self, ev: dict) -> bool:
        """True on a seq gap (missed events). Does not advance last_seq (_frame does, after the commit)."""
        seq = ev.get("seq")
        if not isinstance(seq, int):
            return False
        gap = self.last_seq is not None and seq != self.last_seq + 1
        if gap:
            _log("ws_seq_gap", expected=self.last_seq + 1, got=seq)
        return gap

    async def _mark_alive(self) -> None:
        """Persist the last-alive time of a fully handled frame (never mid catch-up: a restart then still
        starts cursor-less channels at the catch-up's own start)."""
        if self._alive_at is None or self._catchup_pending:
            return
        if time.monotonic() - self._alive_written >= ALIVE_EVERY_S:
            self._alive_written = time.monotonic()
            await asyncio.to_thread(self.state.set_meta, "last_event_at", str(self._alive_at))

    async def _ping(self, ws) -> None:
        for n in itertools.count(1):
            await asyncio.sleep(self.ping_s)
            if not await asyncio.to_thread(self.state.claim_owner, self.clock(), LEASE_TTL_S, "listener_owner"):
                _log("listener_lease_lost", instance=self.state.instance_id)
                await ws.close()
                return
            try:
                await ws.send(json.dumps({"action": "ping", "seq": n}))
            except ConnectionClosed:
                return

    # --- membership + catch-up (architecture 'catch-up channel discovery') -------------------------------------
    async def _paged(self, client, path: str) -> list:
        out, ids = [], set()
        for page in range(MAX_PAGES):
            batch = await client.get(path, page=page, per_page=self.per_page)
            new = [x for x in batch if isinstance(x, dict) and x.get("id") not in ids]
            ids.update(x["id"] for x in new)
            out += new
            if len(batch) < self.per_page or not new:
                break
        return out

    async def _refresh_members(self, client) -> None:
        found = {}
        for t in await self._paged(client, "/users/me/teams"):
            for c in await self._paged(client, "/users/me/teams/%s/channels" % t["id"]):
                if c.get("type") in ("O", "P", "D"):
                    found[c["id"]] = c
        for cid in await asyncio.to_thread(self.state.cursor_channels):
            found.setdefault(cid, self.members.get(cid) or {"id": cid})
        for cid, c in self._seen.items():
            found.setdefault(cid, c)
        self.members, self._refreshed_at = found, time.monotonic()

    async def _refresh_soft(self, client) -> None:
        """Periodic/event refresh: a Mattermost error keeps the old set (catch-up refreshes again)."""
        try:
            await self._refresh_members(client)
        except MMError as e:
            self._refreshed_at = time.monotonic()
            _log("membership_refresh_failed", code=e.code)

    async def _membership_event(self, ev: dict, client) -> None:
        kind, data, bc = ev["event"], ev.get("data") or {}, ev.get("broadcast") or {}
        if kind in ("user_added", "added_to_team") and data.get("user_id") == self.bot_user_id:
            await self._refresh_soft(client)
        elif kind == "user_removed" and self.bot_user_id in (data.get("user_id"), bc.get("user_id")):
            cid = data.get("channel_id") or bc.get("channel_id")
            if cid:
                self.members.pop(cid, None)
                self._seen.pop(cid, None)
                await asyncio.to_thread(self.state.delete_cursor, cid)
                _log("channel_removed", channel_id=cid)

    async def _catch_up(self, client, reason: str, alive_at: int | None) -> None:
        """REST catch-up of every member channel; raises (and stays pending, keeping its start) on MM errors."""
        if not self._catchup_pending:
            self._catchup_pending, self._catchup_from = True, alive_at
        alive_at = self._catchup_from
        await self._refresh_members(client)
        floor = int(self.clock() * 1000) - self.window_ms
        n_posts = n_skipped = 0
        for cid, ch in list(self.members.items()):
            cur = await asyncio.to_thread(self.state.get_cursor, cid)
            if cur is None:
                if alive_at is None:
                    continue                  # first start ever: no backfill of history
                cur = (alive_at, "")
            try:                              # skipped posts are counted at most one window further back
                posts = await self._since(client, cid, max(cur[0], floor - self.window_ms))
            except MMError as e:
                if e.code == "not_found" or e.status == 403:
                    _log("channel_unavailable", channel_id=cid, code=e.code)
                    self.members.pop(cid, None)
                    continue
                raise
            ctype = ch.get("type") or (await self._get(client, self._channels, cid, "/channels/" + cid) or {}).get("type")
            for p in sorted(posts, key=lambda p: (p.get("create_at", 0), p.get("id", ""))):
                at = p.get("create_at")
                if not isinstance(at, int) or at < cur[0] or p.get("delete_at"):
                    continue                  # equal create_at is re-offered: the ledger dedupes (PR-3)
                if at < floor:
                    n_skipped += 1
                    await asyncio.to_thread(self.state.set_cursor, cid, at, p["id"])
                    continue
                ev = {"event": "posted", "data": {"channel_type": ctype, "channel_name": ch.get("name"),
                                                  "channel_display_name": ch.get("display_name"),
                                                  "team_id": ch.get("team_id"), "post": p}}
                intent = decide(ev, self.bot_user_id)
                if intent:
                    n_posts += await self._enqueue(intent, client)
                else:
                    await asyncio.to_thread(self.state.set_cursor, cid, at, p["id"])
        self._catchup_pending = False
        _log("catchup", reason=reason, channels=len(self.members), posts=n_posts, skipped=n_skipped)
        if n_skipped:
            _log("catchup_skipped", n=n_skipped, window_minutes=self.window_ms // 60_000)

    async def _since(self, client, cid: str, since_ms: int) -> list:
        """Every post with create_at >= since_ms. Mattermost ignores page/per_page when `since` is given (and caps
        the result), so this pages by post id instead: the newest page, then `before=<oldest id seen>` until a
        page reaches back past since_ms or runs out. MAX_PAGES (x per_page posts in one channel inside the
        catch-up window) is the only bound; reaching it is logged (`catchup_truncated`)."""
        posts: dict = {}
        before = ""
        for _ in range(MAX_PAGES):
            q = {"page": 0, "per_page": self.per_page}
            if before:
                q["before"] = before
            r = await client.get("/channels/%s/posts" % cid, **q)
            batch = [r["posts"][i] for i in r.get("order", []) if i in r.get("posts", {})]
            new = [p for p in batch if p["id"] not in posts]
            posts.update((p["id"], p) for p in new)
            if len(batch) < self.per_page or not new:
                return list(posts.values())
            oldest = batch[-1]                # Mattermost order is newest first
            if oldest.get("create_at", 0) < since_ms:
                return list(posts.values())
            before = oldest["id"]
        _log("catchup_truncated", channel_id=cid, pages=MAX_PAGES)
        return list(posts.values())

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
