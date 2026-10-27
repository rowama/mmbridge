import logging
import os
import stat

import pytest
from cryptography.fernet import Fernet

from app import store
from app.store import BotConfig, StoreError

CH = "abcdefghijklmnopqrstuvwxyz"   # 26-char Mattermost id
TOKEN = "mmtoken-abcdefghijklmnop-9876"
SECRET = "s" * 43


def cfg(**kw):
    d = dict(token=TOKEN, wake_url="https://wake.example/hook", wake_secret=SECRET, channels=[CH])
    d.update(kw)
    return BotConfig(**d)


@pytest.fixture
def key():
    return Fernet.generate_key().decode()


@pytest.fixture
def path(tmp_path):
    return str(tmp_path / "bots.enc")


def _code(fn, *a):
    with pytest.raises(StoreError) as e:
        fn(*a)
    return e.value


def test_roundtrip(path, key):
    store.save(path, key, cfg())
    assert store.load(path, key) == cfg()


def test_file_is_ciphertext_mode_0600(path, key):
    store.save(path, key, cfg())
    raw = open(path, "rb").read()
    assert TOKEN.encode() not in raw and SECRET.encode() not in raw and b"wake.example" not in raw
    assert stat.S_IMODE(os.stat(path).st_mode) == 0o600
    assert os.listdir(os.path.dirname(path)) == ["bots.enc"]   # no tmp left behind


def test_wrong_key_unreadable(path, key):
    store.save(path, key, cfg())
    assert _code(store.load, path, Fernet.generate_key().decode()).code == "store_unreadable"


@pytest.mark.parametrize("k", [None, "", "  "])
def test_missing_key(path, key, k):
    store.save(path, key, cfg())
    assert _code(store.load, path, k).code == "store_key_missing"


def test_malformed_key_unreadable(path, key):
    store.save(path, key, cfg())
    assert _code(store.load, path, "not-a-fernet-key").code == "store_unreadable"


def test_missing_file_unreadable(path, key):
    assert _code(store.load, path, key).code == "store_unreadable"


def test_tamper_unreadable(path, key):
    store.save(path, key, cfg())
    raw = bytearray(open(path, "rb").read())
    raw[40] = ord("A") if raw[40] != ord("A") else ord("B")
    open(path, "wb").write(bytes(raw))
    assert _code(store.load, path, key).code == "store_unreadable"


def test_repr_masks_token_and_secret():
    r = repr(cfg()) + str(cfg())
    assert TOKEN not in r and SECRET not in r and "9876" in r


def test_store_error_carries_no_key_material(path, key):
    store.save(path, key, cfg())
    e = _code(store.load, path, Fernet.generate_key().decode())
    assert key not in str(e) and TOKEN not in str(e)


def _write_raw(path, key, obj):
    import json
    open(path, "wb").write(Fernet(key.encode()).encrypt(json.dumps(obj).encode()))


def _raw(**bot):
    b = {"token": TOKEN, "wake_url": "https://w.example/h", "wake_secret": SECRET, "channels": [CH]}
    b.update(bot)
    return b


@pytest.mark.parametrize("obj,detail", [
    ({"version": 2, "bot": _raw()}, "unsupported_version"),
    ({"version": 1, "bot": {k: v for k, v in _raw().items() if k != "token"}}, "token"),
    ({"version": 1, "bot": _raw(wake_secret="short")}, "wake_secret"),
    ({"version": 1, "bot": _raw(wake_url="http://w.example/h")}, "wake_url"),
    ({"version": 1, "bot": _raw(channels=["town-square"])}, "channels"),
    ({"version": 1}, "bot"),
    ([1, 2], "format"),
])
def test_load_validates(path, key, obj, detail):
    _write_raw(path, key, obj)
    e = _code(store.load, path, key)
    assert e.code == "store_unreadable" and detail in e.detail


def test_empty_channel_list_is_a_dm_only_bot(path, key):
    _write_raw(path, key, {"version": 1, "bot": _raw(channels=[])})
    assert store.load(path, key).channels == []


def test_http_wake_allowed_only_with_test_flag(path, key, monkeypatch):
    _write_raw(path, key, {"version": 1, "bot": _raw(wake_url="http://w.example/h")})
    monkeypatch.setenv("LIVE_ALLOW_HTTP_WAKE", "true")
    assert store.load(path, key).wake_url == "http://w.example/h"


def test_save_validates_and_writes_nothing(path, key):
    e = _code(store.save, path, key, cfg(wake_secret="x" * 31))
    assert e.code == "store_invalid" and not os.path.exists(path)


# --- PR-7 key rotation (MultiFernet, ADR-0006) -------------------------------------
def test_rotate_key_roundtrip(path):
    old, new = Fernet.generate_key().decode(), Fernet.generate_key().decode()
    store.save(path, old, cfg())
    assert store.load(path, "%s,%s" % (new, old)) == cfg()       # MMB_STORE_KEY=new,old reads old file
    store.rotate(path, new, old)
    assert store.load(path, new) == cfg()
    assert _code(store.load, path, old).code == "store_unreadable"
    assert stat.S_IMODE(os.stat(path).st_mode) == 0o600


def test_rotate_with_wrong_old_key_leaves_file(path):
    old, new = Fernet.generate_key().decode(), Fernet.generate_key().decode()
    store.save(path, old, cfg())
    before = open(path, "rb").read()
    assert _code(store.rotate, path, new, Fernet.generate_key().decode()).code == "store_unreadable"
    assert open(path, "rb").read() == before


# --- REQ-A7: redaction of the stored token/secret in logs ---------------------------
def test_loaded_token_and_secret_redacted_in_logs(path, key, caplog):
    from app import logging as mlog
    mlog.setup()
    store.save(path, key, cfg())
    store.load(path, key)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        mlog.log.info("oops token=%s secret=%s", TOKEN, SECRET)
    assert TOKEN not in caplog.text and SECRET not in caplog.text and "[REDACTED]" in caplog.text


def test_https_ok_rejects_unparseable_urls():
    """Review 4 P2: admin set-bot refuses a wake URL the dispatcher could not send to."""
    from app.store import https_ok
    assert https_ok("https://example.org/wake") and https_ok("https://example.org:8443/wake")
    for bad in ("https://example.org:bad/wake", "https://", "https://:443/x", "https://example.org:99999/x"):
        assert not https_ok(bad), bad
