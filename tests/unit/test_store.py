import json
import logging
import os
import stat

import pytest
from cryptography.fernet import Fernet

from app import store
from app.store import BotEntry, Store, StoreError

CH = "abcdefghijklmnopqrstuvwxyz"   # 26-char Mattermost id (legacy channels key)
TOKEN = "mmtoken-abcdefghijklmnop-9876"
TOKEN2 = "mmtoken-grokgrokgrokgrok-5432"
SECRET = "s" * 43


def bot(name="eddie", **kw):
    d = dict(token=TOKEN, wake_url="https://wake.example/hook", wake_secret=SECRET, name=name)
    d.update(kw)
    return BotEntry(**d)


def cfg(**kw):
    return Store(bots={"eddie": bot(**kw)})


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
    st = Store(bots={"eddie": bot(user_id="u-eddie", username="eddie"),
                     "grok": bot("grok", token=TOKEN2, wake_url="http://relay:8080/wake/grok", wake_secret="g" * 40)})
    store.save(path, key, st)
    assert store.load(path, key) == st


def test_file_is_ciphertext_mode_0600(path, key):
    store.save(path, key, cfg())
    raw = open(path, "rb").read()
    assert TOKEN.encode() not in raw and SECRET.encode() not in raw and b"wake.example" not in raw
    assert stat.S_IMODE(os.stat(path).st_mode) == 0o600
    assert os.listdir(os.path.dirname(path)) == ["bots.enc"]   # no tmp, no backup for a fresh v2 store


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
    r = repr(cfg()) + str(cfg()) + repr(bot()) + str(bot())
    assert TOKEN not in r and SECRET not in r and "9876" in r


def test_store_error_carries_no_key_material(path, key):
    store.save(path, key, cfg())
    e = _code(store.load, path, Fernet.generate_key().decode())
    assert key not in str(e) and TOKEN not in str(e)


def _write_raw(path, key, obj):
    open(path, "wb").write(Fernet(key.encode()).encrypt(json.dumps(obj).encode()))


def _raw(**b):
    d = {"token": TOKEN, "wake_url": "https://w.example/h", "wake_secret": SECRET}
    d.update(b)
    return d


def _v2(**b):
    d = {"token": TOKEN, "user_id": "", "username": "", "wake": {"url": "https://w.example/h", "secret": SECRET}}
    d.update(b)
    return d


@pytest.mark.parametrize("obj,detail", [
    ({"version": 3, "bots": {}}, "unsupported_version"),
    ({"version": 1, "bot": {k: v for k, v in _raw().items() if k != "token"}}, "token"),
    ({"version": 1, "bot": _raw(wake_secret="short")}, "wake_secret"),
    ({"version": 1, "bot": _raw(wake_url="http://w.example/h")}, "wake_url"),
    ({"version": 1}, "bot"),
    ({"version": 2}, "bots"),
    ({"version": 2, "bots": {"Eddie": _v2()}}, "name"),
    ({"version": 2, "bots": {"-x": _v2()}}, "name"),
    ({"version": 2, "bots": {"a" * 33: _v2()}}, "name"),
    ({"version": 2, "bots": {"eddie": _v2(), "grok": _v2()}}, "token: already used by bot eddie"),
    ({"version": 2, "bots": {"eddie": _v2(user_id="u1"), "grok": _v2(token=TOKEN2, user_id="u1")}}, "user_id"),
    ({"version": 2, "bots": {"eddie": _v2(wake=None)}}, "wake"),
    ({"version": 2, "bots": {"eddie": "x"}}, "bots.eddie"),
    ([1, 2], "format"),
])
def test_load_validates(path, key, obj, detail):
    _write_raw(path, key, obj)
    e = _code(store.load, path, key)
    assert e.code == "store_unreadable" and detail in e.detail


@pytest.mark.parametrize("legacy", [[CH], [], ["town-square"], "not-a-list"])
def test_legacy_channels_key_loads_and_is_ignored(path, key, legacy):
    # pre-lb4b /data/bots.enc files carry a "channels" list; membership is the filter now (delta plan)
    _write_raw(path, key, {"version": 1, "bot": _raw(channels=legacy)})
    st = store.load(path, key)
    assert st.bots == {"bot": BotEntry(token=TOKEN, wake_url="https://w.example/h", wake_secret=SECRET, name="bot")}
    assert not hasattr(st.bots["bot"], "channels")


