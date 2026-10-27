---
id: VERIF-20261027-lb4-signed-wake-dispatcher
type: verification
phase: verify
status: pass
owner_agent: eddie
date: 2026-10-27
links: [thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md, thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
git_commit: 219a9a1
---
# Verification: SLICE-20261027-lb4-signed-wake-dispatcher

## Implementation status
- [x] Phase 4: signed wake dispatcher - implemented (commits 446047a, 068ab22; unblock fix 6fc2ce1, DM-only bot `channels: []`; review fixes b061bc3, 1115bc2, e7d4156, 837a9c0, 219a9a1)

## Automated verification (re-executed on Merkle WSL at 219a9a1)
| Command | Exit | Notes |
|---|---|---|
| .venv/bin/pytest tests/unit -q (x3) | 0 | 229 passed, 14 warnings each run (~12.8s); stable |
| .venv/bin/pytest tests/acceptance -q | 0 | 16 passed, 9 skipped |
| PR-12 explicit 7 node ids from card `specs:` (`--channel live`) | 0 | 7 passed |
| python3 .eng/bin/eng-check . | 0 | 0 errors, 0 warnings |
| python3 .eng/bin/eng-spec status . | 0 | lock approval ok; specs and DSL interface match the lock |

Info (previous run, unchanged scope): full live spec file has 1 expected failure, `test_post_during_connection_drop_wakes_exactly_once_after_reconnect` (reconnect, lb5).

## Executable specs (v2.5)
| REQ | specs | result |
|---|---|---|
| REQ-A1/A2/A3/A4/A8 (card specs:) | 7 PR-12 node ids in tests/acceptance/specs/test_live_bots.py | 7/7 pass |

Spec lock: clean (speclock sha256:3108f1fe6a93cfae). No locked spec or DSL step edited.

## Code review findings
Diff 5f70402..219a9a1: app/wake.py (sign/verify/Dispatcher), listener meta identity, store/admin empty channel list + URL parse check, wake receiver + in-process live driver, fake MM mm_ids, 53 new unit tests.
- HMAC: constant-time compare, v1 only, 300 s skew, signed bytes = sent bytes, X-MMB-Delivery bound to signed delivery_id, no token in payload/headers/logs. Pass.
- Identity gate: dispatcher claims nothing until meta `bot_identity` = "<token_fp>:<bot_user_id>" (one row, written by the listener after users/me) matches the current token; old-bot wakes fail `bot_rotated`. Pass.
- Robustness: overall 5 s POST deadline; malformed URL permanent `invalid_url`; any other send error retried; nothing escapes tick()/run(). Pass.

## Cross-model review
`eng-run code-review SLICE-20261027-lb4-signed-wake-dispatcher --base 5f70402` (codex). eng-run's parser wrote "No findings" for every run; findings below are from the terminal output.
| Run log suffix (thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb4-signed-wake-dispatcher*.md) | Finding | Disposition |
|---|---|---|
| -2 | [P1] stale/missing bot_user_id let old wakes go to a new bot | fixed b061bc3 (token fingerprint gate; tests no_identity, restart_after_token_swap) |
| -2 | [P2] timeout per network step, not total | fixed b061bc3 (asyncio.wait_for; test drip_response_hits_overall_deadline) |
| (no suffix) | [P2] unsigned X-MMB-Delivery allows replay under a new key | fixed 1115bc2 (verify requires header == signed delivery_id; 4 reject cases) |
| -3 | [P2] bot_user_id and fp read separately: rotation race | fixed e7d4156 (single meta row bot_identity; test identity_is_one_snapshot) |
| -4 | [P2] malformed wake_url raised InvalidURL out of tick | fixed 837a9c0 (https_ok parses URL; invalid_url permanent; 2 tests) |
| -5 | [P2] DecodingError escaped tick | fixed 219a9a1 (HTTPError/any error -> retry; 2 tests) |
| -6 | none: "No actionable defects were identified" | - |

## Definition of Done
- [x] Automated checks green (unit x3, acceptance, PR-12 7/7, eng-check, eng-spec)
- [x] Independent review findings resolved (all fixed; final review clean)
- [ ] Manual verification (Rob, CP-S): run the README "Wake receiver" example (added with this report) against a local dispatcher and see a signed wake accepted; a hand-tampered request (body, timestamp or X-MMB-Delivery changed) is rejected 401

## Result
**PASS** - pushed to main; CP-S pending (manual check above).
