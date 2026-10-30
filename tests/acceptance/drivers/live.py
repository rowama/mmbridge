"""Live-bots protocol driver (layer 3, ADR-0010). Drivers are not locked; edit freely.

A background event loop serves the fake Mattermost (REST + websocket, MM-shaped channel ids, real-time post
clock) and the HMAC-verifying wake receiver (drivers/wake_receiver.py) on free 127.0.0.1 ports. The bot is set up
with the real admin CLI (token on stdin, wake URL); the printed wake secret is handed to the receiver.
Backoff is scaled by WAKE_BACKOFF_SCALE so retry specs run in seconds; LIVE_ALLOW_HTTP_WAKE=true lets the wake
URL be the plain-HTTP local receiver (tests only).

SUT mode (env LIVE_MODE):
- `container` (default, lb5, ADR-0010 layer 4): the real image (env LIVE_IMAGE, default mmbridge:bs1; build it
  first with `docker build -t mmbridge:bs1 .`) on `--network host` with a fresh named volume at /data, a fresh
  MMB_STORE_KEY and LIVE_BOTS_ENABLED=true. `python -m app.admin set-bot` runs in a one-off container on the same
  volume before the server starts (as an operator would before enabling the flag); `admin failed` runs through
  `docker exec`; `/health` tells when the listener is connected; `docker logs` is the log capture for the token
  scan.
- `inprocess` (lb4): app.admin.main and app.live.LiveRuntime in this process; logs captured from the loggers.
Increment B (B-s1, ADR-0016): `register_bot(name, "grok")` points the bot's wake URL at the real wake relay
(drivers/relay.py: in-process or image RELAY_IMAGE, behind a recording tap) configured with the same name and wake
secret, which forwards to a fake Grok routine (drivers/fake_routine.py, checks the Bearer routine key).
`register_bot(name, "signed")` uses the HMAC receiver as in increment A. Wake secrets are passed to the CLI on
stdin (`--wake-secret-stdin`, as an operator copying one secret to the relay), so the CLI never prints them.
Wake retries: WAKE_BACKOFF_SCALE 0.25 gives ~7 s before a wake fails, enough to restart the relay container.
drop_connection: the fake closes the websocket (no resume: a new connection id) and refuses REST + websocket
until restore_connection, so posts made meanwhile are reachable only by the listener's REST catch-up.
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
import socket
import subprocess
import tempfile
import threading
import time

import httpx
from cryptography.fernet import Fernet

from app import admin
from app import logging as mlog
from app.live import LiveRuntime
from drivers.fake_mattermost import FakeMattermost
from drivers.fake_routine import FakeRoutine
from drivers.relay import RelayHarness
from drivers.wake_receiver import WakeReceiver

TEAM = "rmlab"
WAKE_WITHIN_S = 10.0       # design metric: wake within 10 s
SETTLE_S = 0.3
START_S = 30.0             # container start + listener connect
MARKER_USER = "zz-marker"
LOGGERS = ("mmbridge", "mmbridge.ws", "httpx", "websockets")


class _Capture(logging.Handler):
    def __init__(self):
        super().__init__(logging.DEBUG)
        self.addFilter(mlog.RedactFilter())
        self.lines = []

    def emit(self, record):
        self.lines.append(self.format(record))


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class _InProcess:
    """app.admin.main + app.live.LiveRuntime on the driver's event loop."""

    def __init__(self, drv, env):
        self.drv, self.env, self.runtime = drv, env, None
        self._saved = {k: os.environ.get(k) for k in env}
        os.environ.update(env)
        self._log = _Capture()
        for name in LOGGERS:
            logging.getLogger(name).addHandler(self._log)

    def admin(self, argv, stdin=""):
        out = io.StringIO()
        rc = admin.main(list(argv), stdin=io.StringIO(stdin), stdout=out, transport=self.drv.mm.transport())
        return rc, out.getvalue()

    def start(self):
        # reload_s: the container keeps the production 30 s store reload; in-process reloads fast.
        self.runtime = LiveRuntime(env=dict(os.environ), base_url=self.drv.base, poll_s=0.05, reload_s=0.1)
        self.drv._run(self.runtime.start())

    def listener(self):
        return self.runtime.listener_status() if self.runtime else "off"

    def logs(self):
        return "\n".join(self._log.lines)

    def close(self):
        try:
            if self.runtime:
                self.drv._run(self.runtime.stop())
        finally:
            for name in LOGGERS:
                logging.getLogger(name).removeHandler(self._log)
            for k, v in self._saved.items():
                os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)