def test_save_writes_v2_document_without_channels(path, key):
    store.save(path, key, cfg(user_id="u-eddie", username="eddie"))
    doc = json.loads(Fernet(key.encode()).decrypt(open(path, "rb").read()))
    assert doc == {"version": 2, "bots": {"eddie": {"token": TOKEN, "user_id": "u-eddie", "username": "eddie",
                                                    "wake": {"url": "https://wake.example/hook", "secret": SECRET}}}}


# --- B-s3 v1 -> v2 migration (ADR-0013) ----------------------------------------------
def test_v1_loads_as_one_named_bot_and_first_save_keeps_v1_backup(path, key):
    _write_raw(path, key, {"version": 1, "bot": _raw(channels=[CH])})
    v1_blob = open(path, "rb").read()
    st = store.load(path, key)
    assert st.migrated_from == 1 and list(st.bots) == ["bot"]
    store.rename_v1(st, "Eddie.Bot", "u-eddie")
    assert list(st.bots) == ["eddie-bot"] and st.bots["eddie-bot"].user_id == "u-eddie"
    store.save(path, key, st)
    bak = store.backup_path(path)
    assert open(bak, "rb").read() == v1_blob                          # rollback file = the v0.3.0 store
    assert stat.S_IMODE(os.stat(bak).st_mode) == 0o600
    assert json.loads(Fernet(key.encode()).decrypt(open(bak, "rb").read()))["version"] == 1
    again = store.load(path, key)
    assert again.migrated_from is None and list(again.bots) == ["eddie-bot"]
    assert again.bots["eddie-bot"].token == TOKEN
    st2 = store.load(path, key)                                       # later saves never touch the backup
    st2.bots["grok"] = bot("grok", token=TOKEN2)
    store.save(path, key, st2)
    assert open(bak, "rb").read() == v1_blob


def test_v1_load_name_fallback_and_rename_rules():
    assert store.name_from_username("eddie") == "eddie"
    assert store.name_from_username("Grok_Bot") == "grok-bot"
    assert store.name_from_username(None) == "bot" and store.name_from_username("___") == "bot"
    assert store.name_from_username("x" * 40) == "x" * 32
    st = Store(bots={"bot": bot("bot")}, migrated_from=1)
    store.rename_v1(st, None)
    assert list(st.bots) == ["bot"]
    v2 = cfg()
    assert store.rename_v1(v2, "other") is v2 and list(v2.bots) == ["eddie"]   # v2: no-op


def test_legacy_owner_maps_v1_rows_to_the_right_bot():
    st = Store(bots={"eddie": bot(user_id="u-eddie"), "grok": bot("grok", token=TOKEN2, user_id="u-grok")})
    owner = store.legacy_owner(st)
    assert owner("u-grok") == "grok" and owner("u-eddie") == "eddie" and owner(None) == "bot"
    assert store.legacy_owner(cfg())("u-unknown") == "eddie"
    assert store.legacy_owner(Store())(None) == "bot"


@pytest.mark.parametrize("change,detail", [
    (dict(token=TOKEN), "token: already used by bot eddie"),
    (dict(user_id="u-eddie"), "user_id: same Mattermost user as bot eddie"),
])
def test_save_rejects_duplicate_token_or_user(path, key, change, detail):
    st = Store(bots={"eddie": bot(user_id="u-eddie"), "grok": bot("grok", **{"token": TOKEN2, **change})})
    e = _code(store.save, path, key, st)
    assert e.code == "store_invalid" and detail in e.detail and not os.path.exists(path)


@pytest.mark.parametrize("name", ["Eddie", "-eddie", "ed die", "a" * 33, ""])
def test_save_rejects_bad_names(path, key, name):
    e = _code(store.save, path, key, Store(bots={name: bot(name)}))
    assert e.code == "store_invalid" and "name" in e.detail


def test_http_wake_allowed_only_with_test_flag(path, key, monkeypatch):
    _write_raw(path, key, {"version": 1, "bot": _raw(wake_url="http://w.example/h")})
    monkeypatch.setenv("LIVE_ALLOW_HTTP_WAKE", "true")
    assert store.load(path, key).bots["bot"].wake_url == "http://w.example/h"


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


