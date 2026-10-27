"""Live-bots protocol driver (layer 3, ADR-0010). Drivers are not locked; edit freely.

lb4: in-process mode. A background event loop runs the fake Mattermost (REST + websocket, served on a free
localhost port, MM-shaped channel ids), the real Listener and Dispatcher, and an HMAC-verifying wake receiver
(drivers/wake_receiver.py, reached through an in-process httpx transport at https://receiver.test/wake).
The bot is configured with the real admin CLI (`app.admin.main`, as `python -m app.admin` would run it) on a
temp /data with a fresh MMB_STORE_KEY; the printed wake secret is handed to the receiver. Backoff is scaled
by WAKE_BACKOFF_SCALE so retry specs run in seconds.
lb5 adds container mode (real image) and drop/restore connection.
"""
import asyncio
import hashlib
import hmac
import io
import json
import logging
import os
import re
import secrets
import shutil
import tempfile
import threading
import time

import httpx
from cryptography.fernet import Fernet

from app import admin, store
from app import logging as mlog
from app.listener import Listener
from app.mattermost import Client
from app.state import State
from app.wake import Dispatcher
from drivers.fake_mattermost import FakeMattermost
from drivers.wake_receiver import WakeReceiver

WAKE_URL = "https://receiver.test/wake"
TEAM = "rmlab"
WAKE_WITHIN_S = 10.0       # design metric: wake within 10 s
SETTLE_S = 0.3
MARKER_USER = "zz-marker"


class _Capture(logging.Handler):
    def __init__(self):
        super().__init__(logging.DEBUG)
        self.addFilter(mlog.RedactFilter())
        self.lines = []

    def emit(self, record):
        self.lines.append(self.format(record))


