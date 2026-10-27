---
id: VERIF-20261027-lb2-state-db-wake-queue
type: verification
phase: verify
status: pass
owner_agent: eddie
date: 2026-10-27
links: [thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md, thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
git_commit: 5899378
---
# Verification: SLICE-20261027-lb2-state-db-wake-queue

## Implementation status
- [x] Phase 2: State DB + wake queue - complete (slice status review; commits 6551dd9, dc9efe0, 5899378)

## Automated verification (re-executed in this session on Merkle WSL; paste exit codes)
| Command | Exit | Notes |
|---|---|---|
| .venv/bin/pytest tests/unit -q | 0 | 138 passed in 6.01s |
| .venv/bin/pytest tests/unit/test_state.py -q (x3) | 0 | 20 passed each run (concurrency/owner/lease tests stable) |
| .venv/bin/pytest tests/acceptance -q | 0 | 16 passed, 9 skipped (live-bot specs deferred to lb5) |
| python3 .eng/bin/eng-check . | 0 | 0 errors, 0 warnings, 78 artifacts |
| python3 .eng/bin/eng-spec status . | 0 | lock approval ok (2026-10-27); specs and DSL interface match the lock |

## Executable specs (v2.5)
| REQ | design doc | specs | result |
|---|---|---|---|
| REQ-A4, REQ-A8 | docs/design/2026-10-26-live-bots.md | tests/acceptance/specs/test_live_bots.py | n/a this slice - no listener yet; proven by unit tests; e2e green in lb5 |

Spec lock: clean (speclock sha256:3108f1fe6a93cfae, CP-C 2026-10-27). No locked spec or DSL step edited.

## Code review findings
Diff 37e7131...5899378 matches Phase 2: app/state.py (new, WAL, wakes/cursors/meta), app/admin.py failed [--retry]/stats, tests/unit/test_state.py (20), test_admin.py (+4).
- PR-1: claim_due is one BEGIN IMMEDIATE UPDATE ... RETURNING; mark_* require claimed_by match; recover_stale on lease expiry; claim_owner heartbeat - present and tested.
- PR-3: enqueue_and_advance in one transaction; cursor (create_at, post_id) forward-only via tuple compare - present and tested.
- PR-8: prune deletes only delivered|failed - present and tested. PR-9: latency from post_create_at - present and tested.
- Schema has no token/secret column (tested).
Deviations (recorded on slice card, accepted by planner): status set queued|retry|in_flight|delivered|failed (plan PR-1 over older architecture text); cursor tuple (PR-3 over signature list); state.py 272 lines vs ~170 estimate.
Weakened tests / skips: one added skipif on the read-only-dir test (`os.name != "posix" or os.geteuid() == 0`) - legitimate platform/root guard from Codex P2; runs on Linux non-root (ran here). No timeouts or suppressions added.
Notes (low, follow-up): UPDATE ... RETURNING needs SQLite >= 3.35 (Merkle 3.46.1; python:3.12-slim ships newer) - fine. lb4 will need a method to fail still-queued wakes on bot_rotated (mark_failed only for claimed rows).

## Cross-model review (advisory)
- Findings file: thoughts/shared/verification/2026-10-27-slice-20261027-lb2-state-db-wake-queue-review.md
- Reviewer: codex (codex review --base 37e7131); run log thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb2-state-db-wake-queue.md
- Findings: 1 P2 (medium) - fixed in dc9efe0. 0 high. Status addressed.

## Manual verification required (for Rob)
- [ ] On an empty DB (e.g. `MMB_DATA_DIR=$(mktemp -d)` locally, or in the container with /data), `python -m app.admin failed` prints "no failed wakes".
- [ ] Same DB, `python -m app.admin stats` prints "no wakes yet".

## Definition of Done
- Automated verification re-run: **pass**
- Cross-model review present (required, persistence/dedupe): **pass** (1 medium fixed)
- Spec lock unchanged: **pass**
- No secrets in state: **pass** (schema test)
- Manual operator check: **pending CP-S**

## Verdict
**PASS** (automated). Open for Rob **CP-S** manual steps above. Follow-up for lb4: queued-wake fail path on bot_rotated.
