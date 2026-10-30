"""Wake relay under test (ADR-0011/0016). Drivers are not locked; edit freely.

The real relay (relay/relay.py) runs in-process (uvicorn in the driver's loop, `LIVE_MODE=inprocess`) or as the
real image (`LIVE_MODE=container`, env RELAY_IMAGE, default mmbridge-relay:bs1; build it first with
`docker build -t mmbridge-relay:bs1 relay`) on --network host with a fresh /data volume. Relay config is env only,
so `configure(bots)` (re)starts it with RELAY_BOT_<NAME>_* (container: via a 0600 --env-file, not argv).

mmbridge reaches the relay through a recording tap (`url`): it records each signed wake exactly as sent
(headers + raw body) so specs can tamper with / replay a genuinely captured wake (`send`, straight to the relay).
`down()` stops the relay and the tap (connection refused at mmbridge); `up()` starts both again on the same
ports with the same /data (Seen survives).
Simulated clock (replay N s later): in-process the relay clock is time.time() + offset for that one request.
The container relay has no clock hook (none is added to production code), so there the replay is sent at once
and is refused as a duplicate; the stale-timestamp path is covered by tests/unit/test_relay.py.
"""
import logging
import os
import secrets
import shutil
import socket
import subprocess
import tempfile
import time

import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from drivers import _serve
from relay import relay as relay_mod

START_S = 20.0


def _env(bots, routine_base):
    e = {"RELAY_ALLOW_HTTP_UPSTREAM": "true"}
    for name, b in bots.items():
        n = name.upper().replace("-", "_")
        e["RELAY_BOT_%s_HMAC_SECRET" % n] = b["secret"]
        e["RELAY_BOT_%s_ROUTINE_URL" % n] = "%s/%s" % (routine_base, name)
        e["RELAY_BOT_%s_ROUTINE_KEY" % n] = b["key"]
    return e


class _Capture(logging.Handler):
    """Plain capture: the relay logger's own RedactFilter is what is under test."""

    def __init__(self):
        super().__init__(logging.DEBUG)
        self.lines = []

    def emit(self, record):
        self.lines.append(record.getMessage())


class _InProcessRelay:
    def __init__(self, drv):
        self.drv = drv
        self.tmp = tempfile.mkdtemp(prefix="mmb-relay-")
        self.offset = 0.0
        self.port = 0
        self.env = {}
        self._srv = None
        self._log = _Capture()
        logging.getLogger("relay").addHandler(self._log)

    def _clock(self):
        return time.time() + self.offset

    def start(self, env=None):
        if env is not None:
            self.env = {**env, "RELAY_DATA_DIR": self.tmp}

        async def go():
            app = relay_mod.create_app(self.env, clock=self._clock)
            return await _serve.start(app, self.port, lifespan="on")
        server, task, self.port = self.drv._run(go())
        self._srv = (server, task)
        return "http://127.0.0.1:%d" % self.port

    def stop(self):
        if self._srv:
            self.drv._run(_serve.stop(*self._srv))
            self._srv = None

    def logs(self):
        return "\n".join(self._log.lines)

    def close(self):
        try:
            self.stop()
        finally:
            logging.getLogger("relay").removeHandler(self._log)
            shutil.rmtree(self.tmp, ignore_errors=True)


