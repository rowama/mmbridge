import os
import sqlite3
import stat
import threading

import pytest

from app import state
from app.state import State, StateError

DAY = 86400
CH = "townsquareid0000000000000a"
B = "eddie"


@pytest.fixture
def clock():
    class Clock:
        t = 1_800_000_000.0

        def __call__(self):
            return self.t
    return Clock()


@pytest.fixture
def db(tmp_path, clock):
    return State(str(tmp_path / "state.db"), instance_id="d1", clock=clock)


def now(clock):
    return int(clock())


def test_enqueue_dedupes_on_bot_and_post_id(db):
    assert db.enqueue(B, "p1", CH, {"message": "hi"}) is True
    assert db.enqueue(B, "p1", CH, {"message": "other"}) is False
    rows = db.wakes()
    assert len(rows) == 1 and rows[0].payload == {"message": "hi"} and rows[0].status == "queued"


def test_wal_and_schema_has_no_secret_columns(db, tmp_path):
    con = sqlite3.connect(str(tmp_path / "state.db"))
    assert con.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
    tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    assert {"wakes", "cursors", "meta"} <= set(tables)
    for t in tables:
        for col in con.execute("PRAGMA table_info(%s)" % t):
            assert "token" not in col[1].lower() and "secret" not in col[1].lower()


def test_claim_due_respects_next_at_and_marks_in_flight(db, clock):
    db.enqueue(B, "p1", CH, {})
    db.enqueue(B, "p2", CH, {})
    assert [w.post_id for w in db.claim_due(now(clock))] == ["p1", "p2"]
    w = db.wake(B, "p1")
    assert w.status == "in_flight" and w.claimed_by == "d1" and w.lease_until == now(clock) + state.LEASE_S
    assert w.attempts == 1
    assert db.claim_due(now(clock)) == []                        # in_flight not re-claimable
    db.mark_retry(B, "p1", "http_503", now(clock) + 2)
    assert db.claim_due(now(clock)) == []                        # not due yet
    assert [w.post_id for w in db.claim_due(now(clock) + 2)] == ["p1"]


def test_claim_due_limit(db, clock):
    for i in range(6):
        db.enqueue(B, "p%d" % i, CH, {})
    assert len(db.claim_due(now(clock), limit=4)) == 4
    assert len(db.claim_due(now(clock), limit=4)) == 2


def test_retry_then_failed_after_max_attempts(tmp_path, clock):
    db = State(str(tmp_path / "s.db"), instance_id="d1", clock=clock, max_attempts=3)
    db.enqueue(B, "p1", CH, {})
    t = now(clock)
    for _ in range(2):
        (w,) = db.claim_due(t)
        assert db.mark_retry(B, "p1", "http_503", t) == "retry"
    (w,) = db.claim_due(t)
    assert w.attempts == 3
    assert db.mark_retry(B, "p1", "http_503", t) == "failed"
    w = db.wake(B, "p1")
    assert w.status == "failed" and w.last_error == "http_503" and w.claimed_by is None
    assert db.claim_due(t + 999) == []


def test_mark_failed_and_requeue(db, clock):
    db.enqueue(B, "p1", CH, {})
    db.claim_due(now(clock))
    assert db.mark_failed(B, "p1", "http_401") is True
    assert [w.post_id for w in db.failed()] == ["p1"]
    assert db.requeue(B, "p1") is True
    w = db.wake(B, "p1")
    assert w.status == "queued" and w.attempts == 0 and w.next_at <= now(clock)
    assert db.failed() == []
    assert db.requeue(B, "p1") is False                              # only failed rows
    assert db.requeue(B, "nope") is False


def test_mark_with_wrong_claimer_is_noop(db, tmp_path, clock):
    other = State(str(tmp_path / "state.db"), instance_id="d2", clock=clock)
    db.enqueue(B, "p1", CH, {})
    db.claim_due(now(clock))
    assert other.mark_delivered(B, "p1") is False
    assert other.mark_failed(B, "p1", "x") is False
    assert other.mark_retry(B, "p1", "x", 0) is None
    assert db.wake(B, "p1").status == "in_flight"
    assert db.mark_delivered(B, "p1") is True
    assert db.wake(B, "p1").status == "delivered"


