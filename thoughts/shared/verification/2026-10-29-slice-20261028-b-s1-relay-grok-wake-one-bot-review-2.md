---
id: REVIEW-20261029-slice-20261028-b-s1-relay-grok-wake-one-bot-review-2
type: review-findings
phase: verify
status: open
owner_agent: eng-run
date: 2026-10-29
links: [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md]
review_kind: slice
subject: "SLICE-20261028-b-s1-relay-grok-wake-one-bot (thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md)"
diff: bc73656...abf873a
reviewer: codex
command: "codex review --base bc73656"
run_log: thoughts/shared/runs/2026-10-29-code-review-slice-20261028-b-s1-relay-grok-wake-one-bot-2.md
---
# Independent review: code-review slice-20261028-b-s1-relay-grok-wake-one-bot
<!-- Written by eng-run (prompt code-review v2). Each finding row starts 'open': set disposition fixed (where) |
     accepted-risk (ONLY with Rob's approval, e.g. "Rob 2026-10-29") | rejected (reason). Plan reviews gate
     implementation (medium/large); slice reviews are advisory. -->

## Findings
| # | Severity | Location | Finding | Disposition | Reason / approval |
|---|---|---|---|---|---|

No findings.

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
session id: 01a18b03-f08a-7ef1-a55a-7af3b9481da5
--------
user
changes against 'bc73656'
exec
/bin/bash -lc 'cat PROJECT_STATE.md; git status --short; git diff --stat bc73656559d88e45f7f525d0c8f921d6e034e18d' in /mnt/d/rob/projects/mmbridge
 succeeded in 1019ms:
---
id: STATE
type: project-state
phase: implement
status: active
owner_agent: claude-code
date: 2026-10-29
links: []
triage: large             # unset | small | medium | large
active_slice: SLICE-20261028-b-s1-relay-grok-wake-one-bot
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
[SLICE-20261028-b-s1-relay-grok-wake-one-bot](thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md) (review: implemented cd07811, awaiting Codex review + eng-verify). Previous: lb5 [done](thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md)

## Next action
B-s1: Codex slice review (codex not available on the implementer shell) -> eng-verify -> Rob runs relay/spike_routine.py (OQ-B1/B2) -> CP-S. Then B-s2, B-s3. Open: live Mattermost-restart resume check (TODOS, deferred); OWNER-GUIDE pointer (TODOS P2); flaky timing tests (TODOS P2).

## Blockers
- none

## Pending approvals
See `pending_approvals` in the front matter (the only copy; `.eng/bin/eng-status` renders it). Do not list items here.

## Back-ups to an earlier phase
<!-- date - from phase -> to phase - why (blameless) - artifacts revised -->
none

## Latest artifacts
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
?? receiver.py
?? thoughts/shared/inbox-local-bak-1793080755/
?? thoughts/shared/inbox.md
?? thoughts/shared/runs/2026-10-28-implement-slice-20261027-lb5-wireup-reconnect-acceptance.md
?? thoughts/shared/runs/2026-10-29-code-review-slice-20261028-b-s1-relay-grok-wake-one-bot-2.running.md
?? thoughts/shared/runs/2026-10-29-code-review-slice-20261028-b-s1-relay-grok-wake-one-bot.md
?? thoughts/shared/runs/2026-10-29-implement-slice-20261028-b-s1-relay-grok-wake-one-bot-2.md
?? thoughts/shared/runs/2026-10-29-implement-slice-20261028-b-s1-relay-grok-wake-one-bot.md
?? thoughts/shared/verification/2026-10-29-slice-20261028-b-s1-relay-grok-wake-one-bot-review.md
 AGENTS.md                                          |   7 +-
 CHANGELOG.md                                       |   4 +
 OWNER-GUIDE.md                                     |   2 +
 PROJECT_STATE.md                                   |  10 +-
 README.md                                          |   6 +
 coolify-service.snippet.yaml                       |  26 ++
 relay/.dockerignore                                |   4 +
 relay/Dockerfile                                   |  20 ++
 relay/README.md                                    |  78 +++++
 relay/relay.py                                     | 367 +++++++++++++++++++++
 relay/requirements.txt                             |   3 +
 relay/spike_routine.py                             |  46 +++
 tests/acceptance/drivers/_serve.py                 |  22 ++
 tests/acceptance/drivers/fake_routine.py           |  59 ++++
 tests/acceptance/drivers/live.py                   | 212 +++++++++++-
 tests/acceptance/drivers/relay.py                  | 261 +++++++++++++++
 tests/unit/test_relay.py                           | 364 ++++++++++++++++++++
 ...29_23-08-07_b-s1-implemented-awaiting-review.md |  70 ++++
 .../plans/2026-10-28-grok-webhook-multibot.md      |   2 +-
 .../2026-10-28-b-s1-relay-grok-wake-one-bot.md     |  52 ++-
 20 files changed, 1575 insertions(+), 40 deletions(-)

exec
/bin/bash -lc 'cat thoughts/shared/handoffs/2026-10-29_23-08-07_b-s1-implemented-awaiting-review.md; cat .eng/PROCESS.md; cat .claude/skills/eng-review/SKILL.md; find . -name AGENTS.md -o -name AGENTS.override.md; python3 .eng/bin/eng-check .' in /mnt/d/rob/projects/mmbridge
 succeeded in 2644ms:
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

## 8. Session convention (every skill's Start and Finish)
Skills say "Session: standard" instead of repeating this.
- **Start:** new session. Read only `PROJECT_STATE.md`, the latest handoff it links, and the skill's Inputs. Run `.eng/bin/eng-check .`; if it fails for a reason this skill must not fix, stop and report. If `pending_approvals` holds a checkpoint this skill needs, stop.
- **Finish:** update PROJECT_STATE (`phase`, `active_slice`, `pending_approvals`, `owner_agent`, `date`, Next action, Blockers, Latest artifacts) as part of **eng-handoff**, which is the session end. It writes `thoughts/shared/handoffs/YYYY-MM-DD_HH-MM-SS_<slug>.md` (Tasks+status, Critical References, Recent changes file:line, Learnings, Artifacts, Approvals, Next Steps naming the next skill), runs `.eng/bin/eng-check .` (must pass) and commits the docs. eng-handoff and eng-resume don't call themselves.
- **Resume:** eng-resume reads PROJECT_STATE, the linked handoff fully, then only its Critical References; verifies Recent changes exist (git); reports discrepancies; proceeds only if no needed approval is pending.
- **Latest artifacts (v2.5.8):** PROJECT_STATE `## Latest artifacts` lists the current increment / in-play artifacts only, plus the standing links (AGENTS.md, OWNER-GUIDE.md, docs/definition-of-done.md, thoughts/shared/process-feedback.md, latest handoff). Finished increments move to the optional `## Prior increments` section, which eng-resume does not read. eng-check warns above 12 in-play links.
- **Approval log size (v2.5.8):** eng-check warns when the `## Approval log` table exceeds 40 rows or the section exceeds 3072 bytes. When this fires on an active project, reopen the Approval-log archive design; from then on eng-check must treat the archive as part of the log. No archive exists yet.
- **Stale kit:** when eng-check warns that `.eng/VERSION` is older than the kit, eng-resume asks Rob once per session (Action-for-Rob shape) whether to run `eng upgrade .`, unless `kit_upgrade: deferred` is set in PROJECT_STATE front matter or in `thoughts/shared/process-feedback.md`.
- If the next agent must ask "what was I doing?", the handoff is defective. Log it in `process-feedback.md`.
- Session handoff and **project brief** are different: the handoff passes one session to the next; a brief (`.eng/bin/eng-new brief`) orients a new implementer or reviewer and points at the plan and state.

## 9. Rules for every agent
Recommend; Rob decides. Never weaken a gate or use `--no-verify`. A report is a claim until re-executed. Stop and report on plan/code mismatch ("Issue in Phase N") instead of improvising. No fix without root cause; after 3 failed fixes, stop and hand off. Log process friction in `thoughts/shared/process-feedback.md` as you hit it (in-session; the retro reads that log, not handoffs).

**Owner-facing updates (every project bot).** When you message Rob, use the shape in `.eng/templates/owner-update.md` (LESSONS L-007): (1) brief status prose, or skip if nothing new; (2) a labeled `**Action for Rob**` numbered list — one concrete step per line, pasteable commands each in their own fenced block — or the exact line `No action for you.`; (3) end with the decision he owes when any (`approve` / `defer` / `needs fixes` / `hold` / named CP). Never bury his todos inside a paragraph that mixes status, review results, and an inline list. In sample commands, never use valid shell syntax as an edit placeholder (`$TOKEN`, `${BOT_TOKEN}`); use `PASTE_BOT_TOKEN_HERE` or tell him to paste at the prompt.

**Risk mitigations the agent uncovered.** If the agent finds a risk and would design a mitigation into the design doc, architecture, or plan, that mitigation is not free to absorb. Before it lands: name the risk; cost it (money and especially friction/ops burden); offer a narrower alternative; stop with L-007 **Decision needed** (absorb / accept risk / defer / narrower). Soft acknowledgment is not approval of the cost. Shape: `.eng/templates/owner-update.md` (LESSONS L-008).

## 10. Working agreements (standard; values in PROJECT_STATE front matter)
| Field | Default | Meaning |
|---|---|---|
| `implementer` | `claude-code` | Who writes code: Claude Code on the owner's own PC. Never name it in design docs; reference this field. |
| `planner` | `grok-bot` | Grok Bot assistants plan, write docs, keep state and process. They don't write production code. |
| `cross_review` | `codex-advisory` | Independent cross-model review; advisory, never a gate. `none` disables. |
| `push_permission` | `ask` | `ask` = ask the owner before each push (**except docs-only**); `standing` = after eng-verify PASS, may push to `main` without asking; **docs-only commits always push to `main` without asking** (both modes); tags and force-push still ask; never merge without the owner. Docs-only = documentation/process prose only (Markdown under docs/, thoughts/, templates, PROCESS, README, CHANGELOG, OWNER-GUIDE, AGENTS, LESSONS, skill wording) — no source, tests, scripts, behavior-shipping VERSION, or runtime config (e.g. `runners.toml`). |
| `board` | `none` | Optional Kanban (e.g. self-hosted Vikunja, deferred). If used: board only, one card per slice linking to the repo plan/slice card. The repo stays the single source of truth; never record decisions on the board. |

**Implementer hand-off loop.**
1. When a slice is ready (plan approved with its mandatory plan review clean (M/L), slice is next in PROJECT_STATE `active_slice` with `status: todo`, `pending_approvals` empty, `.eng/bin/eng-check` OK), the planner **starts** implementation on the owner's PC: `python3 .eng/bin/eng-run implement <plan> <slice-id>` (or `eng run implement ...` with the global CLI), then tells Rob once, as FYI, with the standard message from `.eng/templates/ready-to-implement.md` (`.eng/bin/eng-status` prints it filled). His CP-C / slice-ready approval covers starting implement unless he said otherwise — start it; do not block on a one-line ask. **Fallback:** if eng-run or the Claude CLI is unavailable, or Rob wants to drive Claude interactively, send the paste prompt from the same message: `Run eng-resume, then eng-implement-slice for <slice> per <plan>`. Work keeps running until Rob interjects or a real decision is due: CP-S, a push when `push_permission: ask` (docs-only commits push without asking), eng-check failures, locked-spec issues, open critical/high plan-review findings, blockers. **Completion signal:** whoever starts `eng-run implement` owns its completion. Stay on the run (or resume when the process exits), then read the new run log in `thoughts/shared/runs/` plus the latest handoff / PROJECT_STATE, and either continue (eng-verify, request CP-S) or surface the blocker to Rob. No fire-and-forget: Rob should never have to paste the handoff filename back. If the starter cannot stay attached, configure the opt-in `[hooks] implement_on_complete` in `.eng/runners.toml` (e.g. curl a planner routine webhook) so the planner is woken on every exit, ok or failed. Same rule for headless plan-review / code-review runs; see "Wake pair + PID harness" below.
2. The implementer runs the slice on the owner's PC, ends with eng-handoff.
3. **Independent review (advisory):** before eng-verify, the cross-model review runs on the slice diff. Findings go to `thoughts/shared/verification/<date>-<slice>-review.md` (`.eng/bin/eng-new review <slug>`). The implementer fixes or answers each finding, then eng-verify runs.
4. The planner picks up the implementer's handoff and runs `eng-verify` and `.eng/bin/eng-check`, then requests CP-S.

**Mandatory plan review (medium and large; small exempt).** After the plan and slice cards are drafted and before CP-C, the **planner starts** the review on the owner's PC — do not hand Rob the command as the default. Prefer `python3 .eng/bin/eng-run plan-review <plan>` (runner from `.eng/runners.toml`; writes findings + run log and sets empty `plan_review:`). Fallback (eng-run / Codex unavailable, or Rob wants to drive it): `codex exec "review <plan path> and the slice cards <slice glob> against <design doc> (REQ ids), <architecture doc> and <ADR range> for gaps, wrong ordering, missing tests, and security holes; output a numbered list of findings with severity" -o thoughts/shared/verification/<date>-<slug>-plan-review.md`. Drafting the plan for CP-C covers starting this run; tell Rob once as FYI. Own completion (wake pair, PROCESS section 10); then disposition findings and ask for CP-C only when clean. **Codex output always goes straight to a file in the repo, never only the terminal.** Turn that file into the findings artifact in place: add the review-findings front matter and Findings table (from `templates/review-findings.md`) above the raw output ("Reviewer raw output"). Link it from the plan's `plan_review:` field. Each finding gets a severity (critical/high/medium/low) and a disposition: `fixed` (where), `accepted-risk` (only with Rob's approval, recorded in the row), or `rejected` (with a reason). `.eng/bin/eng-check` fails, for medium/large triage, if a slice is in-progress or the phase is implement/verify/ship without a linked plan review, or with any critical/high finding still `open`. **Grandfathered plans** (approved before the review was mandatory): before the next slice starts, either run the review retroactively (same command, link it in `plan_review:`, fix/disposition findings), or record Rob's waiver in the Approval log: `| <date> | CP-C | <plan path> | waiver: plan review - approved by Rob |`. eng-check's error names both routes. This is the one review that is a gate; slice-diff and architecture reviews stay advisory. Work keeps running until Rob interjects or a consequential decision is due (CP approvals, `accepted-risk`, push when `ask` except docs-only, blockers) — starting plan-review / implement / code-review is not a stop.

**Cross-model review (Codex), advisory.** Run it on every slice diff before Rob approves the slice (always for auth, tenancy or security work), and on architecture docs for large work (plans: see the mandatory review above). Skip it for small or docs-only changes (write "skipped: <reason>" in the verification report). In Claude Code, gstack's `/codex` calls the real Codex CLI (diffs: `codex review --base <base> > thoughts/shared/verification/<date>-<slice-slug>-review.md`; documents: `codex exec "<prompt>" -o thoughts/shared/verification/<date>-<slug>-review.md`; always written into the repo). That needs `npm install -g @openai/codex` and `codex login` once on the owner's PC. Findings are recorded in the findings file and summarized in the verification report's "Cross-model review" section. They are advice: Rob decides, and no finding blocks by itself.

**Windows owner machines.**
- Line endings: set per command, not globally: `git -c core.autocrlf=false <cmd>` (or `input`). Kit files are LF.
- Encoding: write files as UTF-8 **without BOM** (PowerShell 5: `Out-File -Encoding utf8` adds a BOM; use `[IO.File]::WriteAllText` or PowerShell 7 `utf8NoBOM`). The scripts tolerate a BOM and print ASCII only.
- Archiving a repo to move it: include dotfiles and `.git` (`tar -czf repo.tgz -C <parent> <repo>`; Explorer's "Send to zip" can skip them).

**Headless agent runs (`eng-run`, v2.3).** From the repo root: `python3 .eng/bin/eng-run plan-review <plan>`, `... implement <plan> <slice-id>`, `... code-review <slice-id | --base REF>`. Prompts are `.eng/prompts/<role>.md` (kit-owned); the runner per role is `.eng/runners.toml` (project-owned, created once; defaults implement=claude, plan-review/code-review=codex), overridable by `ENG_RUNNER_<ROLE>` or `--runner` (`claude`, `codex`, or a `[runners.<name>]` `command` runner). Rules: every run writes a run log `thoughts/shared/runs/<date>-<role>-<target>.md` (command, prompt, output, exit code); every review also writes a review-findings file in `thoughts/shared/verification/` with rows `open` until dispositioned; review output never lives only in the terminal. Plan reviews set an empty `plan_review:` so eng-check's gate applies. eng-run refuses a review by the same runner that implemented the slice (run log, else PROJECT_STATE `implementer`) unless `--allow-self-review`, which must be named in the verification report. `--dry-run` prints the exact command without running. Bots start eng-run on Rob's PC when the process covers it (plan drafted → plan-review; CP-C → implement; slice ready for verify → code-review) and tell him as FYI; ask only for ad-hoc runs outside those paths, or when he said otherwise.

**Wake pair + PID harness (every autonomous eng-run role, v2.5.4; harden v2.5.7).** Applies to `plan-review`, `implement` and `code-review` alike; the starter still owns completion. **Default: stay attached** until eng-run exits (S runs — plan-review / code-review — especially). Fire-and-forget is allowed only when a non-empty `on_complete` / `<role>_on_complete` hook is configured; otherwise eng-run prints a WARNING and eng-check warns on empty `[hooks]`. Set up both halves when you will not watch:
- (A) **Callback:** `[hooks]` in `.eng/runners.toml`. Role-specific `implement_on_complete` / `plan_review_on_complete` / `code_review_on_complete` wins; else the general `on_complete` fires for any role. Runs on every exit (ok or failed) after the run log is written; env `ENG_ROLE ENG_EXIT_CODE ENG_STATUS ENG_RUN_LOG ENG_REPO ENG_PLAN ENG_SLICE ENG_HANDOFF ENG_PID ENG_ENG_RUN_PID`. Empty = stay attached.
- (B) **Effort-based timeout routine** as backup (required if you detach). Starting points by effort: S 45m, M 2h, L 4h (reviews are usually S, implement M or L).
- **PID marker:** right after the runner starts, eng-run writes `thoughts/shared/runs/<stem>.running.md` (`status: running`, `pid`, `eng_run_pid`, `role`, `slice`, `target`, `started`, `run_log`) and deletes it when it writes the finished run log (which also records `pid` / `eng_run_pid`). Marker present = still running or died abruptly.
- **When the timeout fires,** classify with the marker: (1) pid alive past the deadline: soft ping to Rob, optionally extend once by one band; (2) pid dead and a finished run log or new handoff exists: missed callback, wake the starter to resume from it; (3) pid dead and no completion artifact: auto-troubleshoot. Known project-side fixes (config, prompt, missing dependency in the repo) get one retry; otherwise hand platform / environment / silent-subprocess failures to **Ulrik** (sys admin) with: (a) what failed (role + exact command), (b) exact error or symptom plus paths (run log, handoff, marker), (c) what was already tried, (d) machine label and whether it is a registered computer (e.g. Merkle) or the shared box. The project bot owns the re-launch after Ulrik's fix.

## 10a. The kit travels with the repo
The kit is vendored into every repo, so any agent on any machine (box, WSL, Git Bash, macOS) has it without the kit source: skills in `.claude/skills/<name>/SKILL.md`, scripts in `.eng/bin/`, prompts in `.eng/prompts/`, version in `.eng/VERSION`. Always call scripts by repo-relative path from the repo root, through the interpreter (no shebang reliance): `python3 .eng/bin/eng-check .` on Linux/macOS/WSL/Git Bash, `python .eng/bin/eng-check .` or `py .eng/bin/eng-check .` on native Windows. Every path the scripts compare or print is normalized to POSIX form (`/`), so backslash paths in front matter, links or the Approval log work too; always write `/` in docs. Commit `.eng/` and `.claude/skills/`. Never edit vendored files in a repo; change the kit and re-vendor.
- **Upgrade an existing repo** (planner, from the kit source): `<kit>/bin/eng-init <repo> --upgrade`. It overwrites only kit-owned files (`.eng/bin`, `.eng/templates`, `.eng/prompts`, `.eng/PROCESS.md`, `.eng/VERSION`, `.claude/skills/eng-*`), never project files; commit the result as "chore: vendor eng-process vX.Y.Z".
- `--upgrade` also: refreshes template comments/help text in project files (AGENTS.md, CLAUDE.md, OWNER-GUIDE.md, PROJECT_STATE.md body, DoD, ...) only where a section is still unchanged kit boilerplate, and prints every owner-edited stale section to update by hand (never overwrites owner content; front matter untouched); adds an empty `plan_review:` to plans lacking it; maintains the `# >>> eng-process defaults` block in `.gitignore` (`__pycache__/`, `*.pyc`, `.venv/`, ...) adding only lines not already present anywhere in the file (no duplicate block), and prints (never runs) `git rm -r --cached -- <files>` for tracked files the ignore rules now match. `__pycache__`/`.pyc` are never vendored. Stale sections are reported by name with a short diff. New checks start warn-only for one version (stray approvals: warn until v2.4.0; `eng-check --strict` makes them errors).
- `eng-check` fails if `.eng/bin` or `.claude/skills/eng-*` is missing, and warns when `.eng/VERSION` is older than the kit running it (or `$ENG_KIT/VERSION` if set).
- **Optional global install on a dev machine:** copy the skills to Claude Code's personal skill dir so they work in every repo: `mkdir -p ~/.claude/skills && cp -r <repo>/.claude/skills/eng-* ~/.claude/skills/` (WSL: inside the WSL home; Git Bash: `%USERPROFILE%\.claude\skills`). Project skills in the repo are still the source of truth; scripts are always taken from the repo's `.eng/bin/`.

## 11. Brownfield adoption and migration
Use `<kit>/bin/eng-init <repo> --brownfield` (eng-project-init "brownfield mode"). It lists every pre-existing markdown file with a suggested destination and type (a heuristic from its name and path; confirm each).
1. **Never delete history.** Move pre-kit docs with `git mv <old> <new>` in a dedicated commit (`chore: adopt eng-process layout`) so `git log --follow` works. Don't mix moves with content edits in one commit.
2. **Map each doc** to a kit location and type: vision/feature list -> `docs/vision/`; design/spec -> `docs/design/`; architecture -> `docs/architecture/`; codebase notes -> `thoughts/shared/research/`; external/market research -> `thoughts/shared/market-research/`; plans -> `thoughts/shared/plans/`; orientation docs for an implementer -> `thoughts/shared/briefs/`. Add front matter; unknown status -> `draft`.
3. **ADRs:** kit format is `docs/decisions/NNNN-slug.md` with id `ADR-NNNN` (4 digits). Migrate `ADR-001` style: `git mv docs/adr/001-x.md docs/decisions/0001-x.md`, set `id: ADR-0001`, then rewrite cross-references (`grep -rl 'ADR-0\?\([0-9]\{2,3\}\)'` then `sed -E 's/ADR-([0-9]{3})\b/ADR-0\1/g'`, reviewed). Keep numbers stable; never renumber to close gaps. Map old statuses: Deferred -> `deferred`; "accepted with parts open" -> `partially-accepted` + `## Parts`.
4. **Back-fill the Approval log** for decisions already accepted before the kit: one row per artifact, Checkpoint `pre-kit`, Decision `approved (back-filled, pre-kit)` / `accepted (...)`, date = original decision date if known. Set statuses to match. `.eng/bin/eng-check` then passes the log/status cross-check.
5. Delete only generated or duplicate files, and only with Rob's OK. Superseded docs get `status: superseded`.
6. Run the eng-triage **readiness check** to set the true phase.

## 12. Learning loop: predictions, evidence, lessons, adoption
- **Predictions.** Every ADR, advisor-consultation note and retro recommendation records *Expected outcome*, *Check date* and *What would prove it wrong* (templates `adr.md`, `retro.md`). eng-retro scores each past entry whose check date has passed as **right / wrong / unclear** with one line of evidence, in the retro and on the entry's `Score:` line.
- **Rejecting a finding.** A rejected Codex (or any reviewer) finding needs evidence in its Reason cell: a `file:line` (e.g. `src/auth.py:42`) or a test reference (e.g. `tests/test_auth.py::test_expired_token`). `eng-check` fails rejected rows without either (an error since v2.5.0). Retros record the **review hit-rate**: findings accepted vs rejected, and real bugs caught.
- **Research provenance.** Each research file starts with a provenance header: per source, the source (URL or repo), the commit (repos: pinned SHA) or date read (web), and `verified` (checked against the source by the author) or `unverified`. Pin cloned source repos to a commit and record it. When a consultation or decision relies on research, run a **staleness diff** first (`git -C <src> fetch && git -C <src> log --oneline <pinned>..origin/HEAD -- <paths relied on>`; web sources: re-read the page) and note the result. **Snapshot** a web page (save a copy next to the research with its fetch date) only when a decision-driving claim rests on it, and do it at re-derivation time, not by default. See `SOURCES.md`.
- **Kit lessons.** Format **"when X, do Y, because Z"** with origin, confirmation count and status (`templates/kit-lesson.md`). A lesson is a *hypothesis* until a second project confirms it. eng-retro proposes them; **Rob approves** each before it enters the kit's `LESSONS.md`.
- **Design adoption.** `process-feedback.md` has a *Design adoption* section: each kit step adopted or skipped, with reason. A skip the owner made knowingly (informed-owner skip) is recorded but not counted. **Two counted non-safety skips of the same step raise a redesign flag** for that step. **Any skip of a safety gate** (personal data handling, mandatory plan review, CP approvals) **is escalated to Rob immediately.**
- **Waste and time.** Each retro answers "which step felt like waste?" and records rough time per phase, so the kit can be trimmed with evidence.
- **Frontend legibility.** Architecture reviews always ask: *Can the owner judge this frontend's behaviour and code? If not, what reduces that gap?* Plans include a short **Demo script**. Frontend CI checks are opt-in and size-dependent: `.eng/templates/ci-checklist.md` (not enforced by eng-check).

## 13. Executable specifications (v2.5; Dave Farley's ATDD four-layer model)
**Two kinds of "spec", one direction.** *Design-side specs* (the design doc, the architecture doc, ADRs) say **what**
to build and **how** to build it; they are the authority. *Executable specs* are the **test-side** expression of the
design doc's requirements (REQ-n) and its plain-language acceptance examples: pytest tests in domain language under
`tests/acceptance/specs/`, each pointing back at its requirement with `@pytest.mark.req("REQ-n")` (the design doc's
id). They never introduce requirements; a spec without a REQ, or a REQ without a spec, is a gap to fix in the design
doc or the specs.

**Four layers** (`.eng/templates/acceptance/`, copied by `eng-spec init`):
1. **Specs** (`specs/`): what, never how; no URLs, selectors, status codes or sleeps; each creates its own data.
2. **DSL** (`dsl.py`): the shared domain vocabulary; aliases names per run (functional and temporal isolation).
3. **Protocol drivers** (`drivers/`): `api` (httpx), `ui` (Playwright), `mcp`. All system knowledge lives here.
4. **System under test**: deployed like production, started outside the tests; external systems stubbed at its boundary.

**By size.** Small: unchanged (unit/regression tests; no executable specs). Medium: specs on the API channel.
Large: API channel plus one Playwright web journey (`@pytest.mark.channels("api", "ui")`), with an ADR from
`.eng/templates/adr-acceptance-tests.md`.

**Approvals.**
- **CP-A:** Rob approves the plain-language Given/When/Then examples in the design doc's "Acceptance examples".
- **CP-C:** the planner writes the specs and the DSL interface, runs `.eng/bin/eng-spec lock .`, and the CP-C Approval
  log row records `approved speclock sha256:<hex>` (hash of `tests/acceptance/spec-lock.json`, printed by the command).
- **Locked:** spec files, and the DSL public interface (public step names, parameters, docstrings).
- **Flagged:** DSL assertion-step bodies (`assert_`/`then_`/`expect_`/`check_`/`verify_`); the Codex code review must
  name each changed step.
- **Free:** drivers, private DSL helpers (`_x`), `conftest.py`.
- An edit to a locked spec or the DSL interface during implementation is **not** a hard failure: `eng-run implement`
  prints a WARNING and writes an OWNER REVIEW entry in the run log, and `eng-check` warns until Rob re-approves
  (re-lock, new CP-C row) or the edit is reverted.

**Slices.** Each slice card lists `reqs:` and `specs:` (pytest node ids) or `specs: none - <reason>`. The implementer
runs them first and confirms they are red, then makes them green without touching locked files.

**Verify.** Re-run the acceptance suite on every planned channel; paste `eng-spec trace .` (REQ -> specs) with results
into the verification report; `eng-spec status .` must be clean or re-approved.

**eng-check (warn-only until v2.6.0; `--strict` makes them errors)**, active only when the project opted in
(`acceptance: executable-specs` in PROJECT_STATE, or a spec lock exists) and triage is not small:
`speclock-not-approved`, `spec-changed-without-approval`, `dsl-interface-changed`, `dsl-assertion-changed` (cleared
when a review-findings file names the step), `slice-without-spec`, `spec-unknown-node`, `req-without-spec` (at
verify/ship).

**Migration / grandfathering.** Existing projects are unaffected until they opt in with `eng-spec init .` (after
`eng-init --upgrade`). A project mid-increment may opt in at its next plan (CP-C); approved designs without
"Acceptance examples" are grandfathered, and their examples are written straight into specs at CP-C.

cat: .claude/skills/eng-review/SKILL.md: No such file or directory
./.eng/templates/AGENTS.md
./AGENTS.md
WARN  .eng/runners.toml: no on_complete hook configured ([hooks] empty or missing) - bots must stay attached to eng-run until exit; fire-and-forget needs a non-empty on_complete / <role>_on_complete (PROCESS.md section 10, LESSONS L-006)
WARN  PROJECT_STATE.md: ## Latest artifacts has 37 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 33 rows / 6463 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 152 artifact(s) checked

exec
/bin/bash -lc 'git diff bc73656559d88e45f7f525d0c8f921d6e034e18d -- relay/relay.py relay/Dockerfile coolify-service.snippet.yaml; cat relay/README.md' in /mnt/d/rob/projects/mmbridge
 succeeded in 5ms:
diff --git a/coolify-service.snippet.yaml b/coolify-service.snippet.yaml
index 5d22f20..e46bd47 100644
--- a/coolify-service.snippet.yaml
+++ b/coolify-service.snippet.yaml
@@ -23,3 +23,29 @@ services:
       retries: 3
     # Same compose stack => same default network as `mattermost`, so
     # http://mattermost:8065 resolves without exposing Mattermost publicly.
+
+  # Wake relay (ADR-0011, relay/README.md): own app, own domain, holds the Grok routine keys.
+  # Can also be a separate Coolify application built from relay/Dockerfile.
+  relay:
+    build:
+      context: https://github.com/rowama/mmbridge.git#main:relay
+      dockerfile: Dockerfile
+    restart: unless-stopped
+    environment:
+      - SERVICE_FQDN_RELAY_8080=https://relay.rmlab.cloud      # TODO: real relay domain from Rob
+      # Per bot, as Coolify secrets (never commit values): <NAME> = bot name upper-case, '-' -> '_'
+      # - RELAY_BOT_EDDIE_HMAC_SECRET=<eddie's mmbridge wake secret>
+      # - RELAY_BOT_EDDIE_ROUTINE_URL=<Grok Bot routine webhook URL>
+      # - RELAY_BOT_EDDIE_ROUTINE_KEY=<routine Bearer key>
+    volumes:
+      - relay-data:/data
+    expose:
+      - "8080"
+    healthcheck:
+      test: ["CMD", "python", "-c", "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8080/health')"]
+      interval: 30s
+      timeout: 3s
+      retries: 3
+
+volumes:
+  relay-data:
diff --git a/relay/Dockerfile b/relay/Dockerfile
new file mode 100644
index 0000000..5c6193e
--- /dev/null
+++ b/relay/Dockerfile
@@ -0,0 +1,20 @@
+# Wake relay (ADR-0011): own image and Coolify app. Build from the relay/ directory:
+#   docker build -t mmbridge-relay:bs1 relay
+FROM python:3.12-slim
+
+ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
+WORKDIR /app
+
+COPY requirements.txt .
+RUN pip install --no-cache-dir -r requirements.txt
+
+COPY relay.py .
+
+# /data: persistent volume for the dedupe db (relay.db); owned by the app user, private.
+RUN useradd --create-home --uid 10001 appuser && mkdir -p /data && chown 10001:10001 /data && chmod 700 /data
+USER appuser
+
+ENV FORWARDED_ALLOW_IPS=127.0.0.1
+EXPOSE 8080
+HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8080/health')" || exit 1
+CMD ["uvicorn", "relay:create_app", "--factory", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
diff --git a/relay/relay.py b/relay/relay.py
new file mode 100644
index 0000000..a66ca70
--- /dev/null
+++ b/relay/relay.py
@@ -0,0 +1,367 @@
+"""Wake relay (ADR-0011): verifies mmbridge's HMAC-signed wakes and forwards them to a Grok Bot routine with
+that bot's Bearer routine key. Own image and Coolify app; imports nothing from app/ (verify is a copy of
+app.wake.verify, pinned by tests/unit/test_relay.py).
+
+Config is env only (Coolify secrets), per bot: RELAY_BOT_<NAME>_HMAC_SECRET (copy of the bot's mmbridge wake
+secret, >= 32 chars), RELAY_BOT_<NAME>_ROUTINE_URL (https), RELAY_BOT_<NAME>_ROUTINE_KEY. <NAME> is the bot
+name upper-cased with '-' -> '_' (bot "my-bot" -> RELAY_BOT_MY_BOT_*). Optional: RELAY_DATA_DIR (/data),
+RELAY_UPSTREAM_TIMEOUT_S (5), RELAY_RATE_PER_MIN (30), RELAY_BURST (10), RELAY_ALLOW_HTTP_UPSTREAM (tests only).
+Start fails on a bot with a missing field, a short secret or a non-https URL.
+
+POST /wake/{bot}: unknown bot 404; bad signature / stale timestamp (300 s) 401 {"reason"}; delivery already
+forwarded 200 {"status": "duplicate"} (not forwarded); over the per-bot rate 429 {"reason": "rate_limited"};
+else the raw body is forwarded byte-for-byte with Authorization: Bearer <key> and X-MMB-Delivery, and the
+upstream result is mapped by map_upstream (2xx -> 200; 408/429/5xx/timeout/connect -> 503 so mmbridge
+retries; any other status -> 424 {"upstream": code}, permanent).
+Delivery guarantee (accepted risk A, Rob 2026-10-28): a delivery id is recorded in Seen only after upstream
+2xx, so a lost upstream response (logged relay_delivery_ambiguous) or a crash before Seen.add can start the
+routine twice; never zero times. Concurrent identical deliveries forward once (per-delivery lock + in_flight row).
+GET /health: counts only. Logs: JSON lines on logger "relay", every secret and key redacted.
+"""
+import asyncio
+import hashlib
+import hmac
+import json
+import logging
+import os
+import re
+import sqlite3
+import sys
+import threading
+import time
+from collections.abc import Mapping
+from contextlib import asynccontextmanager
+from dataclasses import dataclass
+
+import httpx
+from fastapi import FastAPI, Request
+from fastapi.responses import JSONResponse
+
+WINDOW_S = 300
+MIN_SECRET = 32
+SEEN_TTL_S = 24 * 3600
+IN_FLIGHT_STALE_S = 60
+PRUNE_EVERY_S = 3600
+FIELDS = ("HMAC_SECRET", "ROUTINE_URL", "ROUTINE_KEY")
+_ENV_RE = re.compile(r"^RELAY_BOT_([A-Z0-9_]+)_(%s)$" % "|".join(FIELDS))
+
+
+# --- logging with redaction ----------------------------------------------------------------------------------
+_PATTERNS = [re.compile(r"(?i)bearer\s+\S+"), re.compile(r"(?i)(authorization['\"]?\s*[:=]\s*['\"]?)[^'\",}\s]+")]
+_SECRETS: set[str] = set()
+
+
+def register_secret(value: str) -> None:
+    if isinstance(value, str) and len(value) >= 4:
+        _SECRETS.add(value)
+
+
+def redact(s: str) -> str:
+    for p in _PATTERNS:
+        s = p.sub(lambda m: (m.group(1) if m.groups() else "Bearer ") + "[REDACTED]", s)
+    for v in sorted(_SECRETS, key=len, reverse=True):
+        s = s.replace(v, "[REDACTED]")
+    return s
+
+
+class RedactFilter(logging.Filter):
+    def filter(self, record: logging.LogRecord) -> bool:
+        record.msg, record.args = redact(record.getMessage()), None
+        if record.exc_info:
+            record.exc_text = redact(logging.Formatter().formatException(record.exc_info))
+            record.exc_info = None
+        return True
+
+
+log = logging.getLogger("relay")
+log.setLevel(logging.INFO)
+log.addFilter(RedactFilter())     # on the logger: every handler (stdout, test capture) sees redacted text
+
+
+def _setup_stdout() -> None:
+    if not any(getattr(h, "_relay", False) for h in log.handlers):
+        h = logging.StreamHandler(sys.stdout)
+        h._relay = True
+        log.addHandler(h)
+
+
+def _log(event: str, **fields) -> None:
+    log.info(json.dumps({"event": event, **fields}))
+
+
+# --- config --------------------------------------------------------------------------------------------------
+class ConfigError(Exception):
+    pass
+
+
+@dataclass(frozen=True)
+class RelayBot:
+    name: str
+    hmac_secret: str
+    routine_url: str
+    routine_key: str
+
+
+def _https_ok(url: str, allow_http: bool) -> bool:
+    if url.startswith("https://") and len(url) > 8:
+        return True
+    return allow_http and url.startswith("http://") and len(url) > 7
+
+
+def load_bots(env: Mapping[str, str]) -> dict[str, RelayBot]:
+    """Bots from RELAY_BOT_<NAME>_* env vars. Errors name the bot and field, never a value."""
+    raw: dict[str, dict[str, str]] = {}
+    for k, v in env.items():
+        m = _ENV_RE.match(k)
+        if m:
+            raw.setdefault(m.group(1).lower().replace("_", "-"), {})[m.group(2)] = (v or "").strip()
+    allow_http = env.get("RELAY_ALLOW_HTTP_UPSTREAM", "").strip().lower() == "true"
+    bots = {}
+    for name, f in sorted(raw.items()):
+        for field in FIELDS:
+            if not f.get(field):
+                raise ConfigError("bot %s: %s missing" % (name, field.lower()))
+        if len(f["HMAC_SECRET"]) < MIN_SECRET:
+            raise ConfigError("bot %s: hmac_secret must be at least %d characters" % (name, MIN_SECRET))
+        if not _https_ok(f["ROUTINE_URL"], allow_http):
+            raise ConfigError("bot %s: routine_url must be https" % name)
+        bots[name] = RelayBot(name, f["HMAC_SECRET"], f["ROUTINE_URL"], f["ROUTINE_KEY"])
+    return bots
+
+
+# --- verify: COPY of app.wake.verify (ADR-0008); tests/unit/test_relay.py guards against drift -----------------
+def _mac(secret: str, ts: str, body: bytes) -> str:
+    return hmac.new(secret.encode(), ts.encode() + b"." + body, hashlib.sha256).hexdigest()
+
+
+def verify(secret: str, headers: Mapping, body: bytes, now: int, window: int = WINDOW_S) -> bool:
+    h = {k.lower(): v for k, v in headers.items()}
+    sig, ts = h.get("x-mmb-signature"), h.get("x-mmb-timestamp")
+    if not sig or not ts or not sig.startswith("v1="):
+        return False
+    try:
+        t = int(ts)
+    except ValueError:
+        return False
+    if abs(now - t) > window:
+        return False
+    if not hmac.compare_digest(sig[3:].encode(), _mac(secret, ts, body).encode()):
+        return False
+    # X-MMB-Delivery is not signed itself: it must equal the signed delivery_id, so a captured request
+    # cannot be replayed under a new idempotency key (lb4 review 2 P2).
+    try:
+        signed_id = json.loads(body).get("delivery_id")
+    except (ValueError, AttributeError):
+        return False
+    d = h.get("x-mmb-delivery")
+    return bool(d) and isinstance(signed_id, str) and hmac.compare_digest(d.encode(), signed_id.encode())
+
+
+def _reject_reason(headers: Mapping, now: int) -> str:
+    """Reason for a failed verify: `stale` only when the timestamp itself is outside the window."""
+    try:
+        t = int(headers.get("x-mmb-timestamp", ""))
+    except ValueError:
+        return "bad_sig"
+    return "stale" if abs(now - t) > WINDOW_S else "bad_sig"
+
+
+def map_upstream(status: int | None) -> tuple[int, dict]:
+    """Upstream routine status (None = timeout/connect error) -> relay response to mmbridge."""
+    if status is not None and 200 <= status < 300:
+        return 200, {"status": "forwarded"}
+    if status is None or status in (408, 429) or status >= 500:
+        return 503, {"reason": "upstream_unavailable", "upstream": status}
+    return 424, {"upstream": status}
+
+
+# --- persistent dedupe + in-flight rows ----------------------------------------------------------------------
+class Seen:
+    """sqlite (delivery_id PK, seen_at): deliveries the routine accepted (2xx); pruned after 24 h.
+    in_flight rows guard a delivery while it is upstream; one relay process (single replica), so rows left by a
+    previous process are cleared at start and rows older than IN_FLIGHT_STALE_S are taken over."""
+
+    def __init__(self, path: str):
+        self.path = path
+        self._lock = threading.Lock()
+        self._db = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
+        self._db.execute("PRAGMA journal_mode=WAL")
+        self._db.execute("CREATE TABLE IF NOT EXISTS seen (delivery_id TEXT PRIMARY KEY, seen_at INTEGER NOT NULL)")
+        self._db.execute("CREATE TABLE IF NOT EXISTS in_flight (delivery_id TEXT PRIMARY KEY, "
+                         "started_at INTEGER NOT NULL)")
+        self._db.execute("DELETE FROM in_flight")
+
+    def _q(self, sql: str, args=()):
+        with self._lock:
+            return self._db.execute(sql, args)
+
+    def has(self, d: str) -> bool:
+        return self._q("SELECT 1 FROM seen WHERE delivery_id = ?", (d,)).fetchone() is not None
+
+    def add(self, d: str, now: int) -> None:
+        self._q("INSERT OR IGNORE INTO seen (delivery_id, seen_at) VALUES (?, ?)", (d, int(now)))
+
+    def prune(self, now: int) -> int:
+        return self._q("DELETE FROM seen WHERE seen_at < ?", (int(now) - SEEN_TTL_S,)).rowcount
+
+    def count_since(self, since: int) -> int:
+        return self._q("SELECT COUNT(*) FROM seen WHERE seen_at >= ?", (int(since),)).fetchone()[0]
+
+    def claim(self, d: str, now: int) -> bool:
+        with self._lock:
+            self._db.execute("DELETE FROM in_flight WHERE delivery_id = ? AND started_at < ?",
+                             (d, int(now) - IN_FLIGHT_STALE_S))
+            return self._db.execute("INSERT OR IGNORE INTO in_flight VALUES (?, ?)", (d, int(now))).rowcount == 1
+
+    def release(self, d: str) -> None:
+        self._q("DELETE FROM in_flight WHERE delivery_id = ?", (d,))
+
+
+class RateLimit:
+    """Token bucket per bot: `burst` tokens, refilled at per_min/60 per second."""
+
+    def __init__(self, per_min: float = 30, burst: int = 10):
+        self.rate, self.burst = per_min / 60.0, burst
+        self._b: dict[str, tuple[float, float]] = {}
+
+    def allow(self, bot: str, now: float) -> bool:
+        tokens, last = self._b.get(bot, (float(self.burst), now))
+        tokens = min(float(self.burst), tokens + max(0.0, now - last) * self.rate)
+        ok = tokens >= 1.0
+        self._b[bot] = (tokens - 1.0 if ok else tokens, max(now, last))
+        return ok
+
+
+class _Counter:
+    """Rejections per minute bucket, last 24 h (bounded memory under a flood)."""
+
+    def __init__(self):
+        self._m: dict[int, int] = {}
+
+    def add(self, now: float) -> None:
+        k = int(now) // 60
+        self._m[k] = self._m.get(k, 0) + 1
+        for old in [m for m in self._m if m < k - 24 * 60]:
+            del self._m[old]
+
+    def since(self, now: float) -> int:
+        k = int(now) // 60
+        return sum(v for m, v in self._m.items() if m > k - 24 * 60)
+
+
+class _Relay:
+    def __init__(self, bots, http, clock, seen, rate, timeout_s):
+        self.bots, self.http, self.clock, self.seen, self.rate = bots, http, clock, seen, rate
+        self.timeout_s = timeout_s
+        self.rejected = _Counter()
+        self._locks: dict[str, list] = {}     # delivery id -> [asyncio.Lock, holders+waiters]
+        self._pruned_at = None
+
+    def pending(self, d: str) -> int:
+        """Requests holding or waiting for the in-flight lock of delivery `d` (tests use it as a barrier)."""
+        return self._locks.get(d, [None, 0])[1]
+
+    def _reject(self, now, bot, reason, status, body=None, **fields):
+        self.rejected.add(now)
+        _log("relay_rejected", bot=bot, reason=reason, **fields)
+        return JSONResponse(body or {"reason": reason}, status_code=status)
+
+    async def wake(self, bot_name: str, request: Request):
+        now = self.clock()
+        bot = self.bots.get(bot_name)
+        if bot is None:
+            return self._reject(now, None, "unknown_bot", 404)
+        body = await request.body()
+        if not verify(bot.hmac_secret, request.headers, body, int(now)):
+            return self._reject(now, bot.name, _reject_reason(request.headers, int(now)), 401)
+        d = request.headers["x-mmb-delivery"]
+        if self._pruned_at is None or now - self._pruned_at >= PRUNE_EVERY_S:
+            self.seen.prune(int(now))
+            self._pruned_at = now
+        entry = self._locks.setdefault(d, [asyncio.Lock(), 0])
+        entry[1] += 1
+        try:
+            async with entry[0]:
+                return await self._deliver(bot, d, body, now)
+        finally:
+            entry[1] -= 1
+            if entry[1] == 0:
+                self._locks.pop(d, None)
+
+    async def _deliver(self, bot: RelayBot, d: str, body: bytes, now: float):
+        if self.seen.has(d):
+            return self._reject(now, bot.name, "duplicate", 200, {"status": "duplicate"}, delivery=d)
+        if not self.seen.claim(d, int(now)):         # another relay process holds it: let mmbridge retry
+            return self._reject(now, bot.name, "in_flight", 503, delivery=d)
+        try:
+            if not self.rate.allow(bot.name, now):
+                return self._reject(now, bot.name, "rate_limited", 429, delivery=d)
+            status, err = await self._forward(bot, d, body)
+            if status is not None and 200 <= status < 300:
+                self.seen.add(d, int(self.clock()))   # only after upstream 2xx (accepted risk A)
+                _log("relay_forwarded", bot=bot.name, delivery=d, upstream=status)
+            else:
+                if err not in (None, "connect"):
+                    _log("relay_delivery_ambiguous", bot=bot.name, delivery=d, error=err)
+                _log("relay_upstream", bot=bot.name, delivery=d, code=err or status)
+            code, payload = map_upstream(status)
+            return JSONResponse(payload, status_code=code)
+        finally:
+            self.seen.release(d)
+
+    async def _forward(self, bot: RelayBot, d: str, body: bytes) -> tuple[int | None, str | None]:
+        headers = {"Authorization": "Bearer " + bot.routine_key, "Content-Type": "application/json",
+                   "X-MMB-Delivery": d}
+        try:
+            r = await asyncio.wait_for(
+                self.http.post(bot.routine_url, content=body, headers=headers, timeout=self.timeout_s),
+                self.timeout_s)
+            return r.status_code, None
+        except (httpx.ConnectError, httpx.ConnectTimeout):
+            return None, "connect"                    # never reached the routine: not ambiguous
+        except (httpx.TimeoutException, asyncio.TimeoutError):
+            return None, "timeout"                    # may have started the routine: ambiguous
+        except Exception as e:                        # type only: messages may carry request details
+            return None, "error_" + type(e).__name__
+
+    def health(self) -> dict:
+        now = self.clock()
+        return {"ok": True, "bots": len(self.bots), "forwarded_24h": self.seen.count_since(int(now) - SEEN_TTL_S),
+                "rejected_24h": self.rejected.since(now)}
+
+
+def create_app(env: Mapping[str, str] | None = None, http: httpx.AsyncClient | None = None, clock=time.time,
+               seen: Seen | None = None) -> FastAPI:
+    """App factory (`uvicorn relay:create_app --factory`). Raises ConfigError on bad bot env (fail fast)."""
+    env = os.environ if env is None else env
+    _setup_stdout()
+    bots = load_bots(env)
+    for b in bots.values():
+        register_secret(b.hmac_secret)
+        register_secret(b.routine_key)
+    if seen is None:
+        seen = Seen(os.path.join(env.get("RELAY_DATA_DIR", "/data"), "relay.db"))
+    rate = RateLimit(float(env.get("RELAY_RATE_PER_MIN", "30")), int(env.get("RELAY_BURST", "10")))
+    own_http = http is None
+    client = http or httpx.AsyncClient()
+    relay = _Relay(bots, client, clock, seen, rate, float(env.get("RELAY_UPSTREAM_TIMEOUT_S", "5")))
+
+    @asynccontextmanager
+    async def lifespan(_app):
+        _log("relay_start", bots=len(bots))
+        yield
+        if own_http:
+            await client.aclose()
+
+    app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
+    app.state.relay = relay
+
+    @app.post("/wake/{bot}")
+    async def wake(bot: str, request: Request):
+        return await relay.wake(bot, request)
+
+    @app.get("/health")
+    async def health():
+        return relay.health()
+
+    return app
# Wake relay (Grok Bot routines)

Thin HMAC -> Bearer relay (ADR-0011). mmbridge keeps sending only signed wakes; the relay checks each one and
starts that bot's Grok Bot routine with the routine's Bearer key. Routine keys live only here (Coolify secrets),
never in mmbridge.

```
mmbridge --signed wake--> POST /wake/<bot> --verify, dedupe, rate limit--> POST <routine URL>, Bearer <key>
```

## What it does
- `POST /wake/<bot>`: unknown bot -> 404. Bad signature or timestamp older/newer than 5 min -> 401, nothing
  forwarded. A delivery already forwarded (same `X-MMB-Delivery`, last 24 h) -> 200 `{"status": "duplicate"}`,
  nothing forwarded. Over the per-bot rate (30/min, burst 10) -> 429 (mmbridge retries later). Otherwise the body
  goes to the routine unchanged with `Authorization: Bearer <key>`, `Content-Type: application/json` and
  `X-MMB-Delivery`, 5 s timeout.
- Routine answer -> relay answer: 2xx -> 200 (run started); 408/429/5xx/timeout/no connection -> 503 (mmbridge
  retries, 5 attempts, then one failed wake in `python -m app.admin failed`); anything else (401/403/404/...) ->
  424 `{"upstream": <code>}` (permanent; usually a wrong key or URL).
- Known, accepted (Rob 2026-10-28): if the routine started but its answer was lost (timeout), or the relay died
  right after the routine said 200, mmbridge retries and the routine can start twice for one post (log
  `relay_delivery_ambiguous`). It never silently drops a post.
- `GET /health`: `{"ok": true, "bots": n, "forwarded_24h": n, "rejected_24h": n}` (counts only).
- Logs: one JSON line per event on stdout (`relay_forwarded`, `relay_rejected{reason}`, `relay_upstream{code}`,
  `relay_delivery_ambiguous`); secrets and keys are redacted, message text is never logged.

## Configuration (env only)
Per bot, `<NAME>` = bot name upper-cased with `-` -> `_` (bot `eddie` -> `RELAY_BOT_EDDIE_*`). Use the same name
everywhere: Mattermost bot, mmbridge wake URL `/wake/<name>`, relay env, Grok routine.

| Variable | Value |
|---|---|
| `RELAY_BOT_<NAME>_HMAC_SECRET` | the bot's mmbridge wake secret (>= 32 chars), copied exactly |
| `RELAY_BOT_<NAME>_ROUTINE_URL` | the Grok Bot routine webhook URL (https) |
| `RELAY_BOT_<NAME>_ROUTINE_KEY` | the routine's Bearer key |
| `RELAY_DATA_DIR` | `/data` (default; mount a volume, holds `relay.db`) |
| `RELAY_RATE_PER_MIN`, `RELAY_BURST` | 30, 10 (defaults) |
| `RELAY_UPSTREAM_TIMEOUT_S` | 5 (default) |

The relay refuses to start if a bot is missing a field, its secret is shorter than 32 characters, or its routine
URL is not https (`RELAY_ALLOW_HTTP_UPSTREAM=true` is for tests only). Replicas: 1.

## Setup on Coolify (one bot, e.g. eddie)
1. New application from this repo: build context `relay`, Dockerfile `relay/Dockerfile`, port 8080, a persistent
   volume at `/data`, its own domain (e.g. `https://relay.rmlab.cloud`). See `coolify-service.snippet.yaml`.
2. Secrets: `RELAY_BOT_EDDIE_HMAC_SECRET`, `RELAY_BOT_EDDIE_ROUTINE_URL`, `RELAY_BOT_EDDIE_ROUTINE_KEY`.
   The HMAC secret is eddie's existing mmbridge wake secret. If you don't have it any more, make a new one and
   give it to both sides (step 4 prints nothing then; paste it there too).
3. Deploy; `curl https://relay.rmlab.cloud/health` -> `"ok": true, "bots": 1`.
4. mmbridge container terminal (no redeploy; picked up within 30 s):
   `python -m app.admin set-bot --token-stdin --wake-secret-stdin --wake-url https://relay.rmlab.cloud/wake/eddie`
   and paste two lines at the prompt: eddie's Mattermost token, then the same wake secret as in step 2, then Ctrl-D.
5. Check: post in Town Square and DM eddie -> the Eddie routine starts each time (Grok Bot routine history).
   `curl -X POST https://relay.rmlab.cloud/wake/eddie -d '{}'` -> 401 and no run.

## Grok routine setup
The routine receives the wake JSON as its input: `bot`, `channel` (`name`, `type`: O/P channel, D = DM),
`sender.username`, `post` (`id`, `message`, `root_id`). Until B-s2 adds reply hints, the routine instruction
should say: "You were woken by a Mattermost post. Read `post.message` from `sender.username` in `channel`." (OWNER-GUIDE
gets this text once Rob's pending OWNER-GUIDE edits are committed.)

## Rotating a routine key (runbook)
Do this when the key may have leaked, a person with access leaves, or the relay logs `relay_upstream` with code
401/403 (key revoked or rotated on the Grok side).
1. In Grok Bot, create the new key for the routine (or rotate it).
2. Coolify relay app: set `RELAY_BOT_<NAME>_ROUTINE_KEY` to the new key; redeploy the relay (seconds; wakes in
   between get 503 and mmbridge retries them).
3. In Grok Bot, revoke the old key.
4. Post a test message; the routine starts; relay log shows `relay_forwarded` for it.

Rotating a wake secret: generate one (`python -c "import secrets;print(secrets.token_urlsafe(32))"`), set it in the
relay env and redeploy the relay, then run step 4 of Setup with the new secret. Wakes signed with the old secret in
between get 401 at the relay and show as failed in mmbridge (`python -m app.admin failed --retry <post_id>`).

## Spike (OQ-B1/B2, once, before CP-S)
`python3 relay/spike_routine.py https://<routine-url>` (paste the key at the prompt, or env `SPIKE_ROUTINE_KEY`).
It posts one marker body as valid key / wrong key / bad URL and prints only the status codes. Write down the
three codes and whether the bot saw the JSON body verbatim (the marker).

exec
/bin/bash -lc 'git diff bc73656559d88e45f7f525d0c8f921d6e034e18d -- tests/acceptance/drivers/live.py; cat tests/acceptance/drivers/relay.py' in /mnt/d/rob/projects/mmbridge
 succeeded in 3ms:
diff --git a/tests/acceptance/drivers/live.py b/tests/acceptance/drivers/live.py
index 1dc4627..834265d 100644
--- a/tests/acceptance/drivers/live.py
+++ b/tests/acceptance/drivers/live.py
@@ -7,13 +7,19 @@ Backoff is scaled by WAKE_BACKOFF_SCALE so retry specs run in seconds; LIVE_ALLO
 URL be the plain-HTTP local receiver (tests only).
 
 SUT mode (env LIVE_MODE):
-- `container` (default, lb5, ADR-0010 layer 4): the real image (env LIVE_IMAGE, default mmbridge:lb5; build it
-  first with `docker build -t mmbridge:lb5 .`) on `--network host` with a fresh named volume at /data, a fresh
+- `container` (default, lb5, ADR-0010 layer 4): the real image (env LIVE_IMAGE, default mmbridge:bs1; build it
+  first with `docker build -t mmbridge:bs1 .`) on `--network host` with a fresh named volume at /data, a fresh
   MMB_STORE_KEY and LIVE_BOTS_ENABLED=true. `python -m app.admin set-bot` runs in a one-off container on the same
   volume before the server starts (as an operator would before enabling the flag); `admin failed` runs through
   `docker exec`; `/health` tells when the listener is connected; `docker logs` is the log capture for the token
   scan.
 - `inprocess` (lb4): app.admin.main and app.live.LiveRuntime in this process; logs captured from the loggers.
+Increment B (B-s1, ADR-0016): `register_bot(name, "grok")` points the bot's wake URL at the real wake relay
+(drivers/relay.py: in-process or image RELAY_IMAGE, behind a recording tap) configured with the same name and wake
+secret, which forwards to a fake Grok routine (drivers/fake_routine.py, checks the Bearer routine key).
+`register_bot(name, "signed")` uses the HMAC receiver as in increment A. Wake secrets are passed to the CLI on
+stdin (`--wake-secret-stdin`, as an operator copying one secret to the relay), so the CLI never prints them.
+Wake retries: WAKE_BACKOFF_SCALE 0.25 gives ~7 s before a wake fails, enough to restart the relay container.
 drop_connection: the fake closes the websocket (no resume: a new connection id) and refuses REST + websocket
 until restore_connection, so posts made meanwhile are reachable only by the listener's REST catch-up.
 """
@@ -40,6 +46,8 @@ from app import admin
 from app import logging as mlog
 from app.live import LiveRuntime
 from drivers.fake_mattermost import FakeMattermost
+from drivers.fake_routine import FakeRoutine
+from drivers.relay import RelayHarness
 from drivers.wake_receiver import WakeReceiver
 
 TEAM = "rmlab"
@@ -83,7 +91,8 @@ class _InProcess:
         return rc, out.getvalue()
 
     def start(self):
-        self.runtime = LiveRuntime(env=dict(os.environ), base_url=self.drv.base, poll_s=0.05)
+        # reload_s: the container keeps the production 30 s store reload; in-process reloads fast.
+        self.runtime = LiveRuntime(env=dict(os.environ), base_url=self.drv.base, poll_s=0.05, reload_s=0.1)
         self.drv._run(self.runtime.start())
 
     def listener(self):
@@ -108,7 +117,7 @@ class _Container:
 
     def __init__(self, drv, env):
         self.drv, self.env = drv, env
-        self.image = os.environ.get("LIVE_IMAGE", "mmbridge:lb5")
+        self.image = os.environ.get("LIVE_IMAGE", "mmbridge:bs1")
         self.name = "mmb-live-" + secrets.token_hex(4)
         self.volume = self.name + "-data"
         self.port = _free_port()
@@ -166,6 +175,10 @@ class LiveDriver:
     def __init__(self):
         self.mm = FakeMattermost(mm_ids=True, clock=time.time)
         self.rx = WakeReceiver()
+        self.routine = FakeRoutine()
+        self.bots = {}                 # name -> {"secret", "key", "kind"} (increment B)
+        self.relay = None              # RelayHarness, started by the first grok bot
+        self.started = False
         self.outputs = []              # admin CLI stdout
         self.posts = {}                # message -> post id (latest)
         self.teams = {}                # channel name -> team (given_channel)
@@ -173,11 +186,11 @@ class LiveDriver:
         self._loop = asyncio.new_event_loop()
         self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
         self._thread.start()
-        self._serving = [self.mm.serve(), self.rx.serve()]
-        self.base, self.wake_url = (self._run(cm.__aenter__()) for cm in self._serving)
+        self._serving = [self.mm.serve(), self.rx.serve(), self.routine.serve()]
+        self.base, self.wake_url, self.routine_base = (self._run(cm.__aenter__()) for cm in self._serving)
         env = {"MMB_STORE_KEY": Fernet.generate_key().decode(), "MATTERMOST_URL": self.base,
-               "WAKE_BACKOFF_SCALE": "0.05", "WAKE_MAX_ATTEMPTS": "5", "LIVE_ALLOW_HTTP_WAKE": "true"}
-        mode = os.environ.get("LIVE_MODE", "container")
+               "WAKE_BACKOFF_SCALE": "0.25", "WAKE_MAX_ATTEMPTS": "5", "LIVE_ALLOW_HTTP_WAKE": "true"}
+        mode = self.mode = os.environ.get("LIVE_MODE", "container")
         assert mode in ("container", "inprocess"), "LIVE_MODE must be container or inprocess"
         self._tmp = None
         if mode == "inprocess":
@@ -221,8 +234,13 @@ class LiveDriver:
         rc, out = self._admin("set-bot", "--token-stdin", "--wake-url", self.wake_url, stdin=u["token"] + "\n")
         assert rc == 0, "admin set-bot failed: %s" % out.strip()
         self.rx.secret = re.search(r"wake secret \(shown once[^)]*\): (\S+)", out).group(1)
-        self.sut.start()
-        self._wait(lambda: self.sut.listener() == "ok", START_S, "listener ok in /health")
+        self._start()
+
+    def _start(self):
+        if not self.started:
+            self.sut.start()
+            self.started = True
+            self._wait(lambda: self.sut.listener() == "ok", START_S, "listener ok in /health")
 
     def given_wake_target_down(self):
         self.rx.down = True
@@ -290,14 +308,22 @@ class LiveDriver:
         if thread is not None:
             assert w["post"]["root_id"] == self.posts[thread], "wake does not name the thread %r" % thread
 
-    def assert_not_woken(self, bot, message):
-        # Barrier: a DM posted after the scenario is woken; anything before it has been processed by then.
+    def _barrier(self, bot):
+        """A DM posted after the scenario reaches the bot's current wake target (receiver, or routine via the
+        relay, any status); anything before it has been processed by then. Returns the marker post id."""
         self._user(MARKER_USER)
         marker = "marker %s" % secrets.token_hex(4)
         self.dm(bot, marker, MARKER_USER)
         mid = self.posts[marker]
-        self._wait(lambda: self._delivered(mid), WAKE_WITHIN_S, "marker wake")
+        if self.bots.get(bot, {}).get("kind") == "grok":
+            self._wait(lambda: self.routine.reached(bot, mid), WAKE_WITHIN_S, "marker wake at the routine")
+        else:
+            self._wait(lambda: self._delivered(mid), WAKE_WITHIN_S, "marker wake")
         time.sleep(SETTLE_S)
+        return mid
+
+    def assert_not_woken(self, bot, message):
+        mid = self._barrier(bot)
         others = [r for r in self.rx.requests if r["headers"].get("x-mmb-delivery") != mid]
         if message is not None:
             others = [r for r in others if json.loads(r["body"]).get("post", {}).get("message") == message]
@@ -313,8 +339,31 @@ class LiveDriver:
         assert last["status"] == 401, "receiver accepted a forged wake (HTTP %s)" % last["status"]
         assert last["delivery"] not in self.rx.accepted
 
+    def _mmb_attempts(self, pid):
+        """Attempt numbers of failed deliveries mmbridge logged for this post (wake_retry / wake_failed)."""
+        got = set()
+        for line in self.sut.logs().splitlines():
+            if pid in line and ("wake_retry" in line or "wake_failed" in line) and "{" in line:
+                try:
+                    ev = json.loads(line[line.index("{"):])
+                except ValueError:
+                    continue
+                if ev.get("post_id") == pid and ev.get("event") in ("wake_retry", "wake_failed"):
+                    got.add(ev["attempt"])
+        return got
+
+    def _grok_attempts(self, pid):
+        """Attempt numbers seen at any routine (relay forwarded it) or logged by mmbridge (relay unreachable)."""
+        seen = {json.loads(r["body"])["attempt"] for r in self.routine.requests if self.routine.post_id(r) == pid}
+        return seen | self._mmb_attempts(pid)
+
     def assert_wake_retried(self, minimum):
         pid = self._last_post
+        want = set(range(1, minimum + 1))
+        self._wait(lambda: self.rx.attempts(pid) or want <= self._grok_attempts(pid), WAKE_WITHIN_S,
+                   "%d attempts" % minimum)
+        if not self.rx.attempts(pid):          # grok bot: attempts via relay -> routine, or refused at the relay
+            return
         self._wait(lambda: len(self.rx.attempts(pid)) >= minimum, WAKE_WITHIN_S, "%d attempts" % minimum)
         attempts = self.rx.attempts(pid)
         assert all(self._valid(r) for r in attempts)
@@ -338,6 +387,137 @@ class LiveDriver:
         for r in self.rx.requests:
             assert tok not in r["body"].decode() and tok not in json.dumps(r["headers"]), "token in a wake"
 
+    # --- increment B: Grok routine via the wake relay (B-s1) ---------------------------------------------------
+    def _relay(self):
+        if self.relay is None:
+            self.relay = RelayHarness(self, self.mode, self.routine_base)
+        return self.relay
+
+    def _configure_relay(self):
+        grok = {n: b for n, b in self.bots.items() if b["kind"] == "grok"}
+        if grok:
+            self._relay().configure(grok)
+
+    def _target(self, name, kind):
+        return "%s/wake/%s" % (self._relay().url, name) if kind == "grok" else self.wake_url
+
+    def _set_bot(self, name):
+        b, u = self.bots[name], self._user(name)
+        rc, out = self._admin("set-bot", "--token-stdin", "--wake-secret-stdin", "--wake-url",
+                              self._target(name, b["kind"]), stdin="%s\n%s\n" % (u["token"], b["secret"]))
+        assert rc == 0, "admin set-bot failed: %s" % out.strip()
+
+    def register_bot(self, name, wake):
+        assert wake in ("grok", "signed"), wake
+        u = self._user(name)
+        u["is_bot"], u["token"] = True, "tok-%s-%s" % (name, secrets.token_hex(12))
+        self.bots[name] = {"secret": secrets.token_urlsafe(32), "key": "rk-%s-%s" % (name, secrets.token_hex(16)),
+                           "kind": wake}
+        self.routine.keys[name] = self.bots[name]["key"]
+        if wake == "signed":
+            self.rx.secret = self.bots[name]["secret"]
+        self._configure_relay()                 # relay ready (same name + secret) before mmbridge points at it
+        self._set_bot(name)
+        self._start()
+
+    def _reloads(self):
+        return sum(1 for line in self.sut.logs().splitlines() if "store_updated" in line and '"generation"' in line)
+
+    def switch_wake_target(self, bot, wake):
+        before = self._reloads()
+        self.bots[bot]["kind"] = wake
+        if wake == "signed":
+            self.rx.secret = self.bots[bot]["secret"]
+        self._configure_relay()
+        self._set_bot(bot)                      # same secret (copied to the relay), new wake URL
+        # No redeploy/restart: the running bridge picks the change up on its own store reload (30 s in the image).
+        self._wait(lambda: self._reloads() > before, 45, "the running bridge to reload the store")
+
+    def grok_routine_down(self, bot):
+        self.routine.down.add(bot)
+
+    def grok_routine_up(self, bot):
+        self.routine.down.discard(bot)
+
+    def relay_down(self):
+        self._relay().down()
+
+    def relay_up(self):
+        self._relay().up()
+
+    def forge_wake(self, bot):
+        d = "forged-" + secrets.token_hex(4)
+        body = json.dumps({"version": 1, "kind": "post", "delivery_id": d, "attempt": 1,
+                           "post": {"id": d, "message": "do something bad"} }, separators=(",", ":")).encode()
+        ts = int(time.time())
+        sig = "v1=" + hmac.new(b"not-the-secret", b"%d." % ts + body, hashlib.sha256).hexdigest()
+        return self._relay().send(bot, body, {"Content-Type": "application/json", "X-MMB-Delivery": d,
+                                              "X-MMB-Timestamp": str(ts), "X-MMB-Signature": sig})
+
+    def _captured_headers(self, rec):
+        return {k: v for k, v in rec["headers"].items() if k.startswith("x-mmb-") or k == "content-type"}
+
+    def tamper_wake(self, bot, message):
+        rec = self._relay().last(bot)
+        w = json.loads(rec["body"])
+        w["post"]["message"] = message
+        body = json.dumps(w, separators=(",", ":")).encode()
+        return self._relay().send(bot, body, self._captured_headers(rec))
+
+    def replay_last_wake(self, bot, after_seconds):
+        rec = self._relay().last(bot)
+        return self._relay().send(bot, rec["body"], self._captured_headers(rec), after_seconds=after_seconds)
+
+    def _runs(self, bot, post_id):
+        return [r for r in self.routine.runs(bot) if self.routine.post_id(r) == post_id]
+
+    def assert_routine_started_once(self, bot, channel, sender, message, thread=None):
+        pid = self.posts[message]
+        self._wait(lambda: self._runs(bot, pid), WAKE_WITHIN_S, "routine run for %r" % message)
+        time.sleep(SETTLE_S)
+        got = self._runs(bot, pid)
+        assert len(got) == 1, "expected one routine run for %r, got %d" % (message, len(got))
+        r = got[0]
+        assert r["headers"].get("authorization") == "Bearer " + self.bots[bot]["key"], "routine key not used"
+        w = json.loads(r["body"])
+        assert r["headers"].get("x-mmb-delivery") == w["delivery_id"]
+        assert w["post"]["id"] == pid and w["post"]["message"] == message
+        assert w["bot"]["username"] == bot and w["sender"]["username"] == sender
+        if channel is None:
+            assert w["channel"]["type"] == "D"
+        else:
+            assert w["channel"]["name"] == channel and w["channel"]["type"] == self._channel(channel)["type"]
+            assert w["channel"]["type"] in ("O", "P")
+        if thread is not None:
+            assert w["post"]["root_id"] == self.posts[thread], "wake does not name the thread %r" % thread
+
+    def assert_routine_not_started(self, bot, message):
+        mid = self._barrier(bot)
+        runs = [r for r in self.routine.runs(bot) if self.routine.post_id(r) != mid]
+        if message is not None:
+            runs = [r for r in runs if json.loads(r["body"]).get("post", {}).get("message") == message]
+        assert not runs, "unexpected routine run(s): %s" % [self.routine.post_id(r) for r in runs]
+
+    def assert_no_secret_anywhere(self, bot):
+        tok, b = self._user(bot)["token"], self.bots[bot]
+        secrets_ = {"token": tok, "wake secret": b["secret"], "routine key": b["key"]}
+        logs, relay_logs = self.sut.logs(), self.relay.logs() if self.relay else ""
+        assert '"event": "wake_queued"' in logs, "log capture is empty or not the bridge's logs"
+        if b["kind"] == "grok":
+            assert "relay_forwarded" in relay_logs, "relay log capture is empty or not the relay's logs"
+        places = {"mmbridge logs": logs, "relay logs": relay_logs, "admin output": "\n".join(self.outputs)}
+        for r in self.routine.requests:         # the Bearer key is legitimately in the routine's Authorization
+            h = {k: v for k, v in r["headers"].items() if k != "authorization"}
+            places["routine wake"] = places.get("routine wake", "") + r["body"].decode() + json.dumps(h)
+        for r in self.rx.requests:
+            places["receiver wake"] = places.get("receiver wake", "") + r["body"].decode() + json.dumps(r["headers"])
+        if self.relay:
+            places["relay wake"] = "".join(r["body"].decode() + json.dumps(r["headers"]) for r in self.relay.captured)
+            places["relay responses"] = "".join(r["text"] + json.dumps(r["headers"]) for r in self.relay.responses)
+        for what, value in secrets_.items():
+            for where, text in places.items():
+                assert value not in text, "%s in %s" % (what, where)
+
     def drop_connection(self, seconds):
         # `seconds` is simulated: reconnects stay refused until restore_connection (no real wait).
         def drop():
@@ -351,7 +531,11 @@ class LiveDriver:
 
     def close(self):
         try:
-            self.sut.close()
+            try:
+                self.sut.close()
+            finally:
+                if self.relay:
+                    self.relay.close()
         finally:
             try:
                 for cm in reversed(self._serving):
"""Wake relay under test (ADR-0011/0016). Drivers are not locked; edit freely.

The real relay (relay/relay.py) runs in-process (uvicorn in the driver's loop, `LIVE_MODE=inprocess`) or as the
real image (`LIVE_MODE=container`, env RELAY_IMAGE, default mmbridge-relay:bs1; build it first with
`docker build -t mmbridge-relay:bs1 relay`) on --network host with a fresh /data volume. Relay config is env only,
so `configure(bots)` (re)starts it with RELAY_BOT_<NAME>_* (container: via a 0600 --env-file, not argv).

mmbridge reaches the relay through a recording tap (`url`): it records each signed wake exactly as sent
(headers + raw body) so specs can tamper with / replay a genuinely captured wake (`send`, straight to the relay).
`down()` stops the relay and the tap (connection refused at mmbridge); `up()` starts both again on the same
ports with the same /data (Seen survives).
Simulated clock (replay N s later): in-process the relay clock is time.time() + offset for that one request.
The container relay has no clock hook (none is added to production code), so there the replay is sent at once
and is refused as a duplicate; the stale-timestamp path is covered by tests/unit/test_relay.py.
"""
import logging
import os
import secrets
import shutil
import socket
import subprocess
import tempfile
import time

import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from drivers import _serve
from relay import relay as relay_mod

START_S = 20.0


def _env(bots, routine_base):
    e = {"RELAY_ALLOW_HTTP_UPSTREAM": "true"}
    for name, b in bots.items():
        n = name.upper().replace("-", "_")
        e["RELAY_BOT_%s_HMAC_SECRET" % n] = b["secret"]
        e["RELAY_BOT_%s_ROUTINE_URL" % n] = "%s/%s" % (routine_base, name)
        e["RELAY_BOT_%s_ROUTINE_KEY" % n] = b["key"]
    return e


class _Capture(logging.Handler):
    """Plain capture: the relay logger's own RedactFilter is what is under test."""

    def __init__(self):
        super().__init__(logging.DEBUG)
        self.lines = []

    def emit(self, record):
        self.lines.append(record.getMessage())


class _InProcessRelay:
    def __init__(self, drv):
        self.drv = drv
        self.tmp = tempfile.mkdtemp(prefix="mmb-relay-")
        self.offset = 0.0
        self.port = 0
        self.env = {}
        self._srv = None
        self._log = _Capture()
        logging.getLogger("relay").addHandler(self._log)

    def _clock(self):
        return time.time() + self.offset

    def start(self, env=None):
        if env is not None:
            self.env = {**env, "RELAY_DATA_DIR": self.tmp}

        async def go():
            app = relay_mod.create_app(self.env, clock=self._clock)
            return await _serve.start(app, self.port, lifespan="on")
        server, task, self.port = self.drv._run(go())
        self._srv = (server, task)
        return "http://127.0.0.1:%d" % self.port

    def stop(self):
        if self._srv:
            self.drv._run(_serve.stop(*self._srv))
            self._srv = None

    def logs(self):
        return "\n".join(self._log.lines)

    def close(self):
        try:
            self.stop()
        finally:
            logging.getLogger("relay").removeHandler(self._log)
            shutil.rmtree(self.tmp, ignore_errors=True)


class _ContainerRelay:
    def __init__(self, drv):
        self.drv = drv
        self.image = os.environ.get("RELAY_IMAGE", "mmbridge-relay:bs1")
        self.name = "mmb-relay-" + secrets.token_hex(4)
        self.volume = self.name + "-data"
        self.port = _free_port()
        self.created = False
        self.offset = 0.0                        # no clock hook in the image (see module docstring)
        self._old_logs = ""
        self._envfile = None
        if self._docker("image", "inspect", self.image).returncode != 0:
            raise AssertionError("image %s not found: run `docker build -t %s relay` first" % (self.image, self.image))
        self._docker("volume", "create", self.volume, check=True)

    def _docker(self, *args, check=False, timeout=60):
        r = subprocess.run(["docker", *args], capture_output=True, text=True, timeout=timeout)
        if check and r.returncode != 0:
            raise AssertionError("docker %s failed: %s" % (args[0], r.stderr.strip()))
        return r

    def _wait_health(self):
        end = time.monotonic() + START_S
        while time.monotonic() < end:
            try:
                if httpx.get("http://127.0.0.1:%d/health" % self.port, timeout=1).status_code == 200:
                    return
            except httpx.HTTPError:
                pass
            time.sleep(0.05)
        raise AssertionError("relay container not healthy after %.0fs: %s" % (START_S, self.logs()[-2000:]))

    def start(self, env=None):
        if env is not None:                       # new config: replace the container, keep the volume
            if self.created:
                self._old_logs += self.logs()
                self._docker("rm", "-f", self.name)
                self.created = False
            fd, self._envfile = tempfile.mkstemp(prefix="mmb-relay-env-")
            with os.fdopen(fd, "w") as f:         # mkstemp: mode 0600
                f.write("".join("%s=%s\n" % kv for kv in env.items()))
        if self.created:
            self._docker("start", self.name, check=True)
        else:
            self._docker("run", "-d", "--name", self.name, "--network", "host", "-v", self.volume + ":/data",
                         "--env-file", self._envfile, self.image, "uvicorn", "relay:create_app", "--factory",
                         "--host", "127.0.0.1", "--port", str(self.port), check=True)
            self.created = True
        self._wait_health()
        return "http://127.0.0.1:%d" % self.port

    def stop(self):
        if self.created:
            self._docker("stop", "-t", "2", self.name)

    def logs(self):
        if not self.created:
            return self._old_logs
        r = self._docker("logs", self.name)
        return self._old_logs + r.stdout + r.stderr

    def close(self):
        try:
            if self.created:
                if os.environ.get("LIVE_SHOW_LOGS"):
                    print(self.logs())
                self._docker("rm", "-f", self.name)
        finally:
            self._docker("volume", "rm", "-f", self.volume)
            if self._envfile:
                os.unlink(self._envfile)


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class RelayHarness:
    """Relay (in-process or container) behind a recording tap; all on the driver's event loop."""

    def __init__(self, drv, mode, routine_base):
        self.drv, self.routine_base = drv, routine_base
        self.relay = _InProcessRelay(drv) if mode == "inprocess" else _ContainerRelay(drv)
        self.captured = []          # {"bot", "headers", "body", "status"} as mmbridge sent them
        self.responses = []         # relay responses to `send` (attacker view)
        self.relay_url = None
        self.tap_port = 0
        self._tap = None
        self._http = None
        self.app = Starlette(routes=[Route("/wake/{bot}", self._tap_wake, methods=["POST"])])

    async def _tap_wake(self, request: Request):
        body = await request.body()
        rec = {"bot": request.path_params["bot"], "headers": dict(request.headers), "body": body, "status": None}
        self.captured.append(rec)
        fwd = {k: v for k, v in request.headers.items() if k.startswith("x-mmb-") or k == "content-type"}
        try:
            r = await self._http.post(self.relay_url + request.url.path, content=body, headers=fwd, timeout=10)
        except httpx.HTTPError:
            rec["status"] = 502                    # only while relay and tap are being restarted
            return Response(status_code=502)
        rec["status"] = r.status_code
        return Response(r.content, status_code=r.status_code, media_type="application/json")

    @property
    def url(self):
        """Base URL mmbridge's wake URLs point at (the tap): <url>/wake/<bot>."""
        return "http://127.0.0.1:%d" % self.tap_port

    def configure(self, bots):
        """(Re)start the relay with env for `bots` {name: {"secret", "key"} }; start the tap the first time."""
        if self.relay_url:
            self.relay.stop()
        self.relay_url = self.relay.start(_env(bots, self.routine_base))
        if self._tap is None:
            self._start_tap()

    def _start_tap(self):
        async def go():
            if self._http is None:
                self._http = httpx.AsyncClient()
            return await _serve.start(self.app, self.tap_port)
        server, task, self.tap_port = self.drv._run(go())
        self._tap = (server, task)

    def down(self):
        if self._tap:
            self.drv._run(_serve.stop(*self._tap))
            self._tap = None
        self.relay.stop()

    def up(self):
        self.relay.start()
        self._start_tap()

    def last(self, bot):
        got = [r for r in self.captured if r["bot"] == bot]
        assert got, "no captured wake for %s" % bot
        return got[-1]

    def send(self, bot, body, headers, after_seconds=0.0):
        """POST straight to the relay (not via the tap), `after_seconds` later on the relay's clock."""
        self.relay.offset = float(after_seconds)      # honoured in-process only (module docstring)
        try:
            r = httpx.post("%s/wake/%s" % (self.relay_url, bot), content=body, headers=headers, timeout=10)
        finally:
            self.relay.offset = 0.0
        self.responses.append({"status": r.status_code, "text": r.text, "headers": dict(r.headers)})
        return {"status": r.status_code, "json": r.json() if r.content else None}

    def logs(self):
        return self.relay.logs()

    def close(self):
        try:
            if self._tap:
                self.drv._run(_serve.stop(*self._tap))
            if self._http:
                self.drv._run(self._http.aclose())
        finally:
            self.relay.close()

exec
/bin/bash -lc "cat app/wake.py | tail -130; grep -nE 'name|username' app/admin.py app/bot_store.py; cat relay/spike_routine.py; cat tests/unit/test_relay.py" in /mnt/d/rob/projects/mmbridge
 succeeded in 0ms:
CONCURRENCY = 4
PRUNE_EVERY_S = 6 * 3600
POLL_S = 0.5


def token_fp(token: str) -> str:
    """Non-secret fingerprint of the bot token, stored with bot_user_id in meta bot_identity by the listener."""
    return hashlib.sha256(("mmb-token-fp:" + token).encode()).hexdigest()[:16]


def _mac(secret: str, ts: str, body: bytes) -> str:
    return hmac.new(secret.encode(), ts.encode() + b"." + body, hashlib.sha256).hexdigest()


def sign(secret: str, ts: int, body: bytes) -> str:
    return "v1=" + _mac(secret, str(ts), body)


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


def _log(event: str, **fields) -> None:
    mlog.log.info(json.dumps({"event": event, **fields}))


class Dispatcher:
    def __init__(self, state, cfg, http: httpx.AsyncClient, max_attempts: int | None = None, clock=None,
                 poll_s: float = POLL_S, concurrency: int = CONCURRENCY):
        """cfg: BotConfig or a zero-arg callable returning the current one (read at every send, PR-2)."""
        self.state, self.http = state, http
        self._cfg = cfg if callable(cfg) else (lambda: cfg)
        if max_attempts:
            state.max_attempts = max_attempts
        self.clock = clock or state.clock
        self.poll_s, self.concurrency = poll_s, concurrency
        self.owner = None
        self._pruned_at = None
        self._waiting = False

    async def run(self) -> None:
        while True:
            if not await self.tick():
                await asyncio.sleep(self.poll_s)

    async def tick(self) -> int:
        """One loop pass; returns the number of wakes attempted."""
        st, now = self.state, self.clock()
        owner = await asyncio.to_thread(st.claim_owner, now)
        if owner != self.owner:
            _log("dispatcher_owner" if owner else "dispatcher_standby", instance=st.instance_id)
            self.owner = owner
        if not owner:
            return 0
        await asyncio.to_thread(st.recover_stale, now)
        if self._pruned_at is None or now - self._pruned_at >= PRUNE_EVERY_S:
            n = await asyncio.to_thread(st.prune, 7)
            self._pruned_at = now
            _log("wakes_pruned", count=n)
        cfg = self._cfg()
        # One meta row "<token_fp>:<bot_user_id>", written in one statement by the listener: the id and the
        # token it belongs to are always read as one snapshot (review 3 P2: no split-read race on rotation).
        fp, _, bot_id = (await asyncio.to_thread(st.get_meta, "bot_identity") or "").partition(":")
        if not bot_id or fp != token_fp(cfg.token):
            if not self._waiting:
                _log("dispatcher_waiting_identity", instance=st.instance_id)
                self._waiting = True
            return 0
        self._waiting = False
        due = await asyncio.to_thread(st.claim_due, now, self.concurrency)
        if due:
            await asyncio.gather(*(self._send(w, bot_id, cfg) for w in due))
        return len(due)

    async def _send(self, w, bot_id: str, cfg) -> None:
        st = self.state
        if (w.payload.get("bot") or {}).get("user_id") != bot_id:
            await asyncio.to_thread(st.mark_failed, w.post_id, "bot_rotated")
            _log("wake_failed", post_id=w.post_id, attempt=w.attempts, error="bot_rotated")
            return
        body = json.dumps({**w.payload, "attempt": w.attempts}, separators=(",", ":")).encode()
        ts = int(self.clock())
        headers = {"Content-Type": "application/json", "X-MMB-Delivery": w.post_id,
                   "X-MMB-Timestamp": str(ts), "X-MMB-Signature": sign(cfg.wake_secret, ts, body)}
        try:
            r = await asyncio.wait_for(
                self.http.post(cfg.wake_url, content=body, headers=headers, timeout=TIMEOUT_S), TIMEOUT_S)
            status, err = r.status_code, "http_%d" % r.status_code
        except (httpx.TimeoutException, asyncio.TimeoutError):
            status, err = None, "timeout"
        except httpx.TransportError:
            status, err = None, "connect"
        except (httpx.InvalidURL, ValueError):   # malformed wake_url: permanent, never kills the loop (review 4 P2)
            status, err = 0, "invalid_url"
        except httpx.HTTPError:                  # e.g. DecodingError on a bad gzip body: retryable (review 5 P2)
            status, err = None, "http_error"
        except Exception as e:                   # last line: no send error may stop the dispatcher or strand a claim
            status, err = None, "error_" + type(e).__name__
        if status is not None and 200 <= status < 300:
            await asyncio.to_thread(st.mark_delivered, w.post_id)
            fields = {"post_id": w.post_id, "attempt": w.attempts}
            if w.post_create_at:
                fields["latency_ms"] = int(self.clock() * 1000) - w.post_create_at
            _log("wake_delivered", **fields)
        elif status is None or status in (408, 429) or status >= 500:
            res = await asyncio.to_thread(st.mark_retry, w.post_id, err, self.clock() + next_delay(w.attempts))
            _log("wake_failed" if res == "failed" else "wake_retry", post_id=w.post_id, attempt=w.attempts,
                 error=err)
        else:
            await asyncio.to_thread(st.mark_failed, w.post_id, err)
            _log("wake_failed", post_id=w.post_id, attempt=w.attempts, error=err)
grep: app/bot_store.py: No such file or directory
app/admin.py:48:async def _username(token: str, transport) -> str:
app/admin.py:50:        return (await Client(token, MATTERMOST_URL, transport=transport).get("/users/me"))["username"]
app/admin.py:72:    username = asyncio.run(_username(token, transport))
app/admin.py:82:    print("bot @%s stored: wake_url %s" % (username, cfg.wake_url), file=out)
app/admin.py:151:if __name__ == "__main__":
"""OQ-B1/B2 spike (plan Phase 1): POST one marker JSON body to a real Grok Bot routine and print status codes.

Not in the relay image. The routine key is read from env SPIKE_ROUTINE_KEY or, if unset, from stdin (never
argv, never printed). Cases: valid key, wrong key, bad URL (routine URL with a junk suffix). Prints the case,
the HTTP status (or the error class) and the marker; never the key or response bodies.

    python3 relay/spike_routine.py https://<routine-url>          # paste the key at the prompt
Then check in Grok Bot: did the "valid key" run start, and does the bot see the JSON body verbatim (marker)?
"""
import getpass
import json
import os
import secrets
import sys

import httpx


def post(url: str, key: str, body: bytes) -> str:
    try:
        r = httpx.post(url, content=body, timeout=15, headers={
            "Authorization": "Bearer " + key, "Content-Type": "application/json", "X-MMB-Delivery": "spike"})
        return str(r.status_code)
    except httpx.HTTPError as e:
        return "error " + type(e).__name__


def main(argv) -> int:
    if len(argv) != 2 or not argv[1].startswith("https://"):
        print("usage: python3 relay/spike_routine.py https://<routine-url>  (key via SPIKE_ROUTINE_KEY or prompt)")
        return 2
    url = argv[1]
    key = os.environ.get("SPIKE_ROUTINE_KEY") or getpass.getpass("routine key (not echoed): ").strip()
    marker = "mmb-spike-" + secrets.token_hex(4)
    body = json.dumps({"version": 1, "kind": "post", "delivery_id": marker, "marker": marker,
                       "post": {"id": marker, "message": "spike %s: please echo this marker" % marker} },
                      separators=(",", ":")).encode()
    print("marker:", marker)
    for case, u, k in (("valid key", url, key), ("wrong key", url, "wrong-" + secrets.token_hex(8)),
                       ("bad URL", url.rstrip("/") + "-does-not-exist-" + secrets.token_hex(3), key)):
        print("%-10s -> %s" % (case, post(u, k, body)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
"""Wake relay (ADR-0011, plan Phase 1 / B-s1): env parsing, verify (copy of app.wake.verify, drift guard),
upstream status mapping, byte-identical forward with the Bearer routine key, redaction, replay dedupe,
in-flight guard, per-bot rate limit and the accepted-risk ambiguous outcomes (plan "Delivery guarantee")."""
import asyncio
import json
import logging

import httpx
import pytest

from app import wake as mm_wake
from relay import relay as rl

SECRET = "s" * 40
KEY = "routine-key-" + "k" * 24
URL = "https://routine.test/eddie"
NOW = 1_800_000_000


class Clock:
    def __init__(self, t=float(NOW)):
        self.t = t

    def __call__(self):
        return self.t


def env(**extra):
    e = {"RELAY_BOT_EDDIE_HMAC_SECRET": SECRET, "RELAY_BOT_EDDIE_ROUTINE_URL": URL,
         "RELAY_BOT_EDDIE_ROUTINE_KEY": KEY}
    e.update(extra)
    return e


def wake_body(delivery="p-1", message="hello", attempt=1):
    return json.dumps({"version": 1, "kind": "post", "delivery_id": delivery, "attempt": attempt,
                       "bot": {"user_id": "u-eddie", "username": "eddie"},
                       "post": {"id": delivery, "message": message} }, separators=(",", ":")).encode()


def signed(body, ts=NOW, secret=SECRET, delivery=None):
    d = delivery if delivery is not None else json.loads(body)["delivery_id"]
    return {"Content-Type": "application/json", "X-MMB-Delivery": d, "X-MMB-Timestamp": str(ts),
            "X-MMB-Signature": mm_wake.sign(secret, ts, body)}


class Upstream:
    """httpx MockTransport routine: records requests; `codes` pops one status per call (last one repeats);
    `exc` raises instead; `gate` (asyncio.Event) holds the response until set."""

    def __init__(self, codes=(200,), exc=None):
        self.codes, self.exc, self.gate = list(codes), exc, None
        self.calls = []
        self.called = asyncio.Event()

    async def handler(self, request):
        self.calls.append({"headers": dict(request.headers), "body": request.content, "url": str(request.url)})
        self.called.set()
        if self.gate is not None:
            await self.gate.wait()
        if self.exc is not None:
            exc, self.exc = self.exc, None
            raise exc
        code = self.codes.pop(0) if len(self.codes) > 1 else self.codes[0]
        return httpx.Response(code, json={"ok": code < 300})


@pytest.fixture
def clk():
    return Clock()


@pytest.fixture
def up():
    return Upstream()


@pytest.fixture
def db(tmp_path):
    return str(tmp_path / "relay.db")


def make(up, clk, db, e=None, seen=None):
    http = httpx.AsyncClient(transport=httpx.MockTransport(up.handler))
    app = rl.create_app(env(**(e or {})), http=http, clock=clk, seen=seen or rl.Seen(db))
    c = httpx.AsyncClient(transport=httpx.ASGITransport(app=app, raise_app_exceptions=False),
                          base_url="http://relay.test")
    c.relay = app.state.relay
    return c


async def until(pred, timeout=5.0):
    """Poll with a deadline (no fixed sleeps, AGENTS.md concurrency rule)."""
    loop = asyncio.get_running_loop()
    end = loop.time() + timeout
    while not pred():
        assert loop.time() < end, "condition not reached"
        await asyncio.sleep(0.001)


async def post(c, body, headers, bot="eddie"):
    return await c.post("/wake/" + bot, content=body, headers=headers)


# --- env parsing ---------------------------------------------------------------------------------------------
def test_load_bots_maps_env_names_to_bot_names():
    e = env(**{"RELAY_BOT_MY_BOT_HMAC_SECRET": "t" * 32, "RELAY_BOT_MY_BOT_ROUTINE_URL": "https://r.test/x",
               "RELAY_BOT_MY_BOT_ROUTINE_KEY": "key2", "OTHER": "x"})
    bots = rl.load_bots(e)
    assert set(bots) == {"eddie", "my-bot"}
    assert bots["eddie"] == rl.RelayBot("eddie", SECRET, URL, KEY)


@pytest.mark.parametrize("drop", ["HMAC_SECRET", "ROUTINE_URL", "ROUTINE_KEY"])
def test_load_bots_fails_on_missing_field(drop):
    e = env()
    del e["RELAY_BOT_EDDIE_" + drop]
    with pytest.raises(rl.ConfigError, match=drop.lower()):
        rl.load_bots(e)


def test_load_bots_fails_on_short_secret_without_echoing_it():
    with pytest.raises(rl.ConfigError) as ei:
        rl.load_bots(env(RELAY_BOT_EDDIE_HMAC_SECRET="short-secret-value"))
    assert "32" in str(ei.value) and "short-secret-value" not in str(ei.value)


def test_load_bots_requires_https_unless_test_flag():
    with pytest.raises(rl.ConfigError, match="https"):
        rl.load_bots(env(RELAY_BOT_EDDIE_ROUTINE_URL="http://routine.test/eddie"))
    bots = rl.load_bots(env(RELAY_BOT_EDDIE_ROUTINE_URL="http://routine.test/eddie", RELAY_ALLOW_HTTP_UPSTREAM="true"))
    assert bots["eddie"].routine_url == "http://routine.test/eddie"


# --- verify: copy of app.wake.verify (drift guard) -----------------------------------------------------------
def test_verify_accepts_wake_signed_by_mmbridge_sign():
    body = wake_body()
    assert rl.verify(SECRET, signed(body), body, NOW)


@pytest.mark.parametrize("case", ["ok", "tampered", "wrong_secret", "stale", "future", "no_sig", "no_ts",
                                  "bad_ts", "no_v1", "delivery_mismatch", "no_delivery", "not_json"])
def test_verify_matches_app_wake_verify(case):
    body = wake_body()
    h = signed(body)
    if case == "tampered":
        body = wake_body(message="evil")
    elif case == "wrong_secret":
        h = signed(body, secret="x" * 40)
    elif case == "stale":
        h = signed(body, ts=NOW - 301)
    elif case == "future":
        h = signed(body, ts=NOW + 301)
    elif case == "no_sig":
        del h["X-MMB-Signature"]
    elif case == "no_ts":
        del h["X-MMB-Timestamp"]
    elif case == "bad_ts":
        h["X-MMB-Timestamp"] = "abc"
    elif case == "no_v1":
        h["X-MMB-Signature"] = h["X-MMB-Signature"][3:]
    elif case == "delivery_mismatch":
        h["X-MMB-Delivery"] = "other"
    elif case == "no_delivery":
        del h["X-MMB-Delivery"]
    elif case == "not_json":
        body = b"not json"
        h = signed(body, delivery="p-1")
    assert rl.verify(SECRET, h, body, NOW) == mm_wake.verify(SECRET, h, body, NOW)
    assert rl.verify(SECRET, h, body, NOW) is (case == "ok")


# --- mapping table -------------------------------------------------------------------------------------------
@pytest.mark.parametrize("status,code", [(200, 200), (202, 200), (204, 200), (408, 503), (429, 503), (500, 503),
                                         (502, 503), (503, 503), (None, 503), (400, 424), (401, 424), (403, 424),
                                         (404, 424), (302, 424)])
def test_map_upstream(status, code):
    got, body = rl.map_upstream(status)
    assert got == code
    if code == 424:
        assert body == {"upstream": status}


# --- POST /wake/{bot} ----------------------------------------------------------------------------------------
async def test_valid_wake_forwarded_byte_identical_with_bearer(up, clk, db):
    body = wake_body()
    async with make(up, clk, db) as c:
        r = await post(c, body, signed(body))
    assert r.status_code == 200 and r.json() == {"status": "forwarded"}
    assert len(up.calls) == 1
    call = up.calls[0]
    assert call["url"] == URL and call["body"] == body
    assert call["headers"]["authorization"] == "Bearer " + KEY
    assert call["headers"]["content-type"] == "application/json"
    assert call["headers"]["x-mmb-delivery"] == "p-1"
    assert "x-mmb-signature" not in call["headers"]


async def test_unknown_bot_404_and_not_forwarded(up, clk, db):
    body = wake_body()
    async with make(up, clk, db) as c:
        r = await post(c, body, signed(body), bot="ghost")
    assert r.status_code == 404 and up.calls == []


@pytest.mark.parametrize("case,reason", [("forged", "bad_sig"), ("tampered", "bad_sig"), ("stale", "stale"),
                                         ("no_headers", "bad_sig")])
async def test_bad_wakes_401_and_upstream_not_called(up, clk, db, case, reason):
    body = wake_body()
    h = signed(body)
    if case == "forged":
        h = signed(body, secret="f" * 40)
    elif case == "tampered":
        body = wake_body(message="deploy now")
    elif case == "stale":
        clk.t = NOW + 600
    elif case == "no_headers":
        h = {"Content-Type": "application/json"}
    async with make(up, clk, db) as c:
        r = await post(c, body, h)
    assert r.status_code == 401 and r.json() == {"reason": reason}
    assert up.calls == []


@pytest.mark.parametrize("codes,exc,status", [((500,), None, 503), ((429,), None, 503), ((404,), None, 424),
                                              ((401,), None, 424), ((200,), httpx.ConnectError("x"), 503)])
async def test_upstream_status_mapped_back(clk, db, codes, exc, status):
    up = Upstream(codes, exc)
    body = wake_body()
    async with make(up, clk, db) as c:
        r = await post(c, body, signed(body))
    assert r.status_code == status


async def test_no_key_or_secret_in_logs_or_responses(up, clk, db, caplog):
    caplog.set_level(logging.INFO)
    body = wake_body()
    up.codes = [401, 500, 200]
    async with make(up, clk, db) as c:
        rs = [await post(c, body, signed(body)) for _ in range(3)]
        rs.append(await post(c, body, signed(body, secret="f" * 40)))
        rs.append(await c.get("/health"))
    text = caplog.text + "".join(r.text + json.dumps(dict(r.headers)) for r in rs)
    assert "relay_forwarded" in caplog.text and "relay_upstream" in caplog.text
    assert KEY not in text and SECRET not in text
    rl.log.info("leak check Authorization: Bearer %s secret %s", KEY, SECRET)
    assert KEY not in caplog.text and SECRET not in caplog.text


async def test_health_counts_only(up, clk, db):
    body = wake_body()
    async with make(up, clk, db) as c:
        await post(c, body, signed(body))
        await post(c, body, signed(body, secret="f" * 40))
        h = (await c.get("/health")).json()
    assert h == {"ok": True, "bots": 1, "forwarded_24h": 1, "rejected_24h": 1}


# --- replay / dedupe (required green before the B-s1 live demo) --------------------------------------------
async def test_replay_within_window_is_duplicate_not_forwarded(up, clk, db):
    body = wake_body()
    h = signed(body)
    async with make(up, clk, db) as c:
        r1 = await post(c, body, h)
        clk.t += 5
        r2 = await post(c, body, h)
    assert r1.json() == {"status": "forwarded"}
    assert r2.status_code == 200 and r2.json() == {"status": "duplicate"}
    assert len(up.calls) == 1


async def test_concurrent_identical_deliveries_forward_once(clk, db):
    up = Upstream()
    up.gate = asyncio.Event()
    body = wake_body()
    h = signed(body)
    async with make(up, clk, db) as c:
        t1 = asyncio.create_task(post(c, body, h))
        await asyncio.wait_for(up.called.wait(), 5)
        t2 = asyncio.create_task(post(c, body, h))
        await until(lambda: c.relay.pending("p-1") == 2)    # t2 waits on the in-flight guard, t1 is upstream
        up.gate.set()
        r1, r2 = await asyncio.wait_for(asyncio.gather(t1, t2), 5)
    assert sorted(r.json()["status"] for r in (r1, r2)) == ["duplicate", "forwarded"]
    assert len(up.calls) == 1


async def test_upstream_503_then_retry_forwarded_once_and_recorded(clk, db):
    up = Upstream(codes=(503, 200))
    body = wake_body()
    async with make(up, clk, db) as c:
        r1 = await post(c, body, signed(body))
        r2 = await post(c, body, signed(body, ts=NOW + 1))
        r3 = await post(c, body, signed(body, ts=NOW + 2))
    assert [r1.status_code, r2.status_code, r3.status_code] == [503, 200, 200]
    assert r3.json() == {"status": "duplicate"}
    assert len(up.calls) == 2
    assert rl.Seen(db).has("p-1")


async def test_seen_survives_restart(up, clk, db):
    body = wake_body()
    async with make(up, clk, db) as c:
        await post(c, body, signed(body))
    async with make(up, clk, db) as c:
        r = await post(c, body, signed(body))
    assert r.json() == {"status": "duplicate"} and len(up.calls) == 1


def test_seen_prunes_after_24h(db):
    s = rl.Seen(db)
    s.add("old", NOW)
    s.add("new", NOW + 3600)
    assert s.prune(NOW + 86400 + 1) == 1
    assert not s.has("old") and s.has("new")


async def test_rate_limit_eleventh_burst_request_429_not_forwarded(up, clk, db):
    async with make(up, clk, db) as c:
        rs = []
        for i in range(11):
            body = wake_body(delivery="p-%d" % i)
            rs.append(await post(c, body, signed(body)))
    assert [r.status_code for r in rs] == [200] * 10 + [429]
    assert rs[-1].json() == {"reason": "rate_limited"}
    assert len(up.calls) == 10


def test_rate_limit_refills_with_fake_clock():
    r = rl.RateLimit(per_min=30, burst=10)
    assert all(r.allow("eddie", 0.0) for _ in range(10))
    assert not r.allow("eddie", 0.0)
    assert r.allow("eddie", 2.0)               # 30/min = one token every 2 s
    assert not r.allow("eddie", 2.0)
    assert r.allow("other", 2.0)               # per bot
    assert not r.allow("eddie", 1.0)           # clock going backwards never adds tokens


# --- ambiguous outcomes (accepted risk A, Rob 2026-10-28): documented double wake ---------------------------
async def test_upstream_2xx_but_response_lost_retry_forwards_again(clk, db, caplog):
    caplog.set_level(logging.INFO)
    up = Upstream(exc=httpx.ReadTimeout("response lost"))   # routine started, its 200 never reached us
    body = wake_body()
    async with make(up, clk, db) as c:
        r1 = await post(c, body, signed(body))
        r2 = await post(c, body, signed(body, ts=NOW + 1))
    assert r1.status_code == 503 and r2.status_code == 200
    assert len(up.calls) == 2                                # double wake: accepted, not hidden
    assert "relay_delivery_ambiguous" in caplog.text


async def test_crash_between_upstream_2xx_and_seen_add_retry_forwards_again(up, clk, db):
    class CrashingSeen(rl.Seen):
        def add(self, d, now):
            raise RuntimeError("crash injected after upstream 2xx")

    body = wake_body()
    async with make(up, clk, db, seen=CrashingSeen(db)) as c:
        r1 = await post(c, body, signed(body))
    assert r1.status_code == 500
    async with make(up, clk, db) as c:                       # restarted relay, same db file
        r2 = await post(c, body, signed(body, ts=NOW + 1))
    assert r2.json() == {"status": "forwarded"}
    assert len(up.calls) == 2

exec
/bin/bash -lc '.venv/bin/pytest tests/unit/test_relay.py -q; python3 .eng/bin/eng-check .' in /mnt/d/rob/projects/mmbridge
 succeeded in 6847ms:
.......................................................                  [100%]
55 passed in 1.41s
WARN  .eng/runners.toml: no on_complete hook configured ([hooks] empty or missing) - bots must stay attached to eng-run until exit; fire-and-forget needs a non-empty on_complete / <role>_on_complete (PROCESS.md section 10, LESSONS L-006)
WARN  PROJECT_STATE.md: ## Latest artifacts has 37 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 33 rows / 6463 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 152 artifact(s) checked

codex
No actionable regressions were identified within the B-s1 scope. All 55 relay unit tests passed, and the repository checks completed without errors. Live Coolify/Grok integration was not verified.
No actionable regressions were identified within the B-s1 scope. All 55 relay unit tests passed, and the repository checks completed without errors. Live Coolify/Grok integration was not verified.
````