class _ContainerRelay:
    def __init__(self, drv):
        self.drv = drv
        self.image = os.environ.get("RELAY_IMAGE", "mmbridge-relay:bs1")
        self.name = "mmb-relay-" + secrets.token_hex(4)
        self.volume = self.name + "-data"
        self.port = _free_port()
        self.created = False
        self.offset = 0.0                        # no clock hook in the image (see module docstring)
        self._old_logs = ""
        self._envfile = None
        if self._docker("image", "inspect", self.image).returncode != 0:
            raise AssertionError("image %s not found: run `docker build -t %s relay` first" % (self.image, self.image))
        self._docker("volume", "create", self.volume, check=True)

    def _docker(self, *args, check=False, timeout=60):
        r = subprocess.run(["docker", *args], capture_output=True, text=True, timeout=timeout)
        if check and r.returncode != 0:
            raise AssertionError("docker %s failed: %s" % (args[0], r.stderr.strip()))
        return r

    def _wait_health(self):
        end = time.monotonic() + START_S
        while time.monotonic() < end:
            try:
                if httpx.get("http://127.0.0.1:%d/health" % self.port, timeout=1).status_code == 200:
                    return
            except httpx.HTTPError:
                pass
            time.sleep(0.05)
        raise AssertionError("relay container not healthy after %.0fs: %s" % (START_S, self.logs()[-2000:]))

    def start(self, env=None):
        if env is not None:                       # new config: replace the container, keep the volume
            if self.created:
                self._old_logs += self.logs()
                self._docker("rm", "-f", self.name)
                self.created = False
            fd, self._envfile = tempfile.mkstemp(prefix="mmb-relay-env-")
            with os.fdopen(fd, "w") as f:         # mkstemp: mode 0600
                f.write("".join("%s=%s\n" % kv for kv in env.items()))
        if self.created:
            self._docker("start", self.name, check=True)
        else:
            self._docker("run", "-d", "--name", self.name, "--network", "host", "-v", self.volume + ":/data",
                         "--env-file", self._envfile, self.image, "uvicorn", "relay:create_app", "--factory",
                         "--host", "127.0.0.1", "--port", str(self.port), check=True)
            self.created = True
        self._wait_health()
        return "http://127.0.0.1:%d" % self.port

    def stop(self):
        if self.created:
            self._docker("stop", "-t", "2", self.name)

    def logs(self):
        if not self.created:
            return self._old_logs
        r = self._docker("logs", self.name)
        return self._old_logs + r.stdout + r.stderr

    def close(self):
        try:
            if self.created:
                if os.environ.get("LIVE_SHOW_LOGS"):
                    print(self.logs())
                self._docker("rm", "-f", self.name)
        finally:
            self._docker("volume", "rm", "-f", self.volume)
            if self._envfile:
                os.unlink(self._envfile)


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class RelayHarness:
    """Relay (in-process or container) behind a recording tap; all on the driver's event loop."""

    def __init__(self, drv, mode, routine_base):
        self.drv, self.routine_base = drv, routine_base
        self.relay = _InProcessRelay(drv) if mode == "inprocess" else _ContainerRelay(drv)
        self.captured = []          # {"bot", "headers", "body", "status"} as mmbridge sent them
        self.responses = []         # relay responses to `send` (attacker view)
        self.relay_url = None
        self.tap_port = 0
        self._tap = None
        self._http = None
        self.app = Starlette(routes=[Route("/wake/{bot}", self._tap_wake, methods=["POST"])])

    async def _tap_wake(self, request: Request):
        body = await request.body()
        rec = {"bot": request.path_params["bot"], "headers": dict(request.headers), "body": body, "status": None}
        self.captured.append(rec)
        fwd = {k: v for k, v in request.headers.items() if k.startswith("x-mmb-") or k == "content-type"}
        try:
            r = await self._http.post(self.relay_url + request.url.path, content=body, headers=fwd, timeout=10)
        except httpx.HTTPError:
            rec["status"] = 502                    # only while relay and tap are being restarted
            return Response(status_code=502)
        rec["status"] = r.status_code
        return Response(r.content, status_code=r.status_code, media_type="application/json")

    @property
    def url(self):
        """Base URL mmbridge's wake URLs point at (the tap): <url>/wake/<bot>."""
        return "http://127.0.0.1:%d" % self.tap_port

    def configure(self, bots):
        """(Re)start the relay with env for `bots` {name: {"secret", "key"}}; start the tap the first time."""
        if self.relay_url:
            self.relay.stop()
        self.relay_url = self.relay.start(_env(bots, self.routine_base))
        if self._tap is None:
            self._start_tap()

    def _start_tap(self):
        async def go():
            if self._http is None:
                self._http = httpx.AsyncClient()
            return await _serve.start(self.app, self.tap_port)
        server, task, self.tap_port = self.drv._run(go())
        self._tap = (server, task)

    def down(self):
        if self._tap:
            self.drv._run(_serve.stop(*self._tap))
            self._tap = None
        self.relay.stop()

    def up(self):
        self.relay.start()
        self._start_tap()

    def last(self, bot):
        got = [r for r in self.captured if r["bot"] == bot]
        assert got, "no captured wake for %s" % bot
        return got[-1]

    def send(self, bot, body, headers, after_seconds=0.0):
        """POST straight to the relay (not via the tap), `after_seconds` later on the relay's clock."""
        self.relay.offset = float(after_seconds)      # honoured in-process only (module docstring)
        try:
            r = httpx.post("%s/wake/%s" % (self.relay_url, bot), content=body, headers=headers, timeout=10)
        finally:
            self.relay.offset = 0.0
        self.responses.append({"status": r.status_code, "text": r.text, "headers": dict(r.headers)})
        return {"status": r.status_code, "json": r.json() if r.content else None}

    def logs(self):
        return self.relay.logs()

    def close(self):
        try:
            if self._tap:
                self.drv._run(_serve.stop(*self._tap))
            if self._http:
                self.drv._run(self._http.aclose())
        finally:
            self.relay.close()
