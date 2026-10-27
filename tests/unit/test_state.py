import os
import sqlite3
import stat
import threading

import pytest

from app import state
from app.state import State, StateError

DAY = 86400
CH = "townsquareid0000000000000a"


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


def test_enqueue_dedupes_on_post_id(db):
    assert db.enqueue("p1", CH, {"message": "hi"}) is True
    assert db.enqueue("p1", CH, {"message": "other"}) is False
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
    db.enqueue("p1", CH, {})
    db.enqueue("p2", CH, {})
    assert [w.post_id for w in db.claim_due(now(clock))] == ["p1", "p2"]
    w = db.wake("p1")
    assert w.status == "in_flight" and w.claimed_by == "d1" and w.lease_until == now(clock) + state.LEASE_S
    assert w.attempts == 1
    assert db.claim_due(now(clock)) == []                        # in_flight not re-claimable
    db.mark_retry("p1", "http_503", now(clock) + 2)
    assert db.claim_due(now(clock)) == []                        # not due yet
    assert [w.post_id for w in db.claim_due(now(clock) + 2)] == ["p1"]


def test_claim_due_limit(db, clock):
    for i in range(6):
        db.enqueue("p%d" % i, CH, {})
    assert len(db.claim_due(now(clock), limit=4)) == 4
    assert len(db.claim_due(now(clock), limit=4)) == 2


def test_retry_then_failed_after_max_attempts(tmp_path, clock):
    db = State(str(tmp_path / "s.db"), instance_id="d1", clock=clock, max_attempts=3)
    db.enqueue("p1", CH, {})
    t = now(clock)
    for _ in range(2):
        (w,) = db.claim_due(t)
        assert db.mark_retry("p1", "http_503", t) == "retry"
    (w,) = db.claim_due(t)
    assert w.attempts == 3
    assert db.mark_retry("p1", "http_503", t) == "failed"
    w = db.wake("p1")
    assert w.status == "failed" and w.last_error == "http_503" and w.claimed_by is None
    assert db.claim_due(t + 999) == []


def test_mark_failed_and_requeue(db, clock):
    db.enqueue("p1", CH, {})
    db.claim_due(now(clock))
    assert db.mark_failed("p1", "http_401") is True
    assert [w.post_id for w in db.failed()] == ["p1"]
    assert db.requeue("p1") is True
    w = db.wake("p1")
    assert w.status == "queued" and w.attempts == 0 and w.next_at <= now(clock)
    assert db.failed() == []
    assert db.requeue("p1") is False                              # only failed rows
    assert db.requeue("nope") is False


def test_mark_with_wrong_claimer_is_noop(db, tmp_path, clock):
    other = State(str(tmp_path / "state.db"), instance_id="d2", clock=clock)
    db.enqueue("p1", CH, {})
    db.claim_due(now(clock))
    assert other.mark_delivered("p1") is False
    assert other.mark_failed("p1", "x") is False
    assert other.mark_retry("p1", "x", 0) is None
    assert db.wake("p1").status == "in_flight"
    assert db.mark_delivered("p1") is True
    assert db.wake("p1").status == "delivered"


def test_concurrent_claimers_never_share_a_post(tmp_path, clock):
    path = str(tmp_path / "state.db")
    State(path, clock=clock).close()
    seed = State(path, clock=clock)
    for i in range(200):
        seed.enqueue("p%03d" % i, CH, {})
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
        assert all(seed.wake(p).claimed_by == name for p in ids)


def test_recover_stale_returns_expired_leases_only(db, clock):
    db.enqueue("old", CH, {})
    db.claim_due(now(clock))
    clock.t += 20
    db.enqueue("new", CH, {})
    db.claim_due(now(clock))
    assert db.recover_stale(now(clock) + 15) == 1                  # old lease ended at t0+30, new at t0+50
    old, new = db.wake("old"), db.wake("new")
    assert old.status == "retry" and old.claimed_by is None and old.next_at <= now(clock) + 15
    assert new.status == "in_flight" and new.claimed_by == "d1"
    assert db.mark_delivered("old") is False                       # lease lost
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
    assert db.enqueue_and_advance("p1", CH, {}, 1000) is True
    assert db.get_cursor(CH) == (1000, "p1")

    def boom(*a, **k):
        raise RuntimeError("injected")
    monkeypatch.setattr(db, "_advance", boom)
    with pytest.raises(RuntimeError):
        db.enqueue_and_advance("p2", CH, {}, 2000)
    assert db.wake("p2") is None and db.get_cursor(CH) == (1000, "p1")


def test_cursor_only_moves_forward(db):
    assert db.get_cursor(CH) is None
    db.set_cursor(CH, 2000, "pb")
    db.set_cursor(CH, 1000, "pz")                                  # older: ignored
    assert db.get_cursor(CH) == (2000, "pb")
    db.set_cursor(CH, 2000, "pa")                                  # same ts, smaller id: ignored
    assert db.get_cursor(CH) == (2000, "pb")
    db.set_cursor(CH, 2000, "pc")                                  # same ts, larger id: advances
    assert db.get_cursor(CH) == (2000, "pc")
    assert db.enqueue_and_advance("pold", CH, {}, 500) is True     # late post still enqueued, cursor kept
    assert db.get_cursor(CH) == (2000, "pc")


def test_meta(db):
    assert db.get_meta("connection_id") is None
    db.set_meta("connection_id", "abc")
    db.set_meta("connection_id", "def")
    assert db.get_meta("connection_id") == "def"


def test_prune_terminal_only(db, clock):
    for p in ("del", "fail", "r", "inf"):
        db.enqueue(p, CH, {})
    db.claim_due(now(clock), limit=10)
    db.enqueue("q", CH, {})
    db.mark_delivered("del")
    db.mark_failed("fail", "x")
    db.mark_retry("r", "x", now(clock))
    clock.t += 6 * DAY
    assert db.prune(7) == 0
    clock.t += DAY + 1
    assert db.prune(7) == 2
    assert sorted(w.post_id for w in db.wakes()) == ["inf", "q", "r"]


def test_delivered_latency_from_post_create_at(db, clock):
    t_ms = int(clock() * 1000)
    db.enqueue("p1", CH, {}, post_create_at=t_ms - 3000)
    db.enqueue("p2", CH, {}, post_create_at=t_ms - 1000)
    clock.t += 100                                                  # enqueue time must not matter
    db.claim_due(now(clock))
    db.mark_delivered("p1")
    db.mark_delivered("p2")
    assert db.wake("p1").delivered_at == int(clock() * 1000)
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
