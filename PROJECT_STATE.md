---
id: STATE
type: project-state
phase: implement
status: active
owner_agent: grok-bot
date: 2026-10-30
links: []
triage: large             # unset | small | medium | large
active_slice: SLICE-20261028-b-s2-round-trip-reply-root-id
# Single source of truth for approvals. One item per line: "CP-X: <path> - <decision needed>".
# Later checkpoints (e.g. CP-B while in discover) may be listed early. Quote items containing commas.
pending_approvals: []
# Working agreements (see PROCESS.md section 10). Never hard-code these in design docs.
implementer: claude-code      # who writes code (default: Claude Code on the owner's PC)
planner: grok-bot             # who plans, writes docs, keeps state and process
cross_review: codex-advisory  # codex-advisory | none  (advisory, never a gate)
push_permission: standing     # standing: after eng-verify PASS may push main; tags/force-push still ask (Rob 2026-10-26)
board: none                   # none | vikunja (optional, board only; repo stays the source of truth)
acceptance: executable-specs   # v2.5: tests/acceptance/, see PROCESS.md 13
---
# PROJECT_STATE

> Single entry point. Any agent reads THIS file first, then the latest handoff linked below.
> Update it at the end of every session. Keep it under one screen.

## Current phase
implement (increment B: Grok Bot webhook wake + multi-bot; architecture B done, see Approval log). v0.3.0 Live bots shipped 2026-10-28 (93b4f7d, tag v0.3.0).

## Goal (one sentence)
A public HTTPS MCP bridge (Python, deployed on Coolify at chats.rmlab.cloud) that lets Grok Bots read and post in Rob's self-hosted Mattermost, each bot using its own Mattermost bot token.

## Active slice
[SLICE-20261028-b-s2-round-trip-reply-root-id](thoughts/shared/slices/2026-10-28-b-s2-round-trip-reply-root-id.md) (todo; next for implementer). Previous: B-s1 [done](thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md) (CP-S 2026-10-30)

## Next action
B-s2 (round-trip reply, root_id, relay tripwire; plan Phase 2, security review required): implementer (Claude Code) runs eng-implement-slice on [the slice card](thoughts/shared/slices/2026-10-28-b-s2-round-trip-reply-root-id.md), then Codex review + eng-verify, then CP-S (Rob: "@eddie status?" answer in channel/thread/DM, no re-wake). OQ-B2 = verbatim body (spike), so no `text` fallback field needed. Then B-s3.

B-s1 done (CP-S 2026-10-30). Ops lesson: if mmbridge boots with store_unreadable (no bots.enc yet), a config reload does not start the WS listener; restart the mmbridge container after the first set-bot (candidate fix/TODO). http-wake-internal-hosts slice (8c60bc8) in review, exercised live by the B-s1 demo. Open: live Mattermost-restart resume check (TODOS, deferred); OWNER-GUIDE pointer (TODOS P2); flaky timing tests (TODOS P2).

## Blockers
- none

## Pending approvals
See `pending_approvals` in the front matter (the only copy; `.eng/bin/eng-status` renders it). Do not list items here.

## Back-ups to an earlier phase
<!-- date - from phase -> to phase - why (blameless) - artifacts revised -->
none

