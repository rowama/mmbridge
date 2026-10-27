---
id: SLICE-20261027-lb2-state-db-wake-queue
type: slice
phase: implement
status: done             # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
plan_phase: 2
review: required (persistence/dedupe correctness, ADR-0009) - thoughts/shared/verification/2026-10-27-slice-20261027-lb2-state-db-wake-queue-review.md
reqs: [REQ-A4, REQ-A8]
specs: none - no event source/receiver yet; at-most-once ledger and retry bookkeeping proven by unit tests; specs for A4/A8 turn green in slices 4-5
---
# Slice 2: State DB + wake queue

Plan: [thoughts/shared/plans/2026-10-27-live-bots.md](../plans/2026-10-27-live-bots.md) Phase 2. Architecture: docs/architecture/2026-10-26-live-bots.md. **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
`app/state.py` gives a SQLite (WAL) ledger: enqueue a wake once per post id, claim due wakes, mark delivered/retry/failed, cursors, meta; `admin failed`/`admin stats` read it.

## Acceptance criteria
- [x] `app/state.py`: `State(path)`; schema per architecture (`wakes`, `cursors`, `meta`); `enqueue(post_id, channel_id, payload) -> bool` (INSERT OR IGNORE: the single dedupe gate); `claim_due(now, limit) -> list[Wake]`; `mark_delivered`, `mark_retry(post_id, err, next_at)`, `mark_failed(post_id, err)`; `requeue(post_id)`; `get/set_cursor`; `get/set_meta`; `prune(older_than_days=7)`; no tokens/secrets columns
- [x] Backoff helper `next_delay(attempt) -> 2,4,8,16,32 s`, `WAKE_MAX_ATTEMPTS` default 5
- [x] `app/admin.py`: `failed [--retry POST_ID]`, `stats` (counts, p95 enqueue->delivered latency)
- [x] Unwritable /data -> `StateError('state_unwritable')`
- [x] (PR-1) Atomic `claim_due` (BEGIN IMMEDIATE + in_flight + claimed_by + lease), `recover_stale`, claimer-checked `mark_*`, `meta.dispatcher_owner` heartbeat; concurrency/crash tests per plan Phase 2
- [x] (PR-3) `enqueue_and_advance` atomic enqueue+cursor, cursor `(create_at, post_id)` forward-only
- [x] (PR-9) store `post_create_at`/`delivered_at`; `stats` latency = delivered_at - post_create_at
- [x] (PR-8) `prune(7)` terminal-only; tests keep non-terminal rows
- [x] Plan Phase 2 Automated Verification all exit 0; existing MCP suite (`.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`) still green

## Tasks
- [x] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red) - n/a, see specs:
- [x] Write failing unit tests (tests/unit/) for the behaviours above
- [x] Implement
- [x] Run Phase 2 automated verification (plan), including this slice's specs (now green)
- [x] Do not edit locked files: tests/acceptance/specs/**, DSL public interface (CP-C speclock)

## Size check
~170 lines + tests

## Progress log
<!-- date - agent - what changed (file:line) -->
- 2026-10-27 - claude-code - specs: none (n/a). Wrote tests first: tests/unit/test_state.py (20 tests) + 4 admin tests in tests/unit/test_admin.py; red = `ImportError: cannot import name 'state'` / argparse exit 2 for `failed`/`stats`.
- 2026-10-27 - claude-code - app/state.py (new): schema + WAL + write probe (`State.__init__`, StateError('state_unwritable')); `enqueue` INSERT OR IGNORE; `enqueue_and_advance` + `_advance` forward-only `(create_at, post_id)` row-value compare; `claim_due` BEGIN IMMEDIATE + `UPDATE ... RETURNING` (in_flight, claimed_by, lease_until=now+30, attempts+1); claimer-checked `mark_delivered|mark_failed|mark_retry` (mark_retry -> 'failed' at max_attempts); `recover_stale`; `requeue` (failed only); `claim_owner` (meta.dispatcher_owner heartbeat, TTL 60 s); `prune` terminal-only; `stats` counts + p50/p95 of delivered_at - post_create_at (ms); `next_delay` 2..32 s x WAKE_BACKOFF_SCALE; WAKE_MAX_ATTEMPTS default 5.
- 2026-10-27 - claude-code - app/admin.py: `failed [--retry POST_ID]` (never prints message text; unknown/non-failed -> `not_found`), `stats` ("no wakes yet" on empty DB); StateError -> `error: state_unwritable`. Commit 6551dd9.
- 2026-10-27 - claude-code - Phase 2 automated verification: `.venv/bin/pytest tests/unit -q` exit 0 (138 passed); `.venv/bin/pytest tests/acceptance -q` exit 0 (16 passed, 9 live skipped); `python3 .eng/bin/eng-check .` exit 0; `python3 .eng/bin/eng-spec status .` matches lock. Concurrency/owner/stale tests run 5x, stable.
- 2026-10-27 - claude-code - Codex slice review (eng-run code-review, base 37e7131): 1 finding P2 (Windows collection: `os.geteuid` in skipif) fixed dc9efe0; review file status addressed. Re-ran `.venv/bin/pytest tests/unit -q` exit 0 (138 passed). Slice -> review.

## Blockers / deviations from plan
- Status values follow plan PR-1 (`queued|retry|in_flight|delivered|failed`), not the older architecture CHECK (`pending|delivered|failed`).
- Cursor API follows PR-3 (`(create_at, post_id)`) rather than the plan's earlier key signature: `get_cursor -> (create_at, post_id) | None`, `set_cursor(channel_id, create_at, post_id="")`.
- Additions not named in the plan signature block: `State(path, instance_id=None, clock=time.time, max_attempts=None)`; `enqueue(..., post_create_at=None)`; `claim_owner(now, ttl=60)` for the dispatcher heartbeat; read helpers `wake`, `wakes`, `failed`, `stats`; `mark_retry` returns 'retry'|'failed'|None.
- `attempts` is incremented at claim time (so the claimed Wake carries the attempt number for the lb4 payload); a stale lease recovered by `recover_stale` counts as an attempt.
- `mark_failed` is claimer-checked; lb4's `bot_rotated` (failing queued rows not claimed) will need its own method.
- Size: app/state.py 272 lines (estimate ~170) because of PR-1/3/8/9 additions.
