"""Listener state on the persistent volume (ADR-0009, v2 ADR-0014): /data/state.db, SQLite in WAL mode.

`wakes` is both the at-most-once ledger (INSERT OR IGNORE on (bot, post_id) is the single enqueue gate, per bot)
and the delivery queue: queued|retry -> in_flight (claimed by one dispatcher, with a lease) -> delivered|failed.
`cursors` holds the forward-only (create_at, post_id) per (bot, channel); `meta` holds per-bot keys
`bot:<name>:<key>` (identity, user_id, last_event_at, ws_connection_id, status), the single dispatcher owner
heartbeat and the per-bot listener lease `listener_owner:<name>`. No tokens or secrets are stored; message text is,
and terminal rows are pruned after 7 days. `State.bot(name)` is the one-bot view a Listener uses.
Schema version is PRAGMA user_version (2). A v1 file (lb2..B-s2, one bot) is copied to state.db.v1.bak first,
then migrated in ONE transaction (rows and meta go to the bot `legacy_bot` names); a failure rolls back, leaves the
v1 file as it was and raises StateError(live_migration_failed); rerunning is safe (idempotent).
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

from app import logging as mlog

DAY = 86400
LEASE_S = 30          # in_flight lease; recover_stale returns expired leases to retry
OWNER_TTL_S = 60      # dispatcher owner heartbeat freshness
TERMINAL = ("delivered", "failed")
PENDING = ("queued", "retry", "in_flight")
SCHEMA_VERSION = 2

_TABLES = [
    """CREATE TABLE IF NOT EXISTS wakes (
  bot TEXT NOT NULL,
  post_id TEXT NOT NULL,
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
  updated_at INTEGER NOT NULL,
  PRIMARY KEY (bot, post_id)
)""",
    "CREATE INDEX IF NOT EXISTS wakes_due ON wakes (status, next_at)",
    """CREATE TABLE IF NOT EXISTS cursors (
  bot TEXT NOT NULL,
  channel_id TEXT NOT NULL,
  last_create_at INTEGER NOT NULL,
  last_post_id TEXT NOT NULL,
  PRIMARY KEY (bot, channel_id)
)""",
    "CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)",
]
_V1_COLS = ("post_id, channel_id, payload_json, status, attempts, next_at, last_error, claimed_by, lease_until, "
            "post_create_at, delivered_at, created_at, updated_at")
_COLS = "bot, " + _V1_COLS
# v1 meta key -> per-bot key suffix (bot:<name>:<suffix>)
_V1_META = {"bot_identity": "identity", "bot_user_id": "user_id", "last_event_at": "last_event_at",
            "ws_connection_id": "ws_connection_id"}


def path_from_env() -> str:
    return os.path.join(os.getenv("MMB_DATA_DIR", "/data"), "state.db")


def meta_key(bot: str, key: str) -> str:
    """Per-bot meta key; the v1 names bot_identity / bot_user_id map to identity / user_id."""
    return "bot:%s:%s" % (bot, _V1_META.get(key, key))


def next_delay(attempt: int) -> float:
    """Backoff after the given (1-based) failed attempt: 2, 4, 8, 16, 32 s, times WAKE_BACKOFF_SCALE (tests)."""
    return 2 ** min(max(attempt, 1), 5) * float(os.getenv("WAKE_BACKOFF_SCALE", "1.0"))


class StateError(Exception):
    """code: state_unwritable | live_migration_failed. detail: sqlite reason (no secrets in state)."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__("%s: %s" % (code, detail) if detail else code)
        self.code, self.detail = code, detail


@dataclass
class Wake:
    bot: str
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


def _wake(row) -> Wake:
    r = list(row)
    r[3] = json.loads(r[3])
    return Wake(*r)


def _log(event: str, level: str = "info", **fields) -> None:
    getattr(mlog.log, level)(json.dumps({"event": event, **fields}))


# --- v1 -> v2 migration steps (module level so a test can fail one mid-transaction) -------------------------------
def _v1_rename(c) -> None:
    c.execute("DROP INDEX IF EXISTS wakes_due")
    c.execute("ALTER TABLE wakes RENAME TO wakes_v1")
    c.execute("ALTER TABLE cursors RENAME TO cursors_v1")


