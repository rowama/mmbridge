---
id: VERIF-20261027-lb4-signed-wake-dispatcher
type: verification
phase: verify
status: fail
owner_agent: eddie
date: 2026-10-27
links: [thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md, thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
git_commit: 6fc2ce1
---
# Verification: SLICE-20261027-lb4-signed-wake-dispatcher

## Implementation status
- [x] Phase 4: signed wake dispatcher - implemented (commits 446047a, 068ab22; unblock fix 6fc2ce1, DM-only bot `channels: []`)

## Automated verification (re-executed in this session on Merkle WSL)
| Command | Exit | Notes |
|---|---|---|
| .venv/bin/pytest tests/unit -q (x3) | 0 | 217 passed, 14 warnings each run (~11.7s); stable |
| .venv/bin/pytest tests/acceptance -q | 0 | 16 passed, 9 skipped |
| PR-12 explicit 7 node ids (`--channel live`) | 0 | 7 passed |
| .venv/bin/pytest -q --channel live tests/acceptance/specs/test_live_bots.py (info) | 1 | 8 passed, 1 failed: `test_post_during_connection_drop_wakes_exactly_once_after_reconnect` - reconnect is lb5 scope (drop/restore_connection not built), expected |
| python3 .eng/bin/eng-check . | 0 | 0 errors, 0 warnings |
| python3 .eng/bin/eng-spec status . | 0 | lock approval ok; specs and DSL interface match the lock |

## Executable specs (v2.5)
| REQ | specs | result |
|---|---|---|
| REQ-A1/A2/A3/A4/A8 (card specs:) | 7 PR-12 node ids in tests/acceptance/specs/test_live_bots.py | 7/7 pass |

Spec lock: clean (speclock sha256:3108f1fe6a93cfae). No locked spec or DSL step edited; driver `tests/acceptance/drivers/live.py` (free layer) omits `--channels` for an empty list.

## Code review findings
Diff 5f70402..6fc2ce1: app/wake.py (sign/verify/Dispatcher), listener meta bot_user_id, store/admin empty channel list, wake receiver + in-process live driver, fake MM mm_ids, 41 new unit tests.
- HMAC: constant-time compare, v1 only, 300 s skew, signed bytes = sent bytes, no token in payload/headers/logs. Pass.
- Unblock fix: `channels: []` accepted, ids still validated; `--channels ""` still refused; `--channels` omitted = DM-only. Pass.
- Deviations on card (no cfg_gen column; standby second dispatcher) acceptable, but see Codex P1: the meta-based rotation check is what the review breaks.

## Cross-model review
`eng-run code-review SLICE-20261027-lb4-signed-wake-dispatcher --base 5f70402` (codex, run log thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb4-signed-wake-dispatcher-2.md). eng-run's parser recorded "No findings" in review-2.md, but Codex reported two (first run without --base reviewed an empty diff, discarded):
- **[P1] app/wake.py:93-99** - after a token swap and restart, meta `bot_user_id` still names the previous bot until the listener's users/me completes; the dispatcher can sign old-bot queued wakes with the new bot's url/secret and send them to the new target. Missing meta (`bot_id` None) skips the check entirely. Verifier agrees: real, security-relevant (message content to the wrong receiver), not covered by tests. Fix: dispatcher must not claim/send until the current config's identity is resolved (e.g. `identity` provider from the listener; no meta -> no send) + unit test for restart-after-rotation.
- **[P2] app/wake.py:108-112** - `timeout=5` is per network op, not total; a slow-drip receiver can stall `tick()` and heartbeats, letting another dispatcher take over and redeliver. Verifier agrees. Fix: `asyncio.wait_for(post, TIMEOUT_S)` -> retryable `timeout` + unit test.

## Definition of Done
- [x] Automated checks green (unit x3, acceptance, PR-12 7/7, eng-check, eng-spec)
- [ ] Independent review findings resolved - P1, P2 open
- [ ] Manual verification (Rob, CP-S) - not requested yet

## Result
**FAIL** - back to implementer for P1 and P2 (small, app/wake.py + 2 unit tests). Not pushed. Re-verify after fix, then CP-S.
