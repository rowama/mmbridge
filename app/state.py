"""Listener state on the persistent volume (ADR-0009): /data/state.db, SQLite in WAL mode.

`wakes` is both the at-most-once ledger (INSERT OR IGNORE on post_id is the single enqueue gate) and the
delivery queue: queued|retry -> in_flight (claimed by one dispatcher, with a lease) -> delivered|failed.
`cursors` holds the forward-only (create_at, post_id) per channel; `meta` holds ws state and the dispatcher
owner heartbeat. No tokens or secrets are stored; message text is, and terminal rows are pruned after 7 days.
Blocking stdlib sqlite3: async callers use asyncio.to_thread. One connection per State, guarded by a lock.
"""
import json
import math
import os
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass

DAY = 86400
LEASE_S = 30          # in_flight lease; recover_stale returns expired leases to retry
OWNER_TTL_S = 60      # dispatcher owner heartbeat freshness
TERMINAL = ("delivered", "failed")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS wakes (
  post_id TEXT PRIMARY KEY,
  channel_id TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('queued','retry','in_flight','delivered','failed')),
  attempts INTEGER NOT NULL DEFAULT 0,
  next_at INTEGER NOT NULL,
  last_error TEXT,
  claimed_by TEXT,
  lease_until INTEGER,
  post_create_at INTEGER,
  delivered_at INTEGER,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS wakes_due ON wakes (status, next_at);
