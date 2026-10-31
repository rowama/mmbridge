---
id: REVIEW-20261030-slice-20261028-b-s2-round-trip-reply-root-id-review
type: review-findings
phase: verify
status: addressed
owner_agent: eng-run
date: 2026-10-30
links: [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, thoughts/shared/slices/2026-10-28-b-s2-round-trip-reply-root-id.md]
review_kind: slice
subject: "SLICE-20261028-b-s2-round-trip-reply-root-id (thoughts/shared/slices/2026-10-28-b-s2-round-trip-reply-root-id.md)"
diff: d5dc1ae...e68ee8f
reviewer: codex
command: "codex review --base d5dc1ae"
run_log: thoughts/shared/runs/2026-10-30-code-review-slice-20261028-b-s2-round-trip-reply-root-id.md
---
# Independent review: code-review slice-20261028-b-s2-round-trip-reply-root-id
<!-- Written by eng-run (prompt code-review v2). Each finding row starts 'open': set disposition fixed (where) |
     accepted-risk (ONLY with Rob's approval, e.g. "Rob 2026-10-30") | rejected (reason). Plan reviews gate
     implementation (medium/large); slice reviews are advisory. -->

## Findings
| # | Severity | Location | Finding | Disposition | Reason / approval |
|---|---|---|---|---|---|
| 1 | P2 | app/service.py:74-76 | root_id of a reply (not a thread root) in the target conversation passes the check; MM then rejects the write as generic mattermost_error instead of invalid_root | fixed (B-s2 review-fix commit: `_same_channel` also requires the root to have no root_id; tests/unit/test_root_id.py `test_root_that_is_itself_a_reply_is_invalid_root` for post_channel and dm_send) | |
| 2 | P2 | relay/relay.py:305-309 | bad-signature tracking kept one timestamp per forged request for 10 min and rescanned the list each time (unauthenticated memory/CPU growth) | fixed (B-s2 review-fix commit: 10 s buckets, at most ~61 entries; `test_bad_sig_tracking_is_bounded_under_a_flood`) | |

Note (claude-code): eng-run wrote "No findings." here although Codex's raw output below lists the two P2 findings above; table filled by hand from the raw output.

## Reviewer raw output
````
OpenAI Codex v0.166.0
--------
workdir: /mnt/d/rob/projects/mmbridge
model: gpt-6.1-sol
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR]
reasoning effort: none
reasoning summaries: none
session id: 01a18ff9-1ca1-71a0-861a-c68e974b9072
--------
user
changes against 'd5dc1ae'
exec
/bin/bash -lc 'cat PROJECT_STATE.md; git status --short; git diff --stat d5dc1ae887af7f86e50ba3262b42376a6c3e2722' in /mnt/d/rob/projects/mmbridge
 succeeded in 2992ms:
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

