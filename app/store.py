"""Encrypted store of the live bots' config (ADR-0006, v2 ADR-0013): per named bot its Mattermost token, wake URL and
wake secret, plus the non-secret cached user id / username. No channel list: Mattermost membership decides which
channel posts can wake a bot (delta plan 2026-10-27).

/data/bots.enc is the Fernet ciphertext of {"version": 2, "bots": {"<name>": {"token", "user_id", "username",
"wake": {"url", "secret"}}}}, mode 0600, written atomically. Names match NAME_RE; tokens (and known user ids) are
unique across bots. A v1 document {"version": 1, "bot": {...}} loads as one bot (name `v1_name`, default "bot";
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
            "wake": {"url": b.wake_url, "secret": b.wake_secret}} for n, b in st.bots.items()}}).encode()


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