def test_concurrent_claimers_never_share_a_post(tmp_path, clock):
    path = str(tmp_path / "state.db")
    State(path, clock=clock).close()
    seed = State(path, clock=clock)
    for i in range(200):
        seed.enqueue(B, "p%03d" % i, CH, {})
    got: dict[str, list[str]] = {"a": [], "b": [], "c": []}

    def worker(name):
        s = State(path, instance_id=name, clock=clock)
        while True:
            batch = s.claim_due(now(clock), limit=3)
            if not batch:
                break
            got[name].extend(w.post_id for w in batch)
        s.close()
    ts = [threading.Thread(target=worker, args=(n,)) for n in got]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    allp = got["a"] + got["b"] + got["c"]
    assert len(allp) == 200 and len(set(allp)) == 200
    for name, ids in got.items():
        assert all(seed.wake(B, p).claimed_by == name for p in ids)


def test_recover_stale_returns_expired_leases_only(db, clock):
    db.enqueue(B, "old", CH, {})
    db.claim_due(now(clock))
    clock.t += 20
    db.enqueue(B, "new", CH, {})
    db.claim_due(now(clock))
    assert db.recover_stale(now(clock) + 15) == 1                  # old lease ended at t0+30, new at t0+50
    old, new = db.wake(B, "old"), db.wake(B, "new")
    assert old.status == "retry" and old.claimed_by is None and old.next_at <= now(clock) + 15
    assert new.status == "in_flight" and new.claimed_by == "d1"
    assert db.mark_delivered(B, "old") is False                       # lease lost
    assert [w.post_id for w in db.claim_due(now(clock) + 15)] == ["old"]


def test_dispatcher_owner_heartbeat(tmp_path, clock):
    path = str(tmp_path / "state.db")
    a = State(path, instance_id="A", clock=clock)
    b = State(path, instance_id="B", clock=clock)
    t = now(clock)
    assert a.claim_owner(t) is True
    assert b.claim_owner(t + 10) is False                          # A's heartbeat fresh
    assert a.claim_owner(t + 50) is True                           # heartbeat
    assert b.claim_owner(t + 50 + state.OWNER_TTL_S - 1) is False
    assert b.claim_owner(t + 50 + state.OWNER_TTL_S) is True       # expired -> taken over
    assert a.claim_owner(t + 50 + state.OWNER_TTL_S + 1) is False


def test_enqueue_and_advance_is_atomic(db, monkeypatch):
    assert db.enqueue_and_advance(B, "p1", CH, {}, 1000) is True
    assert db.get_cursor(B, CH) == (1000, "p1")

    def boom(*a, **k):
        raise RuntimeError("injected")
    monkeypatch.setattr(db, "_advance", boom)
    with pytest.raises(RuntimeError):
        db.enqueue_and_advance(B, "p2", CH, {}, 2000)
    assert db.wake(B, "p2") is None and db.get_cursor(B, CH) == (1000, "p1")


def test_cursor_only_moves_forward(db):
    assert db.get_cursor(B, CH) is None
    db.set_cursor(B, CH, 2000, "pb")
    db.set_cursor(B, CH, 1000, "pz")                                  # older: ignored
    assert db.get_cursor(B, CH) == (2000, "pb")
    db.set_cursor(B, CH, 2000, "pa")                                  # same ts, smaller id: ignored
    assert db.get_cursor(B, CH) == (2000, "pb")
    db.set_cursor(B, CH, 2000, "pc")                                  # same ts, larger id: advances
    assert db.get_cursor(B, CH) == (2000, "pc")
    assert db.enqueue_and_advance(B, "pold", CH, {}, 500) is True     # late post still enqueued, cursor kept
    assert db.get_cursor(B, CH) == (2000, "pc")


def test_meta(db):
    assert db.get_meta("connection_id") is None
    db.set_meta("connection_id", "abc")
    db.set_meta("connection_id", "def")
    assert db.get_meta("connection_id") == "def"


def test_prune_terminal_only(db, clock):
    for p in ("del", "fail", "r", "inf"):
        db.enqueue(B, p, CH, {})
    db.claim_due(now(clock), limit=10)
    db.enqueue(B, "q", CH, {})
    db.mark_delivered(B, "del")
    db.mark_failed(B, "fail", "x")
    db.mark_retry(B, "r", "x", now(clock))
    clock.t += 6 * DAY
    assert db.prune(7) == 0
    clock.t += DAY + 1
    assert db.prune(7) == 2
    assert sorted(w.post_id for w in db.wakes()) == ["inf", "q", "r"]


