"""Encrypted store for the ONE live bot's config (ADR-0006): token, wake URL, wake secret, channel ids.

/data/bots.enc is the Fernet ciphertext of {"version": 1, "bot": {...}}, mode 0600, written atomically.
Key from env MMB_STORE_KEY; "new,old" is accepted (MultiFernet) for key rotation. Errors never carry
key material, token or secret. Loaded/saved token and secret are registered with the log redact filter.
"""
import httpx
import json
import os
import re
import tempfile
from dataclasses import dataclass

from cryptography.fernet import Fernet, InvalidToken, MultiFernet

from app import logging as mlog

VERSION = 1
MIN_SECRET = 32
_CHANNEL_ID = re.compile(r"[a-z0-9]{26}")


def path_from_env() -> str:
    return os.path.join(os.getenv("MMB_DATA_DIR", "/data"), "bots.enc")


class StoreError(Exception):
    """code: store_key_missing | store_unreadable | store_invalid (save-time validation). detail: field/reason."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__("%s: %s" % (code, detail) if detail else code)
        self.code, self.detail = code, detail


def _mask(s: str) -> str:
    return "****" + s[-4:] if len(s) > 8 else "****"


@dataclass
class BotConfig:
    token: str
    wake_url: str
    wake_secret: str
    channels: list[str]
    version: int = VERSION

    def __repr__(self) -> str:  # never show token or secret
        return "BotConfig(token=%s, wake_url=%r, wake_secret=****, channels=%r, version=%d)" % (
            _mask(self.token), self.wake_url, self.channels, self.version)

    __str__ = __repr__


def validate(cfg: BotConfig) -> None:
    """Raise ValueError(<field>: <reason>) unless cfg is a valid version-1 config (plan PR-6)."""
    if cfg.version != VERSION:
        raise ValueError("unsupported_version")
    for f in ("token", "wake_url", "wake_secret"):
        if not isinstance(getattr(cfg, f), str) or not getattr(cfg, f).strip():
            raise ValueError("%s: required" % f)
    if not https_ok(cfg.wake_url):
        raise ValueError("wake_url: must be https")
    if len(cfg.wake_secret) < MIN_SECRET:
        raise ValueError("wake_secret: must be at least %d characters" % MIN_SECRET)
    if (not isinstance(cfg.channels, list)
            or not all(isinstance(c, str) and _CHANNEL_ID.fullmatch(c) for c in cfg.channels)):
        raise ValueError("channels: must be a list of 26-char channel ids (empty = DMs only)")


def https_ok(url: str) -> bool:
    try:                                   # must also parse as the dispatcher will send it (review 4 P2)
        u = httpx.URL(url)
        if not u.host or (u.port is not None and not 0 < u.port < 65536):
            return False
    except (httpx.InvalidURL, ValueError, TypeError):
        return False
    if url.startswith("https://") and len(url) > 8:
        return True
    return os.getenv("LIVE_ALLOW_HTTP_WAKE", "").lower() == "true" and url.startswith("http://") and len(url) > 7


def _keys(key: str | None) -> list[Fernet]:
    keys = [k.strip() for k in (key or "").split(",") if k.strip()]
    if not keys:
        raise StoreError("store_key_missing")
    try:
        return [Fernet(k.encode()) for k in keys]
    except (ValueError, TypeError):
        raise StoreError("store_unreadable", "bad_key") from None


def _decode(plain: bytes) -> BotConfig:
    try:
        doc = json.loads(plain)
    except ValueError:
        raise StoreError("store_unreadable", "format") from None
    if not isinstance(doc, dict):
        raise StoreError("store_unreadable", "format")
    if doc.get("version") != VERSION:
        raise StoreError("store_unreadable", "unsupported_version")
    bot = doc.get("bot")
    if not isinstance(bot, dict):
        raise StoreError("store_unreadable", "bot: required")
    try:
        cfg = BotConfig(token=bot.get("token"), wake_url=bot.get("wake_url"), wake_secret=bot.get("wake_secret"),
                        channels=bot.get("channels"), version=doc["version"])
        validate(cfg)
    except ValueError as e:
        raise StoreError("store_unreadable", str(e)) from None
    return cfg


def _read(path: str, f: MultiFernet) -> tuple[bytes, BotConfig]:
    try:
        with open(path, "rb") as fh:
            blob = fh.read()
    except OSError:
        raise StoreError("store_unreadable", "file") from None
    try:
        plain = f.decrypt(blob)
    except InvalidToken:
        raise StoreError("store_unreadable", "decrypt") from None
    cfg = _decode(plain)
    _register(cfg)
    return blob, cfg


def _register(cfg: BotConfig) -> None:
    mlog.register_secret(cfg.token)
    mlog.register_secret(cfg.wake_secret)


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


def load(path: str, key: str | None) -> BotConfig:
    return _read(path, MultiFernet(_keys(key)))[1]


def save(path: str, key: str | None, cfg: BotConfig) -> None:
    f = MultiFernet(_keys(key))
    try:
        validate(cfg)
    except ValueError as e:
        raise StoreError("store_invalid", str(e)) from None
    _register(cfg)
    doc = {"version": cfg.version, "bot": {"token": cfg.token, "wake_url": cfg.wake_url,
                                           "wake_secret": cfg.wake_secret, "channels": list(cfg.channels)}}
    _write(path, f.encrypt(json.dumps(doc).encode()))


def rotate(path: str, new_key: str | None, old_key: str | None) -> None:
    """Re-encrypt the store with the first new key (readable with new or old keys); validated first; atomic, 0600."""
    f = MultiFernet(_keys(new_key) + _keys(old_key))
    blob, _ = _read(path, f)
    _write(path, f.rotate(blob))
