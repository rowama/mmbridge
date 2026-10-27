---
id: PLANREV-20261027-live-bots-2
type: review-findings
phase: plan
status: addressed        # open | addressed | closed
owner_agent: grok-bot
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md]
review_kind: plan
subject: thoughts/shared/plans/2026-10-27-live-bots.md + thoughts/shared/slices/2026-10-27-lb*.md
diff: n.a.
reviewer: codex
command: python3 .eng/bin/eng-run plan-review thoughts/shared/plans/2026-10-27-live-bots.md (run on Merkle; log thoughts/shared/runs/2026-10-27-plan-review-live-bots.md)
---
# Independent review: Live bots (canonical; supersedes stub 2026-10-27-live-bots-plan-review.md)
Findings reconstructed on the box from the Codex output summary (full raw output is on Merkle in this same path; Merkle copy may be merged on next pull). Tests named here live in plan Phase sections, tagged (PR-n).

## Findings
| # | Severity | Location | Finding | Disposition | Reason / approval |
|---|---|---|---|---|---|
| 1 | high | plan Phase 2/4 | claim_due lacks atomic claim, in-flight state, crash recovery, dispatcher ownership + tests | fixed (thoughts/shared/plans/2026-10-27-live-bots.md Phase 2 + Phase 4; thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md, thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md) | BEGIN IMMEDIATE claim -> in_flight+lease, recover_stale, claimer-checked mark_*, meta.dispatcher_owner; concurrency/crash tests |
| 2 | high | plan Phase 4/5 | No coordinated store reload for listener+dispatcher; queued wake ownership on bot/token/secret/target rotation + tests | fixed (thoughts/shared/plans/2026-10-27-live-bots.md Phase 4 + Phase 5; thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md, thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md) | ConfigHolder single reload, send-time config, bot_rotated failure; rotation tests |
| 3 | high | plan Phase 2/3/5 | Catch-up: pagination, equal timestamps, DM discovery during outage, atomic cursor/enqueue + recovery tests | fixed (thoughts/shared/plans/2026-10-27-live-bots.md Phase 2/3/5; thoughts/shared/slices/2026-10-27-lb2-*, thoughts/shared/slices/2026-10-27-lb3-listener-filters.md, thoughts/shared/slices/2026-10-27-lb5-*) | paged since=, (create_at,post_id) cursor, /users/me/channels DM discovery, enqueue_and_advance; pagination/tie/crash tests |
| 4 | high | plan Phase 5 | Seq-gap catch-up, restart with pending wakes, task crash supervision while MCP up + tests | fixed (thoughts/shared/plans/2026-10-27-live-bots.md Phase 5; thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md) | seq gap -> catch-up; supervisor restart + degraded health; startup drains pending exactly once |
| 5 | medium | plan Phase 4 | Forged-wake tests only exercise receiver verify; need bridge-generated sig tests + tamper/skew/unknown version | fixed (thoughts/shared/plans/2026-10-27-live-bots.md Phase 4; thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md) | independent recompute of dispatcher-sent signature, tamper/skew/v2/missing header |
| 6 | medium | plan Phase 1 | Wake secret min strength + config schema/version validation on load | fixed (thoughts/shared/plans/2026-10-27-live-bots.md Phase 1; thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md) | >=32 chars, version==1, field/url/channel validation + tests |
| 7 | medium | plan Phase 1 | ADR-0006 rotate-key MultiFernet not in any slice | fixed (thoughts/shared/plans/2026-10-27-live-bots.md Phase 1; thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md) | admin rotate-key + MMB_STORE_KEY new,old + tests |
| 8 | medium | plan Phase 2/4 | 7-day prune of terminal wakes not scheduled at runtime + tests | fixed (thoughts/shared/plans/2026-10-27-live-bots.md Phase 2 + Phase 4; thoughts/shared/slices/2026-10-27-lb2-*, thoughts/shared/slices/2026-10-27-lb4-*) | prune on start + every 6 h, fake-clock test |
| 9 | medium | plan Phase 2 | admin stats latency must be post create_at -> delivery, not enqueue | fixed (thoughts/shared/plans/2026-10-27-live-bots.md Phase 2; thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md) | post_create_at/delivered_at columns + test |
| 10 | medium | slice lb5 | health must be connecting/ok + wake_failed_24h per architecture (not "on") | fixed (thoughts/shared/plans/2026-10-27-live-bots.md Phase 5 + Demo step 3; thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md) | matches docs/architecture/2026-10-26-live-bots.md:145 |
| 11 | medium | plan Testing Strategy | add eng-spec trace to Testing Strategy / verification report | fixed (thoughts/shared/plans/2026-10-27-live-bots.md Testing Strategy; thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md) | status + trace in every verification report |
| 12 | low | plan Phase 4 | -k expression misses own_post spec | fixed (thoughts/shared/plans/2026-10-27-live-bots.md Phase 4 Automated Verification; thoughts/shared/slices/2026-10-27-lb4-*, thoughts/shared/slices/2026-10-27-lb5-* Tasks) | explicit node ids, exactly 7 passed |

## Status
No open critical/high. Specs unchanged (all fixes are unit/integration tests in tests/unit), speclock unchanged sha256:3108f1fe6a93cfae. Ready for CP-C.
