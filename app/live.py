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