B-s1 done (CP-S 2026-10-30). Ops: boot-before-store fixed 2026-10-30 (Rob "fix it now", small): if mmbridge boots with store_unreadable (no bots.enc yet) it stays `off` and re-tries the store every 30 s; the first set-bot starts the WS listener (log store_appeared). Restart no longer required after first set-bot (needs the new image on Coolify). http-wake-internal-hosts slice (8c60bc8) done (CP-S 2026-10-30). Open: live Mattermost-restart resume check (TODOS, deferred); OWNER-GUIDE pointer (TODOS P2); flaky timing tests (TODOS P2).

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
| 2026-10-30 | CP-S | thoughts/shared/slices/2026-10-30-http-wake-internal-hosts.md | approved (8c60bc8 on main; exercised live by B-s1 demo: wake via http://relay with LIVE_ALLOW_HTTP_WAKE unset in prod; via Eddie) |
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
 M AGENTS.md
 M OWNER-GUIDE.md
 M PROJECT_STATE.md
 M app/live.py
 M tests/unit/test_main_live.py
 M tests/unit/test_store.py
?? receiver.py
?? thoughts/shared/inbox-local-bak-1793080755/
?? thoughts/shared/inbox.md
?? thoughts/shared/runs/2026-10-28-implement-slice-20261027-lb5-wireup-reconnect-acceptance.md
?? thoughts/shared/runs/2026-10-29-implement-slice-20261028-b-s1-relay-grok-wake-one-bot-2.md
?? thoughts/shared/runs/2026-10-29-implement-slice-20261028-b-s1-relay-grok-wake-one-bot.md
?? thoughts/shared/runs/2026-10-30-code-review-slice-20261028-b-s2-round-trip-reply-root-id.running.md
?? thoughts/shared/runs/2026-10-30-implement-slice-20261028-b-s2-round-trip-reply-root-id.running.md
 AGENTS.md                                          |   7 +-
 CHANGELOG.md                                       |   4 +
 OWNER-GUIDE.md                                     |   2 +
 PROJECT_STATE.md                                   | 260 ++++-----
 app/listener.py                                    |  21 +-
 app/live.py                                        | 398 ++++++-------
 app/mcp.py                                         |  24 +-
 app/service.py                                     |  48 +-
 app/validate.py                                    |  10 +
 coolify-service.snippet.yaml                       |   4 +
 relay/README.md                                    |  50 +-
 relay/relay.py                                     | 127 ++++-
 tests/acceptance/drivers/fake_mattermost.py        |  24 +-
 tests/acceptance/drivers/fake_routine.py           |  46 +-
 tests/acceptance/drivers/live.py                   |  67 ++-
 tests/acceptance/drivers/relay.py                  |   6 +-
 tests/unit/test_listener.py                        |  32 +-
 tests/unit/test_main_live.py                       | 628 ++++++++++-----------
 tests/unit/test_relay.py                           | 188 +++++-
 tests/unit/test_root_id.py                         | 168 ++++++
 tests/unit/test_store.py                           |   2 +-
 .../plans/2026-10-28-grok-webhook-multibot.md      |   2 +-
 .../2026-10-28-b-s2-round-trip-reply-root-id.md    |  46 +-
 23 files changed, 1455 insertions(+), 709 deletions(-)

exec
/bin/bash -lc 'cat thoughts/shared/handoffs/2026-10-29_23-08-07_b-s1-implemented-awaiting-review.md; cat .claude/skills/eng-code-review/SKILL.md; cat .eng/PROCESS.md | head -100; find . -name AGENTS.md -o -name AGENTS.override.md; python3 .eng/bin/eng-check .' in /mnt/d/rob/projects/mmbridge
 succeeded in 2731ms:
---
id: HANDO-20261029-b-s1-implemented-awaiting-review
type: handoff
phase: implement
status: complete
owner_agent: claude-code
date: 2026-10-29T23:08:07-05:00
links: [thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md, thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md]
git_commit: cd07811
branch: main
next_skill: eng-verify
---
# Handoff: B-s1 implemented, awaiting review/verify

## Task(s)
- SLICE-20261028-b-s1-relay-grok-wake-one-bot (plan B Phase 1): **implemented, status `review`**. Code commit cd07811 (not pushed). All 11 `$B1` specs + A live + MCP specs green, in-process and container, 3 runs.
- Not done (needs Rob or the planner): OQ-B1/B2 spike run, Codex slice review, OWNER-GUIDE text, CP-S manual checks.

## Critical References
- thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md (Progress log + Blockers/deviations)
- relay/relay.py, relay/README.md
- tests/acceptance/drivers/relay.py (how the relay is run and tapped in the harness)

## Recent changes
- relay/relay.py:1 - new relay app (`create_app` factory; `load_bots`, `verify` copy, `map_upstream`, `Seen`, `RateLimit`, `_Relay.wake/_deliver/_forward`).
- relay/Dockerfile, relay/requirements.txt, relay/.dockerignore, relay/spike_routine.py, relay/README.md - new.
- tests/unit/test_relay.py:1 - 55 unit tests (plan Phase 1 list incl. replay/dedupe and ambiguous outcomes).
- tests/acceptance/drivers/fake_routine.py, drivers/relay.py, drivers/_serve.py - new; drivers/live.py - B-s1 steps (`register_bot` ... `assert_no_secret_anywhere`), generic `_barrier`, `assert_wake_retried` for relay paths, WAKE_BACKOFF_SCALE 0.25, in-process reload_s 0.1, LIVE_IMAGE default mmbridge:bs1.
- README.md "Grok Bot routines (wake relay)"; CHANGELOG.md Unreleased (Added); coolify-service.snippet.yaml relay service + volume.
- No change to app/, tests/acceptance/specs/, or tests/acceptance/dsl.py (no DSL assertion body edits).

## Verification (plan Phase 1 block, run verbatim, exit 0)
```
run 1: unit 322 passed | mcp 16 passed, 36 skipped | live inprocess A+B1 26 passed (65.9s) | live container A+B1 26 passed (169.3s)
run 2: unit 322 passed | mcp 16 passed, 36 skipped | live inprocess 26 passed (64.4s) | live container 26 passed (167.8s)
run 3: unit 322 passed | mcp 16 passed, 36 skipped | live inprocess 26 passed (65.3s) | live container 26 passed (167.6s)
eng-check: OK - 0 error(s), 3 warning(s), 149 artifact(s) checked
eng-spec status: lock approval: ok (2026-10-29); specs and DSL interface match the lock
```
Red first: the 11 specs failed with `AttributeError: 'LiveDriver' object has no attribute 'register_bot'`.

## Learnings
- mmbridge's store reload is a fixed 30 s (app/live.py RELOAD_S, no env), so the container switch spec waits for the bridge's own `store_updated ... generation` log line; in-process passes `reload_s=0.1`.
- The routine only sees the forwarded body (no signature headers), so tamper/replay need the genuinely captured signed request: the harness puts a recording tap between mmbridge and the relay. `relay_down` stops tap + relay (connection refused at mmbridge).
- Relay retries in container mode need time: WAKE_BACKOFF_SCALE 0.25 gives ~7.5 s before a wake fails (was ~1.5 s).
- `codex` is not installed in the implementer's WSL shell, even with `bash -lc`.

## Artifacts
- relay/relay.py, relay/Dockerfile, relay/requirements.txt, relay/.dockerignore, relay/spike_routine.py, relay/README.md
- tests/unit/test_relay.py
- tests/acceptance/drivers/fake_routine.py, tests/acceptance/drivers/relay.py, tests/acceptance/drivers/_serve.py, tests/acceptance/drivers/live.py
- README.md, CHANGELOG.md, coolify-service.snippet.yaml
- thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md (status review, progress log, deviations)
- thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md (Phase 1 automated checkbox ticked)
- Images built locally: mmbridge:bs1, mmbridge-relay:bs1

## Approvals
- None requested or granted this session. Next stop: CP-S for B-s1 (after verify), with the plan Phase 1 manual checks and the Before -> After line, e.g. "Before: a post wakes Eddie's signed receiver. After: a post in Town Square or a DM to eddie starts the Eddie Grok routine once, via the relay."

## Action Items & Next Steps
1. Planner: run the advisory Codex slice review where Codex is available: `python3 .eng/bin/eng-run code-review SLICE-20261028-b-s1-relay-grok-wake-one-bot` (base bc73656). Security-relevant (HMAC verify, dedupe, rate limit, Bearer key, redaction).
2. Planner: eng-verify for B-s1 (re-run the Phase 1 block).
3. Rob before CP-S: run `python3 relay/spike_routine.py https://<eddie-routine-url>` (key at the prompt) and note the 3 codes + whether the bot saw the JSON marker verbatim; planner records them in ADR-0011 as an "Observed" note (and applies the OQ-B1/B2 fallback if they differ).
4. Rob at CP-S: deploy the relay on Coolify per relay/README.md "Setup on Coolify"; plan Phase 1 Manual Verification.
5. OWNER-GUIDE "Grok routine setup": after Rob commits his pending OWNER-GUIDE.md edits (text is in relay/README.md).
6. Push cd07811 only per push_permission (standing: after eng-verify PASS).

## Other Notes
- Container-mode `replay_last_wake(600)` is refused as a duplicate, not as stale (no clock hook in the relay image on purpose); in-process it is refused as stale. Stale is unit-tested.
- Rob's uncommitted AGENTS.md, OWNER-GUIDE.md, receiver.py and untracked thoughts/shared files were not staged.
cat: .claude/skills/eng-code-review/SKILL.md: No such file or directory
<!-- Copy of eng-process kit v2.5.9 PROCESS.md, vendored by eng-init. Do not edit here. -->
# Engineering Process (canonical, kit v2.5.9)

One human approver (Rob, "the owner"), several interchangeable AI agents. **All state lives in files; the repo is the single source of truth.** Any agent must be able to pick up the project from `PROJECT_STATE.md` + the latest handoff alone. This file is the only place the phase-to-skill routing lives (section 3); `AGENTS.md` and skills reference it, and `.eng/PROCESS.md` is a pinned read-only copy written by `eng-init`.

## 1. Repo layout (created by `<kit>/bin/eng-init`)
```
PROJECT_STATE.md          single entry point: phase, triage, working agreements, active slice, next action, approvals
AGENTS.md  (CLAUDE.md -> @AGENTS.md)   commands, architecture map, conventions
OWNER-GUIDE.md            plain-language guide + glossary for the owner
CHANGELOG.md  TODOS.md    release notes; deferred work and scope cuts
docs/definition-of-done.md
docs/vision/              long-lived product vision / feature list (type vision)
docs/design/              design docs per increment (problem -> requirements -> scope [-> architecture])
docs/architecture/        optional separate architecture docs for large work (type architecture)
docs/decisions/           ADRs NNNN-slug.md, id ADR-NNNN, append-only
thoughts/shared/research/         codebase research: what the code IS (type research)
thoughts/shared/market-research/  external/market/methods research (type market-research)
thoughts/shared/briefs/           project briefs for a new implementer/reviewer (type project-brief)
thoughts/shared/{plans,slices,handoffs,retros}/
thoughts/shared/verification/     verification reports + independent review findings (*-review.md)
thoughts/shared/review-notes/     owner's scratch notes; agents don't edit; not checked
thoughts/shared/inbox.md          owner incoming-thoughts inbox (v2.5.6); append-only on capture prefixes; not checked
thoughts/shared/inbox/            rotated inbox archives YYYY-MM-DD-HHMM-inbox.md (committed)
thoughts/shared/process-feedback.md  friction log for the kit (type process-feedback)
.eng/bin/                 vendored kit scripts (eng-check, eng-status, eng-new, eng-init, englib.py); plain python3
.eng/templates/  .eng/PROCESS.md  .eng/VERSION   vendored templates, this file, kit version
.claude/skills/eng-*/SKILL.md     vendored skills (Claude Code project-skill location)
.eng/templates/  .eng/PROCESS.md  .eng/VERSION    kit copy (templates used by .eng/bin/eng-new)
```
Every checked artifact starts with front matter: `id, type, phase, status, owner_agent, date, links`. `.eng/bin/eng-check` enforces it. Inline lists may quote items containing commas (`["a, b", c]`); dash lists also work.

## 2. Triage (`eng-triage`, first step for any request)
| Size | Signal | Phases |
|---|---|---|
| **Small** | about 1 file or an obvious fix, no new interface, no data change, reversible | Implement -> Verify -> Ship (one slice card, no plan) |
| **Medium** | a few files, one component, known patterns | Discover (short design doc) -> Research -> Plan -> Implement -> Verify -> Ship -> Reflect |
| **Large** | new component/interface/data model, cross-cutting, brownfield risk, security/money/data | all nine phases, all checkpoints |
When in doubt, size up. Re-triage if research reveals more than expected. Record it in `PROJECT_STATE.md` (`triage:`).

**Readiness check.** When a project claims to be at a later phase (e.g. "we're already on slice 1"), `eng-triage` verifies that every earlier phase's artifacts and approvals exist for its size (table below; `.eng/bin/eng-status` prints `readiness:` and `.eng/bin/eng-check` fails on gaps). If anything is missing, set `phase` back to the earliest incomplete phase, list exactly what is missing under Blockers, and record the back-up (section 4a).

| To be in phase | Small | Medium | Large |
|---|---|---|---|
| research | n/a | approved design (CP-A) | approved design (CP-A) |
| architecture | n/a | n/a | + approved codebase research (CP-R) |
| plan | n/a | approved design; research doc exists | + approved architecture (CP-B logged, or approved `docs/architecture/` doc) |
| implement | slice card | + approved plan (CP-C) with clean plan review | + approved plan (CP-C) with clean plan review |
| verify | slice card | same as implement | same as implement |
| ship | + verification `pass` (CP-D) | + verification `pass` | + verification `pass` |

## 3. Phases (and the skill for each: this is the routing table)
| # | Phase | Skill | Entry | Output | Exit criteria | Checkpoint |
|---|---|---|---|---|---|---|
| 0 | (any session) | eng-resume to start, eng-handoff to end; eng-triage for new requests; eng-project-init to adopt | | | | |
| 1 | Discover | eng-discover | triaged M/L | `docs/design/*` (+ optional `docs/vision/`, `thoughts/shared/market-research/`) | problem, metric, testable requirements; no `[NEEDS CLARIFICATION]` | **CP-A Product** |
| 2 | Scope | eng-scope-review | CP-A approved | design doc Scope section (baseline = approved requirements list); cuts -> TODOS.md; ADR if durable | mode chosen relative to baseline, in/out lists | (part of CP-A for L) |
| 3 | Research | eng-research | approved design | `thoughts/shared/research/*` | code *as is* with file:line; no recommendations | **CP-R Research** (L; optional M) |
| 4 | Architecture | eng-architecture-review | research approved | design doc Architecture section **or** `docs/architecture/*` linked from it; ADRs | contracts, data, sequence, failure modes, rollback, observability, security | **CP-B Architecture** (L) |
| 5 | Plan | eng-plan | prerequisites (section 2) | `thoughts/shared/plans/*` + slice cards + **mandatory Codex plan review** (M, L) | vertical slices, each with automated + manual criteria; What We're NOT Doing; no open critical/high review finding | **CP-C Plan** (M, L) |
| 6 | Implement | eng-implement-slice (run by the implementer) | plan approved, slice next, no pending approvals | code + tests, plan checkboxes, slice card; then independent review findings | slice's automated criteria pass; review findings answered | **CP-S Slice** per slice |
| 7 | Verify | eng-verify | all slices `review`/`done` | `thoughts/shared/verification/*` | every criterion re-executed; DoD pass; verdict PASS | **CP-D Done** |
| 8 | Ship | eng-ship | verification PASS | CHANGELOG entry, VERSION (if used), PR | CI green, PR opened | **CP-P PR merge/deploy** (Rob merges) |
| 9 | Reflect | eng-retro | shipped (or weekly, or each advisor consultation) | `thoughts/shared/retros/*` + edits | process-feedback pass done; each change applied to a file | none |

**One phase per session, one artifact, then stop for approval.** Discovery tends to pre-draft later artifacts (architecture, plan). That's allowed only as input. **Wording, used everywhere:** `input` = a pre-draft written in an earlier phase than its own, not yet worked on in its own phase; `draft` = being written in its own phase; `in-review` = waiting for Rob. None of these is an approval, and neither is any invented status like `approved-for-review` (`.eng/bin/eng-check` rejects those). Pre-drafts carry `status: input` and the heading note "input, not approved"; their own phase's skill turns them into `draft`. The owner may choose to group phases in one session once familiar with the process; record that in the handoff.

## 4. Approval checkpoints
- **Front matter `pending_approvals` is the single source of truth.** Item format: `CP-X: <path>[ + <path>] - <decision needed>`; paths must exist (CP-P may name a PR URL). The body section only points at it; `.eng/bin/eng-status` renders it. `.eng/bin/eng-check` fails if the body lists CP items that differ.
- Checkpoints for **later** phases may be pending early (e.g. CP-B auth/hosting questions during Discover). A pending checkpoint for an **earlier** phase than the current one blocks (`.eng/bin/eng-check` error); so does any missing prerequisite (section 2), for every phase, not just implement/verify/ship.
- **Owner review workflow.** Rob may jot notes in `thoughts/shared/review-notes/<owner>-review-notes.md`. Agents never edit or act on it until he says the notes are ready. Approvals arrive in chat. The agent then records each one in (1) the PROJECT_STATE Approval log row, (2) the artifact `status`, and (3) an ADR if the decision is durable, removes the pending item, and commits. The repo, not the chat, is the official record. `.eng/bin/eng-check` cross-checks the log and statuses both ways.
- **Notes rotation.** When a cycle finalizes (a slice reaches `done`, or a ship), if the scratch file has notes: `git mv` it to `<cycle-id>-<owner>-review-notes.md` and recreate the empty scratch file from `.eng/templates/review-notes.md`. Done in eng-handoff and eng-ship.
- **Owner inbox (v2.5.6).** Random thoughts and feature ideas go in `thoughts/shared/inbox.md`: Rob edits it directly or prefixes a message with `note:`/`n:`/`idea:`/`feature:`/`future feature:`/`ff:`/`capture:`/`cap:`, and the agent appends the item verbatim. Nothing else happens until he says "process incoming" / "check idea log" / "process notes". Then the agent walks each item with him (classify, clarify one question at a time, move it to its home or act, or defer). Once all are settled it moves the file to `thoughts/shared/inbox/YYYY-MM-DD-HHMM-inbox.md` with a status/action per item and recreates the live inbox holding only deferred items (with deferral date). See skill eng-inbox.
- Rejection: status back to `draft`, reasons in the artifact; for research, discard and redo rather than patch.
- ADR statuses: `proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded`. `partially-accepted` requires a `## Parts` section marking each part; `deferred` sets `revisit:`.

### 4a. Backing up to an earlier phase (blameless)
Discovering that an earlier artifact is wrong is normal. Any agent or the owner can call "back up to <phase>" (usually Discover): set `phase` back, set the design doc back to `draft` and any later-phase pre-drafts to `input`, revise them, move affected approvals back to `pending_approvals`, and add a line to PROJECT_STATE "Back-ups to an earlier phase": date, from -> to, why, artifacts revised. No blame, just the reason.

**Approvals live only in the Approval log table** (`| date | CP-X | path | decision |`). `eng-check` flags an approval written anywhere else in PROJECT_STATE.md (a prose line like "CP-C approved by Rob", a row-like line outside the table, a stray line inside the section), and any `approved` status without a table row.

**Design changes after CP-A.** Once the design doc is approved, editing it needs re-approval: set it back to `in-review` and request CP-A again, then log a **new** Approval log row (newer date). To make the check exact, put the content hash in the decision cell: `approved sha256:<first 12+ hex of sha256 of the file, LF line endings>`. Without a hash, `eng-check` warns when git shows a commit touching the approved design dated after the latest CP-A row. Edits during phase `discover` are never flagged. It also warns when plan or slice drafts exist while no design doc is approved (except triage small, or unset: size unknown before triage). Both checks are errors since v2.5.0.

## 5. WIP rules
- One project phase at a time; **max 1 slice `in-progress`** (enforced). Max open PRs = what Rob can review (default 1).
- Pull the next slice only when the previous is `done` or explicitly `blocked` with a reason.
- A slice is ~100-200 changed lines, end-to-end, demoable. Bigger -> split before starting.
- Deferrals and unrelated discoveries go to `TODOS.md`, not into the current slice.

## 6. Definition of Done
`docs/definition-of-done.md` (project may extend, never weaken). Core: criteria re-executed in the verifying session; tests incl. regression; no weakened gates; docs, CHANGELOG, ADRs, TODOS updated; verification PASS; state + handoff written. Also in the DoD template: default `pytest tests` (or project equivalent) with zero silent collection skips; time/rate tests use an injected/frozen clock from slice 1 (LESSONS L-003).

## 7. Context hygiene
- **One phase per session.** Start fresh; load only PROJECT_STATE, the latest handoff, and the inputs the skill names.
- **~40% rule of thumb:** no context meter exists, so use proxies: when you've read >~15 files, done >~30 tool calls, or been corrected twice, compact: write progress into the artifact + handoff and end the session.
- **Compaction is into files**, never into memory: plan checkboxes, slice progress log, handoff.
- **Sub-tasks for search:** delegate wide searches to sub-agents returning paths + file:line; read critical artifacts directly and fully.
- Codebase research documents what *is*; opinions belong in market research, architecture or plan.
- Keep AGENTS.md short: only what an agent cannot infer from code.

./.eng/templates/AGENTS.md
./AGENTS.md
WARN  .eng/runners.toml: no on_complete hook configured ([hooks] empty or missing) - bots must stay attached to eng-run until exit; fire-and-forget needs a non-empty on_complete / <role>_on_complete (PROCESS.md section 10, LESSONS L-006)
WARN  PROJECT_STATE.md: ## Latest artifacts has 40 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 36 rows / 7331 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 158 artifact(s) checked

exec
/bin/bash -lc 'git diff d5dc1ae -- app/listener.py app/mcp.py app/service.py app/validate.py relay/relay.py' in /mnt/d/rob/projects/mmbridge
 succeeded in 14ms:
diff --git a/app/listener.py b/app/listener.py
index 0b4f19c..f896b5d 100644
--- a/app/listener.py
+++ b/app/listener.py
@@ -450,13 +450,22 @@ class Listener:
         team_id = ch.get("team_id", h.get("team_id")) or ""
         team = await self._get(client, self._teams, team_id, "/teams/" + team_id) if team_id else None
         user = await self._get(client, self._users, w.user_id, "/users/" + w.user_id) or {}
+        channel = {"id": w.channel_id, "name": ch.get("name", h.get("channel_name")),
+                   "display_name": ch.get("display_name", h.get("channel_display_name")),
+                   "type": w.channel_type, "team": (team or {}).get("name")}
+        sender = user.get("username") or (h.get("sender_name") or "").lstrip("@") or None
+        # Reply hints (architecture B, ADR-0015): the tool and target the woken bot answers with. A thread reply
+        # is answered in its thread; a top-level channel post and any DM are answered at top level.
+        if w.channel_type == "D":
+            reply = {"tool": "dm_send", "username": sender, "root_id": None}
+        else:
+            reply = {"tool": "post_channel", "team": channel["team"], "channel": channel["name"], "root_id": w.root_id}
         return {
-            "version": 1, "kind": "post", "delivery_id": w.post_id, "attempt": 1,
+            "version": 2, "kind": "post", "delivery_id": w.post_id, "attempt": 1,
+            "issued_at": _iso(int(self.clock() * 1000)),
             "bot": dict(self._bot),
-            "channel": {"id": w.channel_id, "name": ch.get("name", h.get("channel_name")),
-                        "display_name": ch.get("display_name", h.get("channel_display_name")),
-                        "type": w.channel_type, "team": (team or {}).get("name")},
-            "sender": {"user_id": w.user_id,
-                       "username": user.get("username") or (h.get("sender_name") or "").lstrip("@") or None},
+            "channel": channel,
+            "sender": {"user_id": w.user_id, "username": sender},
             "post": {"id": w.post_id, "message": w.message, "create_at": _iso(w.create_at), "root_id": w.root_id},
+            "reply": reply,
         }
diff --git a/app/mcp.py b/app/mcp.py
index 171667c..21577e0 100644
--- a/app/mcp.py
+++ b/app/mcp.py
@@ -35,10 +35,17 @@ Username = _arg({"type": "string", "pattern": "^[a-z0-9][a-z0-9._-]{0,63}$"}, "M
 Team = _arg({"type": "string", "pattern": "^[a-z0-9][a-z0-9._-]{0,63}$"}, "Team name (URL name, e.g. rmlab).")
 Channel = _arg({"type": "string", "pattern": "^[a-z0-9][a-z0-9._-]{0,63}$"}, "Channel name (URL name, e.g. town-square).")
 Message = _arg({"type": "string", "minLength": 1, "maxLength": validate.MAX_MESSAGE}, "Message text (Markdown).")
+RootId = _arg({"type": ["string", "null"], "pattern": "^[a-z0-9]{26}$"},
+              "Optional thread root post id: reply in that thread (a wake's reply.root_id). The root must be a post "
+              "in the same channel or DM, else invalid_root and nothing is posted. Omit to post at top level.")
 Limit = _arg({"type": "integer", "minimum": 1, "maximum": validate.MAX_LIMIT},
              "How many of the newest posts to return.")
 
 
+async def _dm_send(c: Client, username: str, message: str, root_id: str | None, *, me: dict) -> dict:
+    return await service.dm_send(c, username, message, me=me, root_id=root_id)
+
+
 def build(limiter, mm_transport=None, base_url: str = MATTERMOST_URL) -> FastMCP:
     server = FastMCP("mmbridge", stateless_http=True, json_response=True, streamable_http_path="/mcp",
                      transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False))
@@ -87,20 +94,23 @@ def build(limiter, mm_transport=None, base_url: str = MATTERMOST_URL) -> FastMCP
     async def list_channels() -> CallToolResult:
         return await run("list_channels", service.list_channels)
 
-    @server.tool(description="Post a message to a Mattermost channel this bot is a member of. Never joins channels.")
-    async def post_channel(team: Team, channel: Channel, message: Message) -> CallToolResult:
+    @server.tool(description="Post a message to a Mattermost channel this bot is a member of (optionally as a "
+                             "reply in a thread via root_id). Never joins channels.")
+    async def post_channel(team: Team, channel: Channel, message: Message, root_id: RootId = None) -> CallToolResult:
         return await run("post_channel", service.post_channel, write=True, check=lambda: (
-            validate.identifier("team", team), validate.identifier("channel", channel), validate.message(message)))
+            validate.identifier("team", team), validate.identifier("channel", channel), validate.message(message),
+            validate.post_id(root_id)))
 
     @server.tool(description="Read the newest posts (newest first) of a Mattermost channel this bot is a member of.")
     async def read_channel(team: Team, channel: Channel, limit: Limit = validate.DEFAULT_LIMIT) -> CallToolResult:
         return await run("read_channel", service.read_channel, check=lambda: (
             validate.identifier("team", team), validate.identifier("channel", channel), validate.limit(limit)))
 
