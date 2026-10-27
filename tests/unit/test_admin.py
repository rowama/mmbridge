import io
import logging
import os

import pytest
from cryptography.fernet import Fernet

from app import admin, store
from drivers.fake_mattermost import FakeMattermost

TOWN = "townsquareid0000000000000a"   # 26-char ids, as real Mattermost uses
DEV = "devchannelid00000000000000"
OPS = "opschannelid00000000000000"


def _reid(mm, cid, new):
    c = mm.channels.pop(cid)
    c["id"] = new
    mm.channels[new] = c


@pytest.fixture
def mm():
    m = FakeMattermost()
    m.add_user("eddie", bot=True)
    m.add_user("ada", bot=True)
    _reid(m, m.add_channel("main", "town-square", ["eddie"]), TOWN)
    _reid(m, m.add_channel("main", "dev", ["eddie"], ctype="P"), DEV)
    _reid(m, m.add_channel("main", "ops", ["ada"]), OPS)
    return m


@pytest.fixture
def env(tmp_path, monkeypatch):
    key = Fernet.generate_key().decode()
    monkeypatch.setenv("MMB_STORE_KEY", key)
    monkeypatch.setenv("MMB_DATA_DIR", str(tmp_path))
    monkeypatch.delenv("LIVE_ALLOW_HTTP_WAKE", raising=False)
    return {"key": key, "path": str(tmp_path / "bots.enc")}


def run(mm, *argv, stdin=""):
    out = io.StringIO()
    rc = admin.main(list(argv), stdin=io.StringIO(stdin), stdout=out, transport=mm.transport())
    return rc, out.getvalue()


def tok(mm, name="eddie"):
    return mm.user_by_name(name)["token"]


def set_bot(mm, channels="main/town-square,main/dev", url="https://wake.example/hook", stdin=None):
    return run(mm, "set-bot", "--token-stdin", "--wake-url", url, "--channels", channels,
               stdin=stdin if stdin is not None else tok(mm) + "\n")


def test_set_bot_stores_resolved_ids_and_prints_secret_once(mm, env, caplog):
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        rc, out = set_bot(mm)
    assert rc == 0, out
    cfg = store.load(env["path"], env["key"])
    assert cfg.token == tok(mm) and cfg.channels == [TOWN, DEV] and cfg.wake_url == "https://wake.example/hook"
    assert len(cfg.wake_secret) >= 32 and out.count(cfg.wake_secret) == 1
    assert tok(mm) not in out and tok(mm) not in caplog.text and cfg.wake_secret not in caplog.text
    assert "store_updated" in caplog.text
    for f in ("token", "wake_url", "wake_secret", "channels"):
        assert f in caplog.text
    assert not [c for c in mm.changes]   # never joins / changes the world


def test_show_masks_token_never_prints_secret(mm, env):
    set_bot(mm)
    cfg = store.load(env["path"], env["key"])
    rc, out = run(mm, "show")
    assert rc == 0
    assert tok(mm) not in out and cfg.wake_secret not in out
    assert tok(mm)[-4:] in out and TOWN in out and DEV in out and "https://wake.example/hook" in out


def test_non_member_channel_refused_without_join(mm, env):
    rc, out = set_bot(mm, channels="main/town-square,main/ops")
    assert rc != 0 and "not_member" in out
    assert not os.path.exists(env["path"])
    assert not [c for c in mm.calls if c[0] == "POST"] and mm.changes == []


def test_unknown_channel_refused(mm, env):
    rc, out = set_bot(mm, channels="main/nope")
    assert rc != 0 and "unknown_channel" in out and not os.path.exists(env["path"])


@pytest.mark.parametrize("ch", ["town-square", "main/", "/x", "a/b/c", ""])
def test_bad_channel_spec_refused(mm, env, ch):
    rc, out = set_bot(mm, channels=ch)
    assert rc != 0 and not os.path.exists(env["path"])


def test_http_wake_url_refused(mm, env):
    rc, out = set_bot(mm, url="http://wake.example/hook")
    assert rc != 0 and "https" in out and not os.path.exists(env["path"])
    assert mm.calls == []   # refused before touching Mattermost


def test_http_wake_url_allowed_with_test_flag(mm, env, monkeypatch):
    monkeypatch.setenv("LIVE_ALLOW_HTTP_WAKE", "true")
    rc, out = set_bot(mm, url="http://wake.example/hook")
    assert rc == 0, out


def test_bad_token_refused(mm, env):
    rc, out = set_bot(mm, stdin="wrong-token-xxxxxxxxxxxx\n")
    assert rc != 0 and "unauthorized" in out and "wrong-token" not in out
    assert not os.path.exists(env["path"])


def test_missing_key_refused(mm, env, monkeypatch):
    monkeypatch.delenv("MMB_STORE_KEY")
    rc, out = set_bot(mm)
    assert rc != 0 and "store_key_missing" in out and not os.path.exists(env["path"])


def test_supplied_wake_secret(mm, env):
    secret = "k" * 40
    rc, out = run(mm, "set-bot", "--token-stdin", "--wake-secret-stdin", "--wake-url", "https://w.example/h",
                  "--channels", "main/town-square", stdin="%s\n%s\n" % (tok(mm), secret))
    assert rc == 0, out
    assert store.load(env["path"], env["key"]).wake_secret == secret and secret not in out


def test_short_wake_secret_refused(mm, env):
    rc, out = run(mm, "set-bot", "--token-stdin", "--wake-secret-stdin", "--wake-url", "https://w.example/h",
                  "--channels", "main/town-square", stdin="%s\n%s\n" % (tok(mm), "k" * 31))
    assert rc != 0 and "wake_secret" in out and not os.path.exists(env["path"])


def test_show_without_store(mm, env):
    rc, out = run(mm, "show")
    assert rc != 0 and "store_unreadable" in out


def test_show_wrong_key(mm, env, monkeypatch):
    set_bot(mm)
    monkeypatch.setenv("MMB_STORE_KEY", Fernet.generate_key().decode())
    rc, out = run(mm, "show")
    assert rc != 0 and "store_unreadable" in out and tok(mm) not in out


def test_rotate_key_cli(mm, env, monkeypatch):
    set_bot(mm)
    new = Fernet.generate_key().decode()
    monkeypatch.setenv("NEWK", new)
    rc, out = run(mm, "rotate-key", "--new-key-env", "NEWK", "--old-key-env", "MMB_STORE_KEY")
    assert rc == 0, out
    assert new not in out and env["key"] not in out
    assert store.load(env["path"], new).token == tok(mm)


def test_rotate_key_missing_env(mm, env):
    set_bot(mm)
    rc, out = run(mm, "rotate-key", "--new-key-env", "NOPE_UNSET", "--old-key-env", "MMB_STORE_KEY")
    assert rc != 0 and "store_key_missing" in out