def _v1_create(c) -> None:
    for sql in _TABLES:
        c.execute(sql)


def _v1_copy(c, bot: str) -> None:
    c.execute("INSERT INTO wakes (%s) SELECT ?, %s FROM wakes_v1 ORDER BY rowid" % (_COLS, _V1_COLS), (bot,))
    c.execute("INSERT INTO cursors (bot, channel_id, last_create_at, last_post_id) "
              "SELECT ?, channel_id, last_create_at, last_post_id FROM cursors_v1", (bot,))
    c.execute("DROP TABLE wakes_v1")
    c.execute("DROP TABLE cursors_v1")


def _v1_meta(c, bot: str) -> None:
    for old in _V1_META:
        c.execute("UPDATE OR REPLACE meta SET key=? WHERE key=?", (meta_key(bot, old), old))
    c.execute("UPDATE OR REPLACE meta SET key=? WHERE key='listener_owner'", ("listener_owner:" + bot,))
    c.execute("DELETE FROM meta WHERE key='schema_version'")


class State:
    def __init__(self, path: str, instance_id: str | None = None, clock=time.time, max_attempts: int | None = None,
                 legacy_bot="bot"):
        """legacy_bot: name (or callable(v1 meta bot_user_id) -> name) of the bot that owns the rows of a v1 file."""
        self.path = path
        self.instance_id = instance_id or uuid.uuid4().hex
        self.clock = clock
        self.max_attempts = max_attempts or int(os.getenv("WAKE_MAX_ATTEMPTS", "5"))
        self._lock = threading.Lock()
        try:
            self._conn = sqlite3.connect(path, timeout=10, isolation_level=None, check_same_thread=False)
            self._conn.execute("PRAGMA journal_mode=WAL")
            version = self._conn.execute("PRAGMA user_version").fetchone()[0]
            v1 = version < SCHEMA_VERSION and "bot" not in self._columns("wakes") and self._columns("wakes")
        except sqlite3.Error as e:
            raise StateError("state_unwritable", str(e)) from None
        if v1:
            self._migrate(legacy_bot)
        elif version > SCHEMA_VERSION:
            raise StateError("live_migration_failed", "unknown schema version %d" % version)
        try:
            with self._tx() as c:
                _v1_create(c)
                c.execute("PRAGMA user_version=%d" % SCHEMA_VERSION)
                c.execute("INSERT OR REPLACE INTO meta (key, value) VALUES ('schema_probe', ?)",   # write probe
                          (str(SCHEMA_VERSION),))
        except sqlite3.Error as e:
            raise StateError("state_unwritable", str(e)) from None

    def _columns(self, table: str) -> list[str]:
        return [r[1] for r in self._conn.execute("PRAGMA table_info(%s)" % table)]

    def _migrate(self, legacy_bot) -> None:
        bak = self.path + ".v1.bak"
        try:
            row = self._conn.execute("SELECT value FROM meta WHERE key='bot_user_id'").fetchone() \
                if self._columns("meta") else None
            bot = legacy_bot(row[0] if row else None) if callable(legacy_bot) else legacy_bot
            _log("live_migration_started", from_version=1, to_version=SCHEMA_VERSION, bot=bot)
            os.close(os.open(bak, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600))   # private from the start
            dst = sqlite3.connect(bak)
            try:
                self._conn.backup(dst)           # consistent copy, WAL included
            finally:
                dst.close()
            os.chmod(bak, 0o600)
            with self._tx() as c:
                _v1_rename(c)
                _v1_create(c)
                _v1_copy(c, bot)
                _v1_meta(c, bot)
                c.execute("PRAGMA user_version=%d" % SCHEMA_VERSION)
        except (sqlite3.Error, OSError) as e:
            _log("live_migration_failed", "error", detail=type(e).__name__)
            raise StateError("live_migration_failed", str(e)) from None
        _log("live_migration_done", bot=bot, backup=os.path.basename(bak))

    def close(self) -> None:
        self._conn.close()

    def bot(self, name: str) -> "BotState":
        return BotState(self, name)

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
    def _insert(self, c, bot, post_id, channel_id, payload, post_create_at) -> bool:
        now = self._now()
        cur = c.execute("INSERT OR IGNORE INTO wakes (bot, post_id, channel_id, payload_json, status, next_at, "
                        "post_create_at, created_at, updated_at) VALUES (?,?,?,?,'queued',?,?,?,?)",
                        (bot, post_id, channel_id, json.dumps(payload), now, post_create_at, now, now))
        return cur.rowcount == 1

    def _advance(self, c, bot: str, channel_id: str, create_at: int, post_id: str) -> None:
        c.execute("INSERT INTO cursors (bot, channel_id, last_create_at, last_post_id) VALUES (?,?,?,?) "
                  "ON CONFLICT(bot, channel_id) DO UPDATE SET last_create_at=excluded.last_create_at, "
                  "last_post_id=excluded.last_post_id "
                  "WHERE (excluded.last_create_at, excluded.last_post_id) > (last_create_at, last_post_id)",
                  (bot, channel_id, create_at, post_id))

    def enqueue(self, bot: str, post_id: str, channel_id: str, payload: dict, post_create_at: int | None = None) -> bool:
        """True if newly queued; False if (bot, post_id) was already seen (the dedupe gate)."""
        with self._tx() as c:
            return self._insert(c, bot, post_id, channel_id, payload, post_create_at)

    def enqueue_and_advance(self, bot: str, post_id: str, channel_id: str, payload: dict, create_at: int) -> bool:
        """enqueue + forward-only cursor move in one transaction (PR-3)."""
        with self._tx() as c:
            new = self._insert(c, bot, post_id, channel_id, payload, create_at)
            self._advance(c, bot, channel_id, create_at, post_id)
            return new

    def get_cursor(self, bot: str, channel_id: str) -> tuple[int, str] | None:
        with self._lock:
            row = self._conn.execute("SELECT last_create_at, last_post_id FROM cursors WHERE bot=? AND channel_id=?",
                                     (bot, channel_id)).fetchone()
        return tuple(row) if row else None

    def set_cursor(self, bot: str, channel_id: str, create_at: int, post_id: str = "") -> None:
        with self._tx() as c:
            self._advance(c, bot, channel_id, create_at, post_id)

    def delete_cursor(self, bot: str, channel_id: str) -> None:
        with self._tx() as c:
            c.execute("DELETE FROM cursors WHERE bot=? AND channel_id=?", (bot, channel_id))

    def cursor_channels(self, bot: str) -> list[str]:
        with self._lock:
            return [r[0] for r in self._conn.execute(
                "SELECT channel_id FROM cursors WHERE bot=? ORDER BY channel_id", (bot,))]

    # --- meta ------------------------------------------------------------------------------------------------
    def get_meta(self, key: str) -> str | None:
        with self._lock:
            row = self._conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row[0] if row else None

    def set_meta(self, key: str, value: str) -> None:
        with self._tx() as c:
            c.execute("INSERT INTO meta (key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                      (key, value))

    def claim_owner(self, now: int, ttl: int = OWNER_TTL_S, key: str = "dispatcher_owner") -> bool:
        """Become (or stay, as heartbeat) the single owner of `key` (dispatcher_owner | listener_owner:<bot>);
        refused while another owner is fresh."""
        with self._tx() as c:
            row = c.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
            if row:
                cur = json.loads(row[0])
                if cur["id"] != self.instance_id and now - cur["ts"] < ttl:
                    return False
            c.execute("INSERT INTO meta (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                      (key, json.dumps({"id": self.instance_id, "ts": now})))
            return True

    def release_owner(self, key: str = "dispatcher_owner") -> None:
        """Clean shutdown: drop our lease so a restarted process takes over at once."""
        with self._tx() as c:
            row = c.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
            if row and json.loads(row[0])["id"] == self.instance_id:
                c.execute("DELETE FROM meta WHERE key=?", (key,))

    # --- dispatcher queue ------------------------------------------------------------------------------------
    def due_bots(self, now: int) -> list[str]:
        """Bots with queued/retry rows due at `now`, oldest due first."""
        with self._lock:
            return [r[0] for r in self._conn.execute(
                "SELECT bot FROM wakes WHERE status IN ('queued','retry') AND next_at<=? GROUP BY bot "
                "ORDER BY MIN(next_at), bot", (now,))]

    def claim_due(self, now: int, limit: int = 4, bot: str | None = None) -> list[Wake]:
        """Atomically flip up to `limit` due queued/retry rows (of `bot`, or any) to in_flight for this instance."""
        if limit <= 0:
            return []
        only = " AND bot=?" if bot is not None else ""
        args = (self.instance_id, now + LEASE_S, self._now(), now) + ((bot,) if bot is not None else ()) + (limit,)
        with self._tx() as c:
            rows = c.execute(
                "UPDATE wakes SET status='in_flight', claimed_by=?, lease_until=?, attempts=attempts+1, updated_at=? "
                "WHERE rowid IN (SELECT rowid FROM wakes WHERE status IN ('queued','retry') AND next_at<=?" + only +
                " ORDER BY next_at, rowid LIMIT ?) RETURNING rowid, " + _COLS, args).fetchall()
        rows.sort(key=lambda r: (r[7], r[0]))
        return [_wake(r[1:]) for r in rows]

    def _mine(self, c, bot: str, post_id: str):
        return c.execute("SELECT attempts FROM wakes WHERE bot=? AND post_id=? AND status='in_flight' AND claimed_by=?",
                         (bot, post_id, self.instance_id)).fetchone()

    def mark_delivered(self, bot: str, post_id: str) -> bool:
        now = self.clock()
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='delivered', delivered_at=?, claimed_by=NULL, lease_until=NULL, "
                             "updated_at=? WHERE bot=? AND post_id=? AND status='in_flight' AND claimed_by=?",
                             (int(now * 1000), int(now), bot, post_id, self.instance_id)).rowcount == 1

    def mark_failed(self, bot: str, post_id: str, err: str) -> bool:
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='failed', last_error=?, claimed_by=NULL, lease_until=NULL, "
                             "updated_at=? WHERE bot=? AND post_id=? AND status='in_flight' AND claimed_by=?",
                             (err, self._now(), bot, post_id, self.instance_id)).rowcount == 1

    def mark_retry(self, bot: str, post_id: str, err: str, next_at: int) -> str | None:
        """'retry', or 'failed' once attempts reached max_attempts; None if not claimed by this instance."""
        with self._tx() as c:
            row = self._mine(c, bot, post_id)
            if not row:
                return None
            status = "failed" if row[0] >= self.max_attempts else "retry"
            c.execute("UPDATE wakes SET status=?, last_error=?, next_at=?, claimed_by=NULL, lease_until=NULL, "
                      "updated_at=? WHERE bot=? AND post_id=?", (status, err, next_at, self._now(), bot, post_id))
            return status

    def fail_pending(self, bot: str, err: str) -> int:
        """Operator removed the bot: every queued/retry/in_flight wake of it becomes failed `err`."""
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='failed', last_error=?, claimed_by=NULL, lease_until=NULL, "
                             "updated_at=? WHERE bot=? AND status IN ('queued','retry','in_flight')",
                             (err, self._now(), bot)).rowcount

    def recover_stale(self, now: int) -> int:
        """Return in_flight rows whose lease expired (crashed dispatcher) to retry, due now."""
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='retry', claimed_by=NULL, lease_until=NULL, next_at=?, "
                             "updated_at=? WHERE status='in_flight' AND lease_until < ?",
                             (now, self._now(), now)).rowcount

    def requeue(self, bot: str, post_id: str) -> bool:
        """Operator retry of a failed wake: fresh attempts, due now."""
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='queued', attempts=0, next_at=?, last_error=NULL, "
                             "updated_at=? WHERE bot=? AND post_id=? AND status='failed'",
                             (self._now(), self._now(), bot, post_id)).rowcount == 1

    def prune(self, days: int = 7) -> int:
        """Delete delivered/failed rows older than `days`; never touches queued/retry/in_flight (PR-8)."""
        with self._tx() as c:
            return c.execute("DELETE FROM wakes WHERE status IN ('delivered','failed') AND updated_at < ?",
                             (self._now() - days * DAY,)).rowcount

    # --- reads -----------------------------------------------------------------------------------------------
    def _select(self, where: str = "", args=(), order: str = "rowid") -> list[Wake]:
        with self._lock:
            rows = self._conn.execute("SELECT %s FROM wakes %s ORDER BY %s" % (_COLS, where, order), args).fetchall()
        return [_wake(r) for r in rows]

    @staticmethod
    def _by(bot, where: str = "", args=()):
        if bot is None:
            return ("WHERE " + where if where else ""), tuple(args)
        return "WHERE bot=?" + (" AND " + where if where else ""), (bot, *args)

    def wake(self, bot: str, post_id: str) -> Wake | None:
        rows = self._select("WHERE bot=? AND post_id=?", (bot, post_id))
        return rows[0] if rows else None

    def wakes(self, bot: str | None = None) -> list[Wake]:
        return self._select(*self._by(bot))

    def failed(self, bot: str | None = None) -> list[Wake]:
        return self._select(*self._by(bot, "status='failed'"))

    def failed_for_post(self, post_id: str) -> list[Wake]:
        return self._select("WHERE post_id=? AND status='failed'", (post_id,))

    def last_wake(self, bot: str) -> Wake | None:
        """The bot's most recently updated wake (admin status `last wake`, /health bots_failing)."""
        rows = self._select("WHERE bot=?", (bot,), order="updated_at DESC, rowid DESC LIMIT 1")
        return rows[0] if rows else None

    def failed_count(self, since: int, bot: str | None = None) -> int:
        """Failed wakes whose last update is at or after `since` (unix s): /health wake_failed_24h."""
        where, args = self._by(bot, "status='failed' AND updated_at >= ?", (since,))
        with self._lock:
            return self._conn.execute("SELECT COUNT(*) FROM wakes " + where, args).fetchone()[0]

    def stats(self, bot: str | None = None) -> dict:
        """Counts per status and post->delivered latency (delivered_at - post_create_at, ms; PR-9)."""
        where, args = self._by(bot)
        dwhere, dargs = self._by(bot, "status='delivered' AND delivered_at IS NOT NULL AND post_create_at IS NOT NULL")
        with self._lock:
            counts = dict(self._conn.execute("SELECT status, COUNT(*) FROM wakes %s GROUP BY status" % where,
                                             args).fetchall())
            lat = sorted(r[0] for r in self._conn.execute(
                "SELECT delivered_at - post_create_at FROM wakes " + dwhere, dargs))

        def pct(p):
            return lat[max(math.ceil(p * len(lat)) - 1, 0)] if lat else None
        return {"counts": counts, "latency_ms": {"n": len(lat), "p50": pct(0.5), "p95": pct(0.95)}}