class LiveDriver:
    def __init__(self):
        self._tmp = tempfile.mkdtemp(prefix="mmb-live-")
        env = {"MMB_DATA_DIR": self._tmp, "MMB_STORE_KEY": Fernet.generate_key().decode(),
               "WAKE_BACKOFF_SCALE": "0.05", "WAKE_MAX_ATTEMPTS": "5"}
        self._env_saved = {k: os.environ.get(k) for k in env}
        os.environ.update(env)
        self.mm = FakeMattermost(mm_ids=True)
        self.rx = WakeReceiver()
        self.outputs = []              # admin CLI stdout
        self.posts = {}                # message -> post id (latest)
        self._last_post = None
        self._tasks = []
        self.state = None
        self._log = _Capture()
        for name in ("mmbridge", "mmbridge.ws", "httpx", "websockets"):
            logging.getLogger(name).addHandler(self._log)
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
        self._thread.start()
        self._serving = self.mm.serve()
        self.base = self._run(self._serving.__aenter__())

    def _run(self, coro, timeout=20):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result(timeout)

    def _call(self, fn, *a):
        async def go():
            return fn(*a)
        return self._run(go())

    # --- world ------------------------------------------------------------------------------------------------
    def _user(self, name):
        try:
            return self.mm.user_by_name(name)
        except StopIteration:
            return self.mm.add_user(name)

    def given_channel(self, team, channel, members):
        for m in members:
            self._user(m)
        self.mm.add_channel(team, channel, members)

    def _admin(self, *argv, stdin=""):
        out = io.StringIO()
        rc = admin.main(list(argv), stdin=io.StringIO(stdin), stdout=out, transport=self.mm.transport())
        self.outputs.append(out.getvalue())
        return rc, out.getvalue()

    def given_live_bot(self, name, channels):
        u = self._user(name)
        u["is_bot"], u["token"] = True, "tok-%s-%s" % (name, secrets.token_hex(12))
        rc, out = self._admin("set-bot", "--token-stdin", "--wake-url", WAKE_URL,
                              "--channels", ",".join("%s/%s" % (TEAM, c) for c in channels), stdin=u["token"] + "\n")
        assert rc == 0, "admin set-bot failed: %s" % out.strip()
        self.rx.secret = re.search(r"wake secret \(shown once[^)]*\): (\S+)", out).group(1)
        cfg = store.load(store.path_from_env(), os.environ["MMB_STORE_KEY"])
        self._run(self._start(cfg))

    async def _start(self, cfg):
        self.state = State(os.path.join(self._tmp, "state.db"))
        self.listener = Listener(cfg, self.state, lambda tok: Client(tok, base_url=self.base), base_url=self.base)
        self.http = httpx.AsyncClient(transport=self.rx.transport())
        path, key = store.path_from_env(), os.environ["MMB_STORE_KEY"]
        self.dispatcher = Dispatcher(self.state, lambda: store.load(path, key), self.http, poll_s=0.05)
        self._tasks = [asyncio.create_task(self.listener.run()), asyncio.create_task(self.dispatcher.run())]
        for _ in range(500):
            if self.listener.status == "ok":
                return
            if self._tasks[0].done():
                self._tasks[0].result()
            await asyncio.sleep(0.01)
        raise AssertionError("listener did not connect")

    def given_wake_target_down(self):
        self.rx.down = True

    def _post(self, channel_id, user, message):
        p = self._call(self.mm.add_post, channel_id, self._user(user)["id"], message)
        self.posts[message], self._last_post = p["id"], p["id"]
        return p

    def post_in(self, channel, message, as_user):
        self._post(self.mm.channel_by_name(channel, TEAM)["id"], as_user, message)

    def dm(self, bot, message, as_user):
        c = self.mm.direct_channel(self._user(bot)["id"], self._user(as_user)["id"])
        self._post(c["id"], as_user, message)

    def send_forged_wake(self):
        body = json.dumps({"version": 1, "kind": "post", "delivery_id": "forged-1", "attempt": 1,
                           "post": {"id": "forged-1", "message": "do something bad"}}).encode()
        ts = int(time.time())
        forged_sig = "v1=" + hmac.new(b"not-the-secret", b"%d." % ts + body, hashlib.sha256).hexdigest()

        async def go():
            r = await self.http.post(WAKE_URL, content=body, headers={
                "Content-Type": "application/json", "X-MMB-Delivery": "forged-1", "X-MMB-Timestamp": str(ts),
                "X-MMB-Signature": forged_sig})
            return {"status": r.status_code, "delivery": "forged-1"}
        return self._run(go())

    # --- checks ---------------------------------------------------------------------------------------------
    def _wait(self, pred, timeout, what):
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            if pred():
                return
            time.sleep(0.02)
        raise AssertionError("timed out after %.1fs waiting for %s" % (timeout, what))

    def _valid(self, req):
        """Independent HMAC check of a captured request (not via app.wake.verify)."""
        h = req["headers"]
        mac = hmac.new(self.rx.secret.encode(), h.get("x-mmb-timestamp", "").encode() + b"." + req["body"],
                       hashlib.sha256).hexdigest()
        return hmac.compare_digest(h.get("x-mmb-signature", ""), "v1=" + mac) and \
            abs(time.time() - int(h["x-mmb-timestamp"])) <= 300

    def _delivered(self, post_id):
        return [r for r in self.rx.attempts(post_id) if r["status"] == 204]

    def assert_woken_once(self, bot, channel, sender, message):
        pid = self.posts[message]
        self._wait(lambda: self._delivered(pid), WAKE_WITHIN_S, "wake for %r" % message)
        time.sleep(SETTLE_S)
        got = self._delivered(pid)
        assert len(got) == 1, "expected one delivered wake for %r, got %d" % (message, len(got))
        assert self._valid(got[0]), "wake signature does not verify"
        w = json.loads(got[0]["body"])
        assert w["delivery_id"] == pid and w["post"]["id"] == pid and w["post"]["message"] == message
        assert w["bot"]["username"] == bot and w["sender"]["username"] == sender
        if channel is None:
            assert w["channel"]["type"] == "D"
        else:
            assert w["channel"]["name"] == channel and w["channel"]["type"] in ("O", "P")

    def assert_not_woken(self, bot, message):
        # Barrier: a DM posted after the scenario is woken; anything before it has been processed by then.
        self._user(MARKER_USER)
        marker = "marker %s" % secrets.token_hex(4)
        self.dm(bot, marker, MARKER_USER)
        mid = self.posts[marker]
        self._wait(lambda: self._delivered(mid), WAKE_WITHIN_S, "marker wake")
        time.sleep(SETTLE_S)
        others = [r for r in self.rx.requests if r["headers"].get("x-mmb-delivery") != mid]
        if message is not None:
            others = [r for r in others if json.loads(r["body"]).get("post", {}).get("message") == message]
        assert not others, "unexpected wake(s): %s" % [r["headers"].get("x-mmb-delivery") for r in others]

    def assert_forged_wake_rejected(self, last):
        assert last["status"] == 401, "receiver accepted a forged wake (HTTP %s)" % last["status"]
        assert last["delivery"] not in self.rx.accepted

    def assert_wake_retried(self, minimum):
        pid = self._last_post
        self._wait(lambda: len(self.rx.attempts(pid)) >= minimum, WAKE_WITHIN_S, "%d attempts" % minimum)
        attempts = self.rx.attempts(pid)
        assert all(self._valid(r) for r in attempts)
        assert [json.loads(r["body"])["attempt"] for r in attempts][:minimum] == list(range(1, minimum + 1))

    def assert_failed_wake_visible(self, message):
        pid = self.posts[message] if message is not None else self._last_post
        self._wait(lambda: (w := self.state.wake(pid)) is not None and w.status == "failed", 20, "failed wake")
        rc, out = self._admin("failed")
        assert rc == 0 and pid in out, "admin failed does not list %s: %s" % (pid, out)

    def assert_no_token_anywhere(self, bot):
        tok = self._user(bot)["token"]
        assert tok not in "\n".join(self._log.lines), "token in logs"
        assert tok not in "\n".join(self.outputs), "token in admin output"
        for r in self.rx.requests:
            assert tok not in r["body"].decode() and tok not in json.dumps(r["headers"]), "token in a wake"

    def drop_connection(self, seconds):
        raise NotImplementedError("live driver: drop_connection is built in lb5 (reconnect)")

    def restore_connection(self):
        raise NotImplementedError("live driver: restore_connection is built in lb5 (reconnect)")

    def close(self):
        async def stop():
            for t in self._tasks:
                t.cancel()
            await asyncio.gather(*self._tasks, return_exceptions=True)
            if self._tasks:
                await self.http.aclose()
            await self._serving.__aexit__(None, None, None)
        try:
            self._run(stop())
        finally:
            self._loop.call_soon_threadsafe(self._loop.stop)
            self._thread.join(5)
            self._loop.close()
            if self.state:
                self.state.close()
            for name in ("mmbridge", "mmbridge.ws", "httpx", "websockets"):
                logging.getLogger(name).removeHandler(self._log)
            for k, v in self._env_saved.items():
                os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
            shutil.rmtree(self._tmp, ignore_errors=True)
