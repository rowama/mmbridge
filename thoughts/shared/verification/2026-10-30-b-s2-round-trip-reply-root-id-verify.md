---
id: VERIFY-20261030-b-s2-round-trip-reply-root-id
type: verification
phase: verify
status: pass             # draft | pass | fail
owner_agent: grok-bot
date: 2026-10-30
links: [thoughts/shared/slices/2026-10-28-b-s2-round-trip-reply-root-id.md, thoughts/shared/verification/2026-10-30-slice-20261028-b-s2-round-trip-reply-root-id-review.md]
plan: thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md
git_commit: 30dea81
---
# Verification: B-s2 round-trip reply, root_id, relay tripwire (plan Phase 2)

Verifier: grok-bot (planner). Implementer: claude-code (e68ee8f, 6be652b, 30dea81). grok-bot wrote no code. No `--allow-self-review`. Base d5dc1ae.

## Re-executed Automated Verification (plan Phase 2 block, WSL, LIVE_IMAGE=mmbridge:bs2 RELAY_IMAGE=mmbridge-relay:bs2, images rebuilt)
| Run | unit | mcp | live in-process (A+B1+B2) | live container (A+B1+B2) |
|---|---|---|---|---|
| 1 | 392 passed | 16 passed, 36 skipped | 29 passed | 29 passed |
| 2 | 392 passed | 16 passed, 36 skipped | 29 passed | 29 passed |
| 3 | 392 passed | 16 passed, 36 skipped | 29 passed | 29 passed |
All exit 0. `eng-check .` OK (0 errors, 3 known warnings). `eng-spec status .`: lock approval ok (2026-10-29); specs and DSL interface match the lock.

## Executable specs
| REQ | Spec | Result |
|---|---|---|
| REQ-B2 | test_bot_answer_appears_in_channel_and_does_not_wake_it_again, test_bot_answer_to_thread_reply_lands_in_that_thread | pass x3 both channels |
| REQ-B5 | test_bot_answer_to_dm_appears_in_that_dm (+ B1 security specs) | pass x3 both channels |
`eng-spec trace .` prints "(not in an approved design)" for REQ-B*: known tooling issue (TODOS P3), not a spec gap. Later-slice (B-s3) specs not selected, per plan.

## Diff review
- root_id: 26-char validation; root fetched with bot token before any write; must be top-level post in target channel/DM; MM 400/403/404 -> invalid_root; dm_send fetches root before opening a DM. Matches ADR-0015 and plan review #8 (foreign channel / other DM -> invalid_root, no post: unit-tested).
- listener payload v2 (version, issued_at, reply hints) per architecture contract; DM hints root_id null (contract; accepted by planner - DM-thread answers land at DM top level; revisit if Rob wants otherwise).
- relay Tripwire: bad_sig>5/10min (bounded buckets), rate limit, upstream 401/403, count drift; /health double_forward_24h; optional MM alert env.
- No locked spec, DSL interface, or assertion step body changed. No weakened tests, skips or suppressions found. OQ-B2 fallback `text` not needed (spike chose verbatim body).
- OWNER-GUIDE not edited (Rob's uncommitted changes); routine text in relay/README.md - acceptable per card ("relay/README.md or OWNER-GUIDE").

## Cross-model review
Reviewer codex, `codex review --base d5dc1ae`; 2 P2 (reply-as-root accepted; unbounded bad-sig list), both fixed in 6be652b with tests; 0 high. eng-run "No findings." bug logged in process-feedback.

## DoD
Tests-first evidence (handoff: red specs + 46 failing units) pass; automated block 3x pass; review addressed pass; CHANGELOG pass; docs pass; secrets/no-log (B1 spec) pass; manual verification -> CP-S.

## Verdict
PASS. Next: CP-S (Rob manual verification).