CREATE TABLE IF NOT EXISTS cursors (
  channel_id TEXT PRIMARY KEY,
  last_create_at INTEGER NOT NULL,
  last_post_id TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
"""


def path_from_env() -> str:
    return os.path.join(os.getenv("MMB_DATA_DIR", "/data"), "state.db")


def next_delay(attempt: int) -> float:
    """Backoff after the given (1-based) failed attempt: 2, 4, 8, 16, 32 s, times WAKE_BACKOFF_SCALE (tests)."""
    return 2 ** min(max(attempt, 1), 5) * float(os.getenv("WAKE_BACKOFF_SCALE", "1.0"))


class StateError(Exception):
    """code: state_unwritable. detail: sqlite reason (no secrets in state)."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__("%s: %s" % (code, detail) if detail else code)
        self.code, self.detail = code, detail


@dataclass
class Wake:
    post_id: str
    channel_id: str
    payload: dict
    status: str
    attempts: int
    next_at: int
    last_error: str | None
    claimed_by: str | None
    lease_until: int | None
    post_create_at: int | None
    delivered_at: int | None
    created_at: int
    updated_at: int


_COLS = ("post_id, channel_id, payload_json, status, attempts, next_at, last_error, claimed_by, lease_until, "
         "post_create_at, delivered_at, created_at, updated_at")


def _wake(row) -> Wake:
    r = list(row)
    r[2] = json.loads(r[2])
    return Wake(*r)


class State:
    def __init__(self, path: str, instance_id: str | None = None, clock=time.time, max_attempts: int | None = None):
        self.instance_id = instance_id or uuid.uuid4().hex
        self.clock = clock
        self.max_attempts = max_attempts or int(os.getenv("WAKE_MAX_ATTEMPTS", "5"))
        self._lock = threading.Lock()
        try:
            self._conn = sqlite3.connect(path, timeout=10, isolation_level=None, check_same_thread=False)
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.executescript(_SCHEMA)
            self.set_meta("schema_version", "1")      # write probe: read-only db/dir fails here
        except sqlite3.Error as e:
            raise StateError("state_unwritable", str(e)) from None

    def close(self) -> None:
        self._conn.close()

    def _now(self) -> int:
        return int(self.clock())

    @contextmanager
    def _tx(self):
        with self._lock:
            self._conn.execute("BEGIN IMMEDIATE")
            try:
                yield self._conn
            except BaseException:
                self._conn.execute("ROLLBACK")
                raise
            self._conn.execute("COMMIT")

    # --- enqueue / cursors ---------------------------------------------------------------------------------
    def _insert(self, c, post_id, channel_id, payload, post_create_at) -> bool:
        now = self._now()
        cur = c.execute("INSERT OR IGNORE INTO wakes (post_id, channel_id, payload_json, status, next_at, "
                        "post_create_at, created_at, updated_at) VALUES (?,?,?,'queued',?,?,?,?)",
                        (post_id, channel_id, json.dumps(payload), now, post_create_at, now, now))
        return cur.rowcount == 1

    def _advance(self, c, channel_id: str, create_at: int, post_id: str) -> None:
        c.execute("INSERT INTO cursors (channel_id, last_create_at, last_post_id) VALUES (?,?,?) "
                  "ON CONFLICT(channel_id) DO UPDATE SET last_create_at=excluded.last_create_at, "
                  "last_post_id=excluded.last_post_id "
                  "WHERE (excluded.last_create_at, excluded.last_post_id) > (last_create_at, last_post_id)",
                  (channel_id, create_at, post_id))

    def enqueue(self, post_id: str, channel_id: str, payload: dict, post_create_at: int | None = None) -> bool:
        """True if newly queued; False if post_id was already seen (the dedupe gate)."""
        with self._tx() as c:
            return self._insert(c, post_id, channel_id, payload, post_create_at)

    def enqueue_and_advance(self, post_id: str, channel_id: str, payload: dict, create_at: int) -> bool:
        """enqueue + forward-only cursor move in one transaction (PR-3)."""
        with self._tx() as c:
            new = self._insert(c, post_id, channel_id, payload, create_at)
            self._advance(c, channel_id, create_at, post_id)
            return new

    def get_cursor(self, channel_id: str) -> tuple[int, str] | None:
        with self._lock:
            row = self._conn.execute("SELECT last_create_at, last_post_id FROM cursors WHERE channel_id=?",
                                     (channel_id,)).fetchone()
        return tuple(row) if row else None

    def set_cursor(self, channel_id: str, create_at: int, post_id: str = "") -> None:
        with self._tx() as c:
            self._advance(c, channel_id, create_at, post_id)

    # --- meta ------------------------------------------------------------------------------------------------
    def get_meta(self, key: str) -> str | None:
        with self._lock:
            row = self._conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row[0] if row else None

    def set_meta(self, key: str, value: str) -> None:
        with self._tx() as c:
            c.execute("INSERT INTO meta (key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                      (key, value))

    def claim_owner(self, now: int, ttl: int = OWNER_TTL_S) -> bool:
        """Become (or stay, as heartbeat) the single dispatcher owner; refused while another owner is fresh."""
        with self._tx() as c:
            row = c.execute("SELECT value FROM meta WHERE key='dispatcher_owner'").fetchone()
            if row:
                cur = json.loads(row[0])
                if cur["id"] != self.instance_id and now - cur["ts"] < ttl:
                    return False
            c.execute("INSERT INTO meta (key, value) VALUES ('dispatcher_owner', ?) "
                      "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                      (json.dumps({"id": self.instance_id, "ts": now}),))
            return True

    # --- dispatcher queue ------------------------------------------------------------------------------------
    def claim_due(self, now: int, limit: int = 4) -> list[Wake]:
        """Atomically flip up to `limit` due queued/retry rows to in_flight for this instance (PR-1)."""
        with self._tx() as c:
            rows = c.execute(
                "UPDATE wakes SET status='in_flight', claimed_by=?, lease_until=?, attempts=attempts+1, updated_at=? "
                "WHERE post_id IN (SELECT post_id FROM wakes WHERE status IN ('queued','retry') AND next_at<=? "
                "ORDER BY next_at, rowid LIMIT ?) RETURNING rowid, " + _COLS,
                (self.instance_id, now + LEASE_S, self._now(), now, limit)).fetchall()
        rows.sort(key=lambda r: (r[6], r[0]))
        return [_wake(r[1:]) for r in rows]

    def _mine(self, c, post_id: str):
        return c.execute("SELECT attempts FROM wakes WHERE post_id=? AND status='in_flight' AND claimed_by=?",
                         (post_id, self.instance_id)).fetchone()

    def mark_delivered(self, post_id: str) -> bool:
        now = self.clock()
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='delivered', delivered_at=?, claimed_by=NULL, lease_until=NULL, "
                             "updated_at=? WHERE post_id=? AND status='in_flight' AND claimed_by=?",
                             (int(now * 1000), int(now), post_id, self.instance_id)).rowcount == 1

    def mark_failed(self, post_id: str, err: str) -> bool:
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='failed', last_error=?, claimed_by=NULL, lease_until=NULL, "
                             "updated_at=? WHERE post_id=? AND status='in_flight' AND claimed_by=?",
                             (err, self._now(), post_id, self.instance_id)).rowcount == 1

    def mark_retry(self, post_id: str, err: str, next_at: int) -> str | None:
        """'retry', or 'failed' once attempts reached max_attempts; None if not claimed by this instance."""
        with self._tx() as c:
            row = self._mine(c, post_id)
            if not row:
                return None
            status = "failed" if row[0] >= self.max_attempts else "retry"
            c.execute("UPDATE wakes SET status=?, last_error=?, next_at=?, claimed_by=NULL, lease_until=NULL, "
                      "updated_at=? WHERE post_id=?", (status, err, next_at, self._now(), post_id))
            return status

    def recover_stale(self, now: int) -> int:
        """Return in_flight rows whose lease expired (crashed dispatcher) to retry, due now."""
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='retry', claimed_by=NULL, lease_until=NULL, next_at=?, "
                             "updated_at=? WHERE status='in_flight' AND lease_until < ?",
                             (now, self._now(), now)).rowcount

    def requeue(self, post_id: str) -> bool:
        """Operator retry of a failed wake: fresh attempts, due now."""
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='queued', attempts=0, next_at=?, last_error=NULL, "
                             "updated_at=? WHERE post_id=? AND status='failed'",
                             (self._now(), self._now(), post_id)).rowcount == 1

    def prune(self, days: int = 7) -> int:
        """Delete delivered/failed rows older than `days`; never touches queued/retry/in_flight (PR-8)."""
        with self._tx() as c:
            return c.execute("DELETE FROM wakes WHERE status IN ('delivered','failed') AND updated_at < ?",
                             (self._now() - days * DAY,)).rowcount

    # --- reads -----------------------------------------------------------------------------------------------
    def _select(self, where: str = "", args=()) -> list[Wake]:
        with self._lock:
            rows = self._conn.execute("SELECT %s FROM wakes %s ORDER BY rowid" % (_COLS, where), args).fetchall()
        return [_wake(r) for r in rows]

    def wake(self, post_id: str) -> Wake | None:
        rows = self._select("WHERE post_id=?", (post_id,))
        return rows[0] if rows else None

    def wakes(self) -> list[Wake]:
        return self._select()

    def failed(self) -> list[Wake]:
        return self._select("WHERE status='failed'")

    def stats(self) -> dict:
        """Counts per status and post->delivered latency (delivered_at - post_create_at, ms; PR-9)."""
        with self._lock:
            counts = dict(self._conn.execute("SELECT status, COUNT(*) FROM wakes GROUP BY status").fetchall())
            lat = sorted(r[0] for r in self._conn.execute(
                "SELECT delivered_at - post_create_at FROM wakes WHERE status='delivered' "
                "AND delivered_at IS NOT NULL AND post_create_at IS NOT NULL"))

        def pct(p):
            return lat[max(math.ceil(p * len(lat)) - 1, 0)] if lat else None
        return {"counts": counts, "latency_ms": {"n": len(lat), "p50": pct(0.5), "p95": pct(0.95)}}