-    @server.tool(description="Send a direct message to a Mattermost user by username (opens or reuses the DM).")
-    async def dm_send(username: Username, message: Message) -> CallToolResult:
-        return await run("dm_send", service.dm_send, write=True, with_me=True, check=lambda: (
-            validate.identifier("username", username), validate.message(message)))
+    @server.tool(description="Send a direct message to a Mattermost user by username (opens or reuses the DM; "
+                             "optionally as a reply in a DM thread via root_id).")
+    async def dm_send(username: Username, message: Message, root_id: RootId = None) -> CallToolResult:
+        return await run("dm_send", _dm_send, write=True, with_me=True, check=lambda: (
+            validate.identifier("username", username), validate.message(message), validate.post_id(root_id)))
 
     @server.tool(description="Read the newest posts (newest first) of this bot's DM with a Mattermost user.")
     async def dm_read(username: Username, limit: Limit = validate.DEFAULT_LIMIT) -> CallToolResult:
diff --git a/app/service.py b/app/service.py
index 271cb61..a3cf353 100644
--- a/app/service.py
+++ b/app/service.py
@@ -56,10 +56,42 @@ async def _member_channel(c: Client, team: str, channel: str) -> dict:
     return ch
 
 
-async def post_channel(c: Client, team: str, channel: str, message: str) -> dict:
+_BAD_ROOT = "root_id is not a post in this conversation that the bot can see."
+
+
+async def _root(c: Client, root_id: str) -> dict:
+    """Thread root (ADR-0015), fetched with the bot's own token. Mattermost 400/403/404 (bad id, no access,
+    gone) -> invalid_root."""
+    try:
+        root = await c.get("/posts/%s" % segment(root_id))
+    except MMError as e:
+        if e.status in (400, 403, 404):
+            raise ToolError("invalid_root", _BAD_ROOT)
+        raise
+    return root if isinstance(root, dict) else {}
+
+
+def _same_channel(root: dict, channel_id: str) -> None:
+    if root.get("channel_id") != channel_id:
+        raise ToolError("invalid_root", _BAD_ROOT)
+
+
+async def check_root(c: Client, root_id: str, channel_id: str) -> None:
+    """The root must be a post in `channel_id` the bot can see; checked before any write."""
+    _same_channel(await _root(c, root_id), channel_id)
+
+
+def _new_post(channel_id: str, message: str, root_id: str | None) -> dict:
+    return {"channel_id": channel_id, "message": message, **({"root_id": root_id} if root_id else {})}
+
+
+async def post_channel(c: Client, team: str, channel: str, message: str, root_id: str | None = None) -> dict:
     ch = await _member_channel(c, team, channel)
-    p = await c.post("/posts", {"channel_id": ch["id"], "message": message})
-    return {"post_id": p["id"], "channel": channel, "team": team, "create_at": iso(p["create_at"])}
+    if root_id:
+        await check_root(c, root_id, ch["id"])
+    p = await c.post("/posts", _new_post(ch["id"], message, root_id))
+    out = {"post_id": p["id"], "channel": channel, "team": team, "create_at": iso(p["create_at"])}
+    return {**out, "root_id": root_id} if root_id else out
 
 
 async def _read_posts(c: Client, channel_id: str, limit: int) -> list:
@@ -87,10 +119,14 @@ async def _direct_channel(c: Client, username: str, me: dict) -> dict:
     return await c.post("/channels/direct", [me["id"], user["id"]])
 
 
-async def dm_send(c: Client, username: str, message: str, *, me: dict) -> dict:
+async def dm_send(c: Client, username: str, message: str, *, me: dict, root_id: str | None = None) -> dict:
+    root = await _root(c, root_id) if root_id else None   # a root the bot cannot see: nothing opened or posted
     ch = await _direct_channel(c, username, me)
-    p = await c.post("/posts", {"channel_id": ch["id"], "message": message})
-    return {"post_id": p["id"], "channel_id": ch["id"], "create_at": iso(p["create_at"])}
+    if root is not None:
+        _same_channel(root, ch["id"])
+    p = await c.post("/posts", _new_post(ch["id"], message, root_id))
+    out = {"post_id": p["id"], "channel_id": ch["id"], "create_at": iso(p["create_at"])}
+    return {**out, "root_id": root_id} if root_id else out
 
 
 async def dm_read(c: Client, username: str, limit: int = 20, *, me: dict) -> dict:
diff --git a/app/validate.py b/app/validate.py
index a22f704..a955a0c 100644
--- a/app/validate.py
+++ b/app/validate.py
@@ -9,6 +9,7 @@ from urllib.parse import quote
 from app.errors import ToolError
 
 _IDENT = re.compile(r"[a-z0-9][a-z0-9._-]{0,63}")
+_POST_ID = re.compile(r"[a-z0-9]{26}")   # Mattermost id: 26 chars a-z0-9
 MAX_MESSAGE = 16383
 DEFAULT_LIMIT, MAX_LIMIT = 20, 100
 
@@ -38,5 +39,14 @@ def limit(value) -> int:
     return value
 
 
+def post_id(value) -> str | None:
+    """Optional Mattermost post id (root_id, ADR-0015): None, or exactly 26 chars a-z0-9."""
+    if value is None:
+        return None
+    if not isinstance(value, str) or not _POST_ID.fullmatch(value):
+        raise _bad("root_id must be a Mattermost post id (26 characters a-z, 0-9).")
+    return value
+
+
 def segment(value: str) -> str:
     return quote(value, safe="")
diff --git a/relay/relay.py b/relay/relay.py
index a66ca70..0028d31 100644
--- a/relay/relay.py
+++ b/relay/relay.py
@@ -17,6 +17,15 @@ Delivery guarantee (accepted risk A, Rob 2026-10-28): a delivery id is recorded
 2xx, so a lost upstream response (logged relay_delivery_ambiguous) or a crash before Seen.add can start the
 routine twice; never zero times. Concurrent identical deliveries forward once (per-delivery lock + in_flight row).
 GET /health: counts only. Logs: JSON lines on logger "relay", every secret and key redacted.
