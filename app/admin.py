"""Operator CLI for the live bot (ADR-0006/0009): `python -m app.admin set-bot | show | rotate-key | failed | stats`.

Run inside the container (Coolify terminal). The token is read from stdin only and never printed or logged;
the wake secret is printed once when generated, never by `show`. Channels are resolved by name to ids with the
bot's own token and must already include the bot (REQ-7: never joins). `failed`/`stats` read state.db and
never print message text.
"""
import argparse
import asyncio
import json
import os
import secrets
import sys
import time

from app import logging as mlog
from app import state, store
from app.errors import ToolError
from app.mattermost import MATTERMOST_URL, Client, MMError
from app.service import _member_channel
from app.validate import identifier

FIELDS = ("token", "wake_url", "wake_secret", "channels")


class AdminError(Exception):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(code)
        self.code, self.detail = code, detail


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m app.admin", description="mmbridge live bot admin")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("set-bot", help="store the bot token, wake URL and channels (token read from stdin)")
    s.add_argument("--token-stdin", action="store_true", required=True, help="read the bot token from stdin")
    s.add_argument("--wake-secret-stdin", action="store_true",
                   help="read the wake secret from the next stdin line instead of generating one")
    s.add_argument("--wake-url", required=True)
    s.add_argument("--channels", default=None, help="team/channel,team/channel,... (omit for a DM-only bot)")
    sub.add_parser("show", help="show the stored config (token masked, secret hidden)")
    r = sub.add_parser("rotate-key", help="re-encrypt the store with a new MMB_STORE_KEY")
    r.add_argument("--new-key-env", default="MMB_STORE_KEY_NEW", help="env var holding the new key")
    r.add_argument("--old-key-env", default="MMB_STORE_KEY", help="env var holding the current key(s)")
    f = sub.add_parser("failed", help="list failed wakes, or requeue one")
    f.add_argument("--retry", metavar="POST_ID", help="requeue this failed wake for delivery")
    sub.add_parser("stats", help="wake counts and post->delivered latency")
    return p


def _channel_specs(raw: str) -> list[tuple[str, str]]:
    out = []
    for item in raw.split(","):
        parts = item.strip().split("/")
        if len(parts) != 2:
            raise AdminError("invalid_argument", "channels must be team/channel,... (got %r)" % item.strip())
        try:
            out.append((identifier("team", parts[0]), identifier("channel", parts[1])))
        except ToolError as e:
            raise AdminError("invalid_argument", e.message) from None
    return out


async def _resolve(token: str, specs: list[tuple[str, str]], transport) -> tuple[str, list[str]]:
    c = Client(token, MATTERMOST_URL, transport=transport)
    try:
        me = await c.get("/users/me")
        ids = []
        for team, channel in specs:
            ids.append((await _member_channel(c, team, channel))["id"])
    except ToolError as e:
        raise AdminError(e.code, e.message) from None
    except MMError as e:
        detail = "Mattermost rejected the bot token" if e.code == "unauthorized" else ""
        raise AdminError(e.code, detail) from None
    return me["username"], list(dict.fromkeys(ids))


def _set_bot(a, stdin, out, transport) -> None:
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
    specs = [] if a.channels is None else _channel_specs(a.channels)
    key = os.getenv("MMB_STORE_KEY")
    if not (key or "").strip():
        raise store.StoreError("store_key_missing")
    username, ids = asyncio.run(_resolve(token, specs, transport))
    path = store.path_from_env()
    try:
        prev = store.load(path, key)
    except store.StoreError:
        prev = None
    cfg = store.BotConfig(token=token, wake_url=a.wake_url, wake_secret=secret, channels=ids)
    store.save(path, key, cfg)
    changed = [f for f in FIELDS if prev is None or getattr(prev, f) != getattr(cfg, f)]
    mlog.log.info(json.dumps({"event": "store_updated", "fields": changed}))
    print("bot @%s stored: wake_url %s, channels %s" % (username, cfg.wake_url, ",".join(ids)), file=out)
    if not supplied:
        print("wake secret (shown once; give it to the receiver): %s" % secret, file=out)


def _show(out) -> None:
    cfg = store.load(store.path_from_env(), os.getenv("MMB_STORE_KEY"))
    print("version: %d\ntoken: ****%s\nwake_url: %s\nwake_secret: set (hidden)\nchannels: %s" % (
        cfg.version, cfg.token[-4:], cfg.wake_url, ",".join(cfg.channels)), file=out)


def _rotate_key(a, out) -> None:
    store.rotate(store.path_from_env(), os.getenv(a.new_key_env), os.getenv(a.old_key_env))
    mlog.log.info(json.dumps({"event": "store_updated", "fields": ["key"]}))
    print("store re-encrypted with %s; set MMB_STORE_KEY to that key" % a.new_key_env, file=out)


def _failed(a, out) -> None:
    st = state.State(state.path_from_env())
    if a.retry:
        if not st.requeue(a.retry):
            raise AdminError("not_found", "no failed wake %s" % a.retry)
        mlog.log.info(json.dumps({"event": "wake_requeued", "post_id": a.retry}))
        print("requeued %s" % a.retry, file=out)
        return
    rows = st.failed()
    if not rows:
        print("no failed wakes", file=out)
    for w in rows:
        at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(w.updated_at))
        print("%s  channel %s  attempts %d  error %s  at %s" % (w.post_id, w.channel_id, w.attempts,
                                                              w.last_error or "-", at), file=out)


def _stats(out) -> None:
    s = state.State(state.path_from_env()).stats()
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
        elif a.cmd == "show":
            _show(out)
        elif a.cmd == "rotate-key":
            _rotate_key(a, out)
        elif a.cmd == "failed":
            _failed(a, out)
        else:
            _stats(out)
    except (AdminError, store.StoreError, state.StateError) as e:
        print("error: %s%s" % (e.code, ": " + e.detail if e.detail else ""), file=out)
        return 1
    except OSError as e:
        print("error: store_unwritable: %s" % e.strerror, file=out)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
