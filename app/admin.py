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