class _Container:
    """The real image (ADR-0010): one-off admin containers + the server container on a fresh /data volume."""

    def __init__(self, drv, env):
        self.drv, self.env = drv, env
        self.image = os.environ.get("LIVE_IMAGE", "mmbridge:bs1")
        self.name = "mmb-live-" + secrets.token_hex(4)
        self.volume = self.name + "-data"
        self.port = _free_port()
        self.started = False
        if self._docker("image", "inspect", self.image).returncode != 0:
            raise AssertionError("image %s not found: run `docker build -t %s .` first" % (self.image, self.image))
        self._docker("volume", "create", self.volume, check=True)

    def _docker(self, *args, stdin="", check=False, timeout=60):
        r = subprocess.run(["docker", *args], input=stdin, capture_output=True, text=True, timeout=timeout)
        if check and r.returncode != 0:
            raise AssertionError("docker %s failed: %s" % (args[0], r.stderr.strip()))
        return r

    def _env_args(self):
        return [a for k, v in self.env.items() for a in ("-e", "%s=%s" % (k, v))]

    def admin(self, argv, stdin=""):
        if self.started:
            r = self._docker("exec", "-i", self.name, "python", "-m", "app.admin", *argv, stdin=stdin)
        else:
            r = self._docker("run", "--rm", "-i", "--network", "host", "-v", self.volume + ":/data",
                             *self._env_args(), self.image, "python", "-m", "app.admin", *argv, stdin=stdin)
        return r.returncode, r.stdout + r.stderr

    def start(self):
        # Same image and entrypoint as production; only the port differs (host network: avoid clashes on 8080).
        self._docker("run", "-d", "--name", self.name, "--network", "host", "-v", self.volume + ":/data",
                     *self._env_args(), "-e", "LIVE_BOTS_ENABLED=true", self.image,
                     "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(self.port), "--proxy-headers",
                     check=True)
        self.started = True

    def listener(self):
        try:
            return httpx.get("http://127.0.0.1:%d/health" % self.port, timeout=2).json()["listener"]
        except (httpx.HTTPError, ValueError, KeyError):
            return "starting"

    def logs(self):
        if not self.started:
            return ""
        r = self._docker("logs", self.name)
        return r.stdout + r.stderr

    def close(self):
        if self.started:
            if os.environ.get("LIVE_SHOW_LOGS"):
                print(self.logs())
            self._docker("rm", "-f", self.name)
        self._docker("volume", "rm", "-f", self.volume)