+
+Tripwire (B-s2): logs relay_tripwire{reason} on HMAC failures (bad signature or stale timestamp) > 5 in 10 min
+(`bad_sig`), a rate-limit hit (`rate_limited`), upstream 401/403 (`upstream_http_<code>`: key rotated/revoked) and
+count drift (`double_forward`: a delivery forwarded again although an earlier forward may have started the routine,
+accepted risk A). Every forward is recorded before it is sent and dropped again once the routine definitely did not
+start, so a crash between upstream 2xx and Seen.add is still counted after restart. /health shows
+double_forward_24h; >= 3 in 24 h is the signal to revisit option C (Rob 2026-10-28). Optional Mattermost alert
+post (RELAY_ALERT_URL, RELAY_ALERT_TOKEN, RELAY_ALERT_CHANNEL = channel id; all three or none): one per reason per
+10 min, for double_forward only from 3 in 24 h.
 """
 import asyncio
 import hashlib
@@ -42,6 +51,10 @@ MIN_SECRET = 32
 SEEN_TTL_S = 24 * 3600
 IN_FLIGHT_STALE_S = 60
 PRUNE_EVERY_S = 3600
+TRIP_WINDOW_S = 600
+BAD_SIG_MAX = 5
+DRIFT_ALERT = 3
+ALERT_ENV = ("RELAY_ALERT_URL", "RELAY_ALERT_TOKEN", "RELAY_ALERT_CHANNEL")
 FIELDS = ("HMAC_SECRET", "ROUTINE_URL", "ROUTINE_KEY")
 _ENV_RE = re.compile(r"^RELAY_BOT_([A-Z0-9_]+)_(%s)$" % "|".join(FIELDS))
 
@@ -189,6 +202,8 @@ class Seen:
         self._db.execute("CREATE TABLE IF NOT EXISTS seen (delivery_id TEXT PRIMARY KEY, seen_at INTEGER NOT NULL)")
         self._db.execute("CREATE TABLE IF NOT EXISTS in_flight (delivery_id TEXT PRIMARY KEY, "
                          "started_at INTEGER NOT NULL)")
+        self._db.execute("CREATE TABLE IF NOT EXISTS forwards (id INTEGER PRIMARY KEY AUTOINCREMENT, "
+                         "delivery_id TEXT NOT NULL, at INTEGER NOT NULL)")
         self._db.execute("DELETE FROM in_flight")
 
     def _q(self, sql: str, args=()):
@@ -202,8 +217,27 @@ class Seen:
         self._q("INSERT OR IGNORE INTO seen (delivery_id, seen_at) VALUES (?, ?)", (d, int(now)))
 
     def prune(self, now: int) -> int:
+        self._q("DELETE FROM forwards WHERE at < ?", (int(now) - SEEN_TTL_S,))
         return self._q("DELETE FROM seen WHERE seen_at < ?", (int(now) - SEEN_TTL_S,)).rowcount
 
+    # Forward rows (count drift): one per forward that may have started the routine.
+    def forward_begin(self, d: str, now: int) -> int:
+        """Recorded before the upstream call, so it survives a crash after the routine started."""
+        return self._q("INSERT INTO forwards (delivery_id, at) VALUES (?, ?)", (d, int(now))).lastrowid
+
+    def forward_not_started(self, row: int) -> None:
+        """The routine definitely did not start (a non-2xx answer, or never reached): not a forward."""
+        self._q("DELETE FROM forwards WHERE id = ?", (row,))
+
+    def forwards_of(self, d: str, since: int) -> int:
+        return self._q("SELECT COUNT(*) FROM forwards WHERE delivery_id = ? AND at >= ?",
+                       (d, int(since))).fetchone()[0]
+
+    def double_forwards_since(self, since: int) -> int:
+        """Forwards beyond the first per delivery id: possible double wakes (accepted risk A)."""
+        return self._q("SELECT COUNT(*) - COUNT(DISTINCT delivery_id) FROM forwards WHERE at >= ?",
+                       (int(since),)).fetchone()[0]
+
     def count_since(self, since: int) -> int:
         return self._q("SELECT COUNT(*) FROM seen WHERE seen_at >= ?", (int(since),)).fetchone()[0]
 
@@ -249,10 +283,79 @@ class _Counter:
         return sum(v for m, v in self._m.items() if m > k - 24 * 60)
 
 
+class Tripwire:
+    """relay_tripwire{reason} log + optional alert(reason, fields), throttled to one alert per reason per 10 min."""
+
+    def __init__(self, clock, alert=None):
+        self.clock, self.alert = clock, alert
+        self._bad: list[float] = []               # HMAC failure times inside the window
+        self._alerted: dict[str, float] = {}
+
+    def _trip(self, reason: str, alert: bool = True, **fields) -> None:
+        now = self.clock()
+        _log("relay_tripwire", reason=reason, **fields)
+        if not alert or self.alert is None:
+            return
+        last = self._alerted.get(reason)
+        if last is not None and now - last < TRIP_WINDOW_S:
+            return
+        self._alerted[reason] = now
+        self.alert(reason, fields)
+
+    def bad_sig(self, bot: str) -> None:
+        now = self.clock()
+        self._bad = [t for t in self._bad if now - t < TRIP_WINDOW_S] + [now]
+        if len(self._bad) > BAD_SIG_MAX:
+            self._trip("bad_sig", bot=bot, failures_10m=len(self._bad))
+
+    def rate_limited(self, bot: str) -> None:
+        self._trip("rate_limited", bot=bot)
+
+    def upstream_denied(self, bot: str, code: int) -> None:
+        self._trip("upstream_http_%d" % code, bot=bot)
+
+    def double_forward(self, bot: str, delivery: str, count_24h: int) -> None:
+        self._trip("double_forward", alert=count_24h >= DRIFT_ALERT, bot=bot, delivery=delivery,
+                   double_forward_24h=count_24h)
+
+
+def _alerter(env: Mapping[str, str], http: httpx.AsyncClient):
+    """Mattermost alert post from RELAY_ALERT_* (all three or none). Fire and forget: never blocks a wake."""
+    vals = {k: (env.get(k) or "").strip() for k in ALERT_ENV}
+    if not any(vals.values()):
+        return None
+    if not all(vals.values()):
+        raise ConfigError("alert: set all of %s or none" % ", ".join(ALERT_ENV))
+    url, token, channel = (vals[k] for k in ALERT_ENV)
+    if not _https_ok(url, allow_http=True):
+        raise ConfigError("alert: RELAY_ALERT_URL must be http(s)")
+    register_secret(token)
+    tasks: set = set()
+
+    async def post(reason: str, fields: dict) -> None:
+        detail = ", ".join("%s=%s" % kv for kv in sorted(fields.items()))
+        msg = "mmbridge relay tripwire: %s (%s). See the relay logs (relay_tripwire); runbook: relay/README.md." % (
+            reason, detail)
+        try:
+            r = await http.post(url.rstrip("/") + "/api/v4/posts", json={"channel_id": channel, "message": msg},
+                                headers={"Authorization": "Bearer " + token}, timeout=5)
+            if r.status_code >= 300:
+                _log("relay_alert_failed", reason=reason, status=r.status_code)
+        except Exception as e:                    # type only: messages may carry request details
+            _log("relay_alert_failed", reason=reason, error=type(e).__name__)
+
+    def alert(reason: str, fields: dict) -> None:
+        t = asyncio.get_running_loop().create_task(post(reason, fields))
+        tasks.add(t)
+        t.add_done_callback(tasks.discard)
+    return alert
+
+
 class _Relay:
-    def __init__(self, bots, http, clock, seen, rate, timeout_s):
+    def __init__(self, bots, http, clock, seen, rate, timeout_s, tripwire=None):
         self.bots, self.http, self.clock, self.seen, self.rate = bots, http, clock, seen, rate
         self.timeout_s = timeout_s
+        self.tripwire = tripwire or Tripwire(clock)
         self.rejected = _Counter()
         self._locks: dict[str, list] = {}     # delivery id -> [asyncio.Lock, holders+waiters]
         self._pruned_at = None
@@ -273,7 +376,9 @@ class _Relay:
             return self._reject(now, None, "unknown_bot", 404)
         body = await request.body()
         if not verify(bot.hmac_secret, request.headers, body, int(now)):
-            return self._reject(now, bot.name, _reject_reason(request.headers, int(now)), 401)
+            resp = self._reject(now, bot.name, _reject_reason(request.headers, int(now)), 401)
+            self.tripwire.bad_sig(bot.name)
+            return resp
         d = request.headers["x-mmb-delivery"]
         if self._pruned_at is None or now - self._pruned_at >= PRUNE_EVERY_S:
             self.seen.prune(int(now))
@@ -295,15 +400,25 @@ class _Relay:
             return self._reject(now, bot.name, "in_flight", 503, delivery=d)
         try:
             if not self.rate.allow(bot.name, now):
-                return self._reject(now, bot.name, "rate_limited", 429, delivery=d)
+                resp = self._reject(now, bot.name, "rate_limited", 429, delivery=d)
+                self.tripwire.rate_limited(bot.name)
+                return resp
+            row = self.seen.forward_begin(d, int(now))
             status, err = await self._forward(bot, d, body)
             if status is not None and 200 <= status < 300:
                 self.seen.add(d, int(self.clock()))   # only after upstream 2xx (accepted risk A)
                 _log("relay_forwarded", bot=bot.name, delivery=d, upstream=status)
+                since = int(self.clock()) - SEEN_TTL_S
+                if self.seen.forwards_of(d, since) > 1:
+                    self.tripwire.double_forward(bot.name, d, self.seen.double_forwards_since(since))
             else:
                 if err not in (None, "connect"):
                     _log("relay_delivery_ambiguous", bot=bot.name, delivery=d, error=err)
+                else:                                 # an answer, or never reached: the routine did not start
+                    self.seen.forward_not_started(row)
                 _log("relay_upstream", bot=bot.name, delivery=d, code=err or status)
+                if status in (401, 403):
+                    self.tripwire.upstream_denied(bot.name, status)
             code, payload = map_upstream(status)
             return JSONResponse(payload, status_code=code)
         finally:
@@ -327,7 +442,8 @@ class _Relay:
     def health(self) -> dict:
         now = self.clock()
         return {"ok": True, "bots": len(self.bots), "forwarded_24h": self.seen.count_since(int(now) - SEEN_TTL_S),
-                "rejected_24h": self.rejected.since(now)}
+                "rejected_24h": self.rejected.since(now),
+                "double_forward_24h": self.seen.double_forwards_since(int(now) - SEEN_TTL_S)}
 
 
 def create_app(env: Mapping[str, str] | None = None, http: httpx.AsyncClient | None = None, clock=time.time,
@@ -344,7 +460,8 @@ def create_app(env: Mapping[str, str] | None = None, http: httpx.AsyncClient | N
     rate = RateLimit(float(env.get("RELAY_RATE_PER_MIN", "30")), int(env.get("RELAY_BURST", "10")))
     own_http = http is None
     client = http or httpx.AsyncClient()
-    relay = _Relay(bots, client, clock, seen, rate, float(env.get("RELAY_UPSTREAM_TIMEOUT_S", "5")))
+    tripwire = Tripwire(clock, alert=_alerter(env, client))
+    relay = _Relay(bots, client, clock, seen, rate, float(env.get("RELAY_UPSTREAM_TIMEOUT_S", "5")), tripwire)
 
     @asynccontextmanager
     async def lifespan(_app):

exec
/bin/bash -lc 'git diff d5dc1ae -- app/live.py; cat app/mcp.py | head -100; git diff d5dc1ae -- app/listener.py' in /mnt/d/rob/projects/mmbridge
 succeeded in 51ms:
diff --git a/app/live.py b/app/live.py
index da931d2..aaca6d9 100644
--- a/app/live.py
+++ b/app/live.py
@@ -1,199 +1,199 @@
-"""Live-bots runtime started from the FastAPI lifespan (slice lb5, ADR-0007/0009; plan Phase 5).
-
-LiveRuntime.start(): LIVE_BOTS_ENABLED must be "true" (else health `disabled`), the store must decrypt
-(MMB_STORE_KEY; else `off`, log store_unreadable, and re-try every RELOAD_S so the first set-bot starts the
-listener without a restart, log store_appeared) and /data/state.db must be writable (else `off`, log
-state_unwritable). Then three tasks: Listener and Dispatcher each under supervise() (crash -> log task_crashed,
-health `degraded`, restart with backoff 1->60 s; MCP keeps serving) and the ConfigHolder watcher.
-ConfigHolder (PR-2) re-reads the store when its mtime changes (every RELOAD_S): a valid new config replaces the
-old one for both tasks (listener reconnects on a new token, dispatcher reads url/secret at send time); an invalid
-file keeps the previous config (store_reload_failed). Logs carry field names and error codes, never values.
-"""
-import asyncio
-import json
-import os
-import time
-
-import httpx
-
-from app import logging as mlog
-from app import mattermost, store, wake
-from app.listener import Listener
-from app.mattermost import Client
-from app.state import DAY, State, StateError
-from app.store import StoreError
-from app.wake import Dispatcher
-
-RELOAD_S = 30
-RESTART_BASE_S, RESTART_MAX_S = 1.0, 60.0
-FIELDS = ("token", "wake_url", "wake_secret")
-
-
-def _log(event: str, level: str = "info", **fields) -> None:
-    getattr(mlog.log, level)(json.dumps({"event": event, **fields}))
-
-
-class ConfigHolder:
-    """The current BotConfig plus a generation counter; subscribers get (old, new) on a real change."""
-
-    def __init__(self, path: str, key: str | None, cfg):
-        self.path, self.key, self.cfg = path, key, cfg
-        self.generation = 0
-        self._subs = []
-        self._mtime = self._stat()
-
-    def get(self):
-        return self.cfg
-
-    def subscribe(self, fn) -> None:
-        self._subs.append(fn)
-
-    def _stat(self):
-        try:
-            st = os.stat(self.path)
-            return st.st_mtime_ns, st.st_size, st.st_ino
-        except OSError:
-            return None
-
-    def check(self) -> bool:
-        """Reload if the file changed; True if the config changed (subscribers notified)."""
-        m = self._stat()
-        if m == self._mtime:
-            return False
-        self._mtime = m
-        try:
-            new = store.load(self.path, self.key)
-        except StoreError as e:
-            _log("store_reload_failed", "warning", code=e.code, detail=e.detail)
-            return False
-        changed = [f for f in FIELDS if getattr(new, f) != getattr(self.cfg, f)]
-        if not changed:
-            return False
-        old, self.cfg = self.cfg, new
-        self.generation += 1
-        _log("store_updated", fields=changed, generation=self.generation)
-        for fn in self._subs:
-            fn(old, new)
-        return True
-
-    async def watch(self, every: float = RELOAD_S) -> None:
-        while True:
-            await asyncio.sleep(every)
-            self.check()
-
-
-def restart_delay(attempt: int, base_s: float, max_s: float) -> float:
-    """base_s * 2^(attempt-1) capped at max_s; the exponent is bounded so endless crashes cannot overflow."""
-    return min(max_s, base_s * 2 ** min(max(attempt, 1) - 1, 32))
-
-
-async def supervise(name: str, factory, crashed: set, base_s: float = RESTART_BASE_S,
-                    max_s: float = RESTART_MAX_S) -> None:
-    """Run factory() forever: on an exception (or a return) log task_crashed, mark `name` crashed while waiting
-    the backoff (1->60 s; reset after a run longer than max_s), then restart it."""
-    attempt = 0
-    while True:
-        started = time.monotonic()
-        try:
-            await factory()
-            err = "returned"
-        except asyncio.CancelledError:
-            raise
-        except Exception as e:                      # type only: messages may carry request details
-            err = type(e).__name__
-        attempt = 1 if time.monotonic() - started > max_s else attempt + 1
-        delay = restart_delay(attempt, base_s, max_s)
-        crashed.add(name)
-        _log("task_crashed", "error", task=name, error=err, attempt=attempt, restart_in_s=delay)
-        try:
-            await asyncio.sleep(delay)
-        finally:
-            crashed.discard(name)
-
-
-class LiveRuntime:
-    def __init__(self, env=None, base_url: str | None = None, client_factory=None, http=None,
-                 listener_kw: dict | None = None, restart_base_s: float = RESTART_BASE_S,
-                 reload_s: float = RELOAD_S, poll_s: float = wake.POLL_S):
-        self.env = os.environ if env is None else env
-        self.base_url = base_url or self.env.get("MATTERMOST_URL") or mattermost.MATTERMOST_URL
-        self.client_factory = client_factory or (lambda tok: Client(tok, base_url=self.base_url))
-        self._http, self.listener_kw = http, listener_kw or {}
-        self.restart_base_s, self.reload_s, self.poll_s = restart_base_s, reload_s, poll_s
-        self.status = "disabled"
-        self.state = self.holder = self.listener = self.dispatcher = None
-        self.crashed: set = set()
-        self._tasks: list = []
-
-    def _data(self, name: str) -> str:
-        return os.path.join(self.env.get("MMB_DATA_DIR", "/data"), name)
-
-    async def start(self) -> None:
-        if self.env.get("LIVE_BOTS_ENABLED", "").strip().lower() != "true":
-            _log("listener_disabled")
-            return
-        self.status = "off"
-        path, key = self._data("bots.enc"), self.env.get("MMB_STORE_KEY")
-        try:
-            cfg = store.load(path, key)
-        except StoreError as e:
-            _log("store_unreadable", "error", code=e.code, detail=e.detail)
-            # Stay `off` but keep polling: the first set-bot (or a fixed key file) starts the listener, no restart.
-            self._tasks = [asyncio.create_task(self._await_store(path, key))]
-            return
-        self._launch(path, key, cfg)
-
-    async def _await_store(self, path: str, key: str | None) -> None:
-        """Retry store.load every reload_s until it succeeds (logged once, no values), then launch."""
-        while True:
-            await asyncio.sleep(self.reload_s)
-            try:
-                cfg = store.load(path, key)
-            except StoreError:
-                continue
-            _log("store_appeared")
-            self._launch(path, key, cfg)
-            return
-
-    def _launch(self, path: str, key: str | None, cfg) -> None:
-        try:
-            self.state = State(self._data("state.db"))
-        except StateError as e:
-            _log("state_unwritable", "error", detail=e.detail)
-            return
-        self.holder = ConfigHolder(path, key, cfg)
-        kw = {"catchup_minutes": float(self.env.get("LIVE_CATCHUP_MINUTES", "15")), **self.listener_kw}
-        self.listener = Listener(self.holder.get, self.state, self.client_factory, base_url=self.base_url, **kw)
-        self.holder.subscribe(self.listener.config_changed)
-        self._http = self._http or httpx.AsyncClient()
-        self.dispatcher = Dispatcher(self.state, self.holder.get, self._http, poll_s=self.poll_s)
-        self._tasks += [
-            asyncio.create_task(supervise("listener", self.listener.run, self.crashed, self.restart_base_s)),
-            asyncio.create_task(supervise("dispatcher", self.dispatcher.run, self.crashed, self.restart_base_s)),
-            asyncio.create_task(self.holder.watch(self.reload_s)),
-        ]
-        _log("listener_start", instance=self.state.instance_id)
-
-    async def stop(self) -> None:
-        for t in self._tasks:
-            t.cancel()
-        await asyncio.gather(*self._tasks, return_exceptions=True)
-        if self._http is not None:
-            await self._http.aclose()
-        if self.state is not None:
-            await asyncio.to_thread(self.state.release_owner, "dispatcher_owner")
-            self.state.close()
-        if self._tasks:
-            _log("listener_stop")
-
-    def listener_status(self) -> str:
-        if self.listener is None:
-            return self.status
-        return "degraded" if self.crashed else self.listener.status
-
-    async def health(self) -> dict:
-        """Public /health fields: status words and a count only (no ids or names, ADR-0005)."""
-        n = 0
-        if self.state is not None:
-            n = await asyncio.to_thread(self.state.failed_count, int(time.time()) - DAY)
-        return {"listener": self.listener_status(), "wake_failed_24h": n}
+"""Live-bots runtime started from the FastAPI lifespan (slice lb5, ADR-0007/0009; plan Phase 5).
+
+LiveRuntime.start(): LIVE_BOTS_ENABLED must be "true" (else health `disabled`), the store must decrypt
+(MMB_STORE_KEY; else `off`, log store_unreadable, and re-try every RELOAD_S so the first set-bot starts the
+listener without a restart, log store_appeared) and /data/state.db must be writable (else `off`, log
+state_unwritable). Then three tasks: Listener and Dispatcher each under supervise() (crash -> log task_crashed,
+health `degraded`, restart with backoff 1->60 s; MCP keeps serving) and the ConfigHolder watcher.
+ConfigHolder (PR-2) re-reads the store when its mtime changes (every RELOAD_S): a valid new config replaces the
+old one for both tasks (listener reconnects on a new token, dispatcher reads url/secret at send time); an invalid
+file keeps the previous config (store_reload_failed). Logs carry field names and error codes, never values.
+"""
+import asyncio
+import json
+import os
+import time
+
+import httpx
+
+from app import logging as mlog
+from app import mattermost, store, wake
+from app.listener import Listener
+from app.mattermost import Client
+from app.state import DAY, State, StateError
+from app.store import StoreError
+from app.wake import Dispatcher
+
+RELOAD_S = 30
+RESTART_BASE_S, RESTART_MAX_S = 1.0, 60.0
+FIELDS = ("token", "wake_url", "wake_secret")
+
+
+def _log(event: str, level: str = "info", **fields) -> None:
+    getattr(mlog.log, level)(json.dumps({"event": event, **fields}))
+
+
+class ConfigHolder:
+    """The current BotConfig plus a generation counter; subscribers get (old, new) on a real change."""
+
+    def __init__(self, path: str, key: str | None, cfg):
+        self.path, self.key, self.cfg = path, key, cfg
+        self.generation = 0
+        self._subs = []
+        self._mtime = self._stat()
+
+    def get(self):
+        return self.cfg
+
+    def subscribe(self, fn) -> None:
+        self._subs.append(fn)
+
+    def _stat(self):
+        try:
+            st = os.stat(self.path)
+            return st.st_mtime_ns, st.st_size, st.st_ino
+        except OSError:
+            return None
+
+    def check(self) -> bool:
+        """Reload if the file changed; True if the config changed (subscribers notified)."""
+        m = self._stat()
+        if m == self._mtime:
+            return False
+        self._mtime = m
+        try:
+            new = store.load(self.path, self.key)
+        except StoreError as e:
+            _log("store_reload_failed", "warning", code=e.code, detail=e.detail)
+            return False
+        changed = [f for f in FIELDS if getattr(new, f) != getattr(self.cfg, f)]
+        if not changed:
+            return False
+        old, self.cfg = self.cfg, new
+        self.generation += 1
+        _log("store_updated", fields=changed, generation=self.generation)
+        for fn in self._subs:
+            fn(old, new)
+        return True
+
+    async def watch(self, every: float = RELOAD_S) -> None:
+        while True:
+            await asyncio.sleep(every)
+            self.check()
+
+
+def restart_delay(attempt: int, base_s: float, max_s: float) -> float:
+    """base_s * 2^(attempt-1) capped at max_s; the exponent is bounded so endless crashes cannot overflow."""
+    return min(max_s, base_s * 2 ** min(max(attempt, 1) - 1, 32))
+
+
+async def supervise(name: str, factory, crashed: set, base_s: float = RESTART_BASE_S,
+                    max_s: float = RESTART_MAX_S) -> None:
+    """Run factory() forever: on an exception (or a return) log task_crashed, mark `name` crashed while waiting
+    the backoff (1->60 s; reset after a run longer than max_s), then restart it."""
+    attempt = 0
+    while True:
+        started = time.monotonic()
+        try:
+            await factory()
+            err = "returned"
+        except asyncio.CancelledError:
+            raise
+        except Exception as e:                      # type only: messages may carry request details
+            err = type(e).__name__
+        attempt = 1 if time.monotonic() - started > max_s else attempt + 1
+        delay = restart_delay(attempt, base_s, max_s)
+        crashed.add(name)
+        _log("task_crashed", "error", task=name, error=err, attempt=attempt, restart_in_s=delay)
+        try:
+            await asyncio.sleep(delay)
+        finally:
+            crashed.discard(name)
+
+
+class LiveRuntime:
+    def __init__(self, env=None, base_url: str | None = None, client_factory=None, http=None,
+                 listener_kw: dict | None = None, restart_base_s: float = RESTART_BASE_S,
+                 reload_s: float = RELOAD_S, poll_s: float = wake.POLL_S):
+        self.env = os.environ if env is None else env
+        self.base_url = base_url or self.env.get("MATTERMOST_URL") or mattermost.MATTERMOST_URL
+        self.client_factory = client_factory or (lambda tok: Client(tok, base_url=self.base_url))
+        self._http, self.listener_kw = http, listener_kw or {}
+        self.restart_base_s, self.reload_s, self.poll_s = restart_base_s, reload_s, poll_s
+        self.status = "disabled"
+        self.state = self.holder = self.listener = self.dispatcher = None
+        self.crashed: set = set()
+        self._tasks: list = []
+
+    def _data(self, name: str) -> str:
+        return os.path.join(self.env.get("MMB_DATA_DIR", "/data"), name)
+
+    async def start(self) -> None:
+        if self.env.get("LIVE_BOTS_ENABLED", "").strip().lower() != "true":
+            _log("listener_disabled")
+            return
+        self.status = "off"
+        path, key = self._data("bots.enc"), self.env.get("MMB_STORE_KEY")
+        try:
+            cfg = store.load(path, key)
+        except StoreError as e:
+            _log("store_unreadable", "error", code=e.code, detail=e.detail)
+            # Stay `off` but keep polling: the first set-bot (or a fixed key file) starts the listener, no restart.
+            self._tasks = [asyncio.create_task(self._await_store(path, key))]
+            return
+        self._launch(path, key, cfg)
+
+    async def _await_store(self, path: str, key: str | None) -> None:
+        """Retry store.load every reload_s until it succeeds (logged once, no values), then launch."""
+        while True:
+            await asyncio.sleep(self.reload_s)
+            try:
+                cfg = store.load(path, key)
+            except StoreError:
+                continue
+            _log("store_appeared")
+            self._launch(path, key, cfg)
+            return
+
+    def _launch(self, path: str, key: str | None, cfg) -> None:
+        try:
+            self.state = State(self._data("state.db"))
+        except StateError as e:
+            _log("state_unwritable", "error", detail=e.detail)
+            return
+        self.holder = ConfigHolder(path, key, cfg)
+        kw = {"catchup_minutes": float(self.env.get("LIVE_CATCHUP_MINUTES", "15")), **self.listener_kw}
+        self.listener = Listener(self.holder.get, self.state, self.client_factory, base_url=self.base_url, **kw)
+        self.holder.subscribe(self.listener.config_changed)
+        self._http = self._http or httpx.AsyncClient()
+        self.dispatcher = Dispatcher(self.state, self.holder.get, self._http, poll_s=self.poll_s)
+        self._tasks += [
+            asyncio.create_task(supervise("listener", self.listener.run, self.crashed, self.restart_base_s)),
+            asyncio.create_task(supervise("dispatcher", self.dispatcher.run, self.crashed, self.restart_base_s)),
+            asyncio.create_task(self.holder.watch(self.reload_s)),
+        ]
+        _log("listener_start", instance=self.state.instance_id)
+
+    async def stop(self) -> None:
+        for t in self._tasks:
+            t.cancel()
+        await asyncio.gather(*self._tasks, return_exceptions=True)
+        if self._http is not None:
+            await self._http.aclose()
+        if self.state is not None:
+            await asyncio.to_thread(self.state.release_owner, "dispatcher_owner")
+            self.state.close()
+        if self._tasks:
+            _log("listener_stop")
+
+    def listener_status(self) -> str:
+        if self.listener is None:
+            return self.status
+        return "degraded" if self.crashed else self.listener.status
+
+    async def health(self) -> dict:
+        """Public /health fields: status words and a count only (no ids or names, ADR-0005)."""
+        n = 0
+        if self.state is not None:
+            n = await asyncio.to_thread(self.state.failed_count, int(time.time()) - DAY)
+        return {"listener": self.listener_status(), "wake_failed_24h": n}
"""MCP server (ADR-0003): FastMCP, Streamable HTTP, stateless, JSON responses.

