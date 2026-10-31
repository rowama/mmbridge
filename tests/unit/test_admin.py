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


def only(st):
    (b,) = st.bots.values()
    return b


def set_bot(mm, url="https://wake.example/hook", stdin=None):
    return run(mm, "set-bot", "--token-stdin", "--wake-url", url,
               stdin=stdin if stdin is not None else tok(mm) + "\n")


def test_set_bot_stores_resolved_ids_and_prints_secret_once(mm, env, caplog):
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        rc, out = set_bot(mm)
    assert rc == 0, out
    cfg = only(store.load(env["path"], env["key"]))
    assert cfg.token == tok(mm) and cfg.wake_url == "https://wake.example/hook"
    assert len(cfg.wake_secret) >= 32 and out.count(cfg.wake_secret) == 1
    assert tok(mm) not in out and tok(mm) not in caplog.text and cfg.wake_secret not in caplog.text
    assert "store_updated" in caplog.text
    for f in ("token", "wake_url", "wake_secret"):
        assert f in caplog.text
    assert "channels" not in caplog.text and "channels" not in out
    assert "bot eddie (@eddie) stored: wake_url https://wake.example/hook" in out
    assert not [c for c in mm.changes]   # never joins / changes the world
    assert [c for c in mm.calls if "/channels" in c[1]] == []   # no channel lookups: membership is the filter


def test_show_masks_token_never_prints_secret(mm, env):
    set_bot(mm)
    cfg = only(store.load(env["path"], env["key"]))
    rc, out = run(mm, "show")
    assert rc == 0
    assert tok(mm) not in out and cfg.wake_secret not in out
    assert tok(mm)[-4:] in out and "https://wake.example/hook" in out
    assert "channels" not in out and TOWN not in out


@pytest.mark.parametrize("ch", ["main/town-square", "main/ops", ""])
def test_channels_option_refused_as_no_longer_used(mm, env, ch):
    rc, out = run(mm, "set-bot", "--token-stdin", "--wake-url", "https://wake.example/hook", "--channels", ch,
                  stdin=tok(mm) + "\n")
    assert rc != 0 and "invalid_argument: channels no longer used" in out
    assert not os.path.exists(env["path"])
    assert mm.calls == [] and mm.changes == []   # refused before touching Mattermost


def test_set_bot_keeps_legacy_store_loadable_and_drops_channels(mm, env):
    import json
    open(env["path"], "wb").write(Fernet(env["key"].encode()).encrypt(json.dumps({"version": 1, "bot": {
        "token": "old-token-xxxxxxxx", "wake_url": "https://old.example/h", "wake_secret": "o" * 40,
        "channels": [TOWN]}}).encode()))
    rc, out = run(mm, "show")
    assert rc == 0 and "https://old.example/h" in out and TOWN not in out
    rc, out = set_bot(mm)
    assert rc == 0, out
    assert TOWN.encode() not in Fernet(env["key"].encode()).decrypt(open(env["path"], "rb").read())


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
                  stdin="%s\n%s\n" % (tok(mm), secret))
    assert rc == 0, out
    assert only(store.load(env["path"], env["key"])).wake_secret == secret and secret not in out


def test_short_wake_secret_refused(mm, env):
    rc, out = run(mm, "set-bot", "--token-stdin", "--wake-secret-stdin", "--wake-url", "https://w.example/h",
                  stdin="%s\n%s\n" % (tok(mm), "k" * 31))
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
    assert only(store.load(env["path"], new)).token == tok(mm)


def test_rotate_key_missing_env(mm, env):
    set_bot(mm)
    rc, out = run(mm, "rotate-key", "--new-key-env", "NOPE_UNSET", "--old-key-env", "MMB_STORE_KEY")
    assert rc != 0 and "store_key_missing" in out


# --- lb2: failed / stats (state.db) ---

def _state(env):
    from app.state import State
    import os
    return State(os.path.join(os.path.dirname(env["path"]), "state.db"), instance_id="d1")


def test_failed_and_stats_on_empty_db(mm, env):
    rc, out = run(mm, "failed")
    assert rc == 0 and "no failed wakes" in out
    rc, out = run(mm, "stats")
    assert rc == 0 and "no wakes yet" in out