## Latest artifacts
- B-s1 verify: [thoughts/shared/verification/2026-10-29-b-s1-relay-grok-wake-one-bot-verify.md](thoughts/shared/verification/2026-10-29-b-s1-relay-grok-wake-one-bot-verify.md); review: [thoughts/shared/verification/2026-10-29-slice-20261028-b-s1-relay-grok-wake-one-bot-review-2.md](thoughts/shared/verification/2026-10-29-slice-20261028-b-s1-relay-grok-wake-one-bot-review-2.md); handoff: [thoughts/shared/handoffs/2026-10-29_23-45-00_b-s1-verified-awaiting-cp-s.md](thoughts/shared/handoffs/2026-10-29_23-45-00_b-s1-verified-awaiting-cp-s.md)
<!-- Relative links only; .eng/bin/eng-check verifies they resolve. -->
- Plan B (see Approval log): [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md](thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md); slices B-s1..B-s3 in thoughts/shared/slices/; specs [tests/acceptance/specs/test_grok_multibot.py](tests/acceptance/specs/test_grok_multibot.py)
- Architecture B (approved): [docs/architecture/2026-10-28-grok-webhook-multibot.md](docs/architecture/2026-10-28-grok-webhook-multibot.md); ADR-0011, 0013..0016 (accepted), ADR-0012 (rejected) in [docs/decisions/](docs/decisions/)
- Cross-model review B (awaiting Codex): [thoughts/shared/verification/2026-10-28-grok-webhook-multibot-arch-review.md](thoughts/shared/verification/2026-10-28-grok-webhook-multibot-arch-review.md)
- Research B (accepted): [thoughts/shared/research/2026-10-28-grok-webhook-multibot-current-code.md](thoughts/shared/research/2026-10-28-grok-webhook-multibot-current-code.md)
- Design B Grok Bot webhook + multi-bot (approved; scope HOLD approved 2026-10-28): [docs/design/2026-10-28-grok-webhook-multibot.md](docs/design/2026-10-28-grok-webhook-multibot.md)
- Conventions: [AGENTS.md](AGENTS.md)
- Owner guide: [OWNER-GUIDE.md](OWNER-GUIDE.md)
- Definition of Done: [docs/definition-of-done.md](docs/definition-of-done.md)
- Retro v0.3.0 (done, changes applied 2026-10-28): [thoughts/shared/retros/2026-10-28-v0.3.0-live-bots.md](thoughts/shared/retros/2026-10-28-v0.3.0-live-bots.md)
- Process feedback: [thoughts/shared/process-feedback.md](thoughts/shared/process-feedback.md)
- Design A Live bots (approved; scope REDUCE recorded 2026-10-26): [docs/design/2026-10-26-live-bots.md](docs/design/2026-10-26-live-bots.md)
- Design (approved; scope hold approved): [docs/design/2026-10-25-mmbridge-mcp.md](docs/design/2026-10-25-mmbridge-mcp.md)
- Plan A Live bots (status in front matter): [thoughts/shared/plans/2026-10-27-live-bots.md](thoughts/shared/plans/2026-10-27-live-bots.md)
- Plan review A (AWAITING Codex, mandatory): [thoughts/shared/verification/2026-10-27-live-bots-plan-review.md](thoughts/shared/verification/2026-10-27-live-bots-plan-review.md)
- Review lb2 (addressed): [thoughts/shared/verification/2026-10-27-slice-20261027-lb2-state-db-wake-queue-review.md](thoughts/shared/verification/2026-10-27-slice-20261027-lb2-state-db-wake-queue-review.md)
- Verify lb5 (PASS): [thoughts/shared/verification/2026-10-28-lb5-wireup-reconnect-acceptance-verify.md](thoughts/shared/verification/2026-10-28-lb5-wireup-reconnect-acceptance-verify.md)
- Review lb5 (round 6 clean): [thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-6.md](thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-6.md)
- Specs A: [tests/acceptance/specs/test_live_bots.py](tests/acceptance/specs/test_live_bots.py)
- Architecture A Live bots (approved): [docs/architecture/2026-10-26-live-bots.md](docs/architecture/2026-10-26-live-bots.md)
- Cross-model review A (awaiting Codex): [thoughts/shared/verification/2026-10-26-live-bots-arch-review.md](thoughts/shared/verification/2026-10-26-live-bots-arch-review.md)
- Architecture: [docs/architecture/2026-10-25-mmbridge-mcp.md](docs/architecture/2026-10-25-mmbridge-mcp.md)
- ADRs 0001-0010 (all accepted): [docs/decisions/](docs/decisions/)
- Verification lb4b (PASS): [thoughts/shared/verification/2026-10-27-lb4b-drop-allowlist.md](thoughts/shared/verification/2026-10-27-lb4b-drop-allowlist.md)
- Latest handoff: [thoughts/shared/handoffs/2026-10-29_23-08-07_b-s1-implemented-awaiting-review.md](thoughts/shared/handoffs/2026-10-29_23-08-07_b-s1-implemented-awaiting-review.md)
- Review lb4b (addressed, no findings): [thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review.md](thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review.md)
- Review lb3 (addressed, no findings): [thoughts/shared/verification/2026-10-27-slice-20261027-lb3-listener-filters-review.md](thoughts/shared/verification/2026-10-27-slice-20261027-lb3-listener-filters-review.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
- Plan (approved): [thoughts/shared/plans/2026-10-25-mmbridge-mcp.md](thoughts/shared/plans/2026-10-25-mmbridge-mcp.md)
- Verification s1 (PASS): [thoughts/shared/verification/2026-10-26-s1-verify.md](thoughts/shared/verification/2026-10-26-s1-verify.md)
- Slices: [thoughts/shared/slices/](thoughts/shared/slices/)
- Specs: [tests/acceptance/specs/test_mmbridge.py](tests/acceptance/specs/test_mmbridge.py)
- Research A Live bots (accepted): [thoughts/shared/research/2026-10-26-live-bots-current-code.md](thoughts/shared/research/2026-10-26-live-bots-current-code.md)
- Research: [thoughts/shared/research/2026-10-25-mmbridge-current-code.md](thoughts/shared/research/2026-10-25-mmbridge-current-code.md)
- Deferred work: [TODOS.md](TODOS.md)
- Retro (done): [thoughts/shared/retros/2026-10-26-v0.2.0.md](thoughts/shared/retros/2026-10-26-v0.2.0.md)

## Approval log
<!-- One row per decision. Artifact cell names the file path(s). Decision: approved | accepted | partially accepted | deferred | rejected.
     Pre-kit decisions: back-fill with Checkpoint "pre-kit" and Decision "approved (back-filled, pre-kit)". .eng/bin/eng-check matches rows to statuses. -->
| Date | Checkpoint | Artifact | Decision (Rob) |
|---|---|---|---|
| 2026-10-30 | CP-S | thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md | approved (relay in Mattermost compose stack; live: Rob post in ~acorn woke mmbridge-wake-eddie, run 21:28:50 CDT succeeded, ack in Eddie chat; mmbridge needed a container restart after first set-bot (booted store_unreadable, reload does not start WS); http wake host `relay` only (8c60bc8); Ulrik duplicate re-POST not run; via Eddie) |
| 2026-10-30 | triage (size) | thoughts/shared/slices/2026-10-30-http-wake-internal-hosts.md | approved (small, security; Rob 'Tighten now': no global LIVE_ALLOW_HTTP_WAKE in prod, http only to in-stack relay; via Eddie) |
| 2026-10-29 | CP-C | thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md | approved speclock sha256:ee97d6ceffddcb0b (slices B-s1 -> B-s2 -> B-s3; via Eddie) |
| 2026-10-28 | CP-B | docs/architecture/2026-10-28-grok-webhook-multibot.md, docs/decisions/0011-hmac-to-bearer-wake-relay.md, docs/decisions/0013-multi-bot-store-v2.md, docs/decisions/0014-multi-bot-runtime-state-v2.md, docs/decisions/0015-thread-replies-root-id.md, docs/decisions/0016-acceptance-tests-increment-b.md | approved (architecture B + ADR-0011, 0013..0016 accepted; ADR-0012 claim_wake stays rejected; ops accepted for now: relay Bearer key + routine URL in Coolify env on relay, not mmbridge admin; same bot name ties Mattermost bot, relay and Grok routine; RELAY_BOT_<name>_HMAC_SECRET = copy of the bot wake secret; via Eddie) |
| 2026-10-28 | CP-R | thoughts/shared/research/2026-10-28-grok-webhook-multibot-current-code.md | accepted (via Eddie) |
| 2026-10-28 | CP-A (scope) | docs/design/2026-10-28-grok-webhook-multibot.md | approved (HOLD: In REQ-B1..B8; Out web admin, bot-to-bot wakes/caps, channel ignore-list; A5 suite stays in TODOS; via Eddie) |
| 2026-10-28 | CP-A | docs/design/2026-10-28-grok-webhook-multibot.md | approved (problem, REQ-B1..B8, acceptance examples; Grok wake contract locked: POST per-routine URL, Bearer key, any JSON body, 200=run started; via Eddie) |
| 2026-10-28 | retro | thoughts/shared/retros/2026-10-28-v0.3.0-live-bots.md | approved (all proposals: process changes 1-3 applied; kit lessons K-1..K-4 to Yana; via Eddie) |
| 2026-10-28 | CP-S | thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md | approved (verify PASS 8f987e7; Coolify steps 1-4 and 6 good; step 5 restart Mattermost mid-demo / real-MM resume+catch-up check deferred by Rob; rollback not exercised, LIVE_BOTS_ENABLED left on; via Eddie) |
| 2026-10-28 | CP-S | thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md | approved (verify PASS 14ecd18; demo set-bot + --channels reject; live Mattermost->receiver e2e deferred until listener/dispatcher wired in lb5) |
| 2026-10-27 | CP-C | thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md | approved speclock sha256:ea6a99cbd5601d05 |
| 2026-10-27 | CP-A | docs/design/2026-10-26-live-bots.md | approved amendment: drop allow-list sha256:0f250a0276b5 (via Eddie) |
| 2026-10-27 | CP-S | thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md | approved (verify PASS 219a9a1; README wake-receiver/tamper demo deferred - no set-bot/wake secret yet; via Eddie) |
| 2026-10-27 | CP-S | thoughts/shared/slices/2026-10-27-lb3-listener-filters.md | approved (verify PASS; ws_spike hello+ping reply+posted on Coolify; via Eddie) |
| 2026-10-27 | CP-S | thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md | approved (verify PASS; empty-DB admin failed/stats deferred; via Eddie) |
| 2026-10-27 | CP-S | thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md | approved (verify PASS; live container/Coolify check deferred, not yet redeployed; via Eddie) |
| 2026-10-28 | CP-P | CHANGELOG.md (v0.3.0, commit 93b4f7d, tag v0.3.0) | approved (release v0.3.0; Rob via Eddie; wake rule stays every-post, no @mention change) |
| 2026-10-27 | CP-C | thoughts/shared/plans/2026-10-27-live-bots.md | approved speclock sha256:3108f1fe6a93cfae |
| 2026-10-27 | CP-B | docs/architecture/2026-10-26-live-bots.md | approved (incl. stored-token security review) |
| 2026-10-27 | CP-B | docs/decisions/0006-encrypted-token-store.md, docs/decisions/0007-mattermost-websocket-listener.md, docs/decisions/0008-signed-wake-webhook.md, docs/decisions/0009-listener-state-persistence.md, docs/decisions/0010-acceptance-tests-live-bots.md | accepted (ADR-0006..0010) |
| 2026-10-26 | CP-R | thoughts/shared/research/2026-10-26-live-bots-current-code.md | accepted (via Eddie) |
| 2026-10-26 | CP-A (scope) | docs/design/2026-10-26-live-bots.md | approved (REDUCE: In A1, A2, A3 own-post, A4, A7, A8 one bot, hand-set channels; Out A6, A3 bot-to-bot caps, A5/A5b/A5c auto-join deferred by Rob after first proposal; via Eddie) |
| 2026-10-26 | CP-A | docs/design/2026-10-26-live-bots.md | approved (problem, REQ-A1..A8 incl. A5/A5b/A5c/A6, acceptance examples; via Eddie; later clarified: one-bot wedge = whole v1 ship, multi-bot later increment) |
| 2026-10-26 | triage (size) | docs/design/2026-10-26-live-bots.md | accepted (large confirmed; via Eddie) |
| 2026-10-26 | CP-S | thoughts/shared/slices/2026-10-26-d-hardening-xff-bearer.md | approved (live: FORWARDED_ALLOW_IPS working, logs show public client IPs; 1 container; via Eddie) |
| 2026-10-26 | triage (size) | thoughts/shared/slices/2026-10-26-d-hardening-xff-bearer.md | approved (small confirmed, security; via Eddie) |
| 2026-10-26 | CP-P | CHANGELOG.md (v0.2.0, commit 9946445, tag v0.2.0) | approved (release v0.2.0) |
| 2026-10-26 | CP-S | thoughts/shared/slices/2026-10-25-s3-dm.md | approved (live same-channel dual DM, ping via dm_read, nobody -> unknown_user)
| 2026-10-26 | CP-S | thoughts/shared/slices/2026-10-25-s2-post-read-channel.md | approved (live post/read/not_member)
| 2026-10-25 | CP-A | docs/design/2026-10-25-mmbridge-mcp.md | approved (problem, REQ-1..8, acceptance examples) |
| 2026-10-25 | CP-A (scope) | docs/design/2026-10-25-mmbridge-mcp.md | approved (scope mode hold: REQ-1..8 in; @mention wakes, auto-join, multi-bot, threads/reactions/files out) |
| 2026-10-25 | CP-B | docs/architecture/2026-10-25-mmbridge-mcp.md | approved |
| 2026-10-25 | CP-B | docs/decisions/0001-credential-handoff-bearer-per-call.md, docs/decisions/0002-mattermost-http-client.md, docs/decisions/0003-mcp-surface-streamable-http.md, docs/decisions/0004-per-token-in-memory-rate-limit.md, docs/decisions/0005-structured-logs-public-health.md | accepted (ADR-0001..0005) |
| 2026-10-26 | CP-C | thoughts/shared/plans/2026-10-25-mmbridge-mcp.md | approved speclock sha256:2e4855ad12913e1f |
| 2026-10-26 | CP-S | thoughts/shared/slices/2026-10-25-s1-auth-list-channels.md | approved (manual verification approved by Rob; verify PASS; review F1/F2 accepted-risk) |