Tool arguments are typed Any with an explicit JSON schema: app/validate.py (not pydantic coercion)
decides what is invalid, so every bad input is `invalid_argument` with zero Mattermost calls.
"""
import math
import time
import uuid
from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import CallToolResult
from pydantic import Field, WithJsonSchema

from app import service, validate
from app.auth import current_token, token_hash
from app.errors import ToolError, tool_error, tool_ok
from app.logging import call_line, log
from app.mattermost import MATTERMOST_URL, Client, MMError

_MESSAGES = {
    "unauthorized": "Mattermost rejected this bot's credential.",
    "mattermost_unavailable": "Mattermost is unreachable right now; try again later.",
    "mattermost_error": "Mattermost refused the request.",
    "not_found": "Not found in Mattermost.",
}


def _arg(schema: dict, description: str):
    return Annotated[Any, WithJsonSchema(schema), Field(description=description)]


Username = _arg({"type": "string", "pattern": "^[a-z0-9][a-z0-9._-]{0,63}$"}, "Mattermost username (e.g. rob).")
Team = _arg({"type": "string", "pattern": "^[a-z0-9][a-z0-9._-]{0,63}$"}, "Team name (URL name, e.g. rmlab).")
Channel = _arg({"type": "string", "pattern": "^[a-z0-9][a-z0-9._-]{0,63}$"}, "Channel name (URL name, e.g. town-square).")
Message = _arg({"type": "string", "minLength": 1, "maxLength": validate.MAX_MESSAGE}, "Message text (Markdown).")
RootId = _arg({"type": ["string", "null"], "pattern": "^[a-z0-9]{26}$"},
              "Optional thread root post id: reply in that thread (a wake's reply.root_id). The root must be a post "
              "in the same channel or DM, else invalid_root and nothing is posted. Omit to post at top level.")
Limit = _arg({"type": "integer", "minimum": 1, "maximum": validate.MAX_LIMIT},
             "How many of the newest posts to return.")


async def _dm_send(c: Client, username: str, message: str, root_id: str | None, *, me: dict) -> dict:
    return await service.dm_send(c, username, message, me=me, root_id=root_id)


def build(limiter, mm_transport=None, base_url: str = MATTERMOST_URL) -> FastMCP:
    server = FastMCP("mmbridge", stateless_http=True, json_response=True, streamable_http_path="/mcp",
                     transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False))
    identities = service.IdentityCache()

    async def run(tool: str, fn, check=lambda: (), write: bool = False, with_me: bool = False) -> CallToolResult:
        """check() validates the arguments (before any MM call) and returns them for fn(client, *args).
        with_me: also pass the caller's cached identity as fn(..., me=...)."""
        token = current_token.get()
        th = token_hash(token)
        fields = {"request_id": uuid.uuid4().hex[:12], "tool": tool, "token_hash": th[:8], "bot": None,
                  "mm_status": None}
        t0 = time.monotonic()
        client = Client(token, base_url=base_url, transport=mm_transport)
        try:
            ra = limiter.check_call(th)
            if ra:
                fields["outcome"] = "rate_limited"
                return tool_error("rate_limited", "Too many calls; slow down.", retry_after_s=math.ceil(ra))
            args = check()
            if write and (ra := limiter.check_write(th)):
                fields["outcome"] = "rate_limited"
                return tool_error("rate_limited", "Too many posts; slow down.", retry_after_s=math.ceil(ra))
            me = await identities.me(client, th)
            fields["bot"] = me["username"]
            result = await (fn(client, *args, me=me) if with_me else fn(client, *args))
            fields["outcome"] = "ok"
            return tool_ok(result)
        except ToolError as e:
            fields["outcome"] = e.code
            return tool_error(e.code, e.message, **e.extra)
        except MMError as e:
            fields["outcome"] = e.code
            extra = {"status": e.status} if e.code == "mattermost_error" else {}
            return tool_error(e.code, _MESSAGES.get(e.code, "Mattermost error."), **extra)
        except Exception:
            fields["outcome"] = "internal_error"
            log.exception("internal error request_id=%s", fields["request_id"])
            return tool_error("internal_error", "Internal bridge error (request %s)." % fields["request_id"])
        finally:
            fields["mm_status"] = client.last_status
            fields["latency_ms"] = round((time.monotonic() - t0) * 1000)
            call_line(**fields)

    @server.tool(description="List the Mattermost channels (public and private) this bot is a member of, across its teams.")
    async def list_channels() -> CallToolResult:
        return await run("list_channels", service.list_channels)

    @server.tool(description="Post a message to a Mattermost channel this bot is a member of (optionally as a "
                             "reply in a thread via root_id). Never joins channels.")
    async def post_channel(team: Team, channel: Channel, message: Message, root_id: RootId = None) -> CallToolResult:
        return await run("post_channel", service.post_channel, write=True, check=lambda: (
diff --git a/app/listener.py b/app/listener.py
index 0b4f19c..f896b5d 100644
--- a/app/listener.py
+++ b/app/listener.py
@@ -450,13 +450,22 @@ class Listener:
         team_id = ch.get("team_id", h.get("team_id")) or ""
         team = await self._get(client, self._teams, team_id, "/teams/" + team_id) if team_id else None
         user = await self._get(client, self._users, w.user_id, "/users/" + w.user_id) or {}
+        channel = {"id": w.channel_id, "name": ch.get("name", h.get("channel_name")),
+                   "display_name": ch.get("display_name", h.get("channel_display_name")),
+                   "type": w.channel_type, "team": (team or {}).get("name")}
+        sender = user.get("username") or (h.get("sender_name") or "").lstrip("@") or None
+        # Reply hints (architecture B, ADR-0015): the tool and target the woken bot answers with. A thread reply
+        # is answered in its thread; a top-level channel post and any DM are answered at top level.
+        if w.channel_type == "D":
+            reply = {"tool": "dm_send", "username": sender, "root_id": None}
+        else:
+            reply = {"tool": "post_channel", "team": channel["team"], "channel": channel["name"], "root_id": w.root_id}
         return {
-            "version": 1, "kind": "post", "delivery_id": w.post_id, "attempt": 1,
+            "version": 2, "kind": "post", "delivery_id": w.post_id, "attempt": 1,
+            "issued_at": _iso(int(self.clock() * 1000)),
             "bot": dict(self._bot),
-            "channel": {"id": w.channel_id, "name": ch.get("name", h.get("channel_name")),
-                        "display_name": ch.get("display_name", h.get("channel_display_name")),
-                        "type": w.channel_type, "team": (team or {}).get("name")},
-            "sender": {"user_id": w.user_id,
-                       "username": user.get("username") or (h.get("sender_name") or "").lstrip("@") or None},
+            "channel": channel,
+            "sender": {"user_id": w.user_id, "username": sender},
             "post": {"id": w.post_id, "message": w.message, "create_at": _iso(w.create_at), "root_id": w.root_id},
+            "reply": reply,
         }

exec
/bin/bash -lc "cat tests/unit/test_root_id.py; sed -n '1,200p' relay/relay.py; sed -n '420,500p' relay/relay.py; git diff d5dc1ae -- tests/acceptance/drivers/fake_mattermost.py tests/acceptance/drivers/live.py" in /mnt/d/rob/projects/mmbridge
 succeeded in 25ms:
"""B-s2 (ADR-0015, plan Phase 2): optional root_id on post_channel / dm_send. The root is fetched with the bot's
own token before posting and must belong to the target channel (post_channel) or the bot<->user DM (dm_send);
anything else is `invalid_root` and no post is created."""
import pytest

from conftest import call, payload, tok
from app import service, validate
from app.errors import ToolError
from app.mattermost import MMError
from drivers.fake_mattermost import FakeMattermost


@pytest.fixture
def mm():
    """Mattermost-shaped 26-char ids (root_id is validated as a Mattermost id)."""
    m = FakeMattermost(mm_ids=True)
    eddie, rob, ulrik = m.add_user("eddie", bot=True), m.add_user("rob"), m.add_user("ulrik")
    m.add_channel("rmlab", "dev", ["eddie", "rob"])
    m.add_channel("rmlab", "ops", ["eddie", "rob"])
    m.add_channel("rmlab", "hr", ["rob"], ctype="P")                      # bot is not a member
    m.dm_rob = m.direct_channel(eddie["id"], rob["id"])["id"]
    m.dm_ulrik = m.direct_channel(eddie["id"], ulrik["id"])["id"]
    m.dm_others = m.direct_channel(rob["id"], ulrik["id"])["id"]           # bot is not in it
    return m


def root(mm, where, author="rob", message="root post"):
    cid = mm.channel_by_name(where, "rmlab")["id"] if not where.startswith("dm") else getattr(mm, where)
    return mm.add_post(cid, mm.user_by_name(author)["id"], message)["id"]


def posts_created(mm):
    return [c for c in mm.changes if c[0] == "post"]


def no_post_call(mm):
    return not [c for c in mm.calls if c[0] == "POST" and c[1].endswith("/posts")]


def test_post_id_validator():
    assert validate.post_id(None) is None
    assert validate.post_id("a" * 26) == "a" * 26
    assert validate.post_id("p0000000000000000000000001") == "p0000000000000000000000001"
    for bad in ("a" * 25, "a" * 27, "A" * 26, "p-1", "", "a" * 25 + "/", "a" * 25 + "\n", 26, ["a" * 26]):
        with pytest.raises(ToolError) as e:
            validate.post_id(bad)
        assert e.value.code == "invalid_argument" and e.value.message


async def test_post_channel_root_id_replies_in_thread(bridge, mm):
    r = root(mm, "dev")
    is_err, d = payload(await call(bridge, "post_channel", {"team": "rmlab", "channel": "dev", "message": "on it",
                                                            "root_id": r}, token=tok(mm, "eddie")))
    assert not is_err, d
    assert mm.posts[d["post_id"]]["root_id"] == r and d["root_id"] == r
    assert ("GET", "/api/v4/posts/" + r, tok(mm, "eddie")) in mm.calls       # fetched with the bot's token


async def test_post_channel_without_root_id_unchanged(bridge, mm):
    is_err, d = payload(await call(bridge, "post_channel", {"team": "rmlab", "channel": "dev", "message": "hi"},
                                   token=tok(mm, "eddie")))
    assert not is_err and set(d) == {"post_id", "channel", "team", "create_at"}
    assert mm.posts[d["post_id"]]["root_id"] == ""
    assert not [c for c in mm.calls if c[1].startswith("/api/v4/posts/")]


@pytest.mark.parametrize("where", ["ops", "hr", "dm_rob"])
async def test_post_channel_root_from_another_channel_is_invalid_root(bridge, mm, where):
    """A valid root id of a post in another channel (member or not, or a DM) never posts (plan review #8)."""
    r = root(mm, where)
    is_err, d = payload(await call(bridge, "post_channel", {"team": "rmlab", "channel": "dev", "message": "x",
                                                            "root_id": r}, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "invalid_root" and d["message"]
    assert posts_created(mm) == [] and no_post_call(mm)


async def test_post_channel_unknown_root_is_invalid_root(bridge, mm):
    is_err, d = payload(await call(bridge, "post_channel", {"team": "rmlab", "channel": "dev", "message": "x",
                                                            "root_id": "z" * 26}, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "invalid_root"
    assert posts_created(mm) == [] and no_post_call(mm)


async def test_post_channel_not_member_wins_over_root(bridge, mm):
    r = root(mm, "hr")
    is_err, d = payload(await call(bridge, "post_channel", {"team": "rmlab", "channel": "hr", "message": "x",
                                                            "root_id": r}, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "not_member" and posts_created(mm) == []


@pytest.mark.parametrize("tool,args", [
    ("post_channel", {"team": "rmlab", "channel": "dev", "message": "x"}),
    ("dm_send", {"username": "rob", "message": "x"}),
])
@pytest.mark.parametrize("bad", ["p-1", "A" * 26, "a" * 25, "a" * 27, "../../users/me" + "a" * 12, 7])
async def test_bad_root_id_format_is_invalid_argument_zero_mm_calls(bridge, mm, tool, args, bad):
    is_err, d = payload(await call(bridge, tool, {**args, "root_id": bad}, token=tok(mm, "eddie")))
    assert is_err and d["code"] == "invalid_argument"
    assert mm.calls == []


async def test_dm_send_root_id_replies_in_dm_thread(bridge, mm):
    r = root(mm, "dm_rob")
    is_err, d = payload(await call(bridge, "dm_send", {"username": "rob", "message": "hello Rob", "root_id": r},
                                   token=tok(mm, "eddie")))
    assert not is_err, d
    p = mm.posts[d["post_id"]]
    assert p["root_id"] == r and p["channel_id"] == mm.dm_rob and d["root_id"] == r


@pytest.mark.parametrize("where", ["dm_ulrik", "dm_others", "dev"])
async def test_dm_send_root_from_another_conversation_is_invalid_root(bridge, mm, where):
    """Root of the bot's DM with someone else, of another users' DM (bot not in it) or of a channel post."""
    r = root(mm, where, author="ulrik" if where != "dev" else "rob")
    is_err, d = payload(await call(bridge, "dm_send", {"username": "rob", "message": "x", "root_id": r},
                                   token=tok(mm, "eddie")))
    assert is_err and d["code"] == "invalid_root" and d["message"]
    assert posts_created(mm) == [] and no_post_call(mm)


async def test_dm_send_unknown_root_creates_nothing(bridge, mm):
    is_err, d = payload(await call(bridge, "dm_send", {"username": "rob", "message": "x", "root_id": "z" * 26},
                                   token=tok(mm, "eddie")))
    assert is_err and d["code"] == "invalid_root"
    assert mm.changes == []                    # no post and no new DM conversation


class _Stub:
    def __init__(self, exc=None, post=None):
        self.exc, self.post_ = exc, post

    async def get(self, path, **_):
        if self.exc:
            raise self.exc
        return self.post_


@pytest.mark.parametrize("status", [400, 403, 404])
async def test_root_lookup_mattermost_4xx_is_invalid_root(status):
    code = {404: "not_found"}.get(status, "mattermost_error")
    with pytest.raises(ToolError) as e:
        await service.check_root(_Stub(MMError(code, status)), "a" * 26, "c" * 26)
    assert e.value.code == "invalid_root"


async def test_root_lookup_other_errors_propagate():
    with pytest.raises(MMError):
        await service.check_root(_Stub(MMError("mattermost_unavailable")), "a" * 26, "c" * 26)


async def test_root_lookup_compares_channel():
    await service.check_root(_Stub(post={"id": "a" * 26, "channel_id": "c" * 26}), "a" * 26, "c" * 26)
    with pytest.raises(ToolError):
        await service.check_root(_Stub(post={"id": "a" * 26, "channel_id": "d" * 26}), "a" * 26, "c" * 26)
    with pytest.raises(ToolError):
        await service.check_root(_Stub(post={"id": "a" * 26}), "a" * 26, "c" * 26)


async def test_tool_schema_documents_root_id(bridge, mm):
    r = await bridge.post("/mcp", headers={"accept": "application/json, text/event-stream",
                                           "content-type": "application/json",
                                           "authorization": "Bearer " + tok(mm, "eddie")},
                          json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    tools = {t["name"]: t for t in r.json()["result"]["tools"]}
    for name in ("post_channel", "dm_send"):
        prop = tools[name]["inputSchema"]["properties"]["root_id"]
        assert "thread" in prop["description"].lower()
        assert "root_id" not in tools[name]["inputSchema"].get("required", [])
"""Wake relay (ADR-0011): verifies mmbridge's HMAC-signed wakes and forwards them to a Grok Bot routine with
that bot's Bearer routine key. Own image and Coolify app; imports nothing from app/ (verify is a copy of
app.wake.verify, pinned by tests/unit/test_relay.py).

Config is env only (Coolify secrets), per bot: RELAY_BOT_<NAME>_HMAC_SECRET (copy of the bot's mmbridge wake
secret, >= 32 chars), RELAY_BOT_<NAME>_ROUTINE_URL (https), RELAY_BOT_<NAME>_ROUTINE_KEY. <NAME> is the bot
name upper-cased with '-' -> '_' (bot "my-bot" -> RELAY_BOT_MY_BOT_*). Optional: RELAY_DATA_DIR (/data),
RELAY_UPSTREAM_TIMEOUT_S (5), RELAY_RATE_PER_MIN (30), RELAY_BURST (10), RELAY_ALLOW_HTTP_UPSTREAM (tests only).
Start fails on a bot with a missing field, a short secret or a non-https URL.

POST /wake/{bot}: unknown bot 404; bad signature / stale timestamp (300 s) 401 {"reason"}; delivery already
forwarded 200 {"status": "duplicate"} (not forwarded); over the per-bot rate 429 {"reason": "rate_limited"};
else the raw body is forwarded byte-for-byte with Authorization: Bearer <key> and X-MMB-Delivery, and the
upstream result is mapped by map_upstream (2xx -> 200; 408/429/5xx/timeout/connect -> 503 so mmbridge
retries; any other status -> 424 {"upstream": code}, permanent).
Delivery guarantee (accepted risk A, Rob 2026-10-28): a delivery id is recorded in Seen only after upstream
2xx, so a lost upstream response (logged relay_delivery_ambiguous) or a crash before Seen.add can start the
routine twice; never zero times. Concurrent identical deliveries forward once (per-delivery lock + in_flight row).
GET /health: counts only. Logs: JSON lines on logger "relay", every secret and key redacted.

Tripwire (B-s2): logs relay_tripwire{reason} on HMAC failures (bad signature or stale timestamp) > 5 in 10 min
(`bad_sig`), a rate-limit hit (`rate_limited`), upstream 401/403 (`upstream_http_<code>`: key rotated/revoked) and
count drift (`double_forward`: a delivery forwarded again although an earlier forward may have started the routine,
accepted risk A). Every forward is recorded before it is sent and dropped again once the routine definitely did not
start, so a crash between upstream 2xx and Seen.add is still counted after restart. /health shows
double_forward_24h; >= 3 in 24 h is the signal to revisit option C (Rob 2026-10-28). Optional Mattermost alert
post (RELAY_ALERT_URL, RELAY_ALERT_TOKEN, RELAY_ALERT_CHANNEL = channel id; all three or none): one per reason per
10 min, for double_forward only from 3 in 24 h.
"""
import asyncio
import hashlib
import hmac
import json
import logging
import os
import re
import sqlite3
import sys
import threading
import time
from collections.abc import Mapping
from contextlib import asynccontextmanager
from dataclasses import dataclass

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

WINDOW_S = 300
MIN_SECRET = 32
SEEN_TTL_S = 24 * 3600
IN_FLIGHT_STALE_S = 60
PRUNE_EVERY_S = 3600
TRIP_WINDOW_S = 600
BAD_SIG_MAX = 5
DRIFT_ALERT = 3
ALERT_ENV = ("RELAY_ALERT_URL", "RELAY_ALERT_TOKEN", "RELAY_ALERT_CHANNEL")
FIELDS = ("HMAC_SECRET", "ROUTINE_URL", "ROUTINE_KEY")
_ENV_RE = re.compile(r"^RELAY_BOT_([A-Z0-9_]+)_(%s)$" % "|".join(FIELDS))


# --- logging with redaction ----------------------------------------------------------------------------------
_PATTERNS = [re.compile(r"(?i)bearer\s+\S+"), re.compile(r"(?i)(authorization['\"]?\s*[:=]\s*['\"]?)[^'\",}\s]+")]
_SECRETS: set[str] = set()


def register_secret(value: str) -> None:
    if isinstance(value, str) and len(value) >= 4:
        _SECRETS.add(value)


def redact(s: str) -> str:
    for p in _PATTERNS:
        s = p.sub(lambda m: (m.group(1) if m.groups() else "Bearer ") + "[REDACTED]", s)
    for v in sorted(_SECRETS, key=len, reverse=True):
        s = s.replace(v, "[REDACTED]")
    return s


class RedactFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg, record.args = redact(record.getMessage()), None
        if record.exc_info:
            record.exc_text = redact(logging.Formatter().formatException(record.exc_info))
            record.exc_info = None
        return True


log = logging.getLogger("relay")
log.setLevel(logging.INFO)
log.addFilter(RedactFilter())     # on the logger: every handler (stdout, test capture) sees redacted text


def _setup_stdout() -> None:
    if not any(getattr(h, "_relay", False) for h in log.handlers):
        h = logging.StreamHandler(sys.stdout)
        h._relay = True
        log.addHandler(h)


def _log(event: str, **fields) -> None:
    log.info(json.dumps({"event": event, **fields}))


# --- config --------------------------------------------------------------------------------------------------
class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class RelayBot:
    name: str
    hmac_secret: str
    routine_url: str
    routine_key: str


def _https_ok(url: str, allow_http: bool) -> bool:
    if url.startswith("https://") and len(url) > 8:
        return True
    return allow_http and url.startswith("http://") and len(url) > 7


def load_bots(env: Mapping[str, str]) -> dict[str, RelayBot]:
    """Bots from RELAY_BOT_<NAME>_* env vars. Errors name the bot and field, never a value."""
    raw: dict[str, dict[str, str]] = {}
    for k, v in env.items():
        m = _ENV_RE.match(k)
        if m:
            raw.setdefault(m.group(1).lower().replace("_", "-"), {})[m.group(2)] = (v or "").strip()
    allow_http = env.get("RELAY_ALLOW_HTTP_UPSTREAM", "").strip().lower() == "true"
    bots = {}
    for name, f in sorted(raw.items()):
        for field in FIELDS:
            if not f.get(field):
                raise ConfigError("bot %s: %s missing" % (name, field.lower()))
        if len(f["HMAC_SECRET"]) < MIN_SECRET:
            raise ConfigError("bot %s: hmac_secret must be at least %d characters" % (name, MIN_SECRET))
        if not _https_ok(f["ROUTINE_URL"], allow_http):
            raise ConfigError("bot %s: routine_url must be https" % name)
        bots[name] = RelayBot(name, f["HMAC_SECRET"], f["ROUTINE_URL"], f["ROUTINE_KEY"])
    return bots


# --- verify: COPY of app.wake.verify (ADR-0008); tests/unit/test_relay.py guards against drift -----------------
def _mac(secret: str, ts: str, body: bytes) -> str:
    return hmac.new(secret.encode(), ts.encode() + b"." + body, hashlib.sha256).hexdigest()


def verify(secret: str, headers: Mapping, body: bytes, now: int, window: int = WINDOW_S) -> bool:
    h = {k.lower(): v for k, v in headers.items()}
    sig, ts = h.get("x-mmb-signature"), h.get("x-mmb-timestamp")
    if not sig or not ts or not sig.startswith("v1="):
        return False
    try:
        t = int(ts)
    except ValueError:
        return False
    if abs(now - t) > window:
        return False
    if not hmac.compare_digest(sig[3:].encode(), _mac(secret, ts, body).encode()):
        return False
    # X-MMB-Delivery is not signed itself: it must equal the signed delivery_id, so a captured request
    # cannot be replayed under a new idempotency key (lb4 review 2 P2).
    try:
        signed_id = json.loads(body).get("delivery_id")
    except (ValueError, AttributeError):
        return False
    d = h.get("x-mmb-delivery")
    return bool(d) and isinstance(signed_id, str) and hmac.compare_digest(d.encode(), signed_id.encode())


def _reject_reason(headers: Mapping, now: int) -> str:
    """Reason for a failed verify: `stale` only when the timestamp itself is outside the window."""
    try:
        t = int(headers.get("x-mmb-timestamp", ""))
    except ValueError:
        return "bad_sig"
    return "stale" if abs(now - t) > WINDOW_S else "bad_sig"


def map_upstream(status: int | None) -> tuple[int, dict]:
    """Upstream routine status (None = timeout/connect error) -> relay response to mmbridge."""
    if status is not None and 200 <= status < 300:
        return 200, {"status": "forwarded"}
    if status is None or status in (408, 429) or status >= 500:
        return 503, {"reason": "upstream_unavailable", "upstream": status}
    return 424, {"upstream": status}


# --- persistent dedupe + in-flight rows ----------------------------------------------------------------------
class Seen:
    """sqlite (delivery_id PK, seen_at): deliveries the routine accepted (2xx); pruned after 24 h.
    in_flight rows guard a delivery while it is upstream; one relay process (single replica), so rows left by a
    previous process are cleared at start and rows older than IN_FLIGHT_STALE_S are taken over."""

    def __init__(self, path: str):
        self.path = path
        self._lock = threading.Lock()
        self._db = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
                if status in (401, 403):
                    self.tripwire.upstream_denied(bot.name, status)
            code, payload = map_upstream(status)
            return JSONResponse(payload, status_code=code)
        finally:
            self.seen.release(d)

    async def _forward(self, bot: RelayBot, d: str, body: bytes) -> tuple[int | None, str | None]:
        headers = {"Authorization": "Bearer " + bot.routine_key, "Content-Type": "application/json",
                   "X-MMB-Delivery": d}
        try:
            r = await asyncio.wait_for(
                self.http.post(bot.routine_url, content=body, headers=headers, timeout=self.timeout_s),
                self.timeout_s)
            return r.status_code, None
        except (httpx.ConnectError, httpx.ConnectTimeout):
            return None, "connect"                    # never reached the routine: not ambiguous
        except (httpx.TimeoutException, asyncio.TimeoutError):
            return None, "timeout"                    # may have started the routine: ambiguous
        except Exception as e:                        # type only: messages may carry request details
            return None, "error_" + type(e).__name__

    def health(self) -> dict:
        now = self.clock()
        return {"ok": True, "bots": len(self.bots), "forwarded_24h": self.seen.count_since(int(now) - SEEN_TTL_S),
                "rejected_24h": self.rejected.since(now),
                "double_forward_24h": self.seen.double_forwards_since(int(now) - SEEN_TTL_S)}


def create_app(env: Mapping[str, str] | None = None, http: httpx.AsyncClient | None = None, clock=time.time,
               seen: Seen | None = None) -> FastAPI:
    """App factory (`uvicorn relay:create_app --factory`). Raises ConfigError on bad bot env (fail fast)."""
    env = os.environ if env is None else env
    _setup_stdout()
    bots = load_bots(env)
    for b in bots.values():
        register_secret(b.hmac_secret)
        register_secret(b.routine_key)
    if seen is None:
        seen = Seen(os.path.join(env.get("RELAY_DATA_DIR", "/data"), "relay.db"))
    rate = RateLimit(float(env.get("RELAY_RATE_PER_MIN", "30")), int(env.get("RELAY_BURST", "10")))
    own_http = http is None
    client = http or httpx.AsyncClient()
    tripwire = Tripwire(clock, alert=_alerter(env, client))
    relay = _Relay(bots, client, clock, seen, rate, float(env.get("RELAY_UPSTREAM_TIMEOUT_S", "5")), tripwire)

    @asynccontextmanager
    async def lifespan(_app):
        _log("relay_start", bots=len(bots))
        yield
        if own_http:
            await client.aclose()

    app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
    app.state.relay = relay

    @app.post("/wake/{bot}")
    async def wake(bot: str, request: Request):
        return await relay.wake(bot, request)

    @app.get("/health")
    async def health():
        return relay.health()

    return app
diff --git a/tests/acceptance/drivers/fake_mattermost.py b/tests/acceptance/drivers/fake_mattermost.py
index 257a944..554ea2f 100644
--- a/tests/acceptance/drivers/fake_mattermost.py
+++ b/tests/acceptance/drivers/fake_mattermost.py
@@ -14,6 +14,9 @@ post-id anchors (fix cycle: catch-up pages by id); GET /users/{id}/channels (all
 the user's D/G channels (as Mattermost does); `ws_refuse` (REST 503 + websocket handshake 503, an MM restart);
 resume: a dropped session stays resumable (`ws_drop(resumable=True)`), keeps receiving its events in a dead
 queue, and a reconnect with `?connection_id&sequence_number` gets hello (same id, no seq) + the missed events.
+B-s2 (ADR-0015): GET /posts/{id} (403 unless the caller is in the post's channel, 404 unknown); POST /posts takes
+`root_id` (400 unless the root is a root post in the same channel, as Mattermost); `mm_ids=True` also gives posts
+Mattermost-shaped 26-char ids ("p" + 25 digits; root_id is validated as a Mattermost id).
 """
 import asyncio
 import contextlib
@@ -61,6 +64,7 @@ class FakeMattermost:
             Route("/api/v4/channels/{channel_id}/members/me", self._member_me),
             Route("/api/v4/channels/{channel_id}/posts", self._channel_posts),
             Route("/api/v4/posts", self._create_post, methods=["POST"]),
+            Route("/api/v4/posts/{post_id}", self._get_post),
             Route("/api/v4/users/ids", self._users_by_ids, methods=["POST"]),
             Route("/api/v4/users/username/{username}", self._user_by_username),
             Route("/api/v4/channels/direct", self._direct, methods=["POST"]),
@@ -119,7 +123,8 @@ class FakeMattermost:
     def add_post(self, channel_id, user_id, message, type="", root_id="", create_at=None):
         """Create a post and broadcast `posted` to the channel members' websocket sessions (as Mattermost does,
         including the author's own sessions; dead resumable sessions queue it)."""
-        pid = "p-%d" % next(self._ids)
+        n = next(self._ids)
+        pid = ("p%025d" if self.mm_ids else "p-%d") % n
         self.posts[pid] = p = {"id": pid, "channel_id": channel_id, "user_id": user_id, "message": message,
                                "create_at": self._now_ms() if create_at is None else create_at, "type": type,
                                "root_id": root_id}
@@ -308,10 +313,25 @@ class FakeMattermost:
         c, err = self._member_channel(u, body.get("channel_id"))
         if err:
             return err
-        p = self.add_post(c["id"], u["id"], body["message"])
+        root_id = body.get("root_id") or ""
+        if root_id:
+            r = self.posts.get(root_id)
+            if not r or r["channel_id"] != c["id"] or r.get("root_id"):
+                return JSONResponse({"message": "Invalid RootId parameter."}, status_code=400)
+        p = self.add_post(c["id"], u["id"], body["message"], root_id=root_id)
         self.changes.append(("post", c["id"], p["id"]))
         return JSONResponse(p, status_code=201)
 
+    async def _get_post(self, request):
+        u, err = self._auth(request)
+        if err:
+            return err
+        p = self.posts.get(request.path_params["post_id"])
+        if not p:
+            return JSONResponse({"message": "not found"}, status_code=404)
+        _, err = self._member_channel(u, p["channel_id"])
+        return err or JSONResponse(p)
+
     async def _users_by_ids(self, request):
         u, err = self._auth(request)
         if err:
diff --git a/tests/acceptance/drivers/live.py b/tests/acceptance/drivers/live.py
index 834265d..5b82c53 100644
--- a/tests/acceptance/drivers/live.py
+++ b/tests/acceptance/drivers/live.py
@@ -7,8 +7,8 @@ Backoff is scaled by WAKE_BACKOFF_SCALE so retry specs run in seconds; LIVE_ALLO
 URL be the plain-HTTP local receiver (tests only).
 
 SUT mode (env LIVE_MODE):
-- `container` (default, lb5, ADR-0010 layer 4): the real image (env LIVE_IMAGE, default mmbridge:bs1; build it
-  first with `docker build -t mmbridge:bs1 .`) on `--network host` with a fresh named volume at /data, a fresh
+- `container` (default, lb5, ADR-0010 layer 4): the real image (env LIVE_IMAGE, default mmbridge:bs2; build it
+  first with `docker build -t mmbridge:bs2 .`) on `--network host` with a fresh named volume at /data, a fresh
   MMB_STORE_KEY and LIVE_BOTS_ENABLED=true. `python -m app.admin set-bot` runs in a one-off container on the same
   volume before the server starts (as an operator would before enabling the flag); `admin failed` runs through
   `docker exec`; `/health` tells when the listener is connected; `docker logs` is the log capture for the token
@@ -20,6 +20,9 @@ secret, which forwards to a fake Grok routine (drivers/fake_routine.py, checks t
 `register_bot(name, "signed")` uses the HMAC receiver as in increment A. Wake secrets are passed to the CLI on
 stdin (`--wake-secret-stdin`, as an operator copying one secret to the relay), so the CLI never prints them.
 Wake retries: WAKE_BACKOFF_SCALE 0.25 gives ~7 s before a wake fails, enough to restart the relay container.
+B-s2 (ADR-0015): `given_routine_answers` makes the fake routine act as the bot on every started run: it follows
+the wake's `reply` hints and calls post_channel / dm_send on the real MCP bridge (/mcp of the container; in-process
+an app.main app with the fake Mattermost transport and no live runtime of its own) with the bot's own token.
 drop_connection: the fake closes the websocket (no resume: a new connection id) and refuses REST + websocket
 until restore_connection, so posts made meanwhile are reachable only by the listener's REST catch-up.
 """
@@ -45,6 +48,7 @@ from cryptography.fernet import Fernet
 from app import admin
 from app import logging as mlog
 from app.live import LiveRuntime
+from drivers import _serve
 from drivers.fake_mattermost import FakeMattermost
 from drivers.fake_routine import FakeRoutine
 from drivers.relay import RelayHarness
@@ -52,6 +56,7 @@ from drivers.wake_receiver import WakeReceiver
 
 TEAM = "rmlab"
 WAKE_WITHIN_S = 10.0       # design metric: wake within 10 s
+REPLY_WITHIN_S = 15.0      # wake + the routine's MCP call
 SETTLE_S = 0.3
 START_S = 30.0             # container start + listener connect
 MARKER_USER = "zz-marker"
@@ -74,11 +79,25 @@ def _free_port() -> int:
         return s.getsockname()[1]
 
 
+class _NoLive:
+    """The in-process MCP app's live runtime slot: the driver runs LiveRuntime itself (_InProcess.start)."""
+
+    async def start(self):
+        pass
+
+    async def stop(self):
+        pass
+
+    async def health(self):
+        return {}
+
+
 class _InProcess:
     """app.admin.main + app.live.LiveRuntime on the driver's event loop."""
 
     def __init__(self, drv, env):
         self.drv, self.env, self.runtime = drv, env, None
+        self._mcp = None
         self._saved = {k: os.environ.get(k) for k in env}
         os.environ.update(env)
         self._log = _Capture()
@@ -98,11 +117,25 @@ class _InProcess:
     def listener(self):
         return self.runtime.listener_status() if self.runtime else "off"
 
+    def mcp_url(self):
+        """The real MCP bridge (app.main) over HTTP, Mattermost = the fake (started on first use)."""
+        if self._mcp is None:
+            from app.main import create_app
+
+            async def go():
+                return await _serve.start(create_app(mm_transport=self.drv.mm.transport(), live=_NoLive()),
+                                          lifespan="on")
+            server, task, port = self.drv._run(go())
+            self._mcp = (server, task, port)
+        return "http://127.0.0.1:%d/mcp" % self._mcp[2]
+
     def logs(self):
         return "\n".join(self._log.lines)
 
     def close(self):
         try:
+            if self._mcp:
+                self.drv._run(_serve.stop(*self._mcp[:2]))
             if self.runtime:
                 self.drv._run(self.runtime.stop())
         finally:
@@ -117,7 +150,7 @@ class _Container:
 
     def __init__(self, drv, env):
         self.drv, self.env = drv, env
-        self.image = os.environ.get("LIVE_IMAGE", "mmbridge:bs1")
+        self.image = os.environ.get("LIVE_IMAGE", "mmbridge:bs2")
         self.name = "mmb-live-" + secrets.token_hex(4)
         self.volume = self.name + "-data"
         self.port = _free_port()
@@ -151,6 +184,9 @@ class _Container:
                      check=True)
         self.started = True
 
+    def mcp_url(self):
+        return "http://127.0.0.1:%d/mcp" % self.port
+
     def listener(self):
         try:
             return httpx.get("http://127.0.0.1:%d/health" % self.port, timeout=2).json()["listener"]
@@ -491,6 +527,31 @@ class LiveDriver:
         if thread is not None:
             assert w["post"]["root_id"] == self.posts[thread], "wake does not name the thread %r" % thread
 
+    def given_routine_answers(self, bot, text):
+        self.routine.answer(bot, text, self._user(bot)["token"], self.sut.mcp_url())
+
+    def _conversation(self, bot, where):
+        if where.startswith("dm:"):
+            got = self.mm.direct_channels(self._user(bot)["id"], self._user(where[3:])["id"])
+            return got[0]["id"] if got else None
+        return self._channel(where)["id"]
+
+    def _bot_posts(self, bot, where, text):
+        cid, uid = self._conversation(bot, where), self._user(bot)["id"]
+        return [p for p in self.mm.channel_posts(cid) if p["user_id"] == uid and p["message"] == text] if cid else []
+
+    def assert_replied(self, bot, where, text, thread=None):
+        try:
+            self._wait(lambda: self._call(self._bot_posts, bot, where, text), REPLY_WITHIN_S,
+                       "%s's reply %r in %s" % (bot, text, where))
+        except AssertionError as e:
+            raise AssertionError("%s; routine replies: %s" % (e, self.routine.replies)) from None
+        got = self._call(self._bot_posts, bot, where, text)
+        assert len(got) == 1, "expected one reply %r from %s in %s, got %d" % (text, bot, where, len(got))
+        want_root = self.posts[thread] if thread is not None else ""
+        assert got[0]["root_id"] == want_root, \
+            "reply root_id %r, expected %r (%s)" % (got[0]["root_id"], want_root, thread or "top level")
+
     def assert_routine_not_started(self, bot, message):
         mid = self._barrier(bot)
         runs = [r for r in self.routine.runs(bot) if self.routine.post_id(r) != mid]

exec
/bin/bash -lc "nl -ba app/service.py | sed -n '65,90p'; .venv/bin/pytest tests/unit/test_root_id.py tests/unit/test_relay.py -q" in /mnt/d/rob/projects/mmbridge
exec
/bin/bash -lc "nl -ba relay/relay.py | sed -n '303,318p'; python3 .eng/bin/eng-check ." in /mnt/d/rob/projects/mmbridge
 succeeded in 8521ms:
    65	    try:
    66	        root = await c.get("/posts/%s" % segment(root_id))
    67	    except MMError as e:
    68	        if e.status in (400, 403, 404):
    69	            raise ToolError("invalid_root", _BAD_ROOT)
    70	        raise
    71	    return root if isinstance(root, dict) else {}
    72	
    73	
    74	def _same_channel(root: dict, channel_id: str) -> None:
    75	    if root.get("channel_id") != channel_id:
    76	        raise ToolError("invalid_root", _BAD_ROOT)
    77	
    78	
    79	async def check_root(c: Client, root_id: str, channel_id: str) -> None:
    80	    """The root must be a post in `channel_id` the bot can see; checked before any write."""
    81	    _same_channel(await _root(c, root_id), channel_id)
    82	
    83	
    84	def _new_post(channel_id: str, message: str, root_id: str | None) -> dict:
    85	    return {"channel_id": channel_id, "message": message, **({"root_id": root_id} if root_id else {})}
    86	
    87	
    88	async def post_channel(c: Client, team: str, channel: str, message: str, root_id: str | None = None) -> dict:
    89	    ch = await _member_channel(c, team, channel)
    90	    if root_id:
........................................................................ [ 70%]
..............................                                           [100%]
102 passed in 4.85s

 succeeded in 2343ms:
   303	        self.alert(reason, fields)
   304	
   305	    def bad_sig(self, bot: str) -> None:
   306	        now = self.clock()
   307	        self._bad = [t for t in self._bad if now - t < TRIP_WINDOW_S] + [now]
   308	        if len(self._bad) > BAD_SIG_MAX:
   309	            self._trip("bad_sig", bot=bot, failures_10m=len(self._bad))
   310	
   311	    def rate_limited(self, bot: str) -> None:
   312	        self._trip("rate_limited", bot=bot)
   313	
   314	    def upstream_denied(self, bot: str, code: int) -> None:
   315	        self._trip("upstream_http_%d" % code, bot=bot)
   316	
   317	    def double_forward(self, bot: str, delivery: str, count_24h: int) -> None:
   318	        self._trip("double_forward", alert=count_24h >= DRIFT_ALERT, bot=bot, delivery=delivery,
WARN  .eng/runners.toml: no on_complete hook configured ([hooks] empty or missing) - bots must stay attached to eng-run until exit; fire-and-forget needs a non-empty on_complete / <role>_on_complete (PROCESS.md section 10, LESSONS L-006)
WARN  PROJECT_STATE.md: ## Latest artifacts has 40 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 36 rows / 7331 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 158 artifact(s) checked

codex
Thread-root validation misses reply posts, and failed-signature tracking introduces an avoidable resource-exhaustion path. The 102 focused root-id and relay tests pass but do not cover these cases.

Full review comments:

- [P2] Reject non-root posts before attempting a thread reply — /mnt/d/rob/projects/mmbridge/app/service.py:74-76
  If `root_id` identifies a reply within the target conversation, this check succeeds even though Mattermost requires a top-level thread root. Both tools then attempt the write and return generic `mattermost_error` instead of `invalid_root`; the updated fake Mattermost also explicitly rejects this case. Check that the fetched post has no `root_id` before posting, and add coverage for both tools.

- [P2] Bound the failed-signature tracking state — /mnt/d/rob/projects/mmbridge/relay/relay.py:305-309
  A stream of invalid signatures to a configured bot retains one timestamp per request for ten minutes and copies/scans the entire list on every request. These requests bypass the authenticated rate limiter, so unauthenticated traffic can cause increasing memory consumption and quadratic processing work on the event loop, delaying legitimate wakes. Use bounded time buckets or another bounded sliding-window counter instead of storing every failure.
Thread-root validation misses reply posts, and failed-signature tracking introduces an avoidable resource-exhaustion path. The 102 focused root-id and relay tests pass but do not cover these cases.

Full review comments:

- [P2] Reject non-root posts before attempting a thread reply — /mnt/d/rob/projects/mmbridge/app/service.py:74-76
  If `root_id` identifies a reply within the target conversation, this check succeeds even though Mattermost requires a top-level thread root. Both tools then attempt the write and return generic `mattermost_error` instead of `invalid_root`; the updated fake Mattermost also explicitly rejects this case. Check that the fetched post has no `root_id` before posting, and add coverage for both tools.

- [P2] Bound the failed-signature tracking state — /mnt/d/rob/projects/mmbridge/relay/relay.py:305-309
  A stream of invalid signatures to a configured bot retains one timestamp per request for ten minutes and copies/scans the entire list on every request. These requests bypass the authenticated rate limiter, so unauthenticated traffic can cause increasing memory consumption and quadratic processing work on the event loop, delaying legitimate wakes. Use bounded time buckets or another bounded sliding-window counter instead of storing every failure.
````