def test_delivered_latency_from_post_create_at(db, clock):
    t_ms = int(clock() * 1000)
    db.enqueue(B, "p1", CH, {}, post_create_at=t_ms - 3000)
    db.enqueue(B, "p2", CH, {}, post_create_at=t_ms - 1000)
    clock.t += 100                                                  # enqueue time must not matter
    db.claim_due(now(clock))
    db.mark_delivered(B, "p1")
    db.mark_delivered(B, "p2")
    assert db.wake(B, "p1").delivered_at == int(clock() * 1000)
    s = db.stats()
    assert s["counts"] == {"delivered": 2}
    assert s["latency_ms"] == {"n": 2, "p50": 101000, "p95": 103000}


def test_stats_empty(db):
    assert db.stats() == {"counts": {}, "latency_ms": {"n": 0, "p50": None, "p95": None}}


def test_next_delay(monkeypatch):
    assert [state.next_delay(a) for a in range(1, 6)] == [2, 4, 8, 16, 32]
    monkeypatch.setenv("WAKE_BACKOFF_SCALE", "0.5")
    assert state.next_delay(3) == 4


def test_max_attempts_env(tmp_path, monkeypatch):
    assert State(str(tmp_path / "a.db")).max_attempts == 5
    monkeypatch.setenv("WAKE_MAX_ATTEMPTS", "7")
    assert State(str(tmp_path / "b.db")).max_attempts == 7


@pytest.mark.skipif(os.name != "posix" or os.geteuid() == 0, reason="needs POSIX dir permissions, non-root")
def test_unwritable_dir(tmp_path):
    ro = tmp_path / "ro"
    ro.mkdir()
    ro.chmod(stat.S_IRUSR | stat.S_IXUSR)
    try:
        with pytest.raises(StateError) as e:
            State(str(ro / "state.db"))
        assert e.value.code == "state_unwritable"
    finally:
        ro.chmod(0o700)


def test_missing_dir(tmp_path):
    with pytest.raises(StateError) as e:
        State(str(tmp_path / "nope" / "state.db"))
    assert e.value.code == "state_unwritable"


# --- B-s3 schema v2: per-bot ledger, cursors, meta, view (ADR-0014) ---------------------------------------------
def test_same_post_is_one_wake_per_bot(db):
    assert db.enqueue("eddie", "p1", CH, {"for": "eddie"}) is True
    assert db.enqueue("grok", "p1", CH, {"for": "grok"}) is True          # B6: each bot woken once
    assert db.enqueue("grok", "p1", CH, {}) is False
    assert sorted((w.bot, w.payload["for"]) for w in db.wakes()) == [("eddie", "eddie"), ("grok", "grok")]
    assert [w.bot for w in db.wakes("grok")] == ["grok"]


def test_cursors_are_per_bot(db):
    db.set_cursor("eddie", CH, 1000, "pa")
    db.set_cursor("grok", CH, 5000, "pz")
    assert db.get_cursor("eddie", CH) == (1000, "pa") and db.get_cursor("grok", CH) == (5000, "pz")
    db.delete_cursor("grok", CH)
    assert db.cursor_channels("grok") == [] and db.cursor_channels("eddie") == [CH]


def test_claim_due_by_bot_and_due_bots(db, clock):
    for b in ("eddie", "grok"):
        for i in range(3):
            db.enqueue(b, "p%d" % i, CH, {})
    assert db.due_bots(now(clock)) == ["eddie", "grok"]
    got = db.claim_due(now(clock), 2, "grok")
    assert [(w.bot, w.post_id) for w in got] == [("grok", "p0"), ("grok", "p1")]
    assert db.claim_due(now(clock), 0, "eddie") == []
    assert db.mark_delivered("eddie", "p0") is False                   # (bot, post_id), not post_id alone
    assert db.mark_delivered("grok", "p0") is True