def test_rotate_covers_v2_and_the_v1_backup(path):
    old, new = Fernet.generate_key().decode(), Fernet.generate_key().decode()
    _write_raw(path, old, {"version": 1, "bot": _raw()})
    st = store.load(path, old)
    st.bots["grok"] = bot("grok", token=TOKEN2)
    store.save(path, old, st)
    store.rotate(path, new, old)
    assert sorted(store.load(path, new).bots) == ["bot", "grok"]
    bak = json.loads(Fernet(new.encode()).decrypt(open(store.backup_path(path), "rb").read()))
    assert bak["version"] == 1 and bak["bot"]["token"] == TOKEN       # rollback file readable with the new key
    assert stat.S_IMODE(os.stat(store.backup_path(path)).st_mode) == 0o600


def test_rotate_with_wrong_old_key_leaves_file(path):
    old, new = Fernet.generate_key().decode(), Fernet.generate_key().decode()
    store.save(path, old, cfg())
    before = open(path, "rb").read()
    assert _code(store.rotate, path, new, Fernet.generate_key().decode()).code == "store_unreadable"
    assert open(path, "rb").read() == before


# --- REQ-A7: redaction of the stored token/secret in logs ---------------------------
def test_loaded_tokens_and_secrets_of_all_bots_redacted_in_logs(path, key, caplog):
    from app import logging as mlog
    mlog.setup()
    store.save(path, key, Store(bots={"eddie": bot(), "grok": bot("grok", token=TOKEN2, wake_secret="g" * 40)}))
    store.load(path, key)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        mlog.log.info("oops token=%s secret=%s token2=%s secret2=%s", TOKEN, SECRET, TOKEN2, "g" * 40)
    assert TOKEN not in caplog.text and SECRET not in caplog.text and "[REDACTED]" in caplog.text
    assert TOKEN2 not in caplog.text and "g" * 40 not in caplog.text


def test_https_ok_rejects_unparseable_urls():
    """Review 4 P2: admin set-bot refuses a wake URL the dispatcher could not send to."""
    from app.store import https_ok
    assert https_ok("https://example.org/wake") and https_ok("https://example.org:8443/wake")
    for bad in ("https://example.org:bad/wake", "https://", "https://:443/x", "https://example.org:99999/x"):
        assert not https_ok(bad), bad


# --- http wake only for in-stack internal hosts (Rob 2026-10-30 "Tighten now") -------------------
import pytest as _pt


@_pt.mark.parametrize("url", ["https://w.example/h", "https://relay:8443/x"])
def test_https_wake_always_ok(url, monkeypatch):
    monkeypatch.delenv("LIVE_ALLOW_HTTP_WAKE", raising=False)
    assert store.https_ok(url)


@_pt.mark.parametrize("flag", [None, "false"])
@_pt.mark.parametrize("url", ["http://relay:8080/wake/eddie", "http://RELAY:8080/wake/eddie", "http://relay/wake/x"])
def test_http_wake_internal_relay_ok_without_flag(url, flag, monkeypatch):
    if flag is None:
        monkeypatch.delenv("LIVE_ALLOW_HTTP_WAKE", raising=False)
    else:
        monkeypatch.setenv("LIVE_ALLOW_HTTP_WAKE", flag)
    assert store.https_ok(url)


@_pt.mark.parametrize("url", ["http://evil.example/h", "http://relay.evil.example/h", "http://relayx:8080/h",
                              "http://127.0.0.1:9000/h", "http://localhost/h", "http://8.8.8.8/h",
                              "http://evil.example/relay:8080", "http://relay@evil.example/h"])
def test_http_wake_public_or_other_host_rejected_without_flag(url, monkeypatch):
    monkeypatch.delenv("LIVE_ALLOW_HTTP_WAKE", raising=False)
    assert not store.https_ok(url)


def test_set_bot_validation_accepts_relay_rejects_public_http(monkeypatch):
    monkeypatch.delenv("LIVE_ALLOW_HTTP_WAKE", raising=False)
    store.validate(cfg(wake_url="http://relay:8080/wake/eddie"))
    with _pt.raises(ValueError):
        store.validate(cfg(wake_url="http://evil.example/wake"))


def test_test_flag_still_allows_local_receiver(monkeypatch):
    monkeypatch.setenv("LIVE_ALLOW_HTTP_WAKE", "true")      # acceptance driver's 127.0.0.1 receiver
    assert store.https_ok("http://127.0.0.1:9000/h")