class LiveDriver:
    def __init__(self):
        self.mm = FakeMattermost(mm_ids=True, clock=time.time)
        self.rx = WakeReceiver()
        self.routine = FakeRoutine()
        self.bots = {}                 # name -> {"secret", "key", "kind"} (increment B)
        self.relay = None              # RelayHarness, started by the first grok bot
        self.started = False
        self.outputs = []              # admin CLI stdout
        self.posts = {}                # message -> post id (latest)
        self.teams = {}                # channel name -> team (given_channel)
        self._last_post = None
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
        self._thread.start()
        self._serving = [self.mm.serve(), self.rx.serve(), self.routine.serve()]
        self.base, self.wake_url, self.routine_base = (self._run(cm.__aenter__()) for cm in self._serving)
        env = {"MMB_STORE_KEY": Fernet.generate_key().decode(), "MATTERMOST_URL": self.base,
               "WAKE_BACKOFF_SCALE": "0.25", "WAKE_MAX_ATTEMPTS": "5", "LIVE_ALLOW_HTTP_WAKE": "true"}
        mode = self.mode = os.environ.get("LIVE_MODE", "container")
        assert mode in ("container", "inprocess"), "LIVE_MODE must be container or inprocess"
        self._tmp = None
        if mode == "inprocess":
            self._tmp = tempfile.mkdtemp(prefix="mmb-live-")
            self.sut = _InProcess(self, {**env, "MMB_DATA_DIR": self._tmp, "LIVE_BOTS_ENABLED": "true"})
        else:
            self.sut = _Container(self, env)

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

    def given_channel(self, team, channel, members, private=False):
        for m in members:
            self._user(m)
        self.mm.add_channel(team, channel, members, ctype="P" if private else "O")
        self.teams[channel] = team

    def _channel(self, channel):
        return self.mm.channel_by_name(channel, self.teams.get(channel, TEAM))

    def _admin(self, *argv, stdin=""):
        rc, out = self.sut.admin(argv, stdin)
        self.outputs.append(out)
        return rc, out

    def given_live_bot(self, name):
        u = self._user(name)
        u["is_bot"], u["token"] = True, "tok-%s-%s" % (name, secrets.token_hex(12))
        rc, out = self._admin("set-bot", "--token-stdin", "--wake-url", self.wake_url, stdin=u["token"] + "\n")
        assert rc == 0, "admin set-bot failed: %s" % out.strip()
        self.rx.secret = re.search(r"wake secret \(shown once[^)]*\): (\S+)", out).group(1)
        self._start()

    def _start(self):
        if not self.started:
            self.sut.start()
            self.started = True
            self._wait(lambda: self.sut.listener() == "ok", START_S, "listener ok in /health")

    def given_wake_target_down(self):
        self.rx.down = True

    def _post(self, channel_id, user, message, root_id=""):
        p = self._call(self.mm.add_post, channel_id, self._user(user)["id"], message, "", root_id)
        self.posts[message], self._last_post = p["id"], p["id"]
        return p

    def post_in(self, channel, message, as_user):
        self._post(self._channel(channel)["id"], as_user, message)

    def reply_in_thread(self, channel, to_message, message, as_user):
        self._post(self._channel(channel)["id"], as_user, message, root_id=self.posts[to_message])

    def dm(self, bot, message, as_user):
        c = self.mm.direct_channel(self._user(bot)["id"], self._user(as_user)["id"])
        self._post(c["id"], as_user, message)

    def send_forged_wake(self):
        body = json.dumps({"version": 1, "kind": "post", "delivery_id": "forged-1", "attempt": 1,
                           "post": {"id": "forged-1", "message": "do something bad"}}).encode()
        ts = int(time.time())
        forged_sig = "v1=" + hmac.new(b"not-the-secret", b"%d." % ts + body, hashlib.sha256).hexdigest()
        r = httpx.post(self.wake_url, content=body, timeout=5, headers={
            "Content-Type": "application/json", "X-MMB-Delivery": "forged-1", "X-MMB-Timestamp": str(ts),
            "X-MMB-Signature": forged_sig})
        return {"status": r.status_code, "delivery": "forged-1"}

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

    def assert_woken_once(self, bot, channel, sender, message, thread=None):
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
            assert w["channel"]["name"] == channel and w["channel"]["type"] == self._channel(channel)["type"]
            assert w["channel"]["type"] in ("O", "P")
        if thread is not None:
            assert w["post"]["root_id"] == self.posts[thread], "wake does not name the thread %r" % thread

    def _barrier(self, bot):
        """A DM posted after the scenario reaches the bot's current wake target (receiver, or routine via the
        relay, any status); anything before it has been processed by then. Returns the marker post id."""
        self._user(MARKER_USER)
        marker = "marker %s" % secrets.token_hex(4)
        self.dm(bot, marker, MARKER_USER)
        mid = self.posts[marker]
        if self.bots.get(bot, {}).get("kind") == "grok":
            self._wait(lambda: self.routine.reached(bot, mid), WAKE_WITHIN_S, "marker wake at the routine")
        else:
            self._wait(lambda: self._delivered(mid), WAKE_WITHIN_S, "marker wake")
        time.sleep(SETTLE_S)
        return mid

    def assert_not_woken(self, bot, message):
        mid = self._barrier(bot)
        others = [r for r in self.rx.requests if r["headers"].get("x-mmb-delivery") != mid]
        if message is not None:
            others = [r for r in others if json.loads(r["body"]).get("post", {}).get("message") == message]
        assert not others, "unexpected wake(s): %s" % [r["headers"].get("x-mmb-delivery") for r in others]

    def assert_not_member(self, bot, channel):
        c = self._channel(channel)
        assert self._user(bot)["id"] not in c["members"], "%s is a member of %s" % (bot, channel)
        joins = [x for x in self.mm.calls if x[0] != "GET" and ("/members" in x[1] or c["id"] in x[1])]
        assert joins == [] and self.mm.changes == [], "Mattermost writes: %s %s" % (joins, self.mm.changes)

    def assert_forged_wake_rejected(self, last):
        assert last["status"] == 401, "receiver accepted a forged wake (HTTP %s)" % last["status"]
        assert last["delivery"] not in self.rx.accepted

    def _mmb_attempts(self, pid):
        """Attempt numbers of failed deliveries mmbridge logged for this post (wake_retry / wake_failed)."""
        got = set()
        for line in self.sut.logs().splitlines():
            if pid in line and ("wake_retry" in line or "wake_failed" in line) and "{" in line:
                try:
                    ev = json.loads(line[line.index("{"):])
                except ValueError:
                    continue
                if ev.get("post_id") == pid and ev.get("event") in ("wake_retry", "wake_failed"):
                    got.add(ev["attempt"])
        return got

    def _grok_attempts(self, pid):
        """Attempt numbers seen at any routine (relay forwarded it) or logged by mmbridge (relay unreachable)."""
        seen = {json.loads(r["body"])["attempt"] for r in self.routine.requests if self.routine.post_id(r) == pid}
        return seen | self._mmb_attempts(pid)

    def assert_wake_retried(self, minimum):
        pid = self._last_post
        want = set(range(1, minimum + 1))
        self._wait(lambda: self.rx.attempts(pid) or want <= self._grok_attempts(pid), WAKE_WITHIN_S,
                   "%d attempts" % minimum)
        if not self.rx.attempts(pid):          # grok bot: attempts via relay -> routine, or refused at the relay
            return
        self._wait(lambda: len(self.rx.attempts(pid)) >= minimum, WAKE_WITHIN_S, "%d attempts" % minimum)
        attempts = self.rx.attempts(pid)
        assert all(self._valid(r) for r in attempts)
        assert [json.loads(r["body"])["attempt"] for r in attempts][:minimum] == list(range(1, minimum + 1))

    def assert_failed_wake_visible(self, message):
        pid = self.posts[message] if message is not None else self._last_post
        seen = {}

        def listed():
            seen["rc"], seen["out"] = self._admin("failed")
            return seen["rc"] == 0 and pid in seen["out"]
        self._wait(listed, 20, "admin failed to list %s (last output: %r)" % (pid, seen.get("out")))

    def assert_no_token_anywhere(self, bot):
        tok = self._user(bot)["token"]
        logs = self.sut.logs()
        assert '"event": "wake_queued"' in logs, "log capture is empty or not the bridge's logs"
        assert tok not in logs, "token in logs"
        assert tok not in "\n".join(self.outputs), "token in admin output"
        for r in self.rx.requests:
            assert tok not in r["body"].decode() and tok not in json.dumps(r["headers"]), "token in a wake"

    # --- increment B: Grok routine via the wake relay (B-s1) ---------------------------------------------------
    def _relay(self):
        if self.relay is None:
            self.relay = RelayHarness(self, self.mode, self.routine_base)
        return self.relay

    def _configure_relay(self):
        grok = {n: b for n, b in self.bots.items() if b["kind"] == "grok"}
        if grok:
            self._relay().configure(grok)

    def _target(self, name, kind):
        return "%s/wake/%s" % (self._relay().url, name) if kind == "grok" else self.wake_url

    def _set_bot(self, name):
        b, u = self.bots[name], self._user(name)
        rc, out = self._admin("set-bot", "--token-stdin", "--wake-secret-stdin", "--wake-url",
                              self._target(name, b["kind"]), stdin="%s\n%s\n" % (u["token"], b["secret"]))
        assert rc == 0, "admin set-bot failed: %s" % out.strip()

    def register_bot(self, name, wake):
        assert wake in ("grok", "signed"), wake
        u = self._user(name)
        u["is_bot"], u["token"] = True, "tok-%s-%s" % (name, secrets.token_hex(12))
        self.bots[name] = {"secret": secrets.token_urlsafe(32), "key": "rk-%s-%s" % (name, secrets.token_hex(16)),
                           "kind": wake}
        self.routine.keys[name] = self.bots[name]["key"]
        if wake == "signed":
            self.rx.secret = self.bots[name]["secret"]
        self._configure_relay()                 # relay ready (same name + secret) before mmbridge points at it
        self._set_bot(name)
        self._start()

    def _reloads(self):
        return sum(1 for line in self.sut.logs().splitlines() if "store_updated" in line and '"generation"' in line)

    def switch_wake_target(self, bot, wake):
        before = self._reloads()
        self.bots[bot]["kind"] = wake
        if wake == "signed":
            self.rx.secret = self.bots[bot]["secret"]
        self._configure_relay()
        self._set_bot(bot)                      # same secret (copied to the relay), new wake URL
        # No redeploy/restart: the running bridge picks the change up on its own store reload (30 s in the image).
        self._wait(lambda: self._reloads() > before, 45, "the running bridge to reload the store")

    def grok_routine_down(self, bot):
        self.routine.down.add(bot)

    def grok_routine_up(self, bot):
        self.routine.down.discard(bot)

    def relay_down(self):
        self._relay().down()

    def relay_up(self):
        self._relay().up()

    def forge_wake(self, bot):
        d = "forged-" + secrets.token_hex(4)
        body = json.dumps({"version": 1, "kind": "post", "delivery_id": d, "attempt": 1,
                           "post": {"id": d, "message": "do something bad"}}, separators=(",", ":")).encode()
        ts = int(time.time())
        sig = "v1=" + hmac.new(b"not-the-secret", b"%d." % ts + body, hashlib.sha256).hexdigest()
        return self._relay().send(bot, body, {"Content-Type": "application/json", "X-MMB-Delivery": d,
                                              "X-MMB-Timestamp": str(ts), "X-MMB-Signature": sig})

    def _captured_headers(self, rec):
        return {k: v for k, v in rec["headers"].items() if k.startswith("x-mmb-") or k == "content-type"}

    def tamper_wake(self, bot, message):
        rec = self._relay().last(bot)
        w = json.loads(rec["body"])
        w["post"]["message"] = message
        body = json.dumps(w, separators=(",", ":")).encode()
        return self._relay().send(bot, body, self._captured_headers(rec))

    def replay_last_wake(self, bot, after_seconds):
        rec = self._relay().last(bot)
        return self._relay().send(bot, rec["body"], self._captured_headers(rec), after_seconds=after_seconds)

    def _runs(self, bot, post_id):
        return [r for r in self.routine.runs(bot) if self.routine.post_id(r) == post_id]

    def assert_routine_started_once(self, bot, channel, sender, message, thread=None):
        pid = self.posts[message]
        self._wait(lambda: self._runs(bot, pid), WAKE_WITHIN_S, "routine run for %r" % message)
        time.sleep(SETTLE_S)
        got = self._runs(bot, pid)
        assert len(got) == 1, "expected one routine run for %r, got %d" % (message, len(got))
        r = got[0]
        assert r["headers"].get("authorization") == "Bearer " + self.bots[bot]["key"], "routine key not used"
        w = json.loads(r["body"])
        assert r["headers"].get("x-mmb-delivery") == w["delivery_id"]
        assert w["post"]["id"] == pid and w["post"]["message"] == message
        assert w["bot"]["username"] == bot and w["sender"]["username"] == sender
        if channel is None:
            assert w["channel"]["type"] == "D"
        else:
            assert w["channel"]["name"] == channel and w["channel"]["type"] == self._channel(channel)["type"]
            assert w["channel"]["type"] in ("O", "P")
        if thread is not None:
            assert w["post"]["root_id"] == self.posts[thread], "wake does not name the thread %r" % thread

    def assert_routine_not_started(self, bot, message):
        mid = self._barrier(bot)
        runs = [r for r in self.routine.runs(bot) if self.routine.post_id(r) != mid]
        if message is not None:
            runs = [r for r in runs if json.loads(r["body"]).get("post", {}).get("message") == message]
        assert not runs, "unexpected routine run(s): %s" % [self.routine.post_id(r) for r in runs]

    def assert_no_secret_anywhere(self, bot):
        tok, b = self._user(bot)["token"], self.bots[bot]
        secrets_ = {"token": tok, "wake secret": b["secret"], "routine key": b["key"]}
        logs, relay_logs = self.sut.logs(), self.relay.logs() if self.relay else ""
        assert '"event": "wake_queued"' in logs, "log capture is empty or not the bridge's logs"
        if b["kind"] == "grok":
            assert "relay_forwarded" in relay_logs, "relay log capture is empty or not the relay's logs"
        places = {"mmbridge logs": logs, "relay logs": relay_logs, "admin output": "\n".join(self.outputs)}
        for r in self.routine.requests:         # the Bearer key is legitimately in the routine's Authorization
            h = {k: v for k, v in r["headers"].items() if k != "authorization"}
            places["routine wake"] = places.get("routine wake", "") + r["body"].decode() + json.dumps(h)
        for r in self.rx.requests:
            places["receiver wake"] = places.get("receiver wake", "") + r["body"].decode() + json.dumps(r["headers"])
        if self.relay:
            places["relay wake"] = "".join(r["body"].decode() + json.dumps(r["headers"]) for r in self.relay.captured)
            places["relay responses"] = "".join(r["text"] + json.dumps(r["headers"]) for r in self.relay.responses)
        for what, value in secrets_.items():
            for where, text in places.items():
                assert value not in text, "%s in %s" % (what, where)

    def drop_connection(self, seconds):
        # `seconds` is simulated: reconnects stay refused until restore_connection (no real wait).
        def drop():
            self.mm.ws_refuse = True
            self.mm.ws_drop(resumable=False)
        self._call(drop)
        self._wait(lambda: self.sut.listener() not in ("ok", "starting"), 5, "listener to notice the drop")

    def restore_connection(self):
        self._call(setattr, self.mm, "ws_refuse", False)

    def close(self):
        try:
            try:
                self.sut.close()
            finally:
                if self.relay:
                    self.relay.close()
        finally:
            try:
                for cm in reversed(self._serving):
                    self._run(cm.__aexit__(None, None, None))
            finally:
                self._loop.call_soon_threadsafe(self._loop.stop)
                self._thread.join(5)
                self._loop.close()
                if self._tmp:
                    shutil.rmtree(self._tmp, ignore_errors=True)