def test_fail_pending_for_removed_bot(db, clock):
    db.enqueue("grok", "q", CH, {})
    db.enqueue("grok", "f", CH, {})
    db.enqueue("grok", "d", CH, {})
    db.enqueue("eddie", "q", CH, {})
    db.claim_due(now(clock), 1, "grok")                                 # q in flight
    assert db.mark_delivered("grok", "q") is True
    db.claim_due(now(clock), 1, "grok")                                 # f in flight
    assert db.fail_pending("grok", "bot_removed") == 2                  # f (in flight) + d (queued)
    assert {w.post_id: (w.status, w.last_error) for w in db.wakes("grok")} == {
        "q": ("delivered", None), "f": ("failed", "bot_removed"), "d": ("failed", "bot_removed")}
    assert db.wake("eddie", "q").status == "queued"


def test_failed_stats_last_wake_per_bot(db, clock):
    db.enqueue("eddie", "a", CH, {})
    db.enqueue("grok", "a", CH, {})
    db.claim_due(now(clock), 10)
    db.mark_delivered("eddie", "a")
    clock.t += 1
    db.mark_failed("grok", "a", "http_424")
    assert [w.bot for w in db.failed()] == ["grok"] and db.failed("eddie") == []
    assert [(w.bot, w.post_id) for w in db.failed_for_post("a")] == [("grok", "a")]
    assert db.failed_count(0, "grok") == 1 and db.failed_count(0, "eddie") == 0 and db.failed_count(0) == 1
    assert db.stats("eddie")["counts"] == {"delivered": 1} and db.stats()["counts"] == {"delivered": 1, "failed": 1}
    assert db.last_wake("grok").status == "failed" and db.last_wake("eddie").status == "delivered"
    assert db.last_wake("nobody") is None


def test_bot_view_scopes_rows_meta_and_lease(db, clock):
    e, g = db.bot("eddie"), db.bot("grok")
    assert e.enqueue_and_advance("p1", CH, {}, 1000) is True and g.enqueue("p1", CH, {}) is True
    assert e.get_cursor(CH) == (1000, "p1") and g.get_cursor(CH) is None
    assert [w.bot for w in e.wakes()] == ["eddie"] and e.wake("p1").bot == "eddie"
    e.set_meta("bot_identity", "fp:u-eddie")
    e.set_meta("last_event_at", "123")
    assert db.get_meta("bot:eddie:identity") == "fp:u-eddie" and db.get_meta("bot:eddie:last_event_at") == "123"
    assert g.get_meta("bot_identity") is None
    other = State(db.path, instance_id="d2", clock=clock)
    assert e.claim_owner(now(clock), 60) is True
    assert other.bot("eddie").claim_owner(now(clock), 60) is False      # same bot: one listener
    assert other.bot("grok").claim_owner(now(clock), 60) is True        # other bot: own lease
    assert db.get_meta("listener_owner:eddie") is not None


def test_new_file_is_schema_v2(tmp_path):
    State(str(tmp_path / "state.db")).close()
    con = sqlite3.connect(str(tmp_path / "state.db"))
    assert con.execute("PRAGMA user_version").fetchone()[0] == 2
    assert "bot" in [r[1] for r in con.execute("PRAGMA table_info(wakes)")]
    assert not os.path.exists(str(tmp_path / "state.db.v1.bak"))


# --- v1 -> v2 migration (ADR-0014) ----------------------------------------------------------------------------
_V1 = """
CREATE TABLE wakes (post_id TEXT PRIMARY KEY, channel_id TEXT NOT NULL, payload_json TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('queued','retry','in_flight','delivered','failed')),
  attempts INTEGER NOT NULL DEFAULT 0, next_at INTEGER NOT NULL, last_error TEXT, claimed_by TEXT,
  lease_until INTEGER, post_create_at INTEGER, delivered_at INTEGER, created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL);
CREATE INDEX wakes_due ON wakes (status, next_at);
CREATE TABLE cursors (channel_id TEXT PRIMARY KEY, last_create_at INTEGER NOT NULL, last_post_id TEXT NOT NULL);
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);
INSERT INTO wakes VALUES ('p1', 'c1', '{"delivery_id": "p1"}', 'delivered', 1, 0, NULL, NULL, NULL, 10, 20, 1, 2);
INSERT INTO wakes VALUES ('p2', 'c1', '{"delivery_id": "p2"}', 'queued', 0, 0, NULL, NULL, NULL, 11, NULL, 3, 3);
INSERT INTO wakes VALUES ('p3', 'c2', '{}', 'failed', 5, 0, 'http_424', NULL, NULL, 12, NULL, 4, 4);
INSERT INTO cursors VALUES ('c1', 1000, 'p2');
INSERT INTO meta VALUES ('schema_version', '1'), ('bot_user_id', 'u-eddie'), ('bot_identity', 'fp:u-eddie'),
  ('last_event_at', '999'), ('ws_connection_id', 'conn-1'), ('dispatcher_owner', '{"id": "x", "ts": 1}'),
  ('listener_owner', '{"id": "x", "ts": 1}');
"""


