"""OQ1 spike (slice lb3 manual check): print the shape of Mattermost's websocket hello, ping reply and first
`posted` event, to confirm the listener's contract against the real server version.

    echo "$TOKEN" | python -m app.ws_spike [--timeout 120]

Token from stdin only, never printed. Output is key -> type shapes plus seq/channel_type/connection_id;
message text is not printed.
"""
import argparse
import asyncio
import json
import sys

from app import logging as mlog
from app.listener import connect, ws_url
from app.mattermost import MATTERMOST_URL


def shape(v):
    if isinstance(v, dict):
        return {k: shape(x) for k, x in sorted(v.items())}
    return type(v).__name__


async def spike(token: str, base_url: str, timeout: float, out=print, ws_connect=connect) -> int:
    async with ws_connect(ws_url(base_url), {"Authorization": "Bearer " + token}) as ws:
        hello = json.loads(await asyncio.wait_for(ws.recv(), 10))
        out("hello: event=%s seq=%s connection_id=%s server_version=%s" % (
            hello.get("event"), hello.get("seq"), bool((hello.get("data") or {}).get("connection_id")),
            (hello.get("data") or {}).get("server_version")))
        out("hello shape: " + json.dumps(shape(hello)))
        await ws.send(json.dumps({"action": "ping", "seq": 1}))
        out("waiting up to %ds for a post in any channel the bot is in ..." % timeout)
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout
        while (left := deadline - loop.time()) > 0:
            try:
                ev = json.loads(await asyncio.wait_for(ws.recv(), left))
            except TimeoutError:
                break
            if "seq_reply" in ev:
                out("ping reply shape: " + json.dumps(shape(ev)))
            elif ev.get("event") == "posted":
                data = dict(ev["data"])
                post = json.loads(data["post"]) if isinstance(data.get("post"), str) else data.get("post")
                data["post"] = "<json string>" if isinstance(ev["data"].get("post"), str) else "<object>"
                out("posted: seq=%s channel_type=%s" % (ev.get("seq"), data.get("channel_type")))
                out("posted shape: " + json.dumps(shape({**ev, "data": data})))
                out("post shape: " + json.dumps(shape(post)))
                return 0
            else:
                out("other event: %s seq=%s" % (ev.get("event"), ev.get("seq")))
    out("no posted event within %ds" % timeout)
    return 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="python -m app.ws_spike")
    p.add_argument("--timeout", type=float, default=120)
    a = p.parse_args(argv)
    token = sys.stdin.readline().strip()
    if not token:
        print("token required on stdin", file=sys.stderr)
        return 2
    mlog.setup()
    mlog.register_secret(token)
    return asyncio.run(spike(token, MATTERMOST_URL, a.timeout))


if __name__ == "__main__":
    sys.exit(main())
