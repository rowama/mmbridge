"""Live-bots runtime started from the FastAPI lifespan (slice lb5, ADR-0007/0009; plan Phase 5).

LiveRuntime.start(): LIVE_BOTS_ENABLED must be "true" (else health `disabled`), the store must decrypt
(MMB_STORE_KEY; else `off`, log store_unreadable, and re-try every RELOAD_S so the first set-bot starts the
listener without a restart, log store_appeared) and /data/state.db must be writable (else `off`, log
state_unwritable). Then three tasks: Listener and Dispatcher each under supervise() (crash -> log task_crashed,
health `degraded`, restart with backoff 1->60 s; MCP keeps serving) and the ConfigHolder watcher.
ConfigHolder (PR-2) re-reads the store when its mtime changes (every RELOAD_S): a valid new config replaces the
old one for both tasks (listener reconnects on a new token, dispatcher reads url/secret at send time); an invalid
file keeps the previous config (store_reload_failed). Logs carry field names and error codes, never values.
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
from app.state import DAY, State, StateError
from app.store import StoreError
from app.wake import Dispatcher

RELOAD_S = 30
RESTART_BASE_S, RESTART_MAX_S = 1.0, 60.0
FIELDS = ("token", "wake_url", "wake_secret")


def _log(event: str, level: str = "info", **fields) -> None:
    getattr(mlog.log, level)(json.dumps({"event": event, **fields}))


class ConfigHolder:
    """The current BotConfig plus a generation counter; subscribers get (old, new) on a real change."""

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
        """Reload if the file changed; True if the config changed (subscribers notified)."""
        m = self._stat()
        if m == self._mtime:
            return False
        self._mtime = m
        try:
            new = store.load(self.path, self.key)
        except StoreError as e:
            _log("store_reload_failed", "warning", code=e.code, detail=e.detail)
            return False
        changed = [f for f in FIELDS if getattr(new, f) != getattr(self.cfg, f)]
        if not changed:
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
        self.state = self.holder = self.listener = self.dispatcher = None
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
            cfg = store.load(path, key)
        except StoreError as e:
            _log("store_unreadable", "error", code=e.code, detail=e.detail)
            # Stay `off` but keep polling: the first set-bot (or a fixed key file) starts the listener, no restart.
            self._tasks = [asyncio.create_task(self._await_store(path, key))]
            return
        self._launch(path, key, cfg)

    async def _await_store(self, path: str, key: str | None) -> None:
        """Retry store.load every reload_s until it succeeds (logged once, no values), then launch."""
        while True:
            await asyncio.sleep(self.reload_s)
            try:
                cfg = store.load(path, key)
            except StoreError:
                continue
            _log("store_appeared")
            self._launch(path, key, cfg)
            return

    def _launch(self, path: str, key: str | None, cfg) -> None:
        try:
            self.state = State(self._data("state.db"))
        except StateError as e:
            _log("state_unwritable", "error", detail=e.detail)
            return
        self.holder = ConfigHolder(path, key, cfg)
        kw = {"catchup_minutes": float(self.env.get("LIVE_CATCHUP_MINUTES", "15")), **self.listener_kw}
        self.listener = Listener(self.holder.get, self.state, self.client_factory, base_url=self.base_url, **kw)
        self.holder.subscribe(self.listener.config_changed)
        self._http = self._http or httpx.AsyncClient()
        self.dispatcher = Dispatcher(self.state, self.holder.get, self._http, poll_s=self.poll_s)
        self._tasks += [
            asyncio.create_task(supervise("listener", self.listener.run, self.crashed, self.restart_base_s)),
            asyncio.create_task(supervise("dispatcher", self.dispatcher.run, self.crashed, self.restart_base_s)),
            asyncio.create_task(self.holder.watch(self.reload_s)),
        ]
        _log("listener_start", instance=self.state.instance_id)

    async def stop(self) -> None:
        for t in self._tasks:
            t.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        if self._http is not None:
            await self._http.aclose()
        if self.state is not None:
            await asyncio.to_thread(self.state.release_owner, "dispatcher_owner")
            self.state.close()
        if self._tasks:
            _log("listener_stop")

    def listener_status(self) -> str:
        if self.listener is None:
            return self.status
        return "degraded" if self.crashed else self.listener.status

    async def health(self) -> dict:
        """Public /health fields: status words and a count only (no ids or names, ADR-0005)."""
        n = 0
        if self.state is not None:
            n = await asyncio.to_thread(self.state.failed_count, int(time.time()) - DAY)
        return {"listener": self.listener_status(), "wake_failed_24h": n}