def _v1_db(path):
    con = sqlite3.connect(path)
    con.executescript(_V1)
    con.commit()
    con.close()


def test_v1_file_migrates_in_place_with_backup(tmp_path, clock):
    path = str(tmp_path / "state.db")
    _v1_db(path)
    seen = []
    db = State(path, clock=clock, legacy_bot=lambda uid: seen.append(uid) or "eddie")
    assert seen == ["u-eddie"]                                      # owner chosen by the v1 bot_user_id
    assert [(w.bot, w.post_id, w.status) for w in db.wakes()] == [
        ("eddie", "p1", "delivered"), ("eddie", "p2", "queued"), ("eddie", "p3", "failed")]
    assert db.wake("eddie", "p3").last_error == "http_424" and db.wake("eddie", "p1").delivered_at == 20
    assert db.get_cursor("eddie", "c1") == (1000, "p2")
    assert db.bot("eddie").get_meta("bot_identity") == "fp:u-eddie"
    assert db.bot("eddie").get_meta("last_event_at") == "999"
    assert db.bot("eddie").get_meta("ws_connection_id") == "conn-1"
    assert db.get_meta("listener_owner:eddie") and db.get_meta("dispatcher_owner")
    for k in ("bot_identity", "bot_user_id", "listener_owner", "schema_version"):
        assert db.get_meta(k) is None
    assert db.enqueue("eddie", "p2", "c1", {}) is False              # ledger still dedupes migrated rows
    db.close()
    bak = path + ".v1.bak"
    assert stat.S_IMODE(os.stat(bak).st_mode) == 0o600
    con = sqlite3.connect(bak)
    assert [r[1] for r in con.execute("PRAGMA table_info(wakes)")][0] == "post_id"   # backup is the v1 file
    assert con.execute("SELECT COUNT(*) FROM wakes").fetchone()[0] == 3
    con.close()
    before = open(bak, "rb").read()
    again = State(path, clock=clock, legacy_bot="other")              # idempotent: v2 file opens as is
    assert [w.bot for w in again.wakes()] == ["eddie"] * 3 and open(bak, "rb").read() == before


def test_crash_mid_migration_rolls_back_and_rerun_succeeds(tmp_path, clock, monkeypatch):
    path = str(tmp_path / "state.db")
    _v1_db(path)

    def boom(c, bot):
        raise sqlite3.OperationalError("disk I/O error (injected)")
    real = state._v1_meta
    monkeypatch.setattr(state, "_v1_meta", boom)                     # after rename/create/copy, same transaction
    with pytest.raises(StateError) as e:
        State(path, clock=clock, legacy_bot="eddie")
    assert e.value.code == "live_migration_failed"
    con = sqlite3.connect(path)                                     # untouched v1 file
    assert con.execute("PRAGMA user_version").fetchone()[0] == 0
    assert [r[1] for r in con.execute("PRAGMA table_info(wakes)")][0] == "post_id"
    assert con.execute("SELECT COUNT(*) FROM wakes").fetchone()[0] == 3
    assert {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")} == {"wakes", "cursors",
                                                                                               "meta"}
    con.close()
    monkeypatch.setattr(state, "_v1_meta", real)
    db = State(path, clock=clock, legacy_bot="eddie")
    assert len(db.wakes("eddie")) == 3 and db.bot("eddie").get_meta("bot_identity") == "fp:u-eddie"


def test_unknown_future_schema_refused(tmp_path):
    path = str(tmp_path / "state.db")
    con = sqlite3.connect(path)
    con.execute("PRAGMA user_version=9")
    con.close()
    with pytest.raises(StateError) as e:
        State(path)
    assert e.value.code == "live_migration_failed"