class BotState:
    """One bot's view of State (what its Listener uses): the v1 one-bot method signatures, rows/cursors scoped to
    the bot, meta keys mapped to bot:<name>:<key>, the listener lease to listener_owner:<name>."""

    def __init__(self, core: State, name: str):
        self.core, self.name = core, name

    @property
    def instance_id(self) -> str:
        return self.core.instance_id

    @property
    def clock(self):
        return self.core.clock

    def enqueue(self, post_id, channel_id, payload, post_create_at=None) -> bool:
        return self.core.enqueue(self.name, post_id, channel_id, payload, post_create_at)

    def enqueue_and_advance(self, post_id, channel_id, payload, create_at) -> bool:
        return self.core.enqueue_and_advance(self.name, post_id, channel_id, payload, create_at)

    def get_cursor(self, channel_id):
        return self.core.get_cursor(self.name, channel_id)

    def set_cursor(self, channel_id, create_at, post_id=""):
        self.core.set_cursor(self.name, channel_id, create_at, post_id)

    def delete_cursor(self, channel_id):
        self.core.delete_cursor(self.name, channel_id)

    def cursor_channels(self):
        return self.core.cursor_channels(self.name)

    def get_meta(self, key):
        return self.core.get_meta(meta_key(self.name, key))

    def set_meta(self, key, value):
        self.core.set_meta(meta_key(self.name, key), value)

    def claim_owner(self, now, ttl=OWNER_TTL_S, key="listener_owner") -> bool:
        return self.core.claim_owner(now, ttl, "%s:%s" % (key, self.name))

    def release_owner(self, key="listener_owner") -> None:
        self.core.release_owner("%s:%s" % (key, self.name))

    def wake(self, post_id):
        return self.core.wake(self.name, post_id)

    def wakes(self):
        return self.core.wakes(self.name)

    def failed(self):
        return self.core.failed(self.name)

    def close(self):
        self.core.close()