def test_failed_lists_and_retry_requeues(mm, env):
    s = _state(env)
    s.enqueue("eddie", "postfailed1", TOWN, {"message": "hello there"})
    s.enqueue("eddie", "postok", TOWN, {})
    s.claim_due(2_000_000_000)
    s.mark_failed("eddie", "postfailed1", "http_401")
    rc, out = run(mm, "failed")
    assert rc == 0 and "postfailed1" in out and "http_401" in out and TOWN in out
    assert "postok" not in out and "hello there" not in out          # message text not echoed
    rc, out = run(mm, "failed", "--retry", "postfailed1")
    assert rc == 0 and "requeued eddie:postfailed1" in out
    assert s.wake("eddie", "postfailed1").status == "queued"
    rc, out = run(mm, "failed", "--retry", "postfailed1")
    assert rc == 1 and "not_found" in out


def test_stats_counts_and_latency(mm, env):
    s = _state(env)
    s.enqueue("eddie", "a", TOWN, {}, post_create_at=0)
    s.enqueue("eddie", "b", TOWN, {})
    s.claim_due(2_000_000_000)
    s.mark_delivered("eddie", "a")
    rc, out = run(mm, "stats")
    assert rc == 0 and "delivered: 1" in out and "in_flight: 1" in out and "p95" in out


def test_failed_unwritable_data_dir(mm, env, monkeypatch, tmp_path):
    monkeypatch.setenv("MMB_DATA_DIR", str(tmp_path / "missing"))
    rc, out = run(mm, "failed")
    assert rc == 1 and "state_unwritable" in out


# --- B-s3: several named bots (ADR-0013) ---------------------------------------------------------------------
SECRET_E, SECRET_A = "e" * 40, "a" * 40


def add(mm, name, user=None, url=None, secret=None):
    user = user or name
    argv = ["set-bot", "--token-stdin", "--wake-url", url or "http://relay:8080/wake/%s" % (name or user)]
    if name:
        argv[1:1] = ["--name", name]
    stdin = tok(mm, user) + "\n"
    if secret:
        argv.append("--wake-secret-stdin")
        stdin += secret + "\n"
    return run(mm, *argv, stdin=stdin)


def test_set_bot_with_name_adds_a_second_bot_and_leaves_the_first(mm, env, caplog):
    assert add(mm, "eddie", secret=SECRET_E)[0] == 0
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        rc, out = add(mm, "grok", user="ada", secret=SECRET_A)
    assert rc == 0 and "bot grok (@ada) stored: wake_url http://relay:8080/wake/grok" in out, out
    st = store.load(env["path"], env["key"])
    assert sorted(st.bots) == ["eddie", "grok"]
    e, g = st.bots["eddie"], st.bots["grok"]
    assert (e.token, e.wake_secret, e.user_id, e.username) == (tok(mm), SECRET_E, "u-eddie", "eddie")
    assert (g.token, g.wake_secret, g.user_id, g.username) == (tok(mm, "ada"), SECRET_A, "u-ada", "ada")
    assert '"bot": "grok"' in caplog.text and tok(mm, "ada") not in caplog.text + out


def test_set_bot_without_name_on_one_bot_store_edits_that_bot(mm, env):
    add(mm, "eddie", secret=SECRET_E)
    rc, out = run(mm, "set-bot", "--token-stdin", "--wake-url", "https://new.example/w", stdin=tok(mm) + "\n")
    assert rc == 0 and "bot eddie (@eddie) stored: wake_url https://new.example/w" in out, out
    st = store.load(env["path"], env["key"])
    assert list(st.bots) == ["eddie"] and st.bots["eddie"].wake_url == "https://new.example/w"


def test_set_bot_without_name_on_empty_store_uses_username(mm, env):
    rc, out = add(mm, None, user="ada")
    assert rc == 0 and list(store.load(env["path"], env["key"]).bots) == ["ada"], out


def test_set_bot_without_name_refused_with_several_bots(mm, env):
    add(mm, "eddie")
    add(mm, "grok", user="ada")
    before = open(env["path"], "rb").read()
    rc, out = run(mm, "set-bot", "--token-stdin", "--wake-url", "https://w.example/h", stdin=tok(mm) + "\n")
    assert rc == 1 and "several bots stored (eddie, grok): pass --name" in out
    assert open(env["path"], "rb").read() == before


@pytest.mark.parametrize("user", ["eddie", "same-user"])
def test_token_or_mattermost_user_unique_across_bots(mm, env, user):
    add(mm, "eddie")
    if user == "same-user":                               # a second token of the same Mattermost user
        mm.user_by_name("eddie")["tokens"] = ["tok-eddie-second-" + "z" * 10]
        stdin = "tok-eddie-second-" + "z" * 10 + "\n"
        detail = "same Mattermost user as bot eddie"
    else:
        stdin, detail = tok(mm) + "\n", "token: already used by bot eddie"
    rc, out = run(mm, "set-bot", "--name", "grok", "--token-stdin", "--wake-url", "https://w.example/h", stdin=stdin)
    assert rc == 1 and detail in out
    assert list(store.load(env["path"], env["key"]).bots) == ["eddie"]


