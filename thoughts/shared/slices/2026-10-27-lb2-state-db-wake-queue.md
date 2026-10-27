---
id: SLICE-20261027-lb2-state-db-wake-queue
type: slice
phase: implement
status: todo             # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
plan_phase: 2
review: required (persistence/dedupe correctness, ADR-0009) - thoughts/shared/verification/2026-10-27-lb2-review.md
reqs: [REQ-A4, REQ-A8]
specs: none - no event source/receiver yet; at-most-once ledger and retry bookkeeping proven by unit tests; specs for A4/A8 turn green in slices 4-5
---
# Slice 2: State DB + wake queue

Plan: [thoughts/shared/plans/2026-10-27-live-bots.md](../plans/2026-10-27-live-bots.md) Phase 2. Architecture: docs/architecture/2026-10-26-live-bots.md. **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
`app/state.py` gives a SQLite (WAL) ledger: enqueue a wake once per post id, claim due wakes, mark delivered/retry/failed, cursors, meta; `admin failed`/`admin stats` read it.

## Acceptance criteria
- [ ] `app/state.py`: `State(path)`; schema per architecture (`wakes`, `cursors`, `meta`); `enqueue(post_id, channel_id, payload) -> bool` (INSERT OR IGNORE: the single dedupe gate); `claim_due(now, limit) -> list[Wake]`; `mark_delivered`, `mark_retry(post_id, err, next_at)`, `mark_failed(post_id, err)`; `requeue(post_id)`; `get/set_cursor`; `get/set_meta`; `prune(older_than_days=7)`; no tokens/secrets columns
- [ ] Backoff helper `next_delay(attempt) -> 2,4,8,16,32 s`, `WAKE_MAX_ATTEMPTS` default 5
- [ ] `app/admin.py`: `failed [--retry POST_ID]`, `stats` (counts, p95 enqueue->delivered latency)
- [ ] Unwritable /data -> `StateError('state_unwritable')`
- [ ] (PR-1) Atomic `claim_due` (BEGIN IMMEDIATE + in_flight + claimed_by + lease), `recover_stale`, claimer-checked `mark_*`, `meta.dispatcher_owner` heartbeat; concurrency/crash tests per plan Phase 2
- [ ] (PR-3) `enqueue_and_advance` atomic enqueue+cursor, cursor `(create_at, post_id)` forward-only
- [ ] (PR-9) store `post_create_at`/`delivered_at`; `stats` latency = delivered_at - post_create_at
- [ ] (PR-8) `prune(7)` terminal-only; tests keep non-terminal rows
- [ ] Plan Phase 2 Automated Verification all exit 0; existing MCP suite (`.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`) still green

## Tasks
- [ ] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red) - n/a, see specs:
- [ ] Write failing unit tests (tests/unit/) for the behaviours above
- [ ] Implement
- [ ] Run Phase 2 automated verification (plan), including this slice's specs (now green)
- [ ] Do not edit locked files: tests/acceptance/specs/**, DSL public interface (CP-C speclock)

## Size check
~170 lines + tests

## Progress log
<!-- date - agent - what changed (file:line) -->

## Blockers / deviations from plan
none
