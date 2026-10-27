---
id: VERIF-20261027-lb1-bot-store-admin-cli
type: verification
phase: verify
status: pass
owner_agent: eddie
date: 2026-10-27
links: [thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md, thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
git_commit: 49a4e51
---
# Verification: SLICE-20261027-lb1-bot-store-admin-cli

## Implementation status
- [x] Phase 1: Encrypted bot store + admin CLI — complete (slice status review)

## Automated verification (re-executed in this session; paste exit codes)
| Command | Exit | Notes |
|---|---|---|
| .venv/bin/pytest tests/unit -q | 0 | 114 passed in 6.35s |
| .venv/bin/pytest tests/acceptance -q | 0 | 16 passed, 9 skipped (live-bot specs deferred to later slices) |
| python3 .eng/bin/eng-check . | 0 | 0 errors, 0 warnings, 73 artifacts |
| python3 .eng/bin/eng-spec status . | 0 | lock approval ok (2026-10-27); specs/DSL match lock |
| docker build -t mmbridge:lb1-verify . | 0 | image builds; /data uid 10001 mode 700 in Dockerfile |

## Executable specs (v2.5)
| REQ | design doc | specs | result |
|---|---|---|---|
| REQ-A7 | docs/design/2026-10-26-live-bots.md | tests/acceptance/specs/test_live_bots.py (token secrecy) | n/a this slice — card specs: none; proven by unit tests; e2e turns green in lb5 |

Spec lock: clean — eng-spec status match; speclock sha256:3108f1fe6a93cfae (CP-C 2026-10-27).

## Code review findings
Diff 691f4ac...cf78905 (+docs 49a4e51) matches Phase 1: pp/store.py, pp/admin.py, logging redaction, cryptography pin, Dockerfile /data. Deviations (recorded on slice card, accepted by planner for CP-S):
1. Extra StoreError code store_invalid for save-time validation.
2. Wake secret via --wake-secret-stdin (not argv) so it never hits shell history.
3. 
otate-key defaults MMB_STORE_KEY_NEW / MMB_STORE_KEY.
No weakened tests, timeouts, skips, or suppressions in new unit tests. Live acceptance specs remain skipped until later slices (expected).

## Cross-model review (advisory)
- Findings file: 	houghts/shared/verification/2026-10-27-slice-20261027-lb1-bot-store-admin-cli-review.md
- Reviewer: codex (codex review --base 691f4ac); run log 	houghts/shared/runs/2026-10-27-code-review-slice-20261027-lb1-bot-store-admin-cli.md
- Findings: 0 (No actionable regressions). Status addressed.
- Note: review was started during the implement eng-run (same Merkle session). Advisory only; no high findings.

## Manual verification required (for Rob)
- [ ] In a container with /data + MMB_STORE_KEY, run python -m app.admin set-bot with a real bot token; confirm wake secret prints once.
- [ ] python -m app.admin show masks token to last 4 and never prints the secret.
- [ ] xxd /data/bots.enc (or equivalent) shows no plaintext token/secret.

## Definition of Done
- Automated verification re-run: **pass**
- Cross-model review present for security slice: **pass** (0 findings)
- Specs lock unchanged: **pass**
- Manual operator check: **pending CP-S**
- Deploy prerequisites (Coolify /data, key) not required to mark slice done until enable: **n.a. for lb1**

## Verdict
**PASS** (automated). Open for Rob **CP-S** manual steps above. Follow-ups: none required for lb1; lb4/lb5 fake channel-id length noted on slice card.