@pytest.mark.parametrize("name", ["Eddie", "-x", "ed_die", "a" * 33])
def test_bad_name_refused_before_mattermost(mm, env, name):
    rc, out = run(mm, "set-bot", "--name=" + name, "--token-stdin", "--wake-url", "https://w.example/h",
                  stdin=tok(mm) + "\n")
    assert rc == 1 and "name: must match" in out and mm.calls == []


def test_set_bot_refuses_to_overwrite_an_unreadable_store(mm, env, monkeypatch):
    add(mm, "eddie")
    add(mm, "grok", user="ada")
    before = open(env["path"], "rb").read()
    monkeypatch.setenv("MMB_STORE_KEY", Fernet.generate_key().decode())
    rc, out = add(mm, "test", user="ada")
    assert rc == 1 and "store_unreadable" in out and open(env["path"], "rb").read() == before


def test_set_bot_on_v1_store_migrates_with_backup_and_username(mm, env):
    import json
    v1 = Fernet(env["key"].encode()).encrypt(json.dumps({"version": 1, "bot": {
        "token": tok(mm), "wake_url": "https://old.example/h", "wake_secret": "o" * 40}}).encode())
    open(env["path"], "wb").write(v1)
    rc, out = add(mm, "grok", user="ada")
    assert rc == 0, out
    st = store.load(env["path"], env["key"])
    assert sorted(st.bots) == ["eddie", "grok"]                       # v1 bot named after its MM username
    assert st.bots["eddie"].wake_url == "https://old.example/h" and st.bots["eddie"].user_id == "u-eddie"
    assert open(env["path"] + ".v1.bak", "rb").read() == v1


def test_list_and_show_name(mm, env):
    add(mm, "eddie", url="https://wake.example/hook", secret=SECRET_E)
    add(mm, "grok", user="ada", secret=SECRET_A)
    rc, out = run(mm, "list")
    assert rc == 0 and out.splitlines() == [
        "eddie  @eddie  token ****%s  wake wake.example  secret set (hidden)" % tok(mm)[-4:],
        "grok  @ada  token ****%s  wake relay  secret set (hidden)" % tok(mm, "ada")[-4:]]
    rc, out = run(mm, "show", "grok")
    assert rc == 0 and "name: grok" in out and "http://relay:8080/wake/grok" in out and "@ada" in out
    for secret in (tok(mm), tok(mm, "ada"), SECRET_E, SECRET_A):
        assert secret not in out
    assert run(mm, "show")[1].startswith("error: invalid_argument: pass a bot name (eddie, grok)")
    assert "not_found" in run(mm, "show", "nope")[1]


def test_remove_bot_marks_pending_wakes_failed(mm, env):
    add(mm, "eddie")
    add(mm, "grok", user="ada")
    s = _state(env)
    s.enqueue("grok", "pq", TOWN, {})
    s.enqueue("grok", "pd", TOWN, {})
    s.enqueue("eddie", "pq", TOWN, {})
    s.claim_due(2_000_000_000, 1, "grok")
    s.mark_delivered("grok", "pq")
    rc, out = run(mm, "remove-bot", "grok")
    assert rc == 0 and "removed bot grok; 1 pending wake(s) marked failed (bot_removed)" in out, out
    assert list(store.load(env["path"], env["key"]).bots) == ["eddie"]
    assert (s.wake("grok", "pd").status, s.wake("grok", "pd").last_error) == ("failed", "bot_removed")
    assert s.wake("grok", "pq").status == "delivered" and s.wake("eddie", "pq").status == "queued"
    assert "not_found" in run(mm, "remove-bot", "grok")[1]


def test_status_per_bot(mm, env):
    import json
    import time as _t
    add(mm, "eddie")
    add(mm, "grok", user="ada")
    s = _state(env)
    now = int(_t.time())
    s.set_meta("bot:eddie:status", json.dumps({"status": "ok", "error": None, "at": now}))
    s.set_meta("bot:eddie:last_event_at", str((now - 3) * 1000))
    s.set_meta("bot:grok:status", json.dumps({"status": "degraded", "error": "mm_unauthorized", "at": now}))
    s.enqueue("grok", "p1", TOWN, {})
    s.claim_due(now + 1, 5)
    s.mark_failed("grok", "p1", "http_424")
    rc, out = run(mm, "status")
    lines = out.splitlines()
    assert rc == 0 and len(lines) == 2, out
    assert lines[0].startswith("eddie  listener ok  last event ") and "last wake none  failed_24h 0" in lines[0]
    assert lines[1].startswith("grok  listener degraded (mm_unauthorized)  last event never  ")
    assert "last wake failed (http_424)  failed_24h 1" in lines[1]
    s.set_meta("bot:eddie:status", json.dumps({"status": "ok", "error": None, "at": now - 600}))
    assert "eddie  listener off (no report for " in run(mm, "status")[1]


