---
id: REVIEW-20261031-slice-20261028-b-s3-multi-bot-registry-routing-review
type: review-findings
phase: verify
status: addressed
owner_agent: eng-run
date: 2026-10-31
links: [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, thoughts/shared/slices/2026-10-28-b-s3-multi-bot-registry-routing.md]
review_kind: slice
subject: "SLICE-20261028-b-s3-multi-bot-registry-routing (thoughts/shared/slices/2026-10-28-b-s3-multi-bot-registry-routing.md)"
diff: e2f6091...cfe29e2
reviewer: codex
command: "codex review --base e2f6091"
run_log: thoughts/shared/runs/2026-10-31-code-review-slice-20261028-b-s3-multi-bot-registry-routing.md
---
# Independent review: code-review slice-20261028-b-s3-multi-bot-registry-routing
<!-- Written by eng-run (prompt code-review v2). Each finding row starts 'open': set disposition fixed (where) |
     accepted-risk (ONLY with Rob's approval, e.g. "Rob 2026-10-31") | rejected (reason). Plan reviews gate
     implementation (medium/large); slice reviews are advisory. -->

## Findings
| # | Severity | Location | Finding | Disposition | Reason / approval |
|---|---|---|---|---|---|
| 1 | P2 | app/live.py:258-260 | Startup v1 store migration bypasses the store-edit lock and can overwrite a concurrent `set-bot` with its stale v1 snapshot | fixed (commit after cfe29e2: `store.locked` shared by admin and runtime; runtime re-reads under the lock and keeps an already-v2 file, log `store_migrate_skipped`; test `test_boot_migration_never_overwrites_a_concurrent_set_bot`) | |

Note: eng-run's parser wrote "No findings." although Codex listed one P2 (same parser gap as B-s2, process-feedback.md); table filled by hand from the raw output below.

## Reviewer raw output
```
OpenAI Codex v0.166.0
--------
workdir: /mnt/d/rob/projects/mmbridge
model: gpt-6.1-sol
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR]
reasoning effort: none
reasoning summaries: none
session id: 01a19092-6134-7ca0-a1cf-f607a8415eb6
--------
user
changes against 'e2f6091'
exec
/bin/bash -lc 'cat PROJECT_STATE.md; git diff --stat e2f60917917cf30405578c8cd25ac6ecd50f14da; find .. -name AGENTS.md -o -name AGENTS.override.md' in /mnt/d/rob/projects/mmbridge
exec
/bin/bash -lc "cat thoughts/shared/handoffs/2026-10-30_22-38-17_b-s2-implemented-awaiting-verify.md .eng/PROCESS.md >/tmp/review-context; python3 .eng/bin/eng-check .; find app tests bin -name 'AGENTS*'; git diff e2f60917917cf30405578c8cd25ac6ecd50f14da -- app/live.py app/listener.py app/wake.py" in /mnt/d/rob/projects/mmbridge
 succeeded in 1990ms:
WARN  .eng/runners.toml: no on_complete hook configured ([hooks] empty or missing) - bots must stay attached to eng-run until exit; fire-and-forget needs a non-empty on_complete / <role>_on_complete (PROCESS.md section 10, LESSONS L-006)
WARN  PROJECT_STATE.md: ## Latest artifacts has 41 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 37 rows / 7630 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 163 artifact(s) checked
diff --git a/app/listener.py b/app/listener.py
index f896b5d..11968ff 100644
--- a/app/listener.py
+++ b/app/listener.py
@@ -1,4 +1,4 @@
-"""Mattermost websocket listener for the ONE live bot (ADR-0007).
+"""Mattermost websocket listener for ONE live bot (ADR-0007); B-s3 runs one per registered bot (ADR-0014).
 
 run(): GET /users/me -> WS /api/v4/websocket with `Authorization: Bearer` -> hello{connection_id} -> for each
 `posted` event, live_filter.decide -> wake payload (ADR-0008 schema, no token; channel/team/sender lookups
@@ -12,7 +12,11 @@ seen on the socket), then per channel `GET /channels/{id}/posts` paged back by p
 `since`, which Mattermost does not page), ascending (create_at, post_id),
 each post through decide() and enqueue_and_advance (the ledger dedupes). Channels without a cursor start at meta
 `last_event_at` (last alive); posts older than LIVE_CATCHUP_MINUTES are skipped (`catchup_skipped`). 401 ->
-`degraded`, retry every 5 min or on a config change. One listener per state.db (meta lease `listener_owner`).
+`degraded`, retry every 5 min or on a config change. One listener per bot per state.db (meta lease
+`listener_owner:<bot>`).
+B-s3: `state` is the bot's view (State.bot(name)); posts by any registered bot (`registered()`, user ids) are
+dropped (B7); delivery_id is "<bot>:<post_id>" (one wake per bot per post, relay dedupe per bot); every log line
+carries bot=<name>; `last_error` is the reason shown by admin status.
 """
 import asyncio
 import itertools
@@ -57,10 +61,6 @@ def connect(url: str, headers: dict):
     return websockets.connect(url, additional_headers=headers, ping_interval=None, open_timeout=10, logger=_ws_log)
 
 
-def _log(event: str, **fields) -> None:
-    mlog.log.info(json.dumps({"event": event, **fields}))
-
-
 def _iso(ms: int) -> str:
     return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
 
@@ -79,9 +79,12 @@ class Listener:
                  backoff_s: float = BACKOFF_S, max_backoff_s: float = MAX_BACKOFF_S,
                  auth_retry_s: float = AUTH_RETRY_S, lease_retry_s: float = LEASE_TTL_S / 2,
                  catchup_minutes: float | None = None, refresh_s: float | None = None, per_page: int = PER_PAGE,
-                 rand=random.random):
-        """cfg: BotConfig or a zero-arg callable returning the current one (ConfigHolder.get, PR-2)."""
+                 rand=random.random, registered=None):
+        """cfg: BotEntry or a zero-arg callable returning the current one (PR-2). state: State.bot(name) view.
+        registered: zero-arg callable -> frozenset of the user ids of every registered bot (B7)."""
         self._cfg = cfg if callable(cfg) else (lambda: cfg)
+        self.name = getattr(state, "name", "bot")
+        self._registered = registered or frozenset
         self.state, self.client_factory, self.ws_connect = state, client_factory, ws_connect
         self.clock, self.base_url, self.ping_s, self.idle_s = clock, base_url, ping_s, idle_s
         self.backoff_s, self.max_backoff_s, self.rand = backoff_s, max_backoff_s, rand
@@ -90,6 +93,7 @@ class Listener:
                                        else float(os.getenv("LIVE_CATCHUP_MINUTES", "15"))))
         self.refresh_s = refresh_s if refresh_s is not None else float(os.getenv("LIVE_MEMBERSHIP_REFRESH_S", "300"))
         self.status = "off"                   # off | connecting | ok | degraded (401)
+        self.last_error = None                # reason for admin status (mm_unauthorized, ws error code)
         self.bot_user_id = self.connection_id = self.last_seq = None
         self.members: dict = {}               # channel id -> channel (O/P/D), catch-up set
         self._seen: dict = {}                 # channel id -> type, seen on the socket since start
@@ -106,6 +110,9 @@ class Listener:
         self._ws = None
         self._wake = asyncio.Event()
 
+    def _log(self, event: str, level: str = "info", **fields) -> None:
+        getattr(mlog.log, level)(json.dumps({"event": event, "bot": self.name, **fields}))
+
     @property
     def cfg(self):
         return self._cfg()
@@ -143,19 +150,21 @@ class Listener:
                     attempt = 0 if ok else attempt + 1
                 except Unauthorized:
                     self.status = "degraded"
-                    mlog.log.warning(json.dumps({"event": "mm_unauthorized", "retry_s": self.auth_retry_s}))
+                    self.last_error = "mm_unauthorized"
+                    self._log("mm_unauthorized", "warning", retry_s=self.auth_retry_s)
                     await self._pause(self.auth_retry_s)
                     continue
                 except LeaseHeld:
-                    _log("listener_lease_held", instance=self.state.instance_id)
+                    self._log("listener_lease_held", instance=self.state.instance_id)
                     await self._pause(self.lease_retry_s)
                     continue
                 except (OSError, TimeoutError, MMError, InvalidHandshake, ConnectionClosed) as e:
                     attempt += 1
-                    _log("ws_connect_failed", error=getattr(e, "code", None) or type(e).__name__)
+                    self.last_error = getattr(e, "code", None) or type(e).__name__
+                    self._log("ws_connect_failed", error=self.last_error)
                 delay = self._backoff(attempt)
                 self.status = "connecting"
-                _log("ws_reconnect", attempt=attempt, delay=round(delay, 2))
+                self._log("ws_reconnect", attempt=attempt, delay=round(delay, 2))
                 await self._pause(delay)
         finally:
             self.status = "off"
@@ -183,7 +192,8 @@ class Listener:
                 raise
             if me["id"] != self.bot_user_id:
                 self.connection_id, self.members, self._seen = None, {}, {}
-            self.bot_user_id, self._bot = me["id"], {"user_id": me["id"], "username": me["username"]}
+            self.bot_user_id, self._bot = me["id"], {"name": self.name, "user_id": me["id"],
+                                                     "username": me["username"]}
             await asyncio.to_thread(self.state.set_meta, "bot_user_id", me["id"])   # dispatcher: bot_rotated
             await asyncio.to_thread(self.state.set_meta, "bot_identity",              # id + token as one row
                                     token_fp(cfg.token) + ":" + me["id"])
@@ -201,7 +211,7 @@ class Listener:
             self._ws = ws
             try:
                 if self.cfg.token != cfg.token:   # rotated while connecting: config_changed could not close us
-                    _log("token_changed_during_connect")
+                    self._log("token_changed_during_connect")
                     return True
                 pinger = asyncio.create_task(self._ping(ws))
                 try:
@@ -222,10 +232,10 @@ class Listener:
             try:
                 raw = await asyncio.wait_for(ws.recv(), self.idle_s)
             except TimeoutError:
-                _log("ws_idle", seconds=self.idle_s)
+                self._log("ws_idle", seconds=self.idle_s)
                 return reached
             except ConnectionClosed:
-                _log("ws_closed", connection_id=self.connection_id)
+                self._log("ws_closed", connection_id=self.connection_id)
                 return reached
             prev_alive = self._alive_at
             self._alive_at = int(self.clock() * 1000)   # persisted only once the frame is handled
@@ -243,7 +253,7 @@ class Listener:
         try:
             ev = json.loads(raw)
         except ValueError:
-            mlog.log.warning(json.dumps({"event": "event_invalid", "reason": "json"}))
+            self._log("event_invalid", "warning", reason="json")
             return False
         if not isinstance(ev, dict) or "event" not in ev:
             return False                      # ping replies ({"status","seq_reply"}) and other non-events
@@ -254,13 +264,13 @@ class Listener:
             await asyncio.to_thread(self.state.set_meta, "ws_connection_id", cid or "")
             if not resumed:
                 self.last_seq = ev.get("seq") if isinstance(ev.get("seq"), int) else 0
-            _log("ws_connected", connection_id=cid, resumed=resumed,
+            self._log("ws_connected", connection_id=cid, resumed=resumed,
                  server_version=(ev.get("data") or {}).get("server_version"))
             if not resumed or self._catchup_pending:
                 await self._catch_up(client, "new_connection" if not resumed else "pending", prev_alive)
             elif time.monotonic() - self._refreshed_at >= self.refresh_s:
                 await self._refresh_soft(client)
-            self.status = "ok"
+            self.status, self.last_error = "ok", None
             return True
         seq = ev.get("seq")
         if self._seq_gap(ev):
@@ -268,7 +278,7 @@ class Listener:
         if time.monotonic() - self._refreshed_at >= self.refresh_s:
             await self._refresh_soft(client)
         await self._membership_event(ev, client)
-        intent = decide(ev, self.bot_user_id)
+        intent = decide(ev, self.bot_user_id, self._registered())
         if intent:
             self._seen.setdefault(intent.channel_id, {"id": intent.channel_id, "type": intent.channel_type})
             await self._enqueue(intent, client)
@@ -280,7 +290,7 @@ class Listener:
         payload = await self._payload(intent, client)
         new = await asyncio.to_thread(self.state.enqueue_and_advance, intent.post_id, intent.channel_id,
                                       payload, intent.create_at)
-        _log("wake_queued", post_id=intent.post_id, channel_id=intent.channel_id, new=new)
+        self._log("wake_queued", post_id=intent.post_id, channel_id=intent.channel_id, new=new)
         return new
 
     def _seq_gap(self, ev: dict) -> bool:
@@ -290,7 +300,7 @@ class Listener:
             return False
         gap = self.last_seq is not None and seq != self.last_seq + 1
         if gap:
-            _log("ws_seq_gap", expected=self.last_seq + 1, got=seq)
+            self._log("ws_seq_gap", expected=self.last_seq + 1, got=seq)
         return gap
 
     async def _mark_alive(self) -> None:
@@ -306,7 +316,7 @@ class Listener:
         for n in itertools.count(1):
             await asyncio.sleep(self.ping_s)
             if not await asyncio.to_thread(self.state.claim_owner, self.clock(), LEASE_TTL_S, "listener_owner"):
-                _log("listener_lease_lost", instance=self.state.instance_id)
+                self._log("listener_lease_lost", instance=self.state.instance_id)
                 await ws.close()
                 return
             try:
@@ -339,7 +349,7 @@ class Listener:
         except MMError as e:
             if e.code != "not_found":
                 raise
-            _log("direct_channels_unavailable", code=e.code)   # older server: team lists still carry D
+            self._log("direct_channels_unavailable", code=e.code)   # older server: team lists still carry D
         for cid in await asyncio.to_thread(self.state.cursor_channels):
             found.setdefault(cid, self.members.get(cid) or {"id": cid})
         for cid, c in self._seen.items():
@@ -352,7 +362,7 @@ class Listener:
             await self._refresh_members(client)
         except MMError as e:
             self._refreshed_at = time.monotonic()
-            _log("membership_refresh_failed", code=e.code)
+            self._log("membership_refresh_failed", code=e.code)
 
     async def _membership_event(self, ev: dict, client) -> None:
         kind, data, bc = ev["event"], ev.get("data") or {}, ev.get("broadcast") or {}
@@ -364,7 +374,7 @@ class Listener:
                 self.members.pop(cid, None)
                 self._seen.pop(cid, None)
                 await asyncio.to_thread(self.state.delete_cursor, cid)
-                _log("channel_removed", channel_id=cid)
+                self._log("channel_removed", channel_id=cid)
 
     async def _catch_up(self, client, reason: str, alive_at: int | None) -> None:
         """REST catch-up of every member channel; raises (and stays pending, keeping its start) on MM errors."""
@@ -384,7 +394,7 @@ class Listener:
                 posts = await self._since(client, cid, max(cur[0], floor - self.window_ms))
             except MMError as e:
                 if e.code == "not_found" or e.status == 403:
-                    _log("channel_unavailable", channel_id=cid, code=e.code)
+                    self._log("channel_unavailable", channel_id=cid, code=e.code)
                     self.members.pop(cid, None)
                     continue
                 raise
@@ -400,15 +410,15 @@ class Listener:
                 ev = {"event": "posted", "data": {"channel_type": ctype, "channel_name": ch.get("name"),
                                                   "channel_display_name": ch.get("display_name"),
                                                   "team_id": ch.get("team_id"), "post": p} }
-                intent = decide(ev, self.bot_user_id)
+                intent = decide(ev, self.bot_user_id, self._registered())
                 if intent:
                     n_posts += await self._enqueue(intent, client)
                 else:
                     await asyncio.to_thread(self.state.set_cursor, cid, at, p["id"])
         self._catchup_pending = False
-        _log("catchup", reason=reason, channels=len(self.members), posts=n_posts, skipped=n_skipped)
+        self._log("catchup", reason=reason, channels=len(self.members), posts=n_posts, skipped=n_skipped)
         if n_skipped:
-            _log("catchup_skipped", n=n_skipped, window_minutes=self.window_ms // 60_000)
+            self._log("catchup_skipped", n=n_skipped, window_minutes=self.window_ms // 60_000)
 
     async def _since(self, client, cid: str, since_ms: int) -> list:
         """Every post with create_at >= since_ms. Mattermost ignores page/per_page when `since` is given (and caps
@@ -431,7 +441,7 @@ class Listener:
             if oldest.get("create_at", 0) < since_ms:
                 return list(posts.values())
             before = oldest["id"]
-        _log("catchup_truncated", channel_id=cid, pages=MAX_PAGES)
+        self._log("catchup_truncated", channel_id=cid, pages=MAX_PAGES)
         return list(posts.values())
 
     async def _get(self, client, cache: dict, key: str, path: str) -> dict | None:
@@ -440,7 +450,7 @@ class Listener:
             try:
                 cache[key] = await client.get(path)
             except MMError as e:
-                _log("lookup_failed", path=path.split("/")[1], code=e.code)
+                self._log("lookup_failed", path=path.split("/")[1], code=e.code)
                 return None
         return cache[key]
 
@@ -461,7 +471,7 @@ class Listener:
         else:
             reply = {"tool": "post_channel", "team": channel["team"], "channel": channel["name"], "root_id": w.root_id}
         return {
-            "version": 2, "kind": "post", "delivery_id": w.post_id, "attempt": 1,
+            "version": 2, "kind": "post", "delivery_id": "%s:%s" % (self.name, w.post_id), "attempt": 1,
             "issued_at": _iso(int(self.clock() * 1000)),
             "bot": dict(self._bot),
             "channel": channel,
diff --git a/app/live.py b/app/live.py
index da931d2..5a18f4d 100644
--- a/app/live.py
+++ b/app/live.py
@@ -1,13 +1,18 @@
-"""Live-bots runtime started from the FastAPI lifespan (slice lb5, ADR-0007/0009; plan Phase 5).
+"""Live-bots runtime started from the FastAPI lifespan (slice lb5, ADR-0007/0009; multi-bot B-s3, ADR-0014).
 
 LiveRuntime.start(): LIVE_BOTS_ENABLED must be "true" (else health `disabled`), the store must decrypt
 (MMB_STORE_KEY; else `off`, log store_unreadable, and re-try every RELOAD_S so the first set-bot starts the
-listener without a restart, log store_appeared) and /data/state.db must be writable (else `off`, log
-state_unwritable). Then three tasks: Listener and Dispatcher each under supervise() (crash -> log task_crashed,
-health `degraded`, restart with backoff 1->60 s; MCP keeps serving) and the ConfigHolder watcher.
-ConfigHolder (PR-2) re-reads the store when its mtime changes (every RELOAD_S): a valid new config replaces the
-old one for both tasks (listener reconnects on a new token, dispatcher reads url/secret at send time); an invalid
-file keeps the previous config (store_reload_failed). Logs carry field names and error codes, never values.
+listeners without a restart, log store_appeared) and /data/state.db must be writable (else `off`, log
+state_unwritable) and at schema v2 (a v1 file is migrated first; failure -> `degraded`, log live_migration_failed,
+live runtime off, MCP keeps serving). A v1 store is renamed to its bot's Mattermost username and rewritten as v2
+(bots.enc.v1.bak kept). Then: a BotSupervisor runs one Listener per bot, each under supervise() (crash -> log
+task_crashed, that bot `degraded`, restart with backoff 1->60 s), one shared Dispatcher under supervise(), the
+ConfigHolder watcher and the per-bot status reporter (meta bot:<name>:status, read by `admin status`).
+ConfigHolder (PR-2) re-reads the store when its mtime changes (every RELOAD_S): a valid new store replaces the old
+one; the supervisor reconciles listeners (bot added -> started, removed -> stopped, token changed -> that
+listener reconnects), the dispatcher reads url/secret at send time; an invalid file keeps the previous store
+(store_reload_failed). One bot's 401 or crash never touches another bot's listener (B8). Logs carry bot names,
+field names and error codes, never values.
 """
 import asyncio
 import json
@@ -20,21 +25,32 @@ from app import logging as mlog
 from app import mattermost, store, wake
 from app.listener import Listener
 from app.mattermost import Client
-from app.state import DAY, State, StateError
+from app.state import DAY, State, StateError, meta_key
 from app.store import StoreError
 from app.wake import Dispatcher
 
 RELOAD_S = 30
+REPORT_S, REPORT_REFRESH_S = 0.5, 10.0
 RESTART_BASE_S, RESTART_MAX_S = 1.0, 60.0
 FIELDS = ("token", "wake_url", "wake_secret")
+RANK = {"ok": 0, "connecting": 1, "off": 2, "degraded": 3}    # /health `listener` = worst bot
 
 
 def _log(event: str, level: str = "info", **fields) -> None:
     getattr(mlog.log, level)(json.dumps({"event": event, **fields}))
 
 
+def store_diff(old, new) -> list[str]:
+    """Changed field names per bot ("eddie.wake_url"), added ("+grok") and removed ("-test") bots; no values."""
+    out = ["-" + n for n in old.bots if n not in new.bots] + ["+" + n for n in new.bots if n not in old.bots]
+    for n, b in new.bots.items():
+        if n in old.bots:
+            out += ["%s.%s" % (n, f) for f in FIELDS if getattr(old.bots[n], f) != getattr(b, f)]
+    return out
+
+
 class ConfigHolder:
-    """The current BotConfig plus a generation counter; subscribers get (old, new) on a real change."""
+    """The current Store plus a generation counter; subscribers get (old, new) on a real change."""
 
     def __init__(self, path: str, key: str | None, cfg):
         self.path, self.key, self.cfg = path, key, cfg
@@ -56,7 +72,7 @@ class ConfigHolder:
             return None
 
     def check(self) -> bool:
-        """Reload if the file changed; True if the config changed (subscribers notified)."""
+        """Reload if the file changed; True if the store changed (subscribers notified)."""
         m = self._stat()
         if m == self._mtime:
             return False
@@ -66,8 +82,9 @@ class ConfigHolder:
         except StoreError as e:
             _log("store_reload_failed", "warning", code=e.code, detail=e.detail)
             return False
-        changed = [f for f in FIELDS if getattr(new, f) != getattr(self.cfg, f)]
+        changed = store_diff(self.cfg, new)
         if not changed:
+            self.cfg = new                   # cached ids/usernames may differ: keep the newest
             return False
         old, self.cfg = self.cfg, new
         self.generation += 1
@@ -111,6 +128,86 @@ async def supervise(name: str, factory, crashed: set, base_s: float = RESTART_BA
             crashed.discard(name)
 
 
+class BotSupervisor:
+    """One Listener task per bot in the current store (ADR-0014), reconciled on every store change."""
+
+    def __init__(self, holder: ConfigHolder, state: State, make_listener, crashed: set,
+                 restart_base_s: float = RESTART_BASE_S):
+        self.holder, self.state, self.make_listener = holder, state, make_listener
+        self.crashed, self.restart_base_s = crashed, restart_base_s
+        self.listeners: dict = {}
+        self.tasks: dict = {}
+        self._stopped: set = set()
+        self._reported: dict = {}
+
+    def registered_ids(self) -> frozenset:
+        """User ids of every registered bot: cached in the store, plus what each listener resolved (B7)."""
+        ids = {b.user_id for b in self.holder.get().bots.values() if b.user_id}
+        ids |= {lst.bot_user_id for lst in self.listeners.values() if lst.bot_user_id}
+        return frozenset(ids)
+
+    def reconcile(self, old=None, new=None) -> None:
+        """ConfigHolder subscriber (and the initial start): start/stop/reconnect listeners, no redeploy (B4)."""
+        bots = self.holder.get().bots
+        for name in [n for n in self.listeners if n not in bots]:
+            self._stop(name)
+        for name, b in bots.items():
+            if name not in self.listeners:
+                self._start(name)
+            elif old is not None and name in old.bots and old.bots[name].token != b.token:
+                self.listeners[name].config_changed(old.bots[name], b)
+
+    def _start(self, name: str) -> None:
+        last = {"b": self.holder.get().bots[name]}
+
+        def cfg():
+            b = self.holder.get().bots.get(name)
+            if b is not None:
+                last["b"] = b
+            return last["b"]
+        lst = self.make_listener(cfg, self.state.bot(name), self.registered_ids)
+        self.listeners[name] = lst
+        self.tasks[name] = asyncio.create_task(
+            supervise("listener:" + name, lst.run, self.crashed, self.restart_base_s))
+        _log("bot_started", bot=name)
+
+    def _stop(self, name: str) -> None:
+        t = self.tasks.pop(name)
+        self.listeners.pop(name)
+        t.cancel()
+        self._stopped.add(t)
+        t.add_done_callback(self._stopped.discard)
+        _log("bot_stopped", bot=name)
+
+    def status(self) -> dict:
+        """name -> (off|connecting|ok|degraded, reason or None)."""
+        out = {}
+        for name, lst in self.listeners.items():
+            if "listener:" + name in self.crashed:
+                out[name] = ("degraded", "task_crashed")
+            else:
+                out[name] = (lst.status, lst.last_error if lst.status != "ok" else None)
+        return out
+
+    async def report(self, every: float = REPORT_S) -> None:
+        """Persist per-bot status to meta bot:<name>:status on change (and every REPORT_REFRESH_S as heartbeat)."""
+        while True:
+            now = time.time()
+            for name, (status, err) in self.status().items():
+                prev = self._reported.get(name)
+                if prev is None or prev[0] != (status, err) or now - prev[1] >= REPORT_REFRESH_S:
+                    doc = json.dumps({"status": status, "error": err, "at": int(now)})
+                    await asyncio.to_thread(self.state.set_meta, meta_key(name, "status"), doc)
+                    self._reported[name] = ((status, err), now)
+            await asyncio.sleep(every)
+
+    async def stop(self) -> None:
+        tasks = list(self.tasks.values()) + list(self._stopped)
+        for t in tasks:
+            t.cancel()
+        await asyncio.gather(*tasks, return_exceptions=True)
+
+
 class LiveRuntime:
     def __init__(self, env=None, base_url: str | None = None, client_factory=None, http=None,
                  listener_kw: dict | None = None, restart_base_s: float = RESTART_BASE_S,
@@ -121,7 +218,7 @@ class LiveRuntime:
         self._http, self.listener_kw = http, listener_kw or {}
         self.restart_base_s, self.reload_s, self.poll_s = restart_base_s, reload_s, poll_s
         self.status = "disabled"
-        self.state = self.holder = self.listener = self.dispatcher = None
+        self.state = self.holder = self.supervisor = self.dispatcher = None
         self.crashed: set = set()
         self._tasks: list = []
 
@@ -135,49 +232,82 @@ class LiveRuntime:
         self.status = "off"
         path, key = self._data("bots.enc"), self.env.get("MMB_STORE_KEY")
         try:
-            cfg = store.load(path, key)
+            st = await self._load(path, key)
         except StoreError as e:
             _log("store_unreadable", "error", code=e.code, detail=e.detail)
-            # Stay `off` but keep polling: the first set-bot (or a fixed key file) starts the listener, no restart.
+            # Stay `off` but keep polling: the first set-bot (or a fixed key file) starts the listeners, no restart.
             self._tasks = [asyncio.create_task(self._await_store(path, key))]
             return
-        self._launch(path, key, cfg)
+        self._launch(path, key, st)
+
+    async def _load(self, path: str, key: str | None):
+        st = store.load(path, key)
+        if st.migrated_from == 1:
+            await self._migrate_store(path, key, st)
+        return st
+
+    async def _migrate_store(self, path: str, key: str | None, st) -> None:
+        """v1 store: name its bot after the Mattermost username (fallback `bot`) and save as v2 (+ .v1.bak)."""
+        (b,) = st.bots.values()
+        try:
+            me = await self.client_factory(b.token).get("/users/me")
+            username, uid = me["username"], me["id"]
+        except Exception as e:                       # MM down / token refused: keep the fallback name
+            username, uid = None, ""
+            _log("store_migrate_lookup_failed", "warning", error=getattr(e, "code", None) or type(e).__name__)
+        store.rename_v1(st, username, uid)
+        try:
+            store.save(path, key, st)
+            _log("store_migrated", bot=next(iter(st.bots)), fallback=username is None)
+        except (StoreError, OSError) as e:           # runs from memory; the next start tries again
+            _log("store_migrate_failed", "error", error=getattr(e, "code", None) or type(e).__name__)
 
     async def _await_store(self, path: str, key: str | None) -> None:
-        """Retry store.load every reload_s until it succeeds (logged once, no values), then launch."""
+        """Retry the store load every reload_s until it succeeds (logged once, no values), then launch."""
         while True:
             await asyncio.sleep(self.reload_s)
             try:
-                cfg = store.load(path, key)
+                st = await self._load(path, key)
             except StoreError:
                 continue
             _log("store_appeared")
-            self._launch(path, key, cfg)
+            self._launch(path, key, st)
             return
 
-    def _launch(self, path: str, key: str | None, cfg) -> None:
+    def _make_listener(self, cfg, bot_state, registered):
+        kw = {"catchup_minutes": float(self.env.get("LIVE_CATCHUP_MINUTES", "15")), **self.listener_kw}
+        return Listener(cfg, bot_state, self.client_factory, base_url=self.base_url, registered=registered, **kw)
+
+    def _launch(self, path: str, key: str | None, st) -> None:
         try:
-            self.state = State(self._data("state.db"))
+            self.state = State(self._data("state.db"), legacy_bot=store.legacy_owner(st))
         except StateError as e:
-            _log("state_unwritable", "error", detail=e.detail)
+            if e.code == "live_migration_failed":
+                self.status = "degraded"             # operator restores state.db.v1.bak (or fixes the volume)
+                _log("live_runtime_off", "error", reason=e.code)
+            else:
+                _log("state_unwritable", "error", detail=e.detail)
             return
-        self.holder = ConfigHolder(path, key, cfg)
-        kw = {"catchup_minutes": float(self.env.get("LIVE_CATCHUP_MINUTES", "15")), **self.listener_kw}
-        self.listener = Listener(self.holder.get, self.state, self.client_factory, base_url=self.base_url, **kw)
-        self.holder.subscribe(self.listener.config_changed)
+        self.holder = ConfigHolder(path, key, st)
+        self.supervisor = BotSupervisor(self.holder, self.state, self._make_listener, self.crashed,
+                                        self.restart_base_s)
+        self.holder.subscribe(self.supervisor.reconcile)
+        self.supervisor.reconcile()
         self._http = self._http or httpx.AsyncClient()
         self.dispatcher = Dispatcher(self.state, self.holder.get, self._http, poll_s=self.poll_s)
         self._tasks += [
-            asyncio.create_task(supervise("listener", self.listener.run, self.crashed, self.restart_base_s)),
             asyncio.create_task(supervise("dispatcher", self.dispatcher.run, self.crashed, self.restart_base_s)),
             asyncio.create_task(self.holder.watch(self.reload_s)),
+            asyncio.create_task(self.supervisor.report()),
         ]
-        _log("listener_start", instance=self.state.instance_id)
+        _log("listener_start", instance=self.state.instance_id, bots=len(st.bots))
 
     async def stop(self) -> None:
         for t in self._tasks:
             t.cancel()
         await asyncio.gather(*self._tasks, return_exceptions=True)
+        if self.supervisor is not None:
+            await self.supervisor.stop()
         if self._http is not None:
             await self._http.aclose()
         if self.state is not None:
@@ -186,14 +316,26 @@ class LiveRuntime:
         if self._tasks:
             _log("listener_stop")
 
+    def bot_status(self) -> dict:
+        return self.supervisor.status() if self.supervisor is not None else {}
+
     def listener_status(self) -> str:
-        if self.listener is None:
+        if self.supervisor is None:
             return self.status
-        return "degraded" if self.crashed else self.listener.status
+        statuses = [s for s, _ in self.bot_status().values()]
+        if "dispatcher" in self.crashed:
+            statuses.append("degraded")
+        return max(statuses, key=RANK.__getitem__) if statuses else "off"
 
     async def health(self) -> dict:
-        """Public /health fields: status words and a count only (no ids or names, ADR-0005)."""
-        n = 0
+        """Public /health fields: status words and counts only (no ids or names, ADR-0005)."""
+        n, bots = 0, self.bot_status()
+        failing = sum(1 for s, _ in bots.values() if s == "degraded")
         if self.state is not None:
             n = await asyncio.to_thread(self.state.failed_count, int(time.time()) - DAY)
-        return {"listener": self.listener_status(), "wake_failed_24h": n}
+            for name, (s, _) in bots.items():   # listener fine but its last wake failed for good (dead target)
+                if s != "degraded":
+                    w = await asyncio.to_thread(self.state.last_wake, name)
+                    failing += bool(w and w.status == "failed")
+        return {"listener": self.listener_status(), "wake_failed_24h": n, "bots_total": len(bots),
+                "bots_failing": failing}
diff --git a/app/wake.py b/app/wake.py
index c8d3652..9379f83 100644
--- a/app/wake.py
+++ b/app/wake.py
@@ -1,15 +1,20 @@
 """Signed wake webhook (ADR-0008): sign/verify and the Dispatcher that delivers queued wakes from state.db.
 
-POST <wake_url> with the wake payload as raw JSON body and headers X-MMB-Delivery (post id, idempotency key),
+POST <wake_url> with the wake payload as raw JSON body and headers X-MMB-Delivery (delivery id, idempotency key),
 X-MMB-Timestamp (unix seconds), X-MMB-Signature `v1=<hex HMAC-SHA256(secret, ts + "." + body)>`.
 Receivers: `verify(secret, headers, raw_body, now)`; constant-time, rejects |now - ts| > 300 s, an X-MMB-Delivery that is missing or differs from the signed delivery_id, unknown versions
 and missing headers.
 
-Dispatcher.tick(): heartbeat the single-owner lease (standby while another owner is fresh), recover_stale,
-prune (start + every 6 h), claim_due up to 4 and POST them concurrently (5 s timeout). Config is read at
-send time (url/secret rotation applies to queued wakes); wakes of a previous bot user fail `bot_rotated`.
-Nothing is claimed until the listener has resolved the identity of the CURRENT token (meta bot_identity =
-"<token_fp>:<bot_user_id>", one row, matches the config), so a stale id from a previous token/run never approves old wakes (review P1).
+Dispatcher (B-s3: ONE shared dispatcher for every bot, ADR-0014): each pass heartbeats the single-owner lease
+(standby while another owner is fresh), recover_stale, prune (start + every 6 h), then per bot with due rows
+(round robin) claims up to its free in-flight slots (per-bot cap 2, total cap 4) and POSTs them as background
+tasks (5 s timeout), so a dead target holds at most its own 2 slots and never delays other bots (B8 fairness).
+`tick()` is one pass that also waits for its sends (tests). Config is read per row at send time from the current
+Store (url/secret rotation applies to queued wakes); rows of a bot no longer in the store fail `bot_removed`;
+wakes of a previous bot user fail `bot_rotated`. Nothing of a bot is claimed until its listener has resolved the
+identity of the CURRENT token (meta bot:<name>:identity = "<token_fp>:<bot_user_id>", one row, matches the
+config), so a stale id from a previous token/run never approves old wakes (review P1).
+X-MMB-Delivery = the signed payload's delivery_id ("<bot>:<post_id>").
 Each POST has an overall deadline of TIMEOUT_S (not only per network step), so a slow-drip receiver cannot
 stall the loop and the owner heartbeat (review P2).
 2xx delivered; 408/429/5xx/timeout/connect retry (state.next_delay; failed after max attempts); other 4xx
@@ -25,11 +30,12 @@ from collections.abc import Mapping
 import httpx
 
 from app import logging as mlog
-from app.state import next_delay
+from app.state import meta_key, next_delay
 
 WINDOW_S = 300
 TIMEOUT_S = 5
-CONCURRENCY = 4
+CONCURRENCY = 4          # total in flight
+PER_BOT_IN_FLIGHT = 2    # per bot (fairness: one dead target cannot take every slot)
 PRUNE_EVERY_S = 6 * 3600
 POLL_S = 0.5
 
@@ -76,25 +82,51 @@ def _log(event: str, **fields) -> None:
 
 class Dispatcher:
     def __init__(self, state, cfg, http: httpx.AsyncClient, max_attempts: int | None = None, clock=None,
-                 poll_s: float = POLL_S, concurrency: int = CONCURRENCY):
-        """cfg: BotConfig or a zero-arg callable returning the current one (read at every send, PR-2)."""
+                 poll_s: float = POLL_S, concurrency: int = CONCURRENCY, per_bot_in_flight: int = PER_BOT_IN_FLIGHT):
+        """state: State (all bots). cfg: Store or a zero-arg callable returning the current one (read per send, PR-2)."""
         self.state, self.http = state, http
         self._cfg = cfg if callable(cfg) else (lambda: cfg)
         if max_attempts:
             state.max_attempts = max_attempts
         self.clock = clock or state.clock
-        self.poll_s, self.concurrency = poll_s, concurrency
+        self.poll_s, self.concurrency, self.per_bot = poll_s, concurrency, per_bot_in_flight
         self.owner = None
         self._pruned_at = None
-        self._waiting = False
+        self._waiting: set = set()
+        self._inflight: dict = {}          # bot -> set of send tasks
+        self._rr = 0
+
+    def in_flight(self, bot: str | None = None) -> int:
+        if bot is not None:
+            return len(self._inflight.get(bot, ()))
+        return sum(len(t) for t in self._inflight.values())
+
+    def _tasks(self) -> list:
+        return [t for ts in self._inflight.values() for t in ts]
 
     async def run(self) -> None:
-        while True:
-            if not await self.tick():
-                await asyncio.sleep(self.poll_s)
+        try:
+            while True:
+                if not await self._pass():
+                    await asyncio.sleep(self.poll_s)
+        finally:
+            tasks = self._tasks()
+            for t in tasks:
+                t.cancel()
+            await asyncio.gather(*tasks, return_exceptions=True)   # claims stay in_flight: lease recovery
 
     async def tick(self) -> int:
-        """One loop pass; returns the number of wakes attempted."""
+        """One pass that also waits for the sends it started; returns the number of wakes attempted."""
+        n = await self._pass()
+        await self.drain()
+        return n
+
+    async def drain(self) -> None:
+        tasks = self._tasks()
+        if tasks:
+            await asyncio.gather(*tasks, return_exceptions=True)
+
+    async def _pass(self) -> int:
         st, now = self.state, self.clock()
         owner = await asyncio.to_thread(st.claim_owner, now)
         if owner != self.owner:
@@ -107,30 +139,63 @@ class Dispatcher:
             n = await asyncio.to_thread(st.prune, 7)
             self._pruned_at = now
             _log("wakes_pruned", count=n)
-        cfg = self._cfg()
-        # One meta row "<token_fp>:<bot_user_id>", written in one statement by the listener: the id and the
+        bots = self._cfg().bots
+        due = await asyncio.to_thread(st.due_bots, now)
+        if due:                                   # round robin: a different bot goes first each pass
+            k = self._rr % len(due)
+            due, self._rr = due[k:] + due[:k], self._rr + 1
+        started = 0
+        for name in due:
+            if name not in bots:
+                for w in await asyncio.to_thread(st.claim_due, now, 50, name):
+                    await asyncio.to_thread(st.mark_failed, w.bot, w.post_id, "bot_removed")
+                    _log("wake_failed", bot=w.bot, post_id=w.post_id, attempt=w.attempts, error="bot_removed")
+                    started += 1
+                continue
+            free = min(self.per_bot - self.in_flight(name), self.concurrency - self.in_flight())
+            if free <= 0:
+                continue
+            bot_id = await self._identity(name, bots[name])
+            if not bot_id:
+                continue
+            for w in await asyncio.to_thread(st.claim_due, now, free, name):
+                t = asyncio.create_task(self._send(w, bot_id, bots[name]))
+                ts = self._inflight.setdefault(name, set())
+                ts.add(t)
+                t.add_done_callback(ts.discard)
+                t.add_done_callback(lambda t, w=w: self._crashed(t, w))
+                started += 1
+        return started
+
+    @staticmethod
+    def _crashed(t: asyncio.Task, w) -> None:
+        """A send that raised (e.g. state.db error marking the result): log it; the row stays in_flight and
+        recover_stale retries it after the lease (was a dispatcher crash before sends ran in the background)."""
+        if not t.cancelled() and t.exception() is not None:
+            mlog.log.error(json.dumps({"event": "wake_send_crashed", "bot": w.bot, "post_id": w.post_id,
+                                       "error": type(t.exception()).__name__}))
+
+    async def _identity(self, name: str, entry) -> str | None:
+        # One meta row "<token_fp>:<bot_user_id>" per bot, written in one statement by its listener: the id and the
         # token it belongs to are always read as one snapshot (review 3 P2: no split-read race on rotation).
-        fp, _, bot_id = (await asyncio.to_thread(st.get_meta, "bot_identity") or "").partition(":")
-        if not bot_id or fp != token_fp(cfg.token):
-            if not self._waiting:
-                _log("dispatcher_waiting_identity", instance=st.instance_id)
-                self._waiting = True
-            return 0
-        self._waiting = False
-        due = await asyncio.to_thread(st.claim_due, now, self.concurrency)
-        if due:
-            await asyncio.gather(*(self._send(w, bot_id, cfg) for w in due))
-        return len(due)
+        fp, _, bot_id = (await asyncio.to_thread(self.state.get_meta, meta_key(name, "identity")) or "").partition(":")
+        if not bot_id or fp != token_fp(entry.token):
+            if name not in self._waiting:
+                _log("dispatcher_waiting_identity", bot=name, instance=self.state.instance_id)
+                self._waiting.add(name)
+            return None
+        self._waiting.discard(name)
+        return bot_id
 
     async def _send(self, w, bot_id: str, cfg) -> None:
-        st = self.state
+        st, ids = self.state, {"bot": w.bot, "post_id": w.post_id}
         if (w.payload.get("bot") or {}).get("user_id") != bot_id:
-            await asyncio.to_thread(st.mark_failed, w.post_id, "bot_rotated")
-            _log("wake_failed", post_id=w.post_id, attempt=w.attempts, error="bot_rotated")
+            await asyncio.to_thread(st.mark_failed, w.bot, w.post_id, "bot_rotated")
+            _log("wake_failed", **ids, attempt=w.attempts, error="bot_rotated")
             return
         body = json.dumps({**w.payload, "attempt": w.attempts}, separators=(",", ":")).encode()
         ts = int(self.clock())
-        headers = {"Content-Type": "application/json", "X-MMB-Delivery": w.post_id,
+        headers = {"Content-Type": "application/json", "X-MMB-Delivery": w.payload.get("delivery_id") or w.post_id,
                    "X-MMB-Timestamp": str(ts), "X-MMB-Signature": sign(cfg.wake_secret, ts, body)}
         try:
             r = await asyncio.wait_for(
@@ -147,15 +212,14 @@ class Dispatcher:
         except Exception as e:                   # last line: no send error may stop the dispatcher or strand a claim
             status, err = None, "error_" + type(e).__name__
         if status is not None and 200 <= status < 300:
-            await asyncio.to_thread(st.mark_delivered, w.post_id)
-            fields = {"post_id": w.post_id, "attempt": w.attempts}
+            await asyncio.to_thread(st.mark_delivered, w.bot, w.post_id)
+            fields = {**ids, "attempt": w.attempts}
             if w.post_create_at:
                 fields["latency_ms"] = int(self.clock() * 1000) - w.post_create_at
             _log("wake_delivered", **fields)
         elif status is None or status in (408, 429) or status >= 500:
-            res = await asyncio.to_thread(st.mark_retry, w.post_id, err, self.clock() + next_delay(w.attempts))
-            _log("wake_failed" if res == "failed" else "wake_retry", post_id=w.post_id, attempt=w.attempts,
-                 error=err)
+            res = await asyncio.to_thread(st.mark_retry, w.bot, w.post_id, err, self.clock() + next_delay(w.attempts))
+            _log("wake_failed" if res == "failed" else "wake_retry", **ids, attempt=w.attempts, error=err)
         else:
-            await asyncio.to_thread(st.mark_failed, w.post_id, err)
-            _log("wake_failed", post_id=w.post_id, attempt=w.attempts, error=err)
+            await asyncio.to_thread(st.mark_failed, w.bot, w.post_id, err)
+            _log("wake_failed", **ids, attempt=w.attempts, error=err)

exec
/bin/bash -lc 'cat app/store.py app/live.py' in /mnt/d/rob/projects/mmbridge
 succeeded in 0ms:
"""Encrypted store of the live bots' config (ADR-0006, v2 ADR-0013): per named bot its Mattermost token, wake URL and
wake secret, plus the non-secret cached user id / username. No channel list: Mattermost membership decides which
channel posts can wake a bot (delta plan 2026-10-27).

/data/bots.enc is the Fernet ciphertext of {"version": 2, "bots": {"<name>": {"token", "user_id", "username",
"wake": {"url", "secret"} }} }, mode 0600, written atomically. Names match NAME_RE; tokens (and known user ids) are
unique across bots. A v1 document {"version": 1, "bot": {...} } loads as one bot (name `v1_name`, default "bot";
callers rename it to the Mattermost username with `rename_v1`) with `migrated_from == 1`; the first save over a v1
file keeps that file as bots.enc.v1.bak (0600) for rollback to v0.3.0. Key from env MMB_STORE_KEY; "new,old" is
accepted (MultiFernet) for key rotation, which also re-encrypts the .v1.bak. Errors never carry key material, token
or secret. Loaded/saved tokens and secrets are registered with the log redact filter. A legacy `channels` key
(pre-lb4b stores) is ignored on load and dropped on the next save.
"""
import httpx
import json
import os
import re
import tempfile
from dataclasses import dataclass, field

from cryptography.fernet import Fernet, InvalidToken, MultiFernet

from app import logging as mlog

VERSION = 2
MIN_SECRET = 32
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,31}$")
LEGACY_NAME = "bot"


def path_from_env() -> str:
    return os.path.join(os.getenv("MMB_DATA_DIR", "/data"), "bots.enc")


def backup_path(path: str) -> str:
    return path + ".v1.bak"


class StoreError(Exception):
    """code: store_key_missing | store_unreadable | store_invalid (save-time validation). detail: field/reason."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__("%s: %s" % (code, detail) if detail else code)
        self.code, self.detail = code, detail


def _mask(s: str) -> str:
    return "****" + s[-4:] if len(s) > 8 else "****"


@dataclass
class BotEntry:
    token: str
    wake_url: str
    wake_secret: str
    name: str = LEGACY_NAME
    user_id: str = ""        # cached /users/me id (non-secret): registered-bot filter (B7), state migration
    username: str = ""

    def __repr__(self) -> str:  # never show token or secret
        return "BotEntry(name=%r, token=%s, wake_url=%r, wake_secret=****)" % (self.name, _mask(self.token),
                                                                             self.wake_url)

    __str__ = __repr__


@dataclass
class Store:
    bots: dict = field(default_factory=dict)      # name -> BotEntry
    version: int = VERSION
    migrated_from: int | None = None              # 1 when read from a v1 document (not persisted)


def valid_name(name) -> bool:
    return isinstance(name, str) and bool(NAME_RE.match(name))


def name_from_username(username: str | None) -> str:
    """A store name for a Mattermost username (v1 migration, set-bot without --name); LEGACY_NAME if none fits."""
    n = re.sub(r"[^a-z0-9-]", "-", (username or "").lower()).strip("-")[:32]
    return n if valid_name(n) else LEGACY_NAME


def validate_bot(b: BotEntry) -> None:
    """Raise ValueError(<field>: <reason>) unless b is a valid bot entry (plan PR-6, ADR-0013)."""
    if not valid_name(b.name):
        raise ValueError("name: must match %s" % NAME_RE.pattern)
    for f in ("token", "wake_url", "wake_secret"):
        if not isinstance(getattr(b, f), str) or not getattr(b, f).strip():
            raise ValueError("%s: required" % f)
    if not https_ok(b.wake_url):
        raise ValueError("wake_url: must be https")
    if len(b.wake_secret) < MIN_SECRET:
        raise ValueError("wake_secret: must be at least %d characters" % MIN_SECRET)
    for f in ("user_id", "username"):
        if not isinstance(getattr(b, f), str):
            raise ValueError("%s: must be a string" % f)


def validate(st: Store) -> None:
    if st.version != VERSION:
        raise ValueError("unsupported_version")
    tokens, ids = {}, {}
    for name, b in st.bots.items():
        if b.name != name:
            raise ValueError("name: key %r does not match entry" % name)
        validate_bot(b)
        if b.token in tokens:
            raise ValueError("token: already used by bot %s" % tokens[b.token])
        tokens[b.token] = name
        if b.user_id:
            if b.user_id in ids:
                raise ValueError("user_id: same Mattermost user as bot %s" % ids[b.user_id])
            ids[b.user_id] = name


INTERNAL_HTTP_WAKE_HOSTS = frozenset({"relay"})   # compose service name of the wake relay


def https_ok(url: str) -> bool:
    try:                                   # must also parse as the dispatcher will send it (review 4 P2)
        u = httpx.URL(url)
        if not u.host or (u.port is not None and not 0 < u.port < 65536):
            return False
    except (httpx.InvalidURL, ValueError, TypeError):
        return False
    if url.startswith("https://") and len(url) > 8:
        return True
    if not (url.startswith("http://") and len(url) > 7):
        return False
    # Plain http only to in-stack Docker Compose services on the private network (Rob 2026-10-30
    # "Tighten now"): exact host match, never public hosts. LIVE_ALLOW_HTTP_WAKE=true stays a
    # tests-only escape hatch (acceptance driver's 127.0.0.1 receiver); never set it in production.
    if u.host.lower() in INTERNAL_HTTP_WAKE_HOSTS and not u.userinfo:
        return True
    return os.getenv("LIVE_ALLOW_HTTP_WAKE", "").lower() == "true"


def _keys(key: str | None) -> list[Fernet]:
    keys = [k.strip() for k in (key or "").split(",") if k.strip()]
    if not keys:
        raise StoreError("store_key_missing")
    try:
        return [Fernet(k.encode()) for k in keys]
    except (ValueError, TypeError):
        raise StoreError("store_unreadable", "bad_key") from None


def _entry(name, d: dict, v1: bool) -> BotEntry:
    if not isinstance(d, dict):
        raise ValueError("bot: required" if v1 else "bots.%s: must be an object" % name)
    wake = d if v1 else d.get("wake")
    if not isinstance(wake, dict):
        raise ValueError("wake: required")
    keys = ("wake_url", "wake_secret") if v1 else ("url", "secret")
    return BotEntry(token=d.get("token"), wake_url=wake.get(keys[0]), wake_secret=wake.get(keys[1]), name=name,
                    user_id=d.get("user_id") or "", username=d.get("username") or "")


def _decode(plain: bytes, v1_name: str) -> Store:
    try:
        doc = json.loads(plain)
    except ValueError:
        raise StoreError("store_unreadable", "format") from None
    if not isinstance(doc, dict):
        raise StoreError("store_unreadable", "format")
    try:
        if doc.get("version") == 1:
            st = Store(bots={v1_name: _entry(v1_name, doc.get("bot"), True)}, migrated_from=1)
        elif doc.get("version") == VERSION:
            bots = doc.get("bots")
            if not isinstance(bots, dict):
                raise ValueError("bots: required")
            st = Store(bots={n: _entry(n, d, False) for n, d in bots.items()})
        else:
            raise ValueError("unsupported_version")
        validate(st)
    except ValueError as e:
        raise StoreError("store_unreadable", str(e)) from None
    return st


def _encode(st: Store) -> bytes:
    return json.dumps({"version": VERSION, "bots": {
        n: {"token": b.token, "user_id": b.user_id, "username": b.username,
            "wake": {"url": b.wake_url, "secret": b.wake_secret} } for n, b in st.bots.items()} }).encode()


def _blob(path: str) -> bytes:
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError:
        raise StoreError("store_unreadable", "file") from None


def _plain(blob: bytes, f: MultiFernet) -> bytes:
    try:
        return f.decrypt(blob)
    except InvalidToken:
        raise StoreError("store_unreadable", "decrypt") from None


def _read(path: str, f: MultiFernet, v1_name: str = LEGACY_NAME) -> tuple[bytes, Store]:
    blob = _blob(path)
    st = _decode(_plain(blob, f), v1_name)
    _register(st)
    return blob, st


def _register(st: Store) -> None:
    for b in st.bots.values():
        mlog.register_secret(b.token)
        mlog.register_secret(b.wake_secret)


def _write(path: str, data: bytes) -> None:
    """Atomic replace: 0600 temp file in the same dir, fsync, rename."""
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".bots.", suffix=".tmp")   # mkstemp creates 0600
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def load(path: str, key: str | None, v1_name: str = LEGACY_NAME) -> Store:
    return _read(path, MultiFernet(_keys(key)), v1_name)[1]


def _on_disk_version(path: str, f: MultiFernet) -> int | None:
    try:
        return json.loads(f.decrypt(_blob(path))).get("version")
    except (StoreError, InvalidToken, ValueError, AttributeError):
        return None


def save(path: str, key: str | None, st: Store) -> None:
    """Validate and write v2. Over a v1 file, that file is first kept as bots.enc.v1.bak (0600, once)."""
    f = MultiFernet(_keys(key))
    try:
        validate(st)
    except ValueError as e:
        raise StoreError("store_invalid", str(e)) from None
    _register(st)
    bak = backup_path(path)
    if os.path.exists(path) and not os.path.exists(bak) and _on_disk_version(path, f) == 1:
        _write(bak, _blob(path))
        mlog.log.info(json.dumps({"event": "store_backup", "file": os.path.basename(bak)}))
    _write(path, f.encrypt(_encode(st)))


def rename_v1(st: Store, username: str | None, user_id: str = "") -> Store:
    """A store read from v1: name its one bot after the Mattermost username (fallback LEGACY_NAME) and cache the
    identity. No-op for v2 stores."""
    if st.migrated_from != 1 or len(st.bots) != 1:
        return st
    (b,) = st.bots.values()
    b.name = name_from_username(username)
    b.username, b.user_id = username or b.username, user_id or b.user_id
    st.bots = {b.name: b}
    return st


def legacy_owner(st: Store):
    """For the state.db v1 -> v2 migration: map the v1 meta bot_user_id to the bot that owned the v1 rows (by cached
    user id; else the only bot; else LEGACY_NAME)."""
    def owner(v1_user_id: str | None) -> str:
        for b in st.bots.values():
            if v1_user_id and b.user_id == v1_user_id:
                return b.name
        return next(iter(st.bots)) if len(st.bots) == 1 else LEGACY_NAME
    return owner


def rotate(path: str, new_key: str | None, old_key: str | None) -> None:
    """Re-encrypt the store (and its .v1.bak, if any) with the first new key (readable with new or old keys);
    validated first; atomic, 0600."""
    f = MultiFernet(_keys(new_key) + _keys(old_key))
    blob, _ = _read(path, f)
    bak = backup_path(path)
    if os.path.exists(bak):
        _write(bak, f.rotate(_blob(bak)))
    _write(path, f.rotate(blob))
"""Live-bots runtime started from the FastAPI lifespan (slice lb5, ADR-0007/0009; multi-bot B-s3, ADR-0014).

LiveRuntime.start(): LIVE_BOTS_ENABLED must be "true" (else health `disabled`), the store must decrypt
(MMB_STORE_KEY; else `off`, log store_unreadable, and re-try every RELOAD_S so the first set-bot starts the
listeners without a restart, log store_appeared) and /data/state.db must be writable (else `off`, log
state_unwritable) and at schema v2 (a v1 file is migrated first; failure -> `degraded`, log live_migration_failed,
live runtime off, MCP keeps serving). A v1 store is renamed to its bot's Mattermost username and rewritten as v2
(bots.enc.v1.bak kept). Then: a BotSupervisor runs one Listener per bot, each under supervise() (crash -> log
task_crashed, that bot `degraded`, restart with backoff 1->60 s), one shared Dispatcher under supervise(), the
ConfigHolder watcher and the per-bot status reporter (meta bot:<name>:status, read by `admin status`).
ConfigHolder (PR-2) re-reads the store when its mtime changes (every RELOAD_S): a valid new store replaces the old
one; the supervisor reconciles listeners (bot added -> started, removed -> stopped, token changed -> that
listener reconnects), the dispatcher reads url/secret at send time; an invalid file keeps the previous store
(store_reload_failed). One bot's 401 or crash never touches another bot's listener (B8). Logs carry bot names,
field names and error codes, never values.
"""
import asyncio
import json
import os
import time

import httpx

from app import logging as mlog
from app import mattermost, store, wake
from app.listener import Listener
from app.mattermost import Client
from app.state import DAY, State, StateError, meta_key
from app.store import StoreError
from app.wake import Dispatcher

RELOAD_S = 30
REPORT_S, REPORT_REFRESH_S = 0.5, 10.0
RESTART_BASE_S, RESTART_MAX_S = 1.0, 60.0
FIELDS = ("token", "wake_url", "wake_secret")
RANK = {"ok": 0, "connecting": 1, "off": 2, "degraded": 3}    # /health `listener` = worst bot


def _log(event: str, level: str = "info", **fields) -> None:
    getattr(mlog.log, level)(json.dumps({"event": event, **fields}))


def store_diff(old, new) -> list[str]:
    """Changed field names per bot ("eddie.wake_url"), added ("+grok") and removed ("-test") bots; no values."""
    out = ["-" + n for n in old.bots if n not in new.bots] + ["+" + n for n in new.bots if n not in old.bots]
    for n, b in new.bots.items():
        if n in old.bots:
            out += ["%s.%s" % (n, f) for f in FIELDS if getattr(old.bots[n], f) != getattr(b, f)]
    return out


class ConfigHolder:
    """The current Store plus a generation counter; subscribers get (old, new) on a real change."""

    def __init__(self, path: str, key: str | None, cfg):
        self.path, self.key, self.cfg = path, key, cfg
        self.generation = 0
        self._subs = []
        self._mtime = self._stat()

    def get(self):
        return self.cfg

    def subscribe(self, fn) -> None:
        self._subs.append(fn)

    def _stat(self):
        try:
            st = os.stat(self.path)
            return st.st_mtime_ns, st.st_size, st.st_ino
        except OSError:
            return None

    def check(self) -> bool:
        """Reload if the file changed; True if the store changed (subscribers notified)."""
        m = self._stat()
        if m == self._mtime:
            return False
        self._mtime = m
        try:
            new = store.load(self.path, self.key)
        except StoreError as e:
            _log("store_reload_failed", "warning", code=e.code, detail=e.detail)
            return False
        changed = store_diff(self.cfg, new)
        if not changed:
            self.cfg = new                   # cached ids/usernames may differ: keep the newest
            return False
        old, self.cfg = self.cfg, new
        self.generation += 1
        _log("store_updated", fields=changed, generation=self.generation)
        for fn in self._subs:
            fn(old, new)
        return True

    async def watch(self, every: float = RELOAD_S) -> None:
        while True:
            await asyncio.sleep(every)
            self.check()


def restart_delay(attempt: int, base_s: float, max_s: float) -> float:
    """base_s * 2^(attempt-1) capped at max_s; the exponent is bounded so endless crashes cannot overflow."""
    return min(max_s, base_s * 2 ** min(max(attempt, 1) - 1, 32))


async def supervise(name: str, factory, crashed: set, base_s: float = RESTART_BASE_S,
                    max_s: float = RESTART_MAX_S) -> None:
    """Run factory() forever: on an exception (or a return) log task_crashed, mark `name` crashed while waiting
    the backoff (1->60 s; reset after a run longer than max_s), then restart it."""
    attempt = 0
    while True:
        started = time.monotonic()
        try:
            await factory()
            err = "returned"
        except asyncio.CancelledError:
            raise
        except Exception as e:                      # type only: messages may carry request details
            err = type(e).__name__
        attempt = 1 if time.monotonic() - started > max_s else attempt + 1
        delay = restart_delay(attempt, base_s, max_s)
        crashed.add(name)
        _log("task_crashed", "error", task=name, error=err, attempt=attempt, restart_in_s=delay)
        try:
            await asyncio.sleep(delay)
        finally:
            crashed.discard(name)


class BotSupervisor:
    """One Listener task per bot in the current store (ADR-0014), reconciled on every store change."""

    def __init__(self, holder: ConfigHolder, state: State, make_listener, crashed: set,
                 restart_base_s: float = RESTART_BASE_S):
        self.holder, self.state, self.make_listener = holder, state, make_listener
        self.crashed, self.restart_base_s = crashed, restart_base_s
        self.listeners: dict = {}
        self.tasks: dict = {}
        self._stopped: set = set()
        self._reported: dict = {}

    def registered_ids(self) -> frozenset:
        """User ids of every registered bot: cached in the store, plus what each listener resolved (B7)."""
        ids = {b.user_id for b in self.holder.get().bots.values() if b.user_id}
        ids |= {lst.bot_user_id for lst in self.listeners.values() if lst.bot_user_id}
        return frozenset(ids)

    def reconcile(self, old=None, new=None) -> None:
        """ConfigHolder subscriber (and the initial start): start/stop/reconnect listeners, no redeploy (B4)."""
        bots = self.holder.get().bots
        for name in [n for n in self.listeners if n not in bots]:
            self._stop(name)
        for name, b in bots.items():
            if name not in self.listeners:
                self._start(name)
            elif old is not None and name in old.bots and old.bots[name].token != b.token:
                self.listeners[name].config_changed(old.bots[name], b)

    def _start(self, name: str) -> None:
        last = {"b": self.holder.get().bots[name]}

        def cfg():
            b = self.holder.get().bots.get(name)
            if b is not None:
                last["b"] = b
            return last["b"]
        lst = self.make_listener(cfg, self.state.bot(name), self.registered_ids)
        self.listeners[name] = lst
        self.tasks[name] = asyncio.create_task(
            supervise("listener:" + name, lst.run, self.crashed, self.restart_base_s))
        _log("bot_started", bot=name)

    def _stop(self, name: str) -> None:
        t = self.tasks.pop(name)
        self.listeners.pop(name)
        t.cancel()
        self._stopped.add(t)
        t.add_done_callback(self._stopped.discard)
        _log("bot_stopped", bot=name)

    def status(self) -> dict:
        """name -> (off|connecting|ok|degraded, reason or None)."""
        out = {}
        for name, lst in self.listeners.items():
            if "listener:" + name in self.crashed:
                out[name] = ("degraded", "task_crashed")
            else:
                out[name] = (lst.status, lst.last_error if lst.status != "ok" else None)
        return out

    async def report(self, every: float = REPORT_S) -> None:
        """Persist per-bot status to meta bot:<name>:status on change (and every REPORT_REFRESH_S as heartbeat)."""
        while True:
            now = time.time()
            for name, (status, err) in self.status().items():
                prev = self._reported.get(name)
                if prev is None or prev[0] != (status, err) or now - prev[1] >= REPORT_REFRESH_S:
                    doc = json.dumps({"status": status, "error": err, "at": int(now)})
                    await asyncio.to_thread(self.state.set_meta, meta_key(name, "status"), doc)
                    self._reported[name] = ((status, err), now)
            await asyncio.sleep(every)

    async def stop(self) -> None:
        tasks = list(self.tasks.values()) + list(self._stopped)
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


class LiveRuntime:
    def __init__(self, env=None, base_url: str | None = None, client_factory=None, http=None,
                 listener_kw: dict | None = None, restart_base_s: float = RESTART_BASE_S,
                 reload_s: float = RELOAD_S, poll_s: float = wake.POLL_S):
        self.env = os.environ if env is None else env
        self.base_url = base_url or self.env.get("MATTERMOST_URL") or mattermost.MATTERMOST_URL
        self.client_factory = client_factory or (lambda tok: Client(tok, base_url=self.base_url))
        self._http, self.listener_kw = http, listener_kw or {}
        self.restart_base_s, self.reload_s, self.poll_s = restart_base_s, reload_s, poll_s
        self.status = "disabled"
        self.state = self.holder = self.supervisor = self.dispatcher = None
        self.crashed: set = set()
        self._tasks: list = []

    def _data(self, name: str) -> str:
        return os.path.join(self.env.get("MMB_DATA_DIR", "/data"), name)

    async def start(self) -> None:
        if self.env.get("LIVE_BOTS_ENABLED", "").strip().lower() != "true":
            _log("listener_disabled")
            return
        self.status = "off"
        path, key = self._data("bots.enc"), self.env.get("MMB_STORE_KEY")
        try:
            st = await self._load(path, key)
        except StoreError as e:
            _log("store_unreadable", "error", code=e.code, detail=e.detail)
            # Stay `off` but keep polling: the first set-bot (or a fixed key file) starts the listeners, no restart.
            self._tasks = [asyncio.create_task(self._await_store(path, key))]
            return
        self._launch(path, key, st)

    async def _load(self, path: str, key: str | None):
        st = store.load(path, key)
        if st.migrated_from == 1:
            await self._migrate_store(path, key, st)
        return st

    async def _migrate_store(self, path: str, key: str | None, st) -> None:
        """v1 store: name its bot after the Mattermost username (fallback `bot`) and save as v2 (+ .v1.bak)."""
        (b,) = st.bots.values()
        try:
            me = await self.client_factory(b.token).get("/users/me")
            username, uid = me["username"], me["id"]
        except Exception as e:                       # MM down / token refused: keep the fallback name
            username, uid = None, ""
            _log("store_migrate_lookup_failed", "warning", error=getattr(e, "code", None) or type(e).__name__)
        store.rename_v1(st, username, uid)
        try:
            store.save(path, key, st)
            _log("store_migrated", bot=next(iter(st.bots)), fallback=username is None)
        except (StoreError, OSError) as e:           # runs from memory; the next start tries again
            _log("store_migrate_failed", "error", error=getattr(e, "code", None) or type(e).__name__)

    async def _await_store(self, path: str, key: str | None) -> None:
        """Retry the store load every reload_s until it succeeds (logged once, no values), then launch."""
        while True:
            await asyncio.sleep(self.reload_s)
            try:
                st = await self._load(path, key)
            except StoreError:
                continue
            _log("store_appeared")
            self._launch(path, key, st)
            return

    def _make_listener(self, cfg, bot_state, registered):
        kw = {"catchup_minutes": float(self.env.get("LIVE_CATCHUP_MINUTES", "15")), **self.listener_kw}
        return Listener(cfg, bot_state, self.client_factory, base_url=self.base_url, registered=registered, **kw)

    def _launch(self, path: str, key: str | None, st) -> None:
        try:
            self.state = State(self._data("state.db"), legacy_bot=store.legacy_owner(st))
        except StateError as e:
            if e.code == "live_migration_failed":
                self.status = "degraded"             # operator restores state.db.v1.bak (or fixes the volume)
                _log("live_runtime_off", "error", reason=e.code)
            else:
                _log("state_unwritable", "error", detail=e.detail)
            return
        self.holder = ConfigHolder(path, key, st)
        self.supervisor = BotSupervisor(self.holder, self.state, self._make_listener, self.crashed,
                                        self.restart_base_s)
        self.holder.subscribe(self.supervisor.reconcile)
        self.supervisor.reconcile()
        self._http = self._http or httpx.AsyncClient()
        self.dispatcher = Dispatcher(self.state, self.holder.get, self._http, poll_s=self.poll_s)
        self._tasks += [
            asyncio.create_task(supervise("dispatcher", self.dispatcher.run, self.crashed, self.restart_base_s)),
            asyncio.create_task(self.holder.watch(self.reload_s)),
            asyncio.create_task(self.supervisor.report()),
        ]
        _log("listener_start", instance=self.state.instance_id, bots=len(st.bots))

    async def stop(self) -> None:
        for t in self._tasks:
            t.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        if self.supervisor is not None:
            await self.supervisor.stop()
        if self._http is not None:
            await self._http.aclose()
        if self.state is not None:
            await asyncio.to_thread(self.state.release_owner, "dispatcher_owner")
            self.state.close()
        if self._tasks:
            _log("listener_stop")

    def bot_status(self) -> dict:
        return self.supervisor.status() if self.supervisor is not None else {}

    def listener_status(self) -> str:
        if self.supervisor is None:
            return self.status
        statuses = [s for s, _ in self.bot_status().values()]
        if "dispatcher" in self.crashed:
            statuses.append("degraded")
        return max(statuses, key=RANK.__getitem__) if statuses else "off"

    async def health(self) -> dict:
        """Public /health fields: status words and counts only (no ids or names, ADR-0005)."""
        n, bots = 0, self.bot_status()
        failing = sum(1 for s, _ in bots.values() if s == "degraded")
        if self.state is not None:
            n = await asyncio.to_thread(self.state.failed_count, int(time.time()) - DAY)
            for name, (s, _) in bots.items():   # listener fine but its last wake failed for good (dead target)
                if s != "degraded":
                    w = await asyncio.to_thread(self.state.last_wake, name)
                    failing += bool(w and w.status == "failed")
        return {"listener": self.listener_status(), "wake_failed_24h": n, "bots_total": len(bots),
                "bots_failing": failing}

exec
/bin/bash -lc 'cat app/admin.py app/setbot.py' in /mnt/d/rob/projects/mmbridge
 succeeded in 0ms:
"""Operator CLI for the live bots (ADR-0006/0009, multi-bot ADR-0013): `python -m app.admin set-bot | list | show |
remove-bot | status | rotate-key | failed | stats`.

Run inside the container (Coolify terminal; `bin/set-bot NAME` is the friendly prompt wrapper for set-bot). The token
is read from stdin only and never printed or logged; the wake secret is printed once when generated, never by
`show`/`list`. Each bot has an operator-chosen name (`--name`, ^[a-z0-9][a-z0-9-]{0,31}$, the same name as its relay
env block); `set-bot` without --name edits the only bot (or, on an empty store, names it after the Mattermost
username). Tokens and Mattermost users are unique across bots. Store edits hold an exclusive lock on bots.enc.lock
so two CLI runs cannot clobber each other. No channel list: Mattermost membership decides which channel posts wake
a bot, and the bridge never joins (REQ-7); `--channels` is refused as no longer used. `failed`/`stats`/`status`
read state.db and never print message text.
"""
import argparse
import asyncio
import contextlib
import json
import os
import secrets
import sys
import time

from app import logging as mlog
from app import state, store
from app.mattermost import MATTERMOST_URL, Client, MMError

FIELDS = ("token", "wake_url", "wake_secret")
STATUS_STALE_S = 60


class AdminError(Exception):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(code)
        self.code, self.detail = code, detail


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m app.admin", description="mmbridge live bot admin")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("set-bot", help="store a bot's token and wake URL (token read from stdin)")
    s.add_argument("--name", help="bot name (default: the only bot, or the Mattermost username on an empty store)")
    s.add_argument("--token-stdin", action="store_true", required=True, help="read the bot token from stdin")
    s.add_argument("--wake-secret-stdin", action="store_true",
                   help="read the wake secret from the next stdin line instead of generating one")
    s.add_argument("--wake-url", required=True)
    s.add_argument("--channels", default=None, help=argparse.SUPPRESS)   # removed: refused with a clear error
    sub.add_parser("list", help="one line per bot (token masked, secret hidden)")
    sh = sub.add_parser("show", help="show one bot's stored config (token masked, secret hidden)")
    sh.add_argument("name", nargs="?", help="bot name (optional with one bot)")
    rm = sub.add_parser("remove-bot", help="delete a bot; its pending wakes are marked failed (bot_removed)")
    rm.add_argument("name")
    sub.add_parser("status", help="per bot: listener state, last event, last wake, failed in 24 h")
    r = sub.add_parser("rotate-key", help="re-encrypt the store with a new MMB_STORE_KEY")
    r.add_argument("--new-key-env", default="MMB_STORE_KEY_NEW", help="env var holding the new key")
    r.add_argument("--old-key-env", default="MMB_STORE_KEY", help="env var holding the current key(s)")
    f = sub.add_parser("failed", help="list failed wakes, or requeue one")
    f.add_argument("--bot", help="only this bot")
    f.add_argument("--retry", metavar="BOT:POST_ID", help="requeue this failed wake for delivery")
    st = sub.add_parser("stats", help="wake counts and post->delivered latency")
    st.add_argument("--bot", help="only this bot")
    return p


async def _me(token: str, transport) -> dict:
    try:
        return await Client(token, MATTERMOST_URL, transport=transport).get("/users/me")
    except MMError as e:
        detail = "Mattermost rejected the bot token" if e.code == "unauthorized" else ""
        raise AdminError(e.code, detail) from None


def _key() -> str:
    key = os.getenv("MMB_STORE_KEY")
    if not (key or "").strip():
        raise store.StoreError("store_key_missing")
    return key


@contextlib.contextmanager
def _locked(path: str):
    """Exclusive advisory lock for a load-modify-save of the store (POSIX; no-op where fcntl is missing)."""
    try:
        import fcntl
    except ImportError:                       # pragma: no cover - dev on Windows only
        yield
        return
    with open(path + ".lock", "a") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def _name_v1(st, transport, me: dict | None = None) -> None:
    """A store read from v1: name its bot after the Mattermost username (`me`, or looked up with its own token)."""
    if st.migrated_from != 1:
        return
    if me is None:
        try:
            me = asyncio.run(_me(next(iter(st.bots.values())).token, transport))
        except AdminError:
            me = {}
    store.rename_v1(st, me.get("username"), me.get("id", ""))


def _load(transport, me: dict | None = None):
    st = store.load(store.path_from_env(), _key())
    _name_v1(st, transport, me)
    return st


def _open_state(transport) -> state.State:
    try:
        owner = store.legacy_owner(_load(transport))
    except store.StoreError:
        owner = store.LEGACY_NAME
    return state.State(state.path_from_env(), legacy_bot=owner)


def _set_bot(a, stdin, out, transport) -> None:
    if a.channels is not None:
        raise AdminError("invalid_argument", "channels no longer used (the bot wakes in channels it is a member of)")
    if a.name is not None and not store.valid_name(a.name):
        raise AdminError("invalid_argument", "name: must match %s" % store.NAME_RE.pattern)
    lines = stdin.read().splitlines()
    token = lines[0].strip() if lines else ""
    if not token:
        raise AdminError("invalid_argument", "no token on stdin")
    supplied = a.wake_secret_stdin
    secret = (lines[1].strip() if len(lines) > 1 else "") if supplied else secrets.token_urlsafe(32)
    if supplied and len(secret) < store.MIN_SECRET:
        raise AdminError("invalid_argument", "wake_secret: must be at least %d characters" % store.MIN_SECRET)
    if not store.https_ok(a.wake_url):
        raise AdminError("invalid_argument", "wake_url: must be https")
    key = _key()
    me = asyncio.run(_me(token, transport))
    path = store.path_from_env()
    with _locked(path):
        if os.path.exists(path):           # never overwrite other bots because the store did not decrypt
            st = store.load(path, key)
            _name_v1(st, transport, me if a.name is None else None)
        else:
            st = store.Store()
        if a.name:
            name = a.name
        elif len(st.bots) == 1:
            name = next(iter(st.bots))
        elif not st.bots:
            name = store.name_from_username(me["username"])
        else:
            raise AdminError("invalid_argument", "several bots stored (%s): pass --name" % ", ".join(sorted(st.bots)))
        for other in st.bots.values():
            if other.name != name and other.token == token:
                raise AdminError("invalid_argument", "token: already used by bot %s" % other.name)
            if other.name != name and other.user_id and other.user_id == me["id"]:
                raise AdminError("invalid_argument", "token: same Mattermost user as bot %s" % other.name)
        prev = st.bots.get(name)
        entry = store.BotEntry(token=token, wake_url=a.wake_url, wake_secret=secret, name=name, user_id=me["id"],
                               username=me["username"])
        st.bots[name] = entry
        store.save(path, key, st)
    changed = [f for f in FIELDS if prev is None or getattr(prev, f) != getattr(entry, f)]
    mlog.log.info(json.dumps({"event": "store_updated", "bot": name, "fields": changed}))
    print("bot %s (@%s) stored: wake_url %s" % (name, me["username"], entry.wake_url), file=out)
    if not supplied:
        print("wake secret (shown once; give it to the receiver): %s" % secret, file=out)


def _host(url: str) -> str:
    import httpx
    try:
        return httpx.URL(url).host or url
    except (httpx.InvalidURL, ValueError):
        return url


def _list(out, transport) -> None:
    st = _load(transport)
    if not st.bots:
        print("no bots", file=out)
    for n in sorted(st.bots):
        b = st.bots[n]
        print("%s  @%s  token ****%s  wake %s  secret set (hidden)" % (n, b.username or "?", b.token[-4:],
                                                                      _host(b.wake_url)), file=out)


def _pick(st, name):
    if name is None:
        if len(st.bots) != 1:
            raise AdminError("invalid_argument", "pass a bot name (%s)" % (", ".join(sorted(st.bots)) or "no bots"))
        return next(iter(st.bots.values()))
    if name not in st.bots:
        raise AdminError("not_found", "no bot %s" % name)
    return st.bots[name]


def _show(a, out, transport) -> None:
    b = _pick(_load(transport), a.name)
    print("name: %s\nusername: @%s\ntoken: ****%s\nwake_url: %s\nwake_secret: set (hidden)" % (
        b.name, b.username or "?", b.token[-4:], b.wake_url), file=out)


def _remove_bot(a, out, transport) -> None:
    key, path = _key(), store.path_from_env()
    with _locked(path):
        st = _load(transport)
        if a.name not in st.bots:
            raise AdminError("not_found", "no bot %s" % a.name)
        owner = store.legacy_owner(st)
        del st.bots[a.name]
        store.save(path, key, st)
    n = state.State(state.path_from_env(), legacy_bot=owner).fail_pending(a.name, "bot_removed")
    mlog.log.info(json.dumps({"event": "store_updated", "bot": a.name, "fields": ["removed"]}))
    print("removed bot %s; %d pending wake(s) marked failed (bot_removed)" % (a.name, n), file=out)


def _age(now: float, ms_or_s, ms=False) -> str:
    if ms_or_s in (None, ""):
        return "never"
    t = int(ms_or_s) / (1000 if ms else 1)
    return "%ds ago" % max(int(now - t), 0)


def _status(out, transport) -> None:
    st = _load(transport)
    db = _open_state(transport)
    now = time.time()
    if not st.bots:
        print("no bots", file=out)
    for n in sorted(st.bots):
        raw = db.get_meta(state.meta_key(n, "status"))
        try:
            rep = json.loads(raw) if raw else {}
        except ValueError:
            rep = {}
        if not rep:
            listener = "off (no report yet)"
        elif now - rep.get("at", 0) > STATUS_STALE_S:
            listener = "off (no report for %s; runtime stopped?)" % _age(now, rep.get("at"))[:-4]
        else:
            listener = rep["status"] + (" (%s)" % rep["error"] if rep.get("error") else "")
        w = db.last_wake(n)
        last = "none" if w is None else w.status + (" (%s)" % w.last_error if w.status == "failed" and
                                                    w.last_error else "")
        print("%s  listener %s  last event %s  last wake %s  failed_24h %d" % (
            n, listener, _age(now, db.get_meta(state.meta_key(n, "last_event_at")), ms=True), last,
            db.failed_count(int(now) - state.DAY, n)), file=out)


def _rotate_key(a, out) -> None:
    store.rotate(store.path_from_env(), os.getenv(a.new_key_env), os.getenv(a.old_key_env))
    mlog.log.info(json.dumps({"event": "store_updated", "fields": ["key"]}))
    print("store re-encrypted with %s; set MMB_STORE_KEY to that key" % a.new_key_env, file=out)


def _failed(a, out, transport) -> None:
    st = _open_state(transport)
    if a.retry:
        bot, _, pid = a.retry.rpartition(":")
        if not bot:                            # bare post id: fine while only one bot has it failed
            rows = st.failed_for_post(pid)
            if len(rows) > 1:
                raise AdminError("invalid_argument", "several bots failed %s: use BOT:POST_ID" % pid)
            bot = rows[0].bot if rows else ""
        if not bot or not st.requeue(bot, pid):
            raise AdminError("not_found", "no failed wake %s" % a.retry)
        mlog.log.info(json.dumps({"event": "wake_requeued", "bot": bot, "post_id": pid}))
        print("requeued %s:%s" % (bot, pid), file=out)
        return
    rows = st.failed(a.bot)
    if not rows:
        print("no failed wakes", file=out)
    for w in rows:
        at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(w.updated_at))
        print("bot %s  %s  channel %s  attempts %d  error %s  at %s" % (w.bot, w.post_id, w.channel_id, w.attempts,
                                                                       w.last_error or "-", at), file=out)


def _stats(a, out, transport) -> None:
    s = _open_state(transport).stats(a.bot)
    if not s["counts"]:
        print("no wakes yet", file=out)
        return
    for k in sorted(s["counts"]):
        print("%s: %d" % (k, s["counts"][k]), file=out)
    lat = s["latency_ms"]
    print("latency post->delivered (ms): n=%d p50=%s p95=%s" % (lat["n"], lat["p50"], lat["p95"]), file=out)


def main(argv=None, stdin=None, stdout=None, transport=None) -> int:
    mlog.setup()
    stdin, out = stdin or sys.stdin, stdout or sys.stdout
    a = _parser().parse_args(argv)
    try:
        if a.cmd == "set-bot":
            _set_bot(a, stdin, out, transport)
        elif a.cmd == "list":
            _list(out, transport)
        elif a.cmd == "show":
            _show(a, out, transport)
        elif a.cmd == "remove-bot":
            _remove_bot(a, out, transport)
        elif a.cmd == "status":
            _status(out, transport)
        elif a.cmd == "rotate-key":
            _rotate_key(a, out)
        elif a.cmd == "failed":
            _failed(a, out, transport)
        else:
            _stats(a, out, transport)
    except (AdminError, store.StoreError, state.StateError) as e:
        print("error: %s%s" % (e.code, ": " + e.detail if e.detail else ""), file=out)
        return 1
    except OSError as e:
        print("error: store_unwritable: %s" % e.strerror, file=out)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""Friendly owner wrapper for `python -m app.admin set-bot --name NAME` (Rob 2026-10-30; run as `bin/set-bot NAME`
in the mmbridge container terminal).

Prompts for the bot's Mattermost token (hidden, never echoed: Mattermost shows it once under Integrations > Bot
Accounts; if lost, create a new token there), the wake URL (default http://relay:8080/wake/NAME, the in-stack
relay) and the HMAC-SHA256 wake secret (Enter = generate a new one; or paste the existing one, hidden). Then runs
the real admin set-bot with token + secret on stdin and prints the matching relay env line
`RELAY_BOT_<NAME>_HMAC_SECRET=<secret>` for Coolify. The Fernet store key (MMB_STORE_KEY) is a one-time Coolify env
and is not touched here.
"""
import getpass
import io
import secrets
import sys

from app import admin, store

DEFAULT_WAKE = "http://relay:8080/wake/%s"


def relay_env_name(name: str) -> str:
    return "RELAY_BOT_%s" % name.upper().replace("-", "_")


def main(argv=None, ask=input, ask_hidden=getpass.getpass, out=None, transport=None) -> int:
    out = out or sys.stdout
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1 or argv[0] in ("-h", "--help"):
        print("usage: bin/set-bot NAME   (NAME: lowercase letters, digits, '-'; same name as the relay env block)",
              file=out)
        return 2
    name = argv[0]
    if not store.valid_name(name):
        print("error: invalid_argument: name must match %s" % store.NAME_RE.pattern, file=out)
        return 1
    print("Registering bot %r on mmbridge." % name, file=out)
    token = ask_hidden("Mattermost bot token for %s (hidden; shown once in Mattermost > Integrations > Bot Accounts,"
                       " if lost create a new token there): " % name).strip()
    if not token:
        print("error: invalid_argument: no token entered", file=out)
        return 1
    url = ask("Wake URL [%s]: " % (DEFAULT_WAKE % name)).strip() or DEFAULT_WAKE % name
    secret = ask_hidden("Wake secret (Enter = generate a new one; or paste the existing secret, hidden): ").strip()
    secret = secret or secrets.token_urlsafe(32)
    buf = io.StringIO()
    rc = admin.main(["set-bot", "--name", name, "--token-stdin", "--wake-secret-stdin", "--wake-url", url],
                    stdin=io.StringIO("%s\n%s\n" % (token, secret)), stdout=buf, transport=transport)
    print(buf.getvalue().rstrip(), file=out)
    if rc != 0:
        return rc
    env = relay_env_name(name)
    print("\nPut this line in the relay service env in Coolify (shown once here; same secret on both sides):",
          file=out)
    print("%s_HMAC_SECRET=%s" % (env, secret), file=out)
    print("The relay also needs %s_ROUTINE_URL and %s_ROUTINE_KEY from that bot's Grok routine; redeploy the relay"
          " after editing its env. mmbridge picks the bot up within 30 s, no redeploy." % (env, env), file=out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

exec
/bin/bash -lc 'cat app/state.py' in /mnt/d/rob/projects/mmbridge
 succeeded in 0ms:
"""Listener state on the persistent volume (ADR-0009, v2 ADR-0014): /data/state.db, SQLite in WAL mode.

`wakes` is both the at-most-once ledger (INSERT OR IGNORE on (bot, post_id) is the single enqueue gate, per bot)
and the delivery queue: queued|retry -> in_flight (claimed by one dispatcher, with a lease) -> delivered|failed.
`cursors` holds the forward-only (create_at, post_id) per (bot, channel); `meta` holds per-bot keys
`bot:<name>:<key>` (identity, user_id, last_event_at, ws_connection_id, status), the single dispatcher owner
heartbeat and the per-bot listener lease `listener_owner:<name>`. No tokens or secrets are stored; message text is,
and terminal rows are pruned after 7 days. `State.bot(name)` is the one-bot view a Listener uses.
Schema version is PRAGMA user_version (2). A v1 file (lb2..B-s2, one bot) is copied to state.db.v1.bak first,
then migrated in ONE transaction (rows and meta go to the bot `legacy_bot` names); a failure rolls back, leaves the
v1 file as it was and raises StateError(live_migration_failed); rerunning is safe (idempotent).
Blocking stdlib sqlite3: async callers use asyncio.to_thread. One connection per State, guarded by a lock.
"""
import json
import math
import os
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass

from app import logging as mlog

DAY = 86400
LEASE_S = 30          # in_flight lease; recover_stale returns expired leases to retry
OWNER_TTL_S = 60      # dispatcher owner heartbeat freshness
TERMINAL = ("delivered", "failed")
PENDING = ("queued", "retry", "in_flight")
SCHEMA_VERSION = 2

_TABLES = [
    """CREATE TABLE IF NOT EXISTS wakes (
  bot TEXT NOT NULL,
  post_id TEXT NOT NULL,
  channel_id TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('queued','retry','in_flight','delivered','failed')),
  attempts INTEGER NOT NULL DEFAULT 0,
  next_at INTEGER NOT NULL,
  last_error TEXT,
  claimed_by TEXT,
  lease_until INTEGER,
  post_create_at INTEGER,
  delivered_at INTEGER,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  PRIMARY KEY (bot, post_id)
)""",
    "CREATE INDEX IF NOT EXISTS wakes_due ON wakes (status, next_at)",
    """CREATE TABLE IF NOT EXISTS cursors (
  bot TEXT NOT NULL,
  channel_id TEXT NOT NULL,
  last_create_at INTEGER NOT NULL,
  last_post_id TEXT NOT NULL,
  PRIMARY KEY (bot, channel_id)
)""",
    "CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)",
]
_V1_COLS = ("post_id, channel_id, payload_json, status, attempts, next_at, last_error, claimed_by, lease_until, "
            "post_create_at, delivered_at, created_at, updated_at")
_COLS = "bot, " + _V1_COLS
# v1 meta key -> per-bot key suffix (bot:<name>:<suffix>)
_V1_META = {"bot_identity": "identity", "bot_user_id": "user_id", "last_event_at": "last_event_at",
            "ws_connection_id": "ws_connection_id"}


def path_from_env() -> str:
    return os.path.join(os.getenv("MMB_DATA_DIR", "/data"), "state.db")


def meta_key(bot: str, key: str) -> str:
    """Per-bot meta key; the v1 names bot_identity / bot_user_id map to identity / user_id."""
    return "bot:%s:%s" % (bot, _V1_META.get(key, key))


def next_delay(attempt: int) -> float:
    """Backoff after the given (1-based) failed attempt: 2, 4, 8, 16, 32 s, times WAKE_BACKOFF_SCALE (tests)."""
    return 2 ** min(max(attempt, 1), 5) * float(os.getenv("WAKE_BACKOFF_SCALE", "1.0"))


class StateError(Exception):
    """code: state_unwritable | live_migration_failed. detail: sqlite reason (no secrets in state)."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__("%s: %s" % (code, detail) if detail else code)
        self.code, self.detail = code, detail


@dataclass
class Wake:
    bot: str
    post_id: str
    channel_id: str
    payload: dict
    status: str
    attempts: int
    next_at: int
    last_error: str | None
    claimed_by: str | None
    lease_until: int | None
    post_create_at: int | None
    delivered_at: int | None
    created_at: int
    updated_at: int


def _wake(row) -> Wake:
    r = list(row)
    r[3] = json.loads(r[3])
    return Wake(*r)


def _log(event: str, level: str = "info", **fields) -> None:
    getattr(mlog.log, level)(json.dumps({"event": event, **fields}))


# --- v1 -> v2 migration steps (module level so a test can fail one mid-transaction) -------------------------------
def _v1_rename(c) -> None:
    c.execute("DROP INDEX IF EXISTS wakes_due")
    c.execute("ALTER TABLE wakes RENAME TO wakes_v1")
    c.execute("ALTER TABLE cursors RENAME TO cursors_v1")


def _v1_create(c) -> None:
    for sql in _TABLES:
        c.execute(sql)


def _v1_copy(c, bot: str) -> None:
    c.execute("INSERT INTO wakes (%s) SELECT ?, %s FROM wakes_v1 ORDER BY rowid" % (_COLS, _V1_COLS), (bot,))
    c.execute("INSERT INTO cursors (bot, channel_id, last_create_at, last_post_id) "
              "SELECT ?, channel_id, last_create_at, last_post_id FROM cursors_v1", (bot,))
    c.execute("DROP TABLE wakes_v1")
    c.execute("DROP TABLE cursors_v1")


def _v1_meta(c, bot: str) -> None:
    for old in _V1_META:
        c.execute("UPDATE OR REPLACE meta SET key=? WHERE key=?", (meta_key(bot, old), old))
    c.execute("UPDATE OR REPLACE meta SET key=? WHERE key='listener_owner'", ("listener_owner:" + bot,))
    c.execute("DELETE FROM meta WHERE key='schema_version'")


class State:
    def __init__(self, path: str, instance_id: str | None = None, clock=time.time, max_attempts: int | None = None,
                 legacy_bot="bot"):
        """legacy_bot: name (or callable(v1 meta bot_user_id) -> name) of the bot that owns the rows of a v1 file."""
        self.path = path
        self.instance_id = instance_id or uuid.uuid4().hex
        self.clock = clock
        self.max_attempts = max_attempts or int(os.getenv("WAKE_MAX_ATTEMPTS", "5"))
        self._lock = threading.Lock()
        try:
            self._conn = sqlite3.connect(path, timeout=10, isolation_level=None, check_same_thread=False)
            self._conn.execute("PRAGMA journal_mode=WAL")
            version = self._conn.execute("PRAGMA user_version").fetchone()[0]
            v1 = version < SCHEMA_VERSION and "bot" not in self._columns("wakes") and self._columns("wakes")
        except sqlite3.Error as e:
            raise StateError("state_unwritable", str(e)) from None
        if v1:
            self._migrate(legacy_bot)
        elif version > SCHEMA_VERSION:
            raise StateError("live_migration_failed", "unknown schema version %d" % version)
        try:
            with self._tx() as c:
                _v1_create(c)
                c.execute("PRAGMA user_version=%d" % SCHEMA_VERSION)
                c.execute("INSERT OR REPLACE INTO meta (key, value) VALUES ('schema_probe', ?)",   # write probe
                          (str(SCHEMA_VERSION),))
        except sqlite3.Error as e:
            raise StateError("state_unwritable", str(e)) from None

    def _columns(self, table: str) -> list[str]:
        return [r[1] for r in self._conn.execute("PRAGMA table_info(%s)" % table)]

    def _migrate(self, legacy_bot) -> None:
        bak = self.path + ".v1.bak"
        try:
            row = self._conn.execute("SELECT value FROM meta WHERE key='bot_user_id'").fetchone() \
                if self._columns("meta") else None
            bot = legacy_bot(row[0] if row else None) if callable(legacy_bot) else legacy_bot
            _log("live_migration_started", from_version=1, to_version=SCHEMA_VERSION, bot=bot)
            os.close(os.open(bak, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600))   # private from the start
            dst = sqlite3.connect(bak)
            try:
                self._conn.backup(dst)           # consistent copy, WAL included
            finally:
                dst.close()
            os.chmod(bak, 0o600)
            with self._tx() as c:
                _v1_rename(c)
                _v1_create(c)
                _v1_copy(c, bot)
                _v1_meta(c, bot)
                c.execute("PRAGMA user_version=%d" % SCHEMA_VERSION)
        except (sqlite3.Error, OSError) as e:
            _log("live_migration_failed", "error", detail=type(e).__name__)
            raise StateError("live_migration_failed", str(e)) from None
        _log("live_migration_done", bot=bot, backup=os.path.basename(bak))

    def close(self) -> None:
        self._conn.close()

    def bot(self, name: str) -> "BotState":
        return BotState(self, name)

    def _now(self) -> int:
        return int(self.clock())

    @contextmanager
    def _tx(self):
        with self._lock:
            self._conn.execute("BEGIN IMMEDIATE")
            try:
                yield self._conn
            except BaseException:
                self._conn.execute("ROLLBACK")
                raise
            self._conn.execute("COMMIT")

    # --- enqueue / cursors ---------------------------------------------------------------------------------
    def _insert(self, c, bot, post_id, channel_id, payload, post_create_at) -> bool:
        now = self._now()
        cur = c.execute("INSERT OR IGNORE INTO wakes (bot, post_id, channel_id, payload_json, status, next_at, "
                        "post_create_at, created_at, updated_at) VALUES (?,?,?,?,'queued',?,?,?,?)",
                        (bot, post_id, channel_id, json.dumps(payload), now, post_create_at, now, now))
        return cur.rowcount == 1

    def _advance(self, c, bot: str, channel_id: str, create_at: int, post_id: str) -> None:
        c.execute("INSERT INTO cursors (bot, channel_id, last_create_at, last_post_id) VALUES (?,?,?,?) "
                  "ON CONFLICT(bot, channel_id) DO UPDATE SET last_create_at=excluded.last_create_at, "
                  "last_post_id=excluded.last_post_id "
                  "WHERE (excluded.last_create_at, excluded.last_post_id) > (last_create_at, last_post_id)",
                  (bot, channel_id, create_at, post_id))

    def enqueue(self, bot: str, post_id: str, channel_id: str, payload: dict, post_create_at: int | None = None) -> bool:
        """True if newly queued; False if (bot, post_id) was already seen (the dedupe gate)."""
        with self._tx() as c:
            return self._insert(c, bot, post_id, channel_id, payload, post_create_at)

    def enqueue_and_advance(self, bot: str, post_id: str, channel_id: str, payload: dict, create_at: int) -> bool:
        """enqueue + forward-only cursor move in one transaction (PR-3)."""
        with self._tx() as c:
            new = self._insert(c, bot, post_id, channel_id, payload, create_at)
            self._advance(c, bot, channel_id, create_at, post_id)
            return new

    def get_cursor(self, bot: str, channel_id: str) -> tuple[int, str] | None:
        with self._lock:
            row = self._conn.execute("SELECT last_create_at, last_post_id FROM cursors WHERE bot=? AND channel_id=?",
                                     (bot, channel_id)).fetchone()
        return tuple(row) if row else None

    def set_cursor(self, bot: str, channel_id: str, create_at: int, post_id: str = "") -> None:
        with self._tx() as c:
            self._advance(c, bot, channel_id, create_at, post_id)

    def delete_cursor(self, bot: str, channel_id: str) -> None:
        with self._tx() as c:
            c.execute("DELETE FROM cursors WHERE bot=? AND channel_id=?", (bot, channel_id))

    def cursor_channels(self, bot: str) -> list[str]:
        with self._lock:
            return [r[0] for r in self._conn.execute(
                "SELECT channel_id FROM cursors WHERE bot=? ORDER BY channel_id", (bot,))]

    # --- meta ------------------------------------------------------------------------------------------------
    def get_meta(self, key: str) -> str | None:
        with self._lock:
            row = self._conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row[0] if row else None

    def set_meta(self, key: str, value: str) -> None:
        with self._tx() as c:
            c.execute("INSERT INTO meta (key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                      (key, value))

    def claim_owner(self, now: int, ttl: int = OWNER_TTL_S, key: str = "dispatcher_owner") -> bool:
        """Become (or stay, as heartbeat) the single owner of `key` (dispatcher_owner | listener_owner:<bot>);
        refused while another owner is fresh."""
        with self._tx() as c:
            row = c.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
            if row:
                cur = json.loads(row[0])
                if cur["id"] != self.instance_id and now - cur["ts"] < ttl:
                    return False
            c.execute("INSERT INTO meta (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                      (key, json.dumps({"id": self.instance_id, "ts": now})))
            return True

    def release_owner(self, key: str = "dispatcher_owner") -> None:
        """Clean shutdown: drop our lease so a restarted process takes over at once."""
        with self._tx() as c:
            row = c.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
            if row and json.loads(row[0])["id"] == self.instance_id:
                c.execute("DELETE FROM meta WHERE key=?", (key,))

    # --- dispatcher queue ------------------------------------------------------------------------------------
    def due_bots(self, now: int) -> list[str]:
        """Bots with queued/retry rows due at `now`, oldest due first."""
        with self._lock:
            return [r[0] for r in self._conn.execute(
                "SELECT bot FROM wakes WHERE status IN ('queued','retry') AND next_at<=? GROUP BY bot "
                "ORDER BY MIN(next_at), bot", (now,))]

    def claim_due(self, now: int, limit: int = 4, bot: str | None = None) -> list[Wake]:
        """Atomically flip up to `limit` due queued/retry rows (of `bot`, or any) to in_flight for this instance."""
        if limit <= 0:
            return []
        only = " AND bot=?" if bot is not None else ""
        args = (self.instance_id, now + LEASE_S, self._now(), now) + ((bot,) if bot is not None else ()) + (limit,)
        with self._tx() as c:
            rows = c.execute(
                "UPDATE wakes SET status='in_flight', claimed_by=?, lease_until=?, attempts=attempts+1, updated_at=? "
                "WHERE rowid IN (SELECT rowid FROM wakes WHERE status IN ('queued','retry') AND next_at<=?" + only +
                " ORDER BY next_at, rowid LIMIT ?) RETURNING rowid, " + _COLS, args).fetchall()
        rows.sort(key=lambda r: (r[7], r[0]))
        return [_wake(r[1:]) for r in rows]

    def _mine(self, c, bot: str, post_id: str):
        return c.execute("SELECT attempts FROM wakes WHERE bot=? AND post_id=? AND status='in_flight' AND claimed_by=?",
                         (bot, post_id, self.instance_id)).fetchone()

    def mark_delivered(self, bot: str, post_id: str) -> bool:
        now = self.clock()
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='delivered', delivered_at=?, claimed_by=NULL, lease_until=NULL, "
                             "updated_at=? WHERE bot=? AND post_id=? AND status='in_flight' AND claimed_by=?",
                             (int(now * 1000), int(now), bot, post_id, self.instance_id)).rowcount == 1

    def mark_failed(self, bot: str, post_id: str, err: str) -> bool:
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='failed', last_error=?, claimed_by=NULL, lease_until=NULL, "
                             "updated_at=? WHERE bot=? AND post_id=? AND status='in_flight' AND claimed_by=?",
                             (err, self._now(), bot, post_id, self.instance_id)).rowcount == 1

    def mark_retry(self, bot: str, post_id: str, err: str, next_at: int) -> str | None:
        """'retry', or 'failed' once attempts reached max_attempts; None if not claimed by this instance."""
        with self._tx() as c:
            row = self._mine(c, bot, post_id)
            if not row:
                return None
            status = "failed" if row[0] >= self.max_attempts else "retry"
            c.execute("UPDATE wakes SET status=?, last_error=?, next_at=?, claimed_by=NULL, lease_until=NULL, "
                      "updated_at=? WHERE bot=? AND post_id=?", (status, err, next_at, self._now(), bot, post_id))
            return status

    def fail_pending(self, bot: str, err: str) -> int:
        """Operator removed the bot: every queued/retry/in_flight wake of it becomes failed `err`."""
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='failed', last_error=?, claimed_by=NULL, lease_until=NULL, "
                             "updated_at=? WHERE bot=? AND status IN ('queued','retry','in_flight')",
                             (err, self._now(), bot)).rowcount

    def recover_stale(self, now: int) -> int:
        """Return in_flight rows whose lease expired (crashed dispatcher) to retry, due now."""
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='retry', claimed_by=NULL, lease_until=NULL, next_at=?, "
                             "updated_at=? WHERE status='in_flight' AND lease_until < ?",
                             (now, self._now(), now)).rowcount

    def requeue(self, bot: str, post_id: str) -> bool:
        """Operator retry of a failed wake: fresh attempts, due now."""
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='queued', attempts=0, next_at=?, last_error=NULL, "
                             "updated_at=? WHERE bot=? AND post_id=? AND status='failed'",
                             (self._now(), self._now(), bot, post_id)).rowcount == 1

    def prune(self, days: int = 7) -> int:
        """Delete delivered/failed rows older than `days`; never touches queued/retry/in_flight (PR-8)."""
        with self._tx() as c:
            return c.execute("DELETE FROM wakes WHERE status IN ('delivered','failed') AND updated_at < ?",
                             (self._now() - days * DAY,)).rowcount

    # --- reads -----------------------------------------------------------------------------------------------
    def _select(self, where: str = "", args=(), order: str = "rowid") -> list[Wake]:
        with self._lock:
            rows = self._conn.execute("SELECT %s FROM wakes %s ORDER BY %s" % (_COLS, where, order), args).fetchall()
        return [_wake(r) for r in rows]

    @staticmethod
    def _by(bot, where: str = "", args=()):
        if bot is None:
            return ("WHERE " + where if where else ""), tuple(args)
        return "WHERE bot=?" + (" AND " + where if where else ""), (bot, *args)

    def wake(self, bot: str, post_id: str) -> Wake | None:
        rows = self._select("WHERE bot=? AND post_id=?", (bot, post_id))
        return rows[0] if rows else None

    def wakes(self, bot: str | None = None) -> list[Wake]:
        return self._select(*self._by(bot))

    def failed(self, bot: str | None = None) -> list[Wake]:
        return self._select(*self._by(bot, "status='failed'"))

    def failed_for_post(self, post_id: str) -> list[Wake]:
        return self._select("WHERE post_id=? AND status='failed'", (post_id,))

    def last_wake(self, bot: str) -> Wake | None:
        """The bot's most recently updated wake (admin status `last wake`, /health bots_failing)."""
        rows = self._select("WHERE bot=?", (bot,), order="updated_at DESC, rowid DESC LIMIT 1")
        return rows[0] if rows else None

    def failed_count(self, since: int, bot: str | None = None) -> int:
        """Failed wakes whose last update is at or after `since` (unix s): /health wake_failed_24h."""
        where, args = self._by(bot, "status='failed' AND updated_at >= ?", (since,))
        with self._lock:
            return self._conn.execute("SELECT COUNT(*) FROM wakes " + where, args).fetchone()[0]

    def stats(self, bot: str | None = None) -> dict:
        """Counts per status and post->delivered latency (delivered_at - post_create_at, ms; PR-9)."""
        where, args = self._by(bot)
        dwhere, dargs = self._by(bot, "status='delivered' AND delivered_at IS NOT NULL AND post_create_at IS NOT NULL")
        with self._lock:
            counts = dict(self._conn.execute("SELECT status, COUNT(*) FROM wakes %s GROUP BY status" % where,
                                             args).fetchall())
            lat = sorted(r[0] for r in self._conn.execute(
                "SELECT delivered_at - post_create_at FROM wakes " + dwhere, dargs))

        def pct(p):
            return lat[max(math.ceil(p * len(lat)) - 1, 0)] if lat else None
        return {"counts": counts, "latency_ms": {"n": len(lat), "p50": pct(0.5), "p95": pct(0.95)} }


class BotState:
    """One bot's view of State (what its Listener uses): the v1 one-bot method signatures, rows/cursors scoped to
    the bot, meta keys mapped to bot:<name>:<key>, the listener lease to listener_owner:<name>."""

    def __init__(self, core: State, name: str):
        self.core, self.name = core, name

    @property
    def instance_id(self) -> str:
        return self.core.instance_id

    @property
    def clock(self):
        return self.core.clock

    def enqueue(self, post_id, channel_id, payload, post_create_at=None) -> bool:
        return self.core.enqueue(self.name, post_id, channel_id, payload, post_create_at)

    def enqueue_and_advance(self, post_id, channel_id, payload, create_at) -> bool:
        return self.core.enqueue_and_advance(self.name, post_id, channel_id, payload, create_at)

    def get_cursor(self, channel_id):
        return self.core.get_cursor(self.name, channel_id)

    def set_cursor(self, channel_id, create_at, post_id=""):
        self.core.set_cursor(self.name, channel_id, create_at, post_id)

    def delete_cursor(self, channel_id):
        self.core.delete_cursor(self.name, channel_id)

    def cursor_channels(self):
        return self.core.cursor_channels(self.name)

    def get_meta(self, key):
        return self.core.get_meta(meta_key(self.name, key))

    def set_meta(self, key, value):
        self.core.set_meta(meta_key(self.name, key), value)

    def claim_owner(self, now, ttl=OWNER_TTL_S, key="listener_owner") -> bool:
        return self.core.claim_owner(now, ttl, "%s:%s" % (key, self.name))

    def release_owner(self, key="listener_owner") -> None:
        self.core.release_owner("%s:%s" % (key, self.name))

    def wake(self, post_id):
        return self.core.wake(self.name, post_id)

    def wakes(self):
        return self.core.wakes(self.name)

    def failed(self):
        return self.core.failed(self.name)

    def close(self):
        self.core.close()

exec
/bin/bash -lc "cat relay/app/config.py 2>/dev/null; ls relay; cat .claude/skills/eng-code-review/SKILL.md 2>/dev/null; git diff e2f60917917cf30405578c8cd25ac6ecd50f14da -- Dockerfile app/main.py app/live_filter.py; find . -name AGENTS.md -not -path './.venv/*' -not -path './.git/*'" in /mnt/d/rob/projects/mmbridge
 succeeded in 25004ms:
---
id: STATE
type: project-state
phase: implement
status: active
owner_agent: grok-bot
date: 2026-10-31
links: []
triage: large             # unset | small | medium | large
active_slice: SLICE-20261028-b-s3-multi-bot-registry-routing
# Single source of truth for approvals. One item per line: "CP-X: <path> - <decision needed>".
# Later checkpoints (e.g. CP-B while in discover) may be listed early. Quote items containing commas.
pending_approvals: []
# Working agreements (see PROCESS.md section 10). Never hard-code these in design docs.
implementer: claude-code      # who writes code (default: Claude Code on the owner's PC)
planner: grok-bot             # who plans, writes docs, keeps state and process
cross_review: codex-advisory  # codex-advisory | none  (advisory, never a gate)
push_permission: standing     # standing: after eng-verify PASS may push main; tags/force-push still ask (Rob 2026-10-26)
board: none                   # none | vikunja (optional, board only; repo stays the source of truth)
acceptance: executable-specs   # v2.5: tests/acceptance/, see PROCESS.md 13
---
# PROJECT_STATE

> Single entry point. Any agent reads THIS file first, then the latest handoff linked below.
> Update it at the end of every session. Keep it under one screen.

## Current phase
implement (increment B: Grok Bot webhook wake + multi-bot; architecture B done, see Approval log). v0.3.0 Live bots shipped 2026-10-28 (93b4f7d, tag v0.3.0).

## Goal (one sentence)
A public HTTPS MCP bridge (Python, deployed on Coolify at chats.rmlab.cloud) that lets Grok Bots read and post in Rob's self-hosted Mattermost, each bot using its own Mattermost bot token.

## Active slice
[SLICE-20261028-b-s3-multi-bot-registry-routing](thoughts/shared/slices/2026-10-28-b-s3-multi-bot-registry-routing.md) (in-progress, implementer claude-code via eng-run 2026-10-31; includes friendlier bin/set-bot per Rob 2026-10-30). Previous: B-s2 [done](thoughts/shared/slices/2026-10-28-b-s2-round-trip-reply-root-id.md) (CP-S 2026-10-31), B-s1 [done](thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md) (CP-S 2026-10-30)

## Next action
B-s3 implement started (eng-run implement, claude-code, 2026-10-31): plan Phase 3 + friendlier `bin/set-bot` wrapper (Rob 2026-10-30). Then Codex review, eng-verify, push (standing), CP-S per plan Phase 3 Manual Verification. B-s2 done (CP-S 2026-10-31, see Approval log).

B-s1 done (CP-S 2026-10-30). Ops: boot-before-store fixed 2026-10-30 (Rob "fix it now", small): if mmbridge boots with store_unreadable (no bots.enc yet) it stays `off` and re-tries the store every 30 s; the first set-bot starts the WS listener (log store_appeared). Restart no longer required after first set-bot (needs the new image on Coolify). http-wake-internal-hosts slice (8c60bc8) done (CP-S 2026-10-30). Open: live Mattermost-restart resume check (TODOS, deferred); OWNER-GUIDE pointer (TODOS P2); flaky timing tests (TODOS P2).

## Blockers
- none

## Pending approvals
See `pending_approvals` in the front matter (the only copy; `.eng/bin/eng-status` renders it). Do not list items here.

## Back-ups to an earlier phase
<!-- date - from phase -> to phase - why (blameless) - artifacts revised -->
none

## Latest artifacts
- B-s1 verify: [thoughts/shared/verification/2026-10-29-b-s1-relay-grok-wake-one-bot-verify.md](thoughts/shared/verification/2026-10-29-b-s1-relay-grok-wake-one-bot-verify.md); review: [thoughts/shared/verification/2026-10-29-slice-20261028-b-s1-relay-grok-wake-one-bot-review-2.md](thoughts/shared/verification/2026-10-29-slice-20261028-b-s1-relay-grok-wake-one-bot-review-2.md); handoff: [thoughts/shared/handoffs/2026-10-29_23-45-00_b-s1-verified-awaiting-cp-s.md](thoughts/shared/handoffs/2026-10-29_23-45-00_b-s1-verified-awaiting-cp-s.md)
<!-- Relative links only; .eng/bin/eng-check verifies they resolve. -->
- Plan B (see Approval log): [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md](thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md); slices B-s1..B-s3 in thoughts/shared/slices/; specs [tests/acceptance/specs/test_grok_multibot.py](tests/acceptance/specs/test_grok_multibot.py)
- Architecture B (approved): [docs/architecture/2026-10-28-grok-webhook-multibot.md](docs/architecture/2026-10-28-grok-webhook-multibot.md); ADR-0011, 0013..0016 (accepted), ADR-0012 (rejected) in [docs/decisions/](docs/decisions/)
- Cross-model review B (awaiting Codex): [thoughts/shared/verification/2026-10-28-grok-webhook-multibot-arch-review.md](thoughts/shared/verification/2026-10-28-grok-webhook-multibot-arch-review.md)
- Research B (accepted): [thoughts/shared/research/2026-10-28-grok-webhook-multibot-current-code.md](thoughts/shared/research/2026-10-28-grok-webhook-multibot-current-code.md)
- Design B Grok Bot webhook + multi-bot (approved; scope HOLD approved 2026-10-28): [docs/design/2026-10-28-grok-webhook-multibot.md](docs/design/2026-10-28-grok-webhook-multibot.md)
- Conventions: [AGENTS.md](AGENTS.md)
- Owner guide: [OWNER-GUIDE.md](OWNER-GUIDE.md)
- Definition of Done: [docs/definition-of-done.md](docs/definition-of-done.md)
- Retro v0.3.0 (done, changes applied 2026-10-28): [thoughts/shared/retros/2026-10-28-v0.3.0-live-bots.md](thoughts/shared/retros/2026-10-28-v0.3.0-live-bots.md)
- Process feedback: [thoughts/shared/process-feedback.md](thoughts/shared/process-feedback.md)
- Design A Live bots (approved; scope REDUCE recorded 2026-10-26): [docs/design/2026-10-26-live-bots.md](docs/design/2026-10-26-live-bots.md)
- Design (approved; scope hold approved): [docs/design/2026-10-25-mmbridge-mcp.md](docs/design/2026-10-25-mmbridge-mcp.md)
- Plan A Live bots (status in front matter): [thoughts/shared/plans/2026-10-27-live-bots.md](thoughts/shared/plans/2026-10-27-live-bots.md)
- Plan review A (AWAITING Codex, mandatory): [thoughts/shared/verification/2026-10-27-live-bots-plan-review.md](thoughts/shared/verification/2026-10-27-live-bots-plan-review.md)
- Review lb2 (addressed): [thoughts/shared/verification/2026-10-27-slice-20261027-lb2-state-db-wake-queue-review.md](thoughts/shared/verification/2026-10-27-slice-20261027-lb2-state-db-wake-queue-review.md)
- Verify lb5 (PASS): [thoughts/shared/verification/2026-10-28-lb5-wireup-reconnect-acceptance-verify.md](thoughts/shared/verification/2026-10-28-lb5-wireup-reconnect-acceptance-verify.md)
- Review lb5 (round 6 clean): [thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-6.md](thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-6.md)
- Specs A: [tests/acceptance/specs/test_live_bots.py](tests/acceptance/specs/test_live_bots.py)
- Architecture A Live bots (approved): [docs/architecture/2026-10-26-live-bots.md](docs/architecture/2026-10-26-live-bots.md)
- Cross-model review A (awaiting Codex): [thoughts/shared/verification/2026-10-26-live-bots-arch-review.md](thoughts/shared/verification/2026-10-26-live-bots-arch-review.md)
- Architecture: [docs/architecture/2026-10-25-mmbridge-mcp.md](docs/architecture/2026-10-25-mmbridge-mcp.md)
- ADRs 0001-0010 (all accepted): [docs/decisions/](docs/decisions/)
- Verification lb4b (PASS): [thoughts/shared/verification/2026-10-27-lb4b-drop-allowlist.md](thoughts/shared/verification/2026-10-27-lb4b-drop-allowlist.md)
- Latest handoff: [thoughts/shared/handoffs/2026-10-30_22-38-17_b-s2-implemented-awaiting-verify.md](thoughts/shared/handoffs/2026-10-30_22-38-17_b-s2-implemented-awaiting-verify.md)
- B-s2 review (addressed): [thoughts/shared/verification/2026-10-30-slice-20261028-b-s2-round-trip-reply-root-id-review.md](thoughts/shared/verification/2026-10-30-slice-20261028-b-s2-round-trip-reply-root-id-review.md)
- Review lb4b (addressed, no findings): [thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review.md](thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review.md)
- Review lb3 (addressed, no findings): [thoughts/shared/verification/2026-10-27-slice-20261027-lb3-listener-filters-review.md](thoughts/shared/verification/2026-10-27-slice-20261027-lb3-listener-filters-review.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
- Plan (approved): [thoughts/shared/plans/2026-10-25-mmbridge-mcp.md](thoughts/shared/plans/2026-10-25-mmbridge-mcp.md)
- Verification s1 (PASS): [thoughts/shared/verification/2026-10-26-s1-verify.md](thoughts/shared/verification/2026-10-26-s1-verify.md)
- Slices: [thoughts/shared/slices/](thoughts/shared/slices/)
- Specs: [tests/acceptance/specs/test_mmbridge.py](tests/acceptance/specs/test_mmbridge.py)
- Research A Live bots (accepted): [thoughts/shared/research/2026-10-26-live-bots-current-code.md](thoughts/shared/research/2026-10-26-live-bots-current-code.md)
- Research: [thoughts/shared/research/2026-10-25-mmbridge-current-code.md](thoughts/shared/research/2026-10-25-mmbridge-current-code.md)
- Deferred work: [TODOS.md](TODOS.md)
- Retro (done): [thoughts/shared/retros/2026-10-26-v0.2.0.md](thoughts/shared/retros/2026-10-26-v0.2.0.md)

## Approval log
<!-- One row per decision. Artifact cell names the file path(s). Decision: approved | accepted | partially accepted | deferred | rejected.
     Pre-kit decisions: back-fill with Checkpoint "pre-kit" and Decision "approved (back-filled, pre-kit)". .eng/bin/eng-check matches rows to statuses. -->
| Date | Checkpoint | Artifact | Decision (Rob) |
|---|---|---|---|
| 2026-10-31 | CP-S | thoughts/shared/slices/2026-10-28-b-s2-round-trip-reply-root-id.md | approved (live: Town Square "@eddie status?" answered; DM "hi" answered; volume mmbridge-data persists bots.enc across redeploy (4c3d2cb); MCP reconnected; wake_url http://relay:8080/wake/eddie; via Eddie) |
| 2026-10-30 | CP-S | thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md | approved (relay in Mattermost compose stack; live: Rob post in ~acorn woke mmbridge-wake-eddie, run 21:28:50 CDT succeeded, ack in Eddie chat; mmbridge needed a container restart after first set-bot (booted store_unreadable, reload does not start WS); http wake host `relay` only (8c60bc8); Ulrik duplicate re-POST not run; via Eddie) |
| 2026-10-30 | CP-S | thoughts/shared/slices/2026-10-30-http-wake-internal-hosts.md | approved (8c60bc8 on main; exercised live by B-s1 demo: wake via http://relay with LIVE_ALLOW_HTTP_WAKE unset in prod; via Eddie) |
| 2026-10-30 | triage (size) | thoughts/shared/slices/2026-10-30-http-wake-internal-hosts.md | approved (small, security; Rob 'Tighten now': no global LIVE_ALLOW_HTTP_WAKE in prod, http only to in-stack relay; via Eddie) |
| 2026-10-29 | CP-C | thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md | approved speclock sha256:ee97d6ceffddcb0b (slices B-s1 -> B-s2 -> B-s3; via Eddie) |
| 2026-10-28 | CP-B | docs/architecture/2026-10-28-grok-webhook-multibot.md, docs/decisions/0011-hmac-to-bearer-wake-relay.md, docs/decisions/0013-multi-bot-store-v2.md, docs/decisions/0014-multi-bot-runtime-state-v2.md, docs/decisions/0015-thread-replies-root-id.md, docs/decisions/0016-acceptance-tests-increment-b.md | approved (architecture B + ADR-0011, 0013..0016 accepted; ADR-0012 claim_wake stays rejected; ops accepted for now: relay Bearer key + routine URL in Coolify env on relay, not mmbridge admin; same bot name ties Mattermost bot, relay and Grok routine; RELAY_BOT_<name>_HMAC_SECRET = copy of the bot wake secret; via Eddie) |
| 2026-10-28 | CP-R | thoughts/shared/research/2026-10-28-grok-webhook-multibot-current-code.md | accepted (via Eddie) |
| 2026-10-28 | CP-A (scope) | docs/design/2026-10-28-grok-webhook-multibot.md | approved (HOLD: In REQ-B1..B8; Out web admin, bot-to-bot wakes/caps, channel ignore-list; A5 suite stays in TODOS; via Eddie) |
| 2026-10-28 | CP-A | docs/design/2026-10-28-grok-webhook-multibot.md | approved (problem, REQ-B1..B8, acceptance examples; Grok wake contract locked: POST per-routine URL, Bearer key, any JSON body, 200=run started; via Eddie) |
| 2026-10-28 | retro | thoughts/shared/retros/2026-10-28-v0.3.0-live-bots.md | approved (all proposals: process changes 1-3 applied; kit lessons K-1..K-4 to Yana; via Eddie) |
| 2026-10-28 | CP-S | thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md | approved (verify PASS 8f987e7; Coolify steps 1-4 and 6 good; step 5 restart Mattermost mid-demo / real-MM resume+catch-up check deferred by Rob; rollback not exercised, LIVE_BOTS_ENABLED left on; via Eddie) |
| 2026-10-28 | CP-S | thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md | approved (verify PASS 14ecd18; demo set-bot + --channels reject; live Mattermost->receiver e2e deferred until listener/dispatcher wired in lb5) |
| 2026-10-27 | CP-C | thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md | approved speclock sha256:ea6a99cbd5601d05 |
| 2026-10-27 | CP-A | docs/design/2026-10-26-live-bots.md | approved amendment: drop allow-list sha256:0f250a0276b5 (via Eddie) |
| 2026-10-27 | CP-S | thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md | approved (verify PASS 219a9a1; README wake-receiver/tamper demo deferred - no set-bot/wake secret yet; via Eddie) |
| 2026-10-27 | CP-S | thoughts/shared/slices/2026-10-27-lb3-listener-filters.md | approved (verify PASS; ws_spike hello+ping reply+posted on Coolify; via Eddie) |
| 2026-10-27 | CP-S | thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md | approved (verify PASS; empty-DB admin failed/stats deferred; via Eddie) |
| 2026-10-27 | CP-S | thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md | approved (verify PASS; live container/Coolify check deferred, not yet redeployed; via Eddie) |
| 2026-10-28 | CP-P | CHANGELOG.md (v0.3.0, commit 93b4f7d, tag v0.3.0) | approved (release v0.3.0; Rob via Eddie; wake rule stays every-post, no @mention change) |
| 2026-10-27 | CP-C | thoughts/shared/plans/2026-10-27-live-bots.md | approved speclock sha256:3108f1fe6a93cfae |
| 2026-10-27 | CP-B | docs/architecture/2026-10-26-live-bots.md | approved (incl. stored-token security review) |
| 2026-10-27 | CP-B | docs/decisions/0006-encrypted-token-store.md, docs/decisions/0007-mattermost-websocket-listener.md, docs/decisions/0008-signed-wake-webhook.md, docs/decisions/0009-listener-state-persistence.md, docs/decisions/0010-acceptance-tests-live-bots.md | accepted (ADR-0006..0010) |
| 2026-10-26 | CP-R | thoughts/shared/research/2026-10-26-live-bots-current-code.md | accepted (via Eddie) |
| 2026-10-26 | CP-A (scope) | docs/design/2026-10-26-live-bots.md | approved (REDUCE: In A1, A2, A3 own-post, A4, A7, A8 one bot, hand-set channels; Out A6, A3 bot-to-bot caps, A5/A5b/A5c auto-join deferred by Rob after first proposal; via Eddie) |
| 2026-10-26 | CP-A | docs/design/2026-10-26-live-bots.md | approved (problem, REQ-A1..A8 incl. A5/A5b/A5c/A6, acceptance examples; via Eddie; later clarified: one-bot wedge = whole v1 ship, multi-bot later increment) |
| 2026-10-26 | triage (size) | docs/design/2026-10-26-live-bots.md | accepted (large confirmed; via Eddie) |
| 2026-10-26 | CP-S | thoughts/shared/slices/2026-10-26-d-hardening-xff-bearer.md | approved (live: FORWARDED_ALLOW_IPS working, logs show public client IPs; 1 container; via Eddie) |
| 2026-10-26 | triage (size) | thoughts/shared/slices/2026-10-26-d-hardening-xff-bearer.md | approved (small confirmed, security; via Eddie) |
| 2026-10-26 | CP-P | CHANGELOG.md (v0.2.0, commit 9946445, tag v0.2.0) | approved (release v0.2.0) |
| 2026-10-26 | CP-S | thoughts/shared/slices/2026-10-25-s3-dm.md | approved (live same-channel dual DM, ping via dm_read, nobody -> unknown_user)
| 2026-10-26 | CP-S | thoughts/shared/slices/2026-10-25-s2-post-read-channel.md | approved (live post/read/not_member)
| 2026-10-25 | CP-A | docs/design/2026-10-25-mmbridge-mcp.md | approved (problem, REQ-1..8, acceptance examples) |
| 2026-10-25 | CP-A (scope) | docs/design/2026-10-25-mmbridge-mcp.md | approved (scope mode hold: REQ-1..8 in; @mention wakes, auto-join, multi-bot, threads/reactions/files out) |
| 2026-10-25 | CP-B | docs/architecture/2026-10-25-mmbridge-mcp.md | approved |
| 2026-10-25 | CP-B | docs/decisions/0001-credential-handoff-bearer-per-call.md, docs/decisions/0002-mattermost-http-client.md, docs/decisions/0003-mcp-surface-streamable-http.md, docs/decisions/0004-per-token-in-memory-rate-limit.md, docs/decisions/0005-structured-logs-public-health.md | accepted (ADR-0001..0005) |
| 2026-10-26 | CP-C | thoughts/shared/plans/2026-10-25-mmbridge-mcp.md | approved speclock sha256:2e4855ad12913e1f |
| 2026-10-26 | CP-S | thoughts/shared/slices/2026-10-25-s1-auth-list-channels.md | approved (manual verification approved by Rob; verify PASS; review F1/F2 accepted-risk) |
 .gitattributes                                     |   3 +
 AGENTS.md                                          |   7 +-
 CHANGELOG.md                                       |   4 +
 Dockerfile                                         |   2 +
 OWNER-GUIDE.md                                     |   2 +
 README.md                                          |  29 +-
 app/admin.py                                       | 251 +++++++++++---
 app/listener.py                                    |  76 +++--
 app/live.py                                        | 206 ++++++++++--
 app/live_filter.py                                 |   7 +-
 app/main.py                                        |   3 +-
 app/setbot.py                                      |  61 ++++
 app/state.py                                       | 364 ++++++++++++++++-----
 app/store.py                                       | 211 +++++++++---
 app/wake.py                                        | 144 +++++---
 bin/set-bot                                        |   3 +
 coolify-service.snippet.yaml                       |   4 +
 relay/README.md                                    |  11 +
 tests/acceptance/drivers/fake_mattermost.py        |  10 +
 tests/acceptance/drivers/live.py                   |  94 +++++-
 tests/acceptance/drivers/relay.py                  |   6 +-
 tests/unit/test_admin.py                           | 250 +++++++++++++-
 tests/unit/test_app.py                             |   3 +-
 tests/unit/test_listener.py                        |  10 +-
 tests/unit/test_live_filter.py                     |  12 +-
 tests/unit/test_main_live.py                       | 203 ++++++++++--
 tests/unit/test_reconnect.py                       |  14 +-
 tests/unit/test_state.py                           | 282 ++++++++++++----
 tests/unit/test_store.py                           | 144 ++++++--
 tests/unit/test_wake.py                            | 214 +++++++++---
 .../plans/2026-10-28-grok-webhook-multibot.md      |   2 +-
 .../2026-10-28-b-s3-multi-bot-registry-routing.md  |  57 ++--
 ...6-10-30-b-s2-round-trip-reply-root-id-verify.md |   2 +-
 33 files changed, 2195 insertions(+), 496 deletions(-)
../acorn/.eng/templates/AGENTS.md
../acorn/AGENTS.md
../eng-process/templates/AGENTS.md
../farmer/.eng/templates/AGENTS.md
../farmer/AGENTS.md
../mmbridge/.eng/templates/AGENTS.md
../mmbridge/AGENTS.md
../model_filter/.eng/templates/AGENTS.md
../myaiworld/.eng/templates/AGENTS.md
../myaiworld/AGENTS.md
../myaiworld/docs/_proposed/scaffolding-drafts/AGENTS.md
../qf-builder/.eng/templates/AGENTS.md

 succeeded in 979ms:
Dockerfile
README.md
__pycache__
relay.py
requirements.txt
spike_routine.py
diff --git a/Dockerfile b/Dockerfile
index 57e19fb..9bf08ae 100644
--- a/Dockerfile
+++ b/Dockerfile
@@ -7,6 +7,8 @@ COPY requirements.txt .
 RUN pip install --no-cache-dir -r requirements.txt
 
 COPY app ./app
+COPY bin ./bin
+RUN chmod 755 bin/*
 
 # /data: persistent volume for the encrypted bot store (ADR-0006); owned by the app user, private.
 RUN useradd --create-home --uid 10001 appuser && mkdir -p /data && chown 10001:10001 /data && chmod 700 /data
diff --git a/app/live_filter.py b/app/live_filter.py
index c306c23..cc3bbfe 100644
--- a/app/live_filter.py
+++ b/app/live_filter.py
@@ -1,6 +1,7 @@
 """Which Mattermost websocket events wake the live bot (architecture Filter rules, REQ-A1/A2/A3).
 
-Pure apart from the `event_invalid` log line: no I/O, no state. Drop own posts (A3), system posts (type set) and
+Pure apart from the `event_invalid` log line: no I/O, no state. Drop own posts (A3) and posts by ANY registered bot
+(`registered_ids`, B7: no bot-to-bot wakes), system posts (type set) and
 group DMs (G); wake on DMs (D, A2) and every other post in open/private channels (A1). Membership is the channel
 filter: Mattermost only sends the bot `posted` events for channels it is a member of, so there is no allow-list.
 Thread replies are new posts and wake, carrying root_id. Malformed `posted` events drop and log `event_invalid`
@@ -38,7 +39,7 @@ def _post(data: dict) -> dict | None:
     return post if isinstance(post, dict) else None
 
 
-def decide(event: dict, bot_user_id: str) -> WakeIntent | None:
+def decide(event: dict, bot_user_id: str, registered_ids: frozenset = frozenset()) -> WakeIntent | None:
     if not isinstance(event, dict):
         _invalid("not_object")
         return None
@@ -67,7 +68,7 @@ def decide(event: dict, bot_user_id: str) -> WakeIntent | None:
         _invalid("channel_type")
         return None
 
-    if post["user_id"] == bot_user_id or post.get("type") or ctype == "G":
+    if post["user_id"] == bot_user_id or post["user_id"] in registered_ids or post.get("type") or ctype == "G":
         return None
     hints = {k: data.get(k) for k in ("channel_name", "channel_display_name", "sender_name", "team_id")}
     return WakeIntent(post["id"], post["channel_id"], ctype, post["user_id"], message, create_at,
diff --git a/app/main.py b/app/main.py
index fb3038f..af07171 100644
--- a/app/main.py
+++ b/app/main.py
@@ -1,6 +1,7 @@
 """mmbridge: MCP bridge between Grok Bots and self-hosted Mattermost.
 
-/health (public liveness + live-bots listener state, no ids) and /mcp (Bearer auth, MCP Streamable HTTP).
+/health (public liveness + live-bots state: worst listener status word and counts bots_total/bots_failing, no ids
+or names) and /mcp (Bearer auth, MCP Streamable HTTP).
 Everything else 404. The lifespan also starts the live-bots runtime (app/live.py) when LIVE_BOTS_ENABLED=true.
 """
 import contextlib
./.eng/templates/AGENTS.md
./AGENTS.md

exec
/bin/bash -lc "grep -n -E 'RELAY_BOT|replace|lower|name' relay/relay.py | head -45; ls .claude/skills; cat .eng/PROCESS.md | sed -n '35,85p'; .venv/bin/pytest tests/unit -q" in /mnt/d/rob/projects/mmbridge
exec
/bin/bash -lc "git diff e2f60917917cf30405578c8cd25ac6ecd50f14da -- app/admin.py | tail -95; nl -ba app/live.py | sed -n '247,270p'; nl -ba app/store.py | tail -20; python3 .eng/bin/eng-check ." in /mnt/d/rob/projects/mmbridge
 succeeded in 1783ms:
+
+
+def _status(out, transport) -> None:
+    st = _load(transport)
+    db = _open_state(transport)
+    now = time.time()
+    if not st.bots:
+        print("no bots", file=out)
+    for n in sorted(st.bots):
+        raw = db.get_meta(state.meta_key(n, "status"))
+        try:
+            rep = json.loads(raw) if raw else {}
+        except ValueError:
+            rep = {}
+        if not rep:
+            listener = "off (no report yet)"
+        elif now - rep.get("at", 0) > STATUS_STALE_S:
+            listener = "off (no report for %s; runtime stopped?)" % _age(now, rep.get("at"))[:-4]
+        else:
+            listener = rep["status"] + (" (%s)" % rep["error"] if rep.get("error") else "")
+        w = db.last_wake(n)
+        last = "none" if w is None else w.status + (" (%s)" % w.last_error if w.status == "failed" and
+                                                    w.last_error else "")
+        print("%s  listener %s  last event %s  last wake %s  failed_24h %d" % (
+            n, listener, _age(now, db.get_meta(state.meta_key(n, "last_event_at")), ms=True), last,
+            db.failed_count(int(now) - state.DAY, n)), file=out)
 
 
 def _rotate_key(a, out) -> None:
@@ -96,25 +253,31 @@ def _rotate_key(a, out) -> None:
     print("store re-encrypted with %s; set MMB_STORE_KEY to that key" % a.new_key_env, file=out)
 
 
-def _failed(a, out) -> None:
-    st = state.State(state.path_from_env())
+def _failed(a, out, transport) -> None:
+    st = _open_state(transport)
     if a.retry:
-        if not st.requeue(a.retry):
+        bot, _, pid = a.retry.rpartition(":")
+        if not bot:                            # bare post id: fine while only one bot has it failed
+            rows = st.failed_for_post(pid)
+            if len(rows) > 1:
+                raise AdminError("invalid_argument", "several bots failed %s: use BOT:POST_ID" % pid)
+            bot = rows[0].bot if rows else ""
+        if not bot or not st.requeue(bot, pid):
             raise AdminError("not_found", "no failed wake %s" % a.retry)
-        mlog.log.info(json.dumps({"event": "wake_requeued", "post_id": a.retry}))
-        print("requeued %s" % a.retry, file=out)
+        mlog.log.info(json.dumps({"event": "wake_requeued", "bot": bot, "post_id": pid}))
+        print("requeued %s:%s" % (bot, pid), file=out)
         return
-    rows = st.failed()
+    rows = st.failed(a.bot)
     if not rows:
         print("no failed wakes", file=out)
     for w in rows:
         at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(w.updated_at))
-        print("%s  channel %s  attempts %d  error %s  at %s" % (w.post_id, w.channel_id, w.attempts,
-                                                              w.last_error or "-", at), file=out)
+        print("bot %s  %s  channel %s  attempts %d  error %s  at %s" % (w.bot, w.post_id, w.channel_id, w.attempts,
+                                                                       w.last_error or "-", at), file=out)
 
 
-def _stats(out) -> None:
-    s = state.State(state.path_from_env()).stats()
+def _stats(a, out, transport) -> None:
+    s = _open_state(transport).stats(a.bot)
     if not s["counts"]:
         print("no wakes yet", file=out)
         return
@@ -131,14 +294,20 @@ def main(argv=None, stdin=None, stdout=None, transport=None) -> int:
     try:
         if a.cmd == "set-bot":
             _set_bot(a, stdin, out, transport)
+        elif a.cmd == "list":
+            _list(out, transport)
         elif a.cmd == "show":
-            _show(out)
+            _show(a, out, transport)
+        elif a.cmd == "remove-bot":
+            _remove_bot(a, out, transport)
+        elif a.cmd == "status":
+            _status(out, transport)
         elif a.cmd == "rotate-key":
             _rotate_key(a, out)
         elif a.cmd == "failed":
-            _failed(a, out)
+            _failed(a, out, transport)
         else:
-            _stats(out)
+            _stats(a, out, transport)
     except (AdminError, store.StoreError, state.StateError) as e:
         print("error: %s%s" % (e.code, ": " + e.detail if e.detail else ""), file=out)
         return 1
   247	        return st
   248	
   249	    async def _migrate_store(self, path: str, key: str | None, st) -> None:
   250	        """v1 store: name its bot after the Mattermost username (fallback `bot`) and save as v2 (+ .v1.bak)."""
   251	        (b,) = st.bots.values()
   252	        try:
   253	            me = await self.client_factory(b.token).get("/users/me")
   254	            username, uid = me["username"], me["id"]
   255	        except Exception as e:                       # MM down / token refused: keep the fallback name
   256	            username, uid = None, ""
   257	            _log("store_migrate_lookup_failed", "warning", error=getattr(e, "code", None) or type(e).__name__)
   258	        store.rename_v1(st, username, uid)
   259	        try:
   260	            store.save(path, key, st)
   261	            _log("store_migrated", bot=next(iter(st.bots)), fallback=username is None)
   262	        except (StoreError, OSError) as e:           # runs from memory; the next start tries again
   263	            _log("store_migrate_failed", "error", error=getattr(e, "code", None) or type(e).__name__)
   264	
   265	    async def _await_store(self, path: str, key: str | None) -> None:
   266	        """Retry the store load every reload_s until it succeeds (logged once, no values), then launch."""
   267	        while True:
   268	            await asyncio.sleep(self.reload_s)
   269	            try:
   270	                st = await self._load(path, key)
   272	def legacy_owner(st: Store):
   273	    """For the state.db v1 -> v2 migration: map the v1 meta bot_user_id to the bot that owned the v1 rows (by cached
   274	    user id; else the only bot; else LEGACY_NAME)."""
   275	    def owner(v1_user_id: str | None) -> str:
   276	        for b in st.bots.values():
   277	            if v1_user_id and b.user_id == v1_user_id:
   278	                return b.name
   279	        return next(iter(st.bots)) if len(st.bots) == 1 else LEGACY_NAME
   280	    return owner
   281	
   282	
   283	def rotate(path: str, new_key: str | None, old_key: str | None) -> None:
   284	    """Re-encrypt the store (and its .v1.bak, if any) with the first new key (readable with new or old keys);
   285	    validated first; atomic, 0600."""
   286	    f = MultiFernet(_keys(new_key) + _keys(old_key))
   287	    blob, _ = _read(path, f)
   288	    bak = backup_path(path)
   289	    if os.path.exists(bak):
   290	        _write(bak, f.rotate(_blob(bak)))
   291	    _write(path, f.rotate(blob))
WARN  .eng/runners.toml: no on_complete hook configured ([hooks] empty or missing) - bots must stay attached to eng-run until exit; fire-and-forget needs a non-empty on_complete / <role>_on_complete (PROCESS.md section 10, LESSONS L-006)
WARN  PROJECT_STATE.md: ## Latest artifacts has 41 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 37 rows / 7630 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 163 artifact(s) checked

exec
/bin/bash -lc '.venv/bin/pytest tests/unit -xq' in /mnt/d/rob/projects/mmbridge
 exited 1 in 8499ms:
........................................................................ [ 15%]
.....................................E
==================================== ERRORS ====================================
__________ ERROR at setup of test_qualifying_posts_land_once_in_state __________

self = <uvicorn.server.Server object at 0x723eba950fe0>, sockets = None

    async def startup(self, sockets: list[socket.socket] | None = None) -> None:
        await self.lifespan.startup()
        if self.lifespan.should_exit:
            self.should_exit = True
            return
    
        config = self.config
    
        def create_protocol(
            _loop: asyncio.AbstractEventLoop | None = None,
        ) -> asyncio.Protocol:
            return config.http_protocol_class(  # type: ignore[call-arg]
                config=config,
                server_state=self.server_state,
                app_state=self.lifespan.state,
                _loop=_loop,
            )
    
        loop = asyncio.get_running_loop()
    
        listeners: Sequence[socket.SocketType]
        if sockets is not None:  # pragma: full coverage
            # Explicitly passed a list of open sockets.
            # We use this when the server is run from a Gunicorn worker.
    
            def _share_socket(
                sock: socket.SocketType,
            ) -> socket.SocketType:  # pragma py-linux pragma: py-darwin
                # Windows requires the socket be explicitly shared across
                # multiple workers (processes).
                from socket import fromshare  # type: ignore[attr-defined]
    
                sock_data = sock.share(os.getpid())  # type: ignore[attr-defined]
                return fromshare(sock_data)
    
            self.servers: list[asyncio.base_events.Server] = []
            for sock in sockets:
                is_windows = platform.system() == "Windows"
                if config.workers > 1 and is_windows:  # pragma: py-not-win32
                    sock = _share_socket(sock)  # type: ignore[assignment]
                server = await loop.create_server(create_protocol, sock=sock, ssl=config.ssl, backlog=config.backlog)
                self.servers.append(server)
            listeners = sockets
    
        elif config.fd is not None:  # pragma: py-win32
            # Use an existing socket, from a file descriptor.
            sock = socket.fromfd(config.fd, socket.AF_UNIX, socket.SOCK_STREAM)
            server = await loop.create_server(create_protocol, sock=sock, ssl=config.ssl, backlog=config.backlog)
            assert server.sockets is not None  # mypy
            listeners = server.sockets
            self.servers = [server]
    
        elif config.uds is not None:  # pragma: py-win32
            # Create a socket using UNIX domain socket.
            uds_perms = 0o666
            if os.path.exists(config.uds):
                uds_perms = os.stat(config.uds).st_mode  # pragma: full coverage
            server = await loop.create_unix_server(
                create_protocol, path=config.uds, ssl=config.ssl, backlog=config.backlog
            )
            os.chmod(config.uds, uds_perms)
            assert server.sockets is not None  # mypy
            listeners = server.sockets
            self.servers = [server]
    
        else:
            # Standard case. Create a socket from a host/port pair.
            try:
>               server = await loop.create_server(
                    create_protocol,
                    host=config.host,
                    port=config.port,
                    ssl=config.ssl,
                    backlog=config.backlog,
                )

.venv/lib/python3.12/site-packages/uvicorn/server.py:163: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_UnixSelectorEventLoop running=False closed=False debug=False>
protocol_factory = <function Server.startup.<locals>.create_protocol at 0x723eba9d47c0>
host = '127.0.0.1', port = 0, family = <AddressFamily.AF_UNSPEC: 0>
flags = <AddressInfo.AI_PASSIVE: 1>, sock = None, backlog = 2048, ssl = None
reuse_address = True, reuse_port = None, ssl_handshake_timeout = None
ssl_shutdown_timeout = None, start_serving = True

    async def create_server(
            self, protocol_factory, host=None, port=None,
            *,
            family=socket.AF_UNSPEC,
            flags=socket.AI_PASSIVE,
            sock=None,
            backlog=100,
            ssl=None,
            reuse_address=None,
            reuse_port=None,
            ssl_handshake_timeout=None,
            ssl_shutdown_timeout=None,
            start_serving=True):
        """Create a TCP server.
    
        The host parameter can be a string, in that case the TCP server is
        bound to host and port.
    
        The host parameter can also be a sequence of strings and in that case
        the TCP server is bound to all hosts of the sequence. If a host
        appears multiple times (possibly indirectly e.g. when hostnames
        resolve to the same IP address), the server is only bound once to that
        host.
    
        Return a Server object which can be used to stop the service.
    
        This method is a coroutine.
        """
        if isinstance(ssl, bool):
            raise TypeError('ssl argument must be an SSLContext or None')
    
        if ssl_handshake_timeout is not None and ssl is None:
            raise ValueError(
                'ssl_handshake_timeout is only meaningful with ssl')
    
        if ssl_shutdown_timeout is not None and ssl is None:
            raise ValueError(
                'ssl_shutdown_timeout is only meaningful with ssl')
    
        if sock is not None:
            _check_ssl_socket(sock)
    
        if host is not None or port is not None:
            if sock is not None:
                raise ValueError(
                    'host/port and sock can not be specified at the same time')
    
            if reuse_address is None:
                reuse_address = os.name == "posix" and sys.platform != "cygwin"
            sockets = []
            if host == '':
                hosts = [None]
            elif (isinstance(host, str) or
                  not isinstance(host, collections.abc.Iterable)):
                hosts = [host]
            else:
                hosts = host
    
            fs = [self._create_server_getaddrinfo(host, port, family=family,
                                                  flags=flags)
                  for host in hosts]
            infos = await tasks.gather(*fs)
            infos = set(itertools.chain.from_iterable(infos))
    
            completed = False
            try:
                for res in infos:
                    af, socktype, proto, canonname, sa = res
                    try:
                        sock = socket.socket(af, socktype, proto)
                    except socket.error:
                        # Assume it's a bad family/type/protocol combination.
                        if self._debug:
                            logger.warning('create_server() failed to create '
                                           'socket.socket(%r, %r, %r)',
                                           af, socktype, proto, exc_info=True)
                        continue
                    sockets.append(sock)
                    if reuse_address:
                        sock.setsockopt(
                            socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
                    # Since Linux 6.12.9, SO_REUSEPORT is not allowed
                    # on other address families than AF_INET/AF_INET6.
                    if reuse_port and af in (socket.AF_INET, socket.AF_INET6):
                        _set_reuseport(sock)
                    # Disable IPv4/IPv6 dual stack support (enabled by
                    # default on Linux) which makes a single socket
                    # listen on both address families.
                    if (_HAS_IPv6 and
                            af == socket.AF_INET6 and
                            hasattr(socket, 'IPPROTO_IPV6')):
                        sock.setsockopt(socket.IPPROTO_IPV6,
                                        socket.IPV6_V6ONLY,
                                        True)
                    try:
                        sock.bind(sa)
                    except OSError as err:
                        msg = ('error while attempting '
                               'to bind on address %r: %s'
                               % (sa, str(err).lower()))
                        if err.errno == errno.EADDRNOTAVAIL:
                            # Assume the family is not enabled (bpo-30945)
                            sockets.pop()
                            sock.close()
                            if self._debug:
                                logger.warning(msg)
                            continue
                        raise OSError(err.errno, msg) from None
    
                if not sockets:
>                   raise OSError('could not bind on any address out of %r'
                                  % ([info[4] for info in infos],))
E                                 OSError: could not bind on any address out of [('127.0.0.1', 0)]

/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py:1587: OSError

During handling of the above exception, another exception occurred:

self = <Coroutine test_qualifying_posts_land_once_in_state>

    def setup(self) -> None:
        runner_fixture_id = f"_{self._loop_scope}_scoped_runner"
        if runner_fixture_id not in self.fixturenames:
            self.fixturenames.append(runner_fixture_id)
        # When loop factories are configured, resolve the loop factory
        # fixture early so that a factory variant change cascades cache
        # invalidation before any async fixture checks its cache.
        hook_caller = self.config.hook.pytest_asyncio_loop_factories
        if hook_caller.get_hookimpls():
            _ = self._request.getfixturevalue(_asyncio_loop_factory.__name__)
>       return super().setup()
               ^^^^^^^^^^^^^^^

.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:559: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:945: in pytest_fixture_setup
    hook_result = yield
                  ^^^^^
.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:408: in _asyncgen_fixture_wrapper
    result = runner.run(setup(), context=context)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/runners.py:118: in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py:678: in run_until_complete
    self.run_forever()
/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py:645: in run_forever
    self._run_once()
/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py:1999: in _run_once
    handle._run()
/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/events.py:88: in _run
    self._context.run(self._callback, *self._args)
.venv/lib/python3.12/site-packages/uvicorn/server.py:70: in serve
    await self._serve(sockets)
.venv/lib/python3.12/site-packages/uvicorn/server.py:85: in _serve
    await self.startup(sockets=sockets)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <uvicorn.server.Server object at 0x723eba950fe0>, sockets = None

    async def startup(self, sockets: list[socket.socket] | None = None) -> None:
        await self.lifespan.startup()
        if self.lifespan.should_exit:
            self.should_exit = True
            return
    
        config = self.config
    
        def create_protocol(
            _loop: asyncio.AbstractEventLoop | None = None,
        ) -> asyncio.Protocol:
            return config.http_protocol_class(  # type: ignore[call-arg]
                config=config,
                server_state=self.server_state,
                app_state=self.lifespan.state,
                _loop=_loop,
            )
    
        loop = asyncio.get_running_loop()
    
        listeners: Sequence[socket.SocketType]
        if sockets is not None:  # pragma: full coverage
            # Explicitly passed a list of open sockets.
            # We use this when the server is run from a Gunicorn worker.
    
            def _share_socket(
                sock: socket.SocketType,
            ) -> socket.SocketType:  # pragma py-linux pragma: py-darwin
                # Windows requires the socket be explicitly shared across
                # multiple workers (processes).
                from socket import fromshare  # type: ignore[attr-defined]
    
                sock_data = sock.share(os.getpid())  # type: ignore[attr-defined]
                return fromshare(sock_data)
    
            self.servers: list[asyncio.base_events.Server] = []
            for sock in sockets:
                is_windows = platform.system() == "Windows"
                if config.workers > 1 and is_windows:  # pragma: py-not-win32
                    sock = _share_socket(sock)  # type: ignore[assignment]
                server = await loop.create_server(create_protocol, sock=sock, ssl=config.ssl, backlog=config.backlog)
                self.servers.append(server)
            listeners = sockets
    
        elif config.fd is not None:  # pragma: py-win32
            # Use an existing socket, from a file descriptor.
            sock = socket.fromfd(config.fd, socket.AF_UNIX, socket.SOCK_STREAM)
            server = await loop.create_server(create_protocol, sock=sock, ssl=config.ssl, backlog=config.backlog)
            assert server.sockets is not None  # mypy
            listeners = server.sockets
            self.servers = [server]
    
        elif config.uds is not None:  # pragma: py-win32
            # Create a socket using UNIX domain socket.
            uds_perms = 0o666
            if os.path.exists(config.uds):
                uds_perms = os.stat(config.uds).st_mode  # pragma: full coverage
            server = await loop.create_unix_server(
                create_protocol, path=config.uds, ssl=config.ssl, backlog=config.backlog
            )
            os.chmod(config.uds, uds_perms)
            assert server.sockets is not None  # mypy
            listeners = server.sockets
            self.servers = [server]
    
        else:
            # Standard case. Create a socket from a host/port pair.
            try:
                server = await loop.create_server(
                    create_protocol,
                    host=config.host,
                    port=config.port,
                    ssl=config.ssl,
                    backlog=config.backlog,
                )
            except OSError as exc:
                logger.error(exc)
                await self.lifespan.shutdown()
>               sys.exit(1)
E               SystemExit: 1

.venv/lib/python3.12/site-packages/uvicorn/server.py:173: SystemExit
---------------------------- Captured stderr setup -----------------------------
ERROR:    could not bind on any address out of [('127.0.0.1', 0)]
=============================== warnings summary ===============================
tests/unit/test_listener.py::test_qualifying_posts_land_once_in_state
  /mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/websockets/legacy/__init__.py:6: DeprecationWarning: websockets.legacy is deprecated; see https://websockets.readthedocs.io/en/stable/howto/upgrade.html for upgrade instructions
    warnings.warn(  # deprecated in 14.0 - 2024-11-09

tests/unit/test_listener.py::test_qualifying_posts_land_once_in_state
  /mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/uvicorn/protocols/websockets/websockets_impl.py:17: DeprecationWarning: websockets.server.WebSocketServerProtocol is deprecated
    from websockets.server import WebSocketServerProtocol

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
ERROR tests/unit/test_listener.py::test_qualifying_posts_land_once_in_state
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!Task exception was never retrieved
future: <Task finished name='Task-446' coro=<Server.serve() done, defined at /mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/uvicorn/server.py:68> exception=SystemExit(1)>
Traceback (most recent call last):
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/uvicorn/server.py", line 163, in startup
    server = await loop.create_server(
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py", line 1587, in create_server
    raise OSError('could not bind on any address out of %r'
OSError: could not bind on any address out of [('127.0.0.1', 0)]

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/runner.py", line 361, in from_call
    result: TResult | None = func()
                             ^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/runner.py", line 250, in <lambda>
    lambda: runtest_hook(item=item, **kwds),
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_caller.py", line 197, in __call__
    return self._hookexec(
           ^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_manager.py", line 183, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 195, in _multicall
    raise exception
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 167, in _multicall
    teardown.throw(exception)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/logging.py", line 858, in pytest_runtest_setup
    yield
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 167, in _multicall
    teardown.throw(exception)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/capture.py", line 895, in pytest_runtest_setup
    return (yield)
            ^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 147, in _multicall
    res = hook_impl.function(*args)
          ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/runner.py", line 170, in pytest_runtest_setup
    item.session._setupstate.setup(item)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/runner.py", line 536, in setup
    col.setup()
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py", line 559, in setup
    return super().setup()
           ^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/python.py", line 1710, in setup
    self._request._fillfixtures()
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 806, in _fillfixtures
    item.funcargs[argname] = self.getfixturevalue(argname)
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 630, in getfixturevalue
    fixturedef = self._get_active_fixturedef(argname)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 726, in _get_active_fixturedef
    fixturedef.execute(request=subrequest)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 1181, in execute
    fixturedef = request._get_active_fixturedef(argname)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 726, in _get_active_fixturedef
    fixturedef.execute(request=subrequest)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 1232, in execute
    result: FixtureValue = ihook.pytest_fixture_setup(
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_caller.py", line 197, in __call__
    return self._hookexec(
           ^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_manager.py", line 183, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 195, in _multicall
    raise exception
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 167, in _multicall
    teardown.throw(exception)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py", line 945, in pytest_fixture_setup
    hook_result = yield
                  ^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 167, in _multicall
    teardown.throw(exception)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 64, in run_old_style_hookwrapper
    return result.get_result()
           ^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_result.py", line 103, in get_result
    raise exc.with_traceback(tb)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 49, in run_old_style_hookwrapper
    res = yield
          ^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 167, in _multicall
    teardown.throw(exception)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/setuponly.py", line 36, in pytest_fixture_setup
    return (yield)
            ^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 147, in _multicall
    res = hook_impl.function(*args)
          ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 1328, in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 1005, in call_fixture_func
    fixture_result = fixturefunc(**kwargs)
                     ^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py", line 408, in _asyncgen_fixture_wrapper
    result = runner.run(setup(), context=context)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py", line 678, in run_until_complete
    self.run_forever()
  File "/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py", line 645, in run_forever
    self._run_once()
  File "/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py", line 1999, in _run_once
    handle._run()
  File "/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/events.py", line 88, in _run
    self._context.run(self._callback, *self._args)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/uvicorn/server.py", line 85, in _serve
    await self.startup(sockets=sockets)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/uvicorn/server.py", line 173, in startup
    sys.exit(1)
SystemExit: 1

109 passed, 2 warnings, 1 error in 6.89s

codex
Startup store migration can overwrite successful concurrent administrative changes because it bypasses the store-edit lock and saves a stale snapshot.

Review comment:

- [P2] Serialize startup migration with admin store edits — /mnt/d/rob/projects/mmbridge/app/live.py:258-260
  If `set-bot` runs during the startup migration's awaited `/users/me` lookup, it can successfully save an updated v2 store before this code overwrites it with the previously loaded v1 snapshot. This silently loses added bots or credential changes despite the CLI's exclusive lock. Acquire the same store lock and reload/recheck the on-disk version before committing migration, preserving any intervening edits.
Startup store migration can overwrite successful concurrent administrative changes because it bypasses the store-edit lock and saves a stale snapshot.

Review comment:

- [P2] Serialize startup migration with admin store edits — /mnt/d/rob/projects/mmbridge/app/live.py:258-260
  If `set-bot` runs during the startup migration's awaited `/users/me` lookup, it can successfully save an updated v2 store before this code overwrites it with the previously loaded v1 snapshot. This silently loses added bots or credential changes despite the CLI's exclusive lock. Acquire the same store lock and reload/recheck the on-disk version before committing migration, preserving any intervening edits.
```