def test_failed_by_bot_and_retry_bot_post(mm, env):
    s = _state(env)
    for b in ("eddie", "grok"):
        s.enqueue(b, "p1", TOWN, {})
    s.enqueue("grok", "p2", TOWN, {})
    s.claim_due(2_000_000_000, 10)
    for b, p in (("eddie", "p1"), ("grok", "p1"), ("grok", "p2")):
        s.mark_failed(b, p, "http_503")
    rc, out = run(mm, "failed", "--bot", "grok")
    assert rc == 0 and [x.split()[1] for x in out.splitlines()] == ["grok", "grok"] and "eddie" not in out
    assert all(x.startswith("bot grok  p") for x in out.splitlines())
    rc, out = run(mm, "failed", "--retry", "p1")                     # ambiguous bare id
    assert rc == 1 and "several bots failed p1: use BOT:POST_ID" in out
    rc, out = run(mm, "failed", "--retry", "grok:p1")
    assert rc == 0 and "requeued grok:p1" in out
    assert s.wake("grok", "p1").status == "queued" and s.wake("eddie", "p1").status == "failed"
    assert run(mm, "failed", "--retry", "p2")[1].strip() == "requeued grok:p2"   # unambiguous bare id
    rc, out = run(mm, "stats", "--bot", "eddie")
    assert rc == 0 and out.splitlines()[0] == "failed: 1"


# --- bin/set-bot friendly wrapper (Rob 2026-10-30) -------------------------------------------------------------
def _wrapper(mm, answers, hidden, argv=("grok",)):
    from app import setbot
    out = io.StringIO()
    asked = []

    def ask(prompt):
        asked.append(prompt)
        return answers.pop(0)

    def ask_hidden(prompt):
        asked.append(prompt)
        return hidden.pop(0)
    rc = setbot.main(list(argv), ask=ask, ask_hidden=ask_hidden, out=out, transport=mm.transport())
    return rc, out.getvalue(), asked


def test_set_bot_wrapper_defaults_relay_url_generates_secret_prints_relay_line(mm, env):
    rc, out, asked = _wrapper(mm, [""], [tok(mm, "ada"), ""])
    assert rc == 0, out
    b = store.load(env["path"], env["key"]).bots["grok"]
    assert b.wake_url == "http://relay:8080/wake/grok" and b.token == tok(mm, "ada") and len(b.wake_secret) >= 32
    assert "RELAY_BOT_GROK_HMAC_SECRET=%s" % b.wake_secret in out.splitlines()
    assert out.count(b.wake_secret) == 1 and tok(mm, "ada") not in out
    assert "RELAY_BOT_GROK_ROUTINE_URL" in out and "RELAY_BOT_GROK_ROUTINE_KEY" in out
    assert "shown once in Mattermost" in asked[0] and "if lost create a new token" in asked[0]
    assert "[http://relay:8080/wake/grok]" in asked[1]


def test_set_bot_wrapper_accepts_existing_secret_and_custom_url(mm, env):
    rc, out, _ = _wrapper(mm, ["https://recv.example/wake"], [tok(mm, "ada"), "x" * 40], argv=("my-bot",))
    assert rc == 0, out
    b = store.load(env["path"], env["key"]).bots["my-bot"]
    assert b.wake_url == "https://recv.example/wake" and b.wake_secret == "x" * 40
    assert "RELAY_BOT_MY_BOT_HMAC_SECRET=" + "x" * 40 in out


@pytest.mark.parametrize("argv,hidden,code,msg", [
    ((), [], 2, "usage: bin/set-bot NAME"),
    (("Bad_Name",), [], 1, "name must match"),
    (("grok",), ["", ""], 1, "no token entered"),
    (("grok",), ["wrong-token-xxxxxxxxxx", ""], 1, "unauthorized"),
])
def test_set_bot_wrapper_errors(mm, env, argv, hidden, code, msg):
    rc, out, _ = _wrapper(mm, [""], list(hidden), argv=argv)
    assert rc == code and msg in out and "HMAC_SECRET" not in out
    assert not os.path.exists(env["path"])
