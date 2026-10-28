---
id: RUN-2026-10-27-code-review-slice-20261027-lb4b-drop-allowlist
type: run-log
phase: verify
status: ok
owner_agent: eng-run
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md, thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md, thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review.md]
role: code-review
runner: codex
tool: codex
slice: SLICE-20261027-lb4b-drop-allowlist
plan: thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md
base: cb4e711
exit_code: 0
pid: 49608
eng_run_pid: 49607
started: 2026-10-27T22:23:54
prompt_template: code-review.md v2
---
# eng-run code-review slice-20261027-lb4b-drop-allowlist

## Summary
- role: code-review; runner: codex (codex); exit code: 0; started 2026-10-27 22:23:54
- review file: thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review.md - No findings.

## Command
````
codex review --base cb4e711
````

## Prompt
````
You are the independent code reviewer for this repository (eng-process kit v2.5.9). You did not write this code. Do not edit any file.

Follow the cross-model review step of eng-verify (.claude/skills/eng-verify/SKILL.md) and .eng/PROCESS.md section 10.

Review the changes of slice SLICE-20261027-lb4b-drop-allowlist (diff cb4e711...HEAD; slice card: thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md; plan: thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md) for correctness against the slice's acceptance criteria, missing or weak tests, security (auth, tenancy, secrets, injection), error handling, and maintainability.

Executable specs (v2.5): run `python .eng/bin/eng-spec status .`. Any change to locked specs or the DSL public interface is a [high] finding unless Rob re-approved it (new CP-C speclock row). For every changed DSL assertion step (assert_/then_/expect_/check_/verify_) name the step (e.g. `assert_order_placed`) in a finding and say whether the check got weaker. Driver changes are fine unless they hide failures (swallowed errors, retries that mask bugs, sleeps).

Output: a numbered list of findings, each as
  N. [severity] file:line - finding - suggested fix
with severity one of critical | high | medium | low. If you find nothing, write exactly "No findings."
Your final message is saved by eng-run to thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review.md (a review-findings artifact). Findings are advisory; Rob decides.
````

## Output
````
OpenAI Codex v0.164.0
--------
workdir: /mnt/d/rob/projects/mmbridge
model: gpt-6.1-sol
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR]
reasoning effort: none
reasoning summaries: none
session id: 01a18089-288d-70e0-bdd6-67f9364213ac
--------
user
changes against 'cb4e711'
exec
/bin/bash -lc 'cat PROJECT_STATE.md; git status --short; git diff --stat cb4e71149cda690e854f165684c09565c12fac13' in /mnt/d/rob/projects/mmbridge
 succeeded in 894ms:
---
id: STATE
type: project-state
phase: implement
status: active
owner_agent: claude-code
date: 2026-10-27
links: []
triage: large             # unset | small | medium | large
active_slice: SLICE-20261027-lb4-signed-wake-dispatcher
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
implement (increment A Live bots, Large) - PROCESS.md section 3.

## Goal (one sentence)
A public HTTPS MCP bridge (Python, deployed on Coolify at chats.rmlab.cloud) that lets Grok Bots read and post in Rob's self-hosted Mattermost, each bot using its own Mattermost bot token.

## Active slice
[SLICE-20261027-lb4-signed-wake-dispatcher](thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md) (done: verify PASS at 219a9a1; see Approval log). Previous: lb3 [done](thoughts/shared/slices/2026-10-27-lb3-listener-filters.md)

## Next action
lb4 done (see Approval log; README wake-receiver/tamper demo deferred until set-bot + wake secret exist). Allow-list delta: CP-A amendment + CP-C speclock rows in the Approval log; re-locked specs/DSL applied (new live specs red until lb4b implements). F8 dispositioned (live-only per ADR-0010). Next: lb4b (thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md) - do not start until the planner says; then lb5. Deploy prerequisites before enabling: Coolify volume /data (uid 10001), env MMB_STORE_KEY, replicas 1.

## Blockers
- none

## Pending approvals
See `pending_approvals` in the front matter (the only copy; `.eng/bin/eng-status` renders it). Do not list items here.

## Back-ups to an earlier phase
<!-- date - from phase -> to phase - why (blameless) - artifacts revised -->
none

## Latest artifacts
<!-- Relative links only; .eng/bin/eng-check verifies they resolve. -->
- Conventions: [AGENTS.md](AGENTS.md)
- Owner guide: [OWNER-GUIDE.md](OWNER-GUIDE.md)
- Definition of Done: [docs/definition-of-done.md](docs/definition-of-done.md)
- Process feedback: [thoughts/shared/process-feedback.md](thoughts/shared/process-feedback.md)
- Design A Live bots (approved; scope REDUCE recorded 2026-10-26): [docs/design/2026-10-26-live-bots.md](docs/design/2026-10-26-live-bots.md)
- Design (approved; scope hold approved): [docs/design/2026-10-25-mmbridge-mcp.md](docs/design/2026-10-25-mmbridge-mcp.md)
- Plan A Live bots (status in front matter): [thoughts/shared/plans/2026-10-27-live-bots.md](thoughts/shared/plans/2026-10-27-live-bots.md)
- Plan review A (AWAITING Codex, mandatory): [thoughts/shared/verification/2026-10-27-live-bots-plan-review.md](thoughts/shared/verification/2026-10-27-live-bots-plan-review.md)
- Review lb2 (addressed): [thoughts/shared/verification/2026-10-27-slice-20261027-lb2-state-db-wake-queue-review.md](thoughts/shared/verification/2026-10-27-slice-20261027-lb2-state-db-wake-queue-review.md)
- Specs A: [tests/acceptance/specs/test_live_bots.py](tests/acceptance/specs/test_live_bots.py)
- Architecture A Live bots (approved): [docs/architecture/2026-10-26-live-bots.md](docs/architecture/2026-10-26-live-bots.md)
- Cross-model review A (awaiting Codex): [thoughts/shared/verification/2026-10-26-live-bots-arch-review.md](thoughts/shared/verification/2026-10-26-live-bots-arch-review.md)
- Architecture: [docs/architecture/2026-10-25-mmbridge-mcp.md](docs/architecture/2026-10-25-mmbridge-mcp.md)
- ADRs 0001-0010 (all accepted): [docs/decisions/](docs/decisions/)
- Latest handoff: [thoughts/shared/handoffs/2026-10-27_12-53-47_lb4-blocked-dm-only-bot.md](thoughts/shared/handoffs/2026-10-27_12-53-47_lb4-blocked-dm-only-bot.md)
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
| 2026-10-27 | CP-C | thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md | approved speclock sha256:ea6a99cbd5601d05 |
| 2026-10-27 | CP-A | docs/design/2026-10-26-live-bots.md | approved amendment: drop allow-list sha256:0f250a0276b5 (via Eddie) |
| 2026-10-27 | CP-S | thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md | approved (verify PASS 219a9a1; README wake-receiver/tamper demo deferred - no set-bot/wake secret yet; via Eddie) |
| 2026-10-27 | CP-S | thoughts/shared/slices/2026-10-27-lb3-listener-filters.md | approved (verify PASS; ws_spike hello+ping reply+posted on Coolify; via Eddie) |
| 2026-10-27 | CP-S | thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md | approved (verify PASS; empty-DB admin failed/stats deferred; via Eddie) |
| 2026-10-27 | CP-S | thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md | approved (verify PASS; live container/Coolify check deferred, not yet redeployed; via Eddie) |
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
?? thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb4b-drop-allowlist.running.md
?? thoughts/shared/runs/2026-10-27-implement-slice-20261027-lb4b-drop-allowlist.running.md
 AGENTS.md                        |  7 ++++--
 CHANGELOG.md                     |  4 ++++
 OWNER-GUIDE.md                   |  2 ++
 app/admin.py                     | 52 ++++++++++++----------------------------
 app/listener.py                  |  2 +-
 app/live_filter.py               | 11 ++++-----
 app/store.py                     | 18 ++++++--------
 tests/acceptance/drivers/live.py | 37 ++++++++++++++++++++--------
 tests/unit/test_admin.py         | 51 ++++++++++++++++++++-------------------
 tests/unit/test_listener.py      | 13 ++++++----
 tests/unit/test_live_filter.py   | 51 ++++++++++++++++++++++++---------------
 tests/unit/test_store.py         | 25 +++++++++++++------
 tests/unit/test_wake.py          |  2 +-
 13 files changed, 151 insertions(+), 124 deletions(-)

exec
/bin/bash -lc "cat thoughts/shared/handoffs/2026-10-27_12-53-47_lb4-blocked-dm-only-bot.md; cat .eng/PROCESS.md; cat .claude/skills/eng-review/SKILL.md; find . -name 'AGENTS*' -not -path './.git/*'; python3 .eng/bin/eng-check ." in /mnt/d/rob/projects/mmbridge
 succeeded in 2696ms:
---
id: HANDO-20261027-lb4-blocked-dm-only-bot
type: handoff
phase: implement
status: complete
owner_agent: claude-code
date: 2026-10-27T12:53:47-05:00
links: [thoughts/shared/plans/2026-10-27-live-bots.md, thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md]
git_commit: 446047a
branch: main
next_skill: eng-implement-slice
---
# Handoff: lb4 blocked on a DM-only bot config (Issue in Phase 4)
<!-- Session handoff (agent to agent, one session). A standing orientation for a new implementer is a project brief: .eng/bin/eng-new brief. -->

## Task(s)
- SLICE-20261027-lb4-signed-wake-dispatcher (plan Phase 4): **blocked**. Test-first. The dispatcher, the HMAC receiver and the in-process live driver are done, and 5 of 7 lb4 specs are green. Two specs need a DM-only bot (`channels=[]`), which lb1 validation rejects. Reported as "Issue in Phase 4" rather than improvised.

## Critical References
- thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md (Progress log, Blockers with the suggested resolution, deviations)
- thoughts/shared/plans/2026-10-27-live-bots.md Phase 4
- docs/decisions/0008-signed-wake-webhook.md

## Recent changes
- app/wake.py:37 `sign`, :41 `verify`, :59 `Dispatcher`, :77 `tick` (owner heartbeat/standby, recover_stale, prune at start and every 6 h, claim 4), :97 `_send` (bot_rotated, attempt-stamped signed body, 5 s timeout, retry classes)
- app/listener.py:70 writes meta `bot_user_id`
- tests/unit/test_wake.py (40 tests), tests/unit/test_listener.py:122 (meta assertion)
- tests/acceptance/drivers/wake_receiver.py (new), tests/acceptance/drivers/live.py (in-process mode), tests/acceptance/drivers/fake_mattermost.py (`mm_ids=True`)
- Commit 446047a

## Learnings
- In-process driver pattern: a background event loop thread for fake MM, listener and dispatcher. Fake mutations (`add_post`) must run on that loop (`_call`), because the session queues are asyncio queues. `admin.main` runs on the spec thread (it calls `asyncio.run` itself).
- `assert_not_woken` needs a barrier, not just a sleep: post a marker DM, wait for its wake, then check. The ws events are ordered and the dispatcher claims in rowid order.
- SQLite INTEGER columns keep fractional `next_at` as REAL, so a scaled backoff (`WAKE_BACKOFF_SCALE=0.05`) works without schema changes.
- Codex CLI is not installed on this implementer PC, so the slice-diff review could not run.

## Artifacts
- app/wake.py, app/listener.py
- tests/unit/test_wake.py, tests/unit/test_listener.py
- tests/acceptance/drivers/live.py, tests/acceptance/drivers/wake_receiver.py, tests/acceptance/drivers/fake_mattermost.py
- thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md (status blocked)
- thoughts/shared/plans/2026-10-27-live-bots.md (Phase 4 unit box ticked)
- PROJECT_STATE.md (Blockers, Next action)

## Approvals
- Requested (decision for Rob, via the planner): resolve the Issue in Phase 4. Option A (suggested): allow an empty `channels` list in `store.validate` and `admin set-bot` (DM-only bot, REQ-A2), and flip `tests/unit/test_store.py:107`. Option B: change the two specs (needs a re-lock/CP-C).
- None granted this session.

## Action Items & Next Steps
1. Planner: put the Issue in Phase 4 to Rob; record the decision (approval log, plus an ADR-0006 note if Option A).
2. Implementer: eng-implement-slice lb4 again to apply the decision. Then run the PR-12 spec command; it should show exactly 7 passed.
3. Run the Codex slice review where codex is available: `python3 .eng/bin/eng-run code-review SLICE-20261027-lb4-signed-wake-dispatcher` (security slice). Answer its findings, then slice -> review, then eng-verify.
4. Not pushed.

## Other Notes
- Verification at 446047a: unit 216 passed (exit 0); acceptance default 16 passed / 9 skipped (exit 0); eng-spec status matches lock; PR-12 lb4 specs 5 passed / 2 failed (blocked). Out of scope but green: `test_bot_token_never_appears_in_logs_output_or_wakes`.
- No locked spec, no DSL file, no DSL assertion step body edited.
- Untracked files left as found: thoughts/shared/inbox.md, thoughts/shared/inbox-local-bak-1793080755/, the eng-run `.running.md` marker.
- No CHANGELOG entry: nothing is user-visible until lb5 wires the listener.
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
WARN  PROJECT_STATE.md: ## Latest artifacts has 25 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 24 rows / 4221 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 107 artifact(s) checked

exec
/bin/bash -lc 'git diff cb4e71149cda690e854f165684c09565c12fac13 -- app tests; cat app/store.py; cat app/live_filter.py' in /mnt/d/rob/projects/mmbridge
 succeeded in 141ms:
diff --git a/app/admin.py b/app/admin.py
index 7c549e1..9fe92fe 100644
--- a/app/admin.py
+++ b/app/admin.py
@@ -1,9 +1,9 @@
 """Operator CLI for the live bot (ADR-0006/0009): `python -m app.admin set-bot | show | rotate-key | failed | stats`.
 
 Run inside the container (Coolify terminal). The token is read from stdin only and never printed or logged;
-the wake secret is printed once when generated, never by `show`. Channels are resolved by name to ids with the
-bot's own token and must already include the bot (REQ-7: never joins). `failed`/`stats` read state.db and
-never print message text.
+the wake secret is printed once when generated, never by `show`. No channel list: Mattermost membership decides
+which channel posts wake the bot, and the bridge never joins (REQ-7); `--channels` is refused as no longer used.
+`failed`/`stats` read state.db and never print message text.
 """
 import argparse
 import asyncio
@@ -15,12 +15,9 @@ import time
 
 from app import logging as mlog
 from app import state, store
-from app.errors import ToolError
 from app.mattermost import MATTERMOST_URL, Client, MMError
-from app.service import _member_channel
-from app.validate import identifier
 
-FIELDS = ("token", "wake_url", "wake_secret", "channels")
+FIELDS = ("token", "wake_url", "wake_secret")
 
 
 class AdminError(Exception):
@@ -32,12 +29,12 @@ class AdminError(Exception):
 def _parser() -> argparse.ArgumentParser:
     p = argparse.ArgumentParser(prog="python -m app.admin", description="mmbridge live bot admin")
     sub = p.add_subparsers(dest="cmd", required=True)
-    s = sub.add_parser("set-bot", help="store the bot token, wake URL and channels (token read from stdin)")
+    s = sub.add_parser("set-bot", help="store the bot token and wake URL (token read from stdin)")
     s.add_argument("--token-stdin", action="store_true", required=True, help="read the bot token from stdin")
     s.add_argument("--wake-secret-stdin", action="store_true",
                    help="read the wake secret from the next stdin line instead of generating one")
     s.add_argument("--wake-url", required=True)
-    s.add_argument("--channels", default=None, help="team/channel,team/channel,... (omit for a DM-only bot)")
+    s.add_argument("--channels", default=None, help=argparse.SUPPRESS)   # removed: refused with a clear error
     sub.add_parser("show", help="show the stored config (token masked, secret hidden)")
     r = sub.add_parser("rotate-key", help="re-encrypt the store with a new MMB_STORE_KEY")
     r.add_argument("--new-key-env", default="MMB_STORE_KEY_NEW", help="env var holding the new key")
@@ -48,35 +45,17 @@ def _parser() -> argparse.ArgumentParser:
     return p
 
 
-def _channel_specs(raw: str) -> list[tuple[str, str]]:
-    out = []
-    for item in raw.split(","):
-        parts = item.strip().split("/")
-        if len(parts) != 2:
-            raise AdminError("invalid_argument", "channels must be team/channel,... (got %r)" % item.strip())
-        try:
-            out.append((identifier("team", parts[0]), identifier("channel", parts[1])))
-        except ToolError as e:
-            raise AdminError("invalid_argument", e.message) from None
-    return out
-
-
-async def _resolve(token: str, specs: list[tuple[str, str]], transport) -> tuple[str, list[str]]:
-    c = Client(token, MATTERMOST_URL, transport=transport)
+async def _username(token: str, transport) -> str:
     try:
-        me = await c.get("/users/me")
-        ids = []
-        for team, channel in specs:
-            ids.append((await _member_channel(c, team, channel))["id"])
-    except ToolError as e:
-        raise AdminError(e.code, e.message) from None
+        return (await Client(token, MATTERMOST_URL, transport=transport).get("/users/me"))["username"]
     except MMError as e:
         detail = "Mattermost rejected the bot token" if e.code == "unauthorized" else ""
         raise AdminError(e.code, detail) from None
-    return me["username"], list(dict.fromkeys(ids))
 
 
 def _set_bot(a, stdin, out, transport) -> None:
+    if a.channels is not None:
+        raise AdminError("invalid_argument", "channels no longer used (the bot wakes in channels it is a member of)")
     lines = stdin.read().splitlines()
     token = lines[0].strip() if lines else ""
     if not token:
@@ -87,29 +66,28 @@ def _set_bot(a, stdin, out, transport) -> None:
         raise AdminError("invalid_argument", "wake_secret: must be at least %d characters" % store.MIN_SECRET)
     if not store.https_ok(a.wake_url):
         raise AdminError("invalid_argument", "wake_url: must be https")
-    specs = [] if a.channels is None else _channel_specs(a.channels)
     key = os.getenv("MMB_STORE_KEY")
     if not (key or "").strip():
         raise store.StoreError("store_key_missing")
-    username, ids = asyncio.run(_resolve(token, specs, transport))
+    username = asyncio.run(_username(token, transport))
     path = store.path_from_env()
     try:
         prev = store.load(path, key)
     except store.StoreError:
         prev = None
-    cfg = store.BotConfig(token=token, wake_url=a.wake_url, wake_secret=secret, channels=ids)
+    cfg = store.BotConfig(token=token, wake_url=a.wake_url, wake_secret=secret)
     store.save(path, key, cfg)
     changed = [f for f in FIELDS if prev is None or getattr(prev, f) != getattr(cfg, f)]
     mlog.log.info(json.dumps({"event": "store_updated", "fields": changed}))
-    print("bot @%s stored: wake_url %s, channels %s" % (username, cfg.wake_url, ",".join(ids)), file=out)
+    print("bot @%s stored: wake_url %s" % (username, cfg.wake_url), file=out)
     if not supplied:
         print("wake secret (shown once; give it to the receiver): %s" % secret, file=out)
 
 
 def _show(out) -> None:
     cfg = store.load(store.path_from_env(), os.getenv("MMB_STORE_KEY"))
-    print("version: %d\ntoken: ****%s\nwake_url: %s\nwake_secret: set (hidden)\nchannels: %s" % (
-        cfg.version, cfg.token[-4:], cfg.wake_url, ",".join(cfg.channels)), file=out)
+    print("version: %d\ntoken: ****%s\nwake_url: %s\nwake_secret: set (hidden)" % (
+        cfg.version, cfg.token[-4:], cfg.wake_url), file=out)
 
 
 def _rotate_key(a, out) -> None:
diff --git a/app/listener.py b/app/listener.py
index b859f45..19eed23 100644
--- a/app/listener.py
+++ b/app/listener.py
@@ -105,7 +105,7 @@ class Listener:
                 _log("ws_connected", connection_id=self.connection_id,
                      server_version=(ev.get("data") or {}).get("server_version"))
                 continue
-            intent = decide(ev, self.bot_user_id, set(self.cfg.channels))
+            intent = decide(ev, self.bot_user_id)
             if intent:
                 payload = await self._payload(intent, client)
                 new = await asyncio.to_thread(self.state.enqueue_and_advance, intent.post_id, intent.channel_id,
diff --git a/app/live_filter.py b/app/live_filter.py
index c662aee..c306c23 100644
--- a/app/live_filter.py
+++ b/app/live_filter.py
@@ -1,8 +1,9 @@
 """Which Mattermost websocket events wake the live bot (architecture Filter rules, REQ-A1/A2/A3).
 
-Pure apart from the `event_invalid` log line: no I/O, no state. Drop own posts (A3), system posts (type set),
-group DMs (G) and open/private channels not chosen (A1); wake on DMs (D, A2) and chosen channels. Thread
-replies are new posts and wake, carrying root_id. Malformed `posted` events drop and log `event_invalid`
+Pure apart from the `event_invalid` log line: no I/O, no state. Drop own posts (A3), system posts (type set) and
+group DMs (G); wake on DMs (D, A2) and every other post in open/private channels (A1). Membership is the channel
+filter: Mattermost only sends the bot `posted` events for channels it is a member of, so there is no allow-list.
+Thread replies are new posts and wake, carrying root_id. Malformed `posted` events drop and log `event_invalid`
 (reason only; never the message text).
 """
 import json
@@ -37,7 +38,7 @@ def _post(data: dict) -> dict | None:
     return post if isinstance(post, dict) else None
 
 
-def decide(event: dict, bot_user_id: str, chosen: set[str]) -> WakeIntent | None:
+def decide(event: dict, bot_user_id: str) -> WakeIntent | None:
     if not isinstance(event, dict):
         _invalid("not_object")
         return None
@@ -68,8 +69,6 @@ def decide(event: dict, bot_user_id: str, chosen: set[str]) -> WakeIntent | None
 
     if post["user_id"] == bot_user_id or post.get("type") or ctype == "G":
         return None
-    if ctype in ("O", "P") and post["channel_id"] not in chosen:
-        return None
     hints = {k: data.get(k) for k in ("channel_name", "channel_display_name", "sender_name", "team_id")}
     return WakeIntent(post["id"], post["channel_id"], ctype, post["user_id"], message, create_at,
                       post.get("root_id") or None, hints)
diff --git a/app/store.py b/app/store.py
index 830fa33..83dd055 100644
--- a/app/store.py
+++ b/app/store.py
@@ -1,13 +1,14 @@
-"""Encrypted store for the ONE live bot's config (ADR-0006): token, wake URL, wake secret, channel ids.
+"""Encrypted store for the ONE live bot's config (ADR-0006): token, wake URL, wake secret. No channel list:
+Mattermost membership decides which channel posts can wake the bot (delta plan 2026-10-27).
 
 /data/bots.enc is the Fernet ciphertext of {"version": 1, "bot": {...} }, mode 0600, written atomically.
 Key from env MMB_STORE_KEY; "new,old" is accepted (MultiFernet) for key rotation. Errors never carry
 key material, token or secret. Loaded/saved token and secret are registered with the log redact filter.
+A legacy `channels` key (pre-lb4b stores) is ignored on load and dropped on the next save.
 """
 import httpx
 import json
 import os
-import re
 import tempfile
 from dataclasses import dataclass
 
@@ -17,7 +18,6 @@ from app import logging as mlog
 
 VERSION = 1
 MIN_SECRET = 32
-_CHANNEL_ID = re.compile(r"[a-z0-9]{26}")
 
 
 def path_from_env() -> str:
@@ -41,12 +41,11 @@ class BotConfig:
     token: str
     wake_url: str
     wake_secret: str
-    channels: list[str]
     version: int = VERSION
 
     def __repr__(self) -> str:  # never show token or secret
-        return "BotConfig(token=%s, wake_url=%r, wake_secret=****, channels=%r, version=%d)" % (
-            _mask(self.token), self.wake_url, self.channels, self.version)
+        return "BotConfig(token=%s, wake_url=%r, wake_secret=****, version=%d)" % (
+            _mask(self.token), self.wake_url, self.version)
 
     __str__ = __repr__
 
@@ -62,9 +61,6 @@ def validate(cfg: BotConfig) -> None:
         raise ValueError("wake_url: must be https")
     if len(cfg.wake_secret) < MIN_SECRET:
         raise ValueError("wake_secret: must be at least %d characters" % MIN_SECRET)
-    if (not isinstance(cfg.channels, list)
-            or not all(isinstance(c, str) and _CHANNEL_ID.fullmatch(c) for c in cfg.channels)):
-        raise ValueError("channels: must be a list of 26-char channel ids (empty = DMs only)")
 
 
 def https_ok(url: str) -> bool:
@@ -103,7 +99,7 @@ def _decode(plain: bytes) -> BotConfig:
         raise StoreError("store_unreadable", "bot: required")
     try:
         cfg = BotConfig(token=bot.get("token"), wake_url=bot.get("wake_url"), wake_secret=bot.get("wake_secret"),
-                        channels=bot.get("channels"), version=doc["version"])
+                        version=doc["version"])
         validate(cfg)
     except ValueError as e:
         raise StoreError("store_unreadable", str(e)) from None
@@ -159,7 +155,7 @@ def save(path: str, key: str | None, cfg: BotConfig) -> None:
         raise StoreError("store_invalid", str(e)) from None
     _register(cfg)
     doc = {"version": cfg.version, "bot": {"token": cfg.token, "wake_url": cfg.wake_url,
-                                           "wake_secret": cfg.wake_secret, "channels": list(cfg.channels)} }
+                                           "wake_secret": cfg.wake_secret} }
     _write(path, f.encrypt(json.dumps(doc).encode()))
 
 
diff --git a/tests/acceptance/drivers/live.py b/tests/acceptance/drivers/live.py
index 50f0441..fad2654 100644
--- a/tests/acceptance/drivers/live.py
+++ b/tests/acceptance/drivers/live.py
@@ -6,6 +6,7 @@ localhost port, MM-shaped channel ids), the real Listener and Dispatcher, and an
 The bot is configured with the real admin CLI (`app.admin.main`, as `python -m app.admin` would run it) on a
 temp /data with a fresh MMB_STORE_KEY; the printed wake secret is handed to the receiver. Backoff is scaled
 by WAKE_BACKOFF_SCALE so retry specs run in seconds.
+lb4b: no channel list in set-bot; the fake only sends `posted` to channel members, so membership is the filter.
 lb5 adds container mode (real image) and drop/restore connection.
 """
 import asyncio
@@ -62,6 +63,7 @@ class LiveDriver:
         self.rx = WakeReceiver()
         self.outputs = []              # admin CLI stdout
         self.posts = {}                # message -> post id (latest)
+        self.teams = {}                # channel name -> team (given_channel)
         self._last_post = None
         self._tasks = []
         self.state = None
@@ -89,10 +91,14 @@ class LiveDriver:
         except StopIteration:
             return self.mm.add_user(name)
 
-    def given_channel(self, team, channel, members):
+    def given_channel(self, team, channel, members, private=False):
         for m in members:
             self._user(m)
-        self.mm.add_channel(team, channel, members)
+        self.mm.add_channel(team, channel, members, ctype="P" if private else "O")
+        self.teams[channel] = team
+
+    def _channel(self, channel):
+        return self.mm.channel_by_name(channel, self.teams.get(channel, TEAM))
 
     def _admin(self, *argv, stdin=""):
         out = io.StringIO()
@@ -100,11 +106,10 @@ class LiveDriver:
         self.outputs.append(out.getvalue())
         return rc, out.getvalue()
 
-    def given_live_bot(self, name, channels):
+    def given_live_bot(self, name):
         u = self._user(name)
         u["is_bot"], u["token"] = True, "tok-%s-%s" % (name, secrets.token_hex(12))
-        chan = ["--channels", ",".join("%s/%s" % (TEAM, c) for c in channels)] if channels else []
-        rc, out = self._admin("set-bot", "--token-stdin", "--wake-url", WAKE_URL, *chan, stdin=u["token"] + "\n")
+        rc, out = self._admin("set-bot", "--token-stdin", "--wake-url", WAKE_URL, stdin=u["token"] + "\n")
         assert rc == 0, "admin set-bot failed: %s" % out.strip()
         self.rx.secret = re.search(r"wake secret \(shown once[^)]*\): (\S+)", out).group(1)
         cfg = store.load(store.path_from_env(), os.environ["MMB_STORE_KEY"])
@@ -128,13 +133,16 @@ class LiveDriver:
     def given_wake_target_down(self):
         self.rx.down = True
 
-    def _post(self, channel_id, user, message):
-        p = self._call(self.mm.add_post, channel_id, self._user(user)["id"], message)
+    def _post(self, channel_id, user, message, root_id=""):
+        p = self._call(self.mm.add_post, channel_id, self._user(user)["id"], message, "", root_id)
         self.posts[message], self._last_post = p["id"], p["id"]
         return p
 
     def post_in(self, channel, message, as_user):
-        self._post(self.mm.channel_by_name(channel, TEAM)["id"], as_user, message)
+        self._post(self._channel(channel)["id"], as_user, message)
+
+    def reply_in_thread(self, channel, to_message, message, as_user):
+        self._post(self._channel(channel)["id"], as_user, message, root_id=self.posts[to_message])
 
     def dm(self, bot, message, as_user):
         c = self.mm.direct_channel(self._user(bot)["id"], self._user(as_user)["id"])
@@ -173,7 +181,7 @@ class LiveDriver:
     def _delivered(self, post_id):
         return [r for r in self.rx.attempts(post_id) if r["status"] == 204]
 
-    def assert_woken_once(self, bot, channel, sender, message):
+    def assert_woken_once(self, bot, channel, sender, message, thread=None):
         pid = self.posts[message]
         self._wait(lambda: self._delivered(pid), WAKE_WITHIN_S, "wake for %r" % message)
         time.sleep(SETTLE_S)
@@ -186,7 +194,10 @@ class LiveDriver:
         if channel is None:
             assert w["channel"]["type"] == "D"
         else:
-            assert w["channel"]["name"] == channel and w["channel"]["type"] in ("O", "P")
+            assert w["channel"]["name"] == channel and w["channel"]["type"] == self._channel(channel)["type"]
+            assert w["channel"]["type"] in ("O", "P")
+        if thread is not None:
+            assert w["post"]["root_id"] == self.posts[thread], "wake does not name the thread %r" % thread
 
     def assert_not_woken(self, bot, message):
         # Barrier: a DM posted after the scenario is woken; anything before it has been processed by then.
@@ -201,6 +212,12 @@ class LiveDriver:
             others = [r for r in others if json.loads(r["body"]).get("post", {}).get("message") == message]
         assert not others, "unexpected wake(s): %s" % [r["headers"].get("x-mmb-delivery") for r in others]
 
+    def assert_not_member(self, bot, channel):
+        c = self._channel(channel)
+        assert self._user(bot)["id"] not in c["members"], "%s is a member of %s" % (bot, channel)
+        joins = [x for x in self.mm.calls if x[0] != "GET" and ("/members" in x[1] or c["id"] in x[1])]
+        assert joins == [] and self.mm.changes == [], "Mattermost writes: %s %s" % (joins, self.mm.changes)
+
     def assert_forged_wake_rejected(self, last):
         assert last["status"] == 401, "receiver accepted a forged wake (HTTP %s)" % last["status"]
         assert last["delivery"] not in self.rx.accepted
diff --git a/tests/unit/test_admin.py b/tests/unit/test_admin.py
index 552c507..1d65749 100644
--- a/tests/unit/test_admin.py
+++ b/tests/unit/test_admin.py
@@ -49,8 +49,8 @@ def tok(mm, name="eddie"):
     return mm.user_by_name(name)["token"]
 
 
-def set_bot(mm, channels="main/town-square,main/dev", url="https://wake.example/hook", stdin=None):
-    return run(mm, "set-bot", "--token-stdin", "--wake-url", url, "--channels", channels,
+def set_bot(mm, url="https://wake.example/hook", stdin=None):
+    return run(mm, "set-bot", "--token-stdin", "--wake-url", url,
                stdin=stdin if stdin is not None else tok(mm) + "\n")
 
 
@@ -59,13 +59,16 @@ def test_set_bot_stores_resolved_ids_and_prints_secret_once(mm, env, caplog):
         rc, out = set_bot(mm)
     assert rc == 0, out
     cfg = store.load(env["path"], env["key"])
-    assert cfg.token == tok(mm) and cfg.channels == [TOWN, DEV] and cfg.wake_url == "https://wake.example/hook"
+    assert cfg.token == tok(mm) and cfg.wake_url == "https://wake.example/hook"
     assert len(cfg.wake_secret) >= 32 and out.count(cfg.wake_secret) == 1
     assert tok(mm) not in out and tok(mm) not in caplog.text and cfg.wake_secret not in caplog.text
     assert "store_updated" in caplog.text
-    for f in ("token", "wake_url", "wake_secret", "channels"):
+    for f in ("token", "wake_url", "wake_secret"):
         assert f in caplog.text
+    assert "channels" not in caplog.text and "channels" not in out
+    assert "bot @eddie stored: wake_url https://wake.example/hook" in out
     assert not [c for c in mm.changes]   # never joins / changes the world
+    assert [c for c in mm.calls if "/channels" in c[1]] == []   # no channel lookups: membership is the filter
 
 
 def test_show_masks_token_never_prints_secret(mm, env):
@@ -74,31 +77,29 @@ def test_show_masks_token_never_prints_secret(mm, env):
     rc, out = run(mm, "show")
     assert rc == 0
     assert tok(mm) not in out and cfg.wake_secret not in out
-    assert tok(mm)[-4:] in out and TOWN in out and DEV in out and "https://wake.example/hook" in out
+    assert tok(mm)[-4:] in out and "https://wake.example/hook" in out
+    assert "channels" not in out and TOWN not in out
 
 
-def test_non_member_channel_refused_without_join(mm, env):
-    rc, out = set_bot(mm, channels="main/town-square,main/ops")
-    assert rc != 0 and "not_member" in out
+@pytest.mark.parametrize("ch", ["main/town-square", "main/ops", ""])
+def test_channels_option_refused_as_no_longer_used(mm, env, ch):
+    rc, out = run(mm, "set-bot", "--token-stdin", "--wake-url", "https://wake.example/hook", "--channels", ch,
+                  stdin=tok(mm) + "\n")
+    assert rc != 0 and "invalid_argument: channels no longer used" in out
     assert not os.path.exists(env["path"])
-    assert not [c for c in mm.calls if c[0] == "POST"] and mm.changes == []
+    assert mm.calls == [] and mm.changes == []   # refused before touching Mattermost
 
 
-def test_unknown_channel_refused(mm, env):
-    rc, out = set_bot(mm, channels="main/nope")
-    assert rc != 0 and "unknown_channel" in out and not os.path.exists(env["path"])
-
-
-@pytest.mark.parametrize("ch", ["town-square", "main/", "/x", "a/b/c", ""])
-def test_bad_channel_spec_refused(mm, env, ch):
-    rc, out = set_bot(mm, channels=ch)
-    assert rc != 0 and not os.path.exists(env["path"])
-
-
-def test_set_bot_without_channels_is_dm_only(mm, env):
-    rc, out = run(mm, "set-bot", "--token-stdin", "--wake-url", "https://wake.example/hook", stdin=tok(mm) + "\n")
+def test_set_bot_keeps_legacy_store_loadable_and_drops_channels(mm, env):
+    import json
+    open(env["path"], "wb").write(Fernet(env["key"].encode()).encrypt(json.dumps({"version": 1, "bot": {
+        "token": "old-token-xxxxxxxx", "wake_url": "https://old.example/h", "wake_secret": "o" * 40,
+        "channels": [TOWN]} }).encode()))
+    rc, out = run(mm, "show")
+    assert rc == 0 and "https://old.example/h" in out and TOWN not in out
+    rc, out = set_bot(mm)
     assert rc == 0, out
-    assert store.load(env["path"], env["key"]).channels == []
+    assert TOWN.encode() not in Fernet(env["key"].encode()).decrypt(open(env["path"], "rb").read())
 
 
 def test_http_wake_url_refused(mm, env):
@@ -128,14 +129,14 @@ def test_missing_key_refused(mm, env, monkeypatch):
 def test_supplied_wake_secret(mm, env):
     secret = "k" * 40
     rc, out = run(mm, "set-bot", "--token-stdin", "--wake-secret-stdin", "--wake-url", "https://w.example/h",
-                  "--channels", "main/town-square", stdin="%s\n%s\n" % (tok(mm), secret))
+                  stdin="%s\n%s\n" % (tok(mm), secret))
     assert rc == 0, out
     assert store.load(env["path"], env["key"]).wake_secret == secret and secret not in out
 
 
 def test_short_wake_secret_refused(mm, env):
     rc, out = run(mm, "set-bot", "--token-stdin", "--wake-secret-stdin", "--wake-url", "https://w.example/h",
-                  "--channels", "main/town-square", stdin="%s\n%s\n" % (tok(mm), "k" * 31))
+                  stdin="%s\n%s\n" % (tok(mm), "k" * 31))
     assert rc != 0 and "wake_secret" in out and not os.path.exists(env["path"])
 
 
diff --git a/tests/unit/test_listener.py b/tests/unit/test_listener.py
index 1e4e929..19a6624 100644
--- a/tests/unit/test_listener.py
+++ b/tests/unit/test_listener.py
@@ -21,9 +21,10 @@ def world():
     m.add_team("main")
     chosen = m.add_channel("main", "town-square", ["eddie", "rob"])
     other = m.add_channel("main", "off-topic", ["eddie", "rob"])
+    hr = m.add_channel("main", "hr", ["rob"], ctype="P")          # bot is not a member
     group = m.add_channel("main", "gdm", ["eddie", "rob"], ctype="G")
     dm = m.direct_channel(bot["id"], rob["id"])["id"]
-    return m, {"bot": bot, "rob": rob, "chosen": chosen, "other": other, "group": group, "dm": dm}
+    return m, {"bot": bot, "rob": rob, "chosen": chosen, "other": other, "hr": hr, "group": group, "dm": dm}
 
 
 @pytest.fixture
@@ -35,8 +36,7 @@ async def served(world):
 
 def make(served, tmp_path, **kw):
     m, w, base = served
-    cfg = BotConfig(token=w["bot"]["token"], wake_url="https://wake.example/hook", wake_secret="s" * 40,
-                    channels=[w["chosen"]])
+    cfg = BotConfig(token=w["bot"]["token"], wake_url="https://wake.example/hook", wake_secret="s" * 40)
     state = State(str(tmp_path / "state.db"))
     lis = Listener(cfg, state, lambda tok: Client(tok, base_url=base), base_url=base, **kw)
     return lis, state
@@ -69,7 +69,8 @@ async def test_qualifying_posts_land_once_in_state(running):
     m, w, lis, state = running
     rob, bot = w["rob"]["id"], w["bot"]["id"]
     wake1 = m.add_post(w["chosen"], rob, "eddie is great")
-    m.add_post(w["other"], rob, "not chosen")
+    other = m.add_post(w["other"], rob, "@channel any member channel wakes")
+    m.add_post(w["hr"], rob, "salary review")             # non-member: Mattermost never sends it to the bot
     m.add_post(w["chosen"], bot, "my own post")
     m.add_post(w["chosen"], rob, "rob joined", type="system_join_channel")
     m.add_post(w["group"], rob, "group dm")
@@ -78,9 +79,11 @@ async def test_qualifying_posts_land_once_in_state(running):
     m.ws_resend_last()                      # duplicate delivery of the reply event: dedupe gate
     marker = m.add_post(w["dm"], rob, "marker")
     await until(lambda: state.wake(marker["id"]) is not None)
-    assert [x.post_id for x in state.wakes()] == [wake1["id"], wake2["id"], reply["id"], marker["id"]]
+    assert [x.post_id for x in state.wakes()] == [wake1["id"], other["id"], wake2["id"], reply["id"],
+                                                  marker["id"]]
     assert all(x.status == "queued" for x in state.wakes())
     assert state.get_cursor(w["chosen"]) == (reply["create_at"], reply["id"])
+    assert state.get_cursor(w["hr"]) is None
     assert state.get_cursor(w["dm"]) == (marker["create_at"], marker["id"])
     assert state.wake(reply["id"]).payload["post"]["root_id"] == wake1["id"]
     assert state.wake(wake1["id"]).post_create_at == wake1["create_at"]
diff --git a/tests/unit/test_live_filter.py b/tests/unit/test_live_filter.py
index 3c8290d..46c3578 100644
--- a/tests/unit/test_live_filter.py
+++ b/tests/unit/test_live_filter.py
@@ -1,4 +1,5 @@
-"""live_filter.decide: architecture Filter rules (REQ-A1 chosen channels, A2 DMs, A3 own posts)."""
+"""live_filter.decide: architecture Filter rules (REQ-A1 member channels, A2 DMs, A3 own posts). Membership is the
+channel filter: Mattermost only sends the bot `posted` events for channels it is a member of."""
 import json
 import logging
 
@@ -7,7 +8,6 @@ import pytest
 from app.live_filter import WakeIntent, decide
 
 BOT = "u-eddie"
-CHOSEN = {"c-main-town-square"}
 
 
 def posted(channel_id="c-main-town-square", ctype="O", user_id="u-rob", ptype="", root_id="", message="hi",
@@ -20,53 +20,66 @@ def posted(channel_id="c-main-town-square", ctype="O", user_id="u-rob", ptype=""
             "broadcast": {"channel_id": channel_id} }
 
 
-def test_chosen_channel_wakes():
-    w = decide(posted(), BOT, CHOSEN)
+def test_member_channel_post_wakes():
+    w = decide(posted(), BOT)
     assert isinstance(w, WakeIntent)
     assert (w.post_id, w.channel_id, w.channel_type, w.user_id, w.message, w.create_at, w.root_id) == (
         "p-1", "c-main-town-square", "O", "u-rob", "hi", 1_700_000_000_000, None)
 
 
 @pytest.mark.parametrize("ctype", ["O", "P"])
-def test_non_chosen_open_or_private_channel_drops(ctype):
-    assert decide(posted(channel_id="c-main-other", ctype=ctype), BOT, CHOSEN) is None
+def test_any_open_or_private_channel_post_wakes(ctype):
+    w = decide(posted(channel_id="c-main-other", ctype=ctype), BOT)
+    assert w is not None and (w.channel_id, w.channel_type) == ("c-main-other", ctype)
 
 
-def test_chosen_private_channel_wakes():
-    assert decide(posted(ctype="P"), BOT, CHOSEN) is not None
+@pytest.mark.parametrize("wide", ["@channel", "@here", "@all"])
+def test_channel_wide_mention_wakes(wide):
+    w = decide(posted(message=wide + " standup in 5"), BOT)
+    assert w is not None and w.message == wide + " standup in 5"
 
 
-def test_dm_wakes_without_being_chosen():
-    w = decide(posted(channel_id="d-u-eddie__u-rob", ctype="D"), BOT, CHOSEN)
+def test_post_without_mention_wakes():
+    assert decide(posted(message="eddie is great"), BOT) is not None
+
+
+def test_dm_wakes():
+    w = decide(posted(channel_id="d-u-eddie__u-rob", ctype="D"), BOT)
     assert w is not None and w.channel_type == "D"
 
 
-def test_group_dm_drops_even_if_chosen():
-    assert decide(posted(ctype="G"), BOT, CHOSEN) is None
+def test_group_dm_drops():
+    assert decide(posted(ctype="G"), BOT) is None
+
+
+def test_decide_takes_no_channel_set():
+    with pytest.raises(TypeError):
+        decide(posted(), BOT, {"c-main-town-square"})
 
 
 @pytest.mark.parametrize("ctype", ["O", "D"])
 def test_own_post_drops(ctype):
-    assert decide(posted(ctype=ctype, user_id=BOT), BOT, CHOSEN) is None
+    assert decide(posted(ctype=ctype, user_id=BOT), BOT) is None
 
 
 @pytest.mark.parametrize("ptype", ["system_join_channel", "system_add_to_channel", "system_header_change"])
 def test_system_post_drops(ptype):
-    assert decide(posted(ptype=ptype), BOT, CHOSEN) is None
+    assert decide(posted(ptype=ptype), BOT) is None
 
 
-def test_thread_reply_wakes_with_root_id():
-    w = decide(posted(root_id="p-root"), BOT, CHOSEN)
+@pytest.mark.parametrize("ctype", ["O", "P", "D"])
+def test_thread_reply_wakes_with_root_id(ctype):
+    w = decide(posted(root_id="p-root", ctype=ctype), BOT)
     assert w is not None and w.root_id == "p-root"
 
 
 def test_post_given_as_dict_is_accepted():
-    assert decide(posted(post_as_str=False), BOT, CHOSEN) is not None
+    assert decide(posted(post_as_str=False), BOT) is not None
 
 
 def test_non_posted_event_is_ignored_silently(caplog):
     with caplog.at_level(logging.INFO, logger="mmbridge"):
-        assert decide({"event": "typing", "data": {}, "seq": 2}, BOT, CHOSEN) is None
+        assert decide({"event": "typing", "data": {}, "seq": 2}, BOT) is None
     assert "event_invalid" not in caplog.text
 
 
@@ -88,6 +101,6 @@ def _broken():
 @pytest.mark.parametrize("label,event", list(_broken()), ids=[x[0] for x in _broken()])
 def test_malformed_event_drops_and_logs_event_invalid(label, event, caplog):
     with caplog.at_level(logging.INFO, logger="mmbridge"):
-        assert decide(event, BOT, CHOSEN) is None
+        assert decide(event, BOT) is None
     assert "event_invalid" in caplog.text
     assert "m-private-text" not in caplog.text   # message text never logged
diff --git a/tests/unit/test_store.py b/tests/unit/test_store.py
index ba6fdca..ab2d222 100644
--- a/tests/unit/test_store.py
+++ b/tests/unit/test_store.py
@@ -8,13 +8,13 @@ from cryptography.fernet import Fernet
 from app import store
 from app.store import BotConfig, StoreError
 
-CH = "abcdefghijklmnopqrstuvwxyz"   # 26-char Mattermost id
+CH = "abcdefghijklmnopqrstuvwxyz"   # 26-char Mattermost id (legacy channels key)
 TOKEN = "mmtoken-abcdefghijklmnop-9876"
 SECRET = "s" * 43
 
 
 def cfg(**kw):
-    d = dict(token=TOKEN, wake_url="https://wake.example/hook", wake_secret=SECRET, channels=[CH])
+    d = dict(token=TOKEN, wake_url="https://wake.example/hook", wake_secret=SECRET)
     d.update(kw)
     return BotConfig(**d)
 
@@ -93,7 +93,7 @@ def _write_raw(path, key, obj):
 
 
 def _raw(**bot):
-    b = {"token": TOKEN, "wake_url": "https://w.example/h", "wake_secret": SECRET, "channels": [CH]}
+    b = {"token": TOKEN, "wake_url": "https://w.example/h", "wake_secret": SECRET}
     b.update(bot)
     return b
 
@@ -103,7 +103,6 @@ def _raw(**bot):
     ({"version": 1, "bot": {k: v for k, v in _raw().items() if k != "token"} }, "token"),
     ({"version": 1, "bot": _raw(wake_secret="short")}, "wake_secret"),
     ({"version": 1, "bot": _raw(wake_url="http://w.example/h")}, "wake_url"),
-    ({"version": 1, "bot": _raw(channels=["town-square"])}, "channels"),
     ({"version": 1}, "bot"),
     ([1, 2], "format"),
 ])
@@ -113,9 +112,21 @@ def test_load_validates(path, key, obj, detail):
     assert e.code == "store_unreadable" and detail in e.detail
 
 
-def test_empty_channel_list_is_a_dm_only_bot(path, key):
-    _write_raw(path, key, {"version": 1, "bot": _raw(channels=[])})
-    assert store.load(path, key).channels == []
+@pytest.mark.parametrize("legacy", [[CH], [], ["town-square"], "not-a-list"])
+def test_legacy_channels_key_loads_and_is_ignored(path, key, legacy):
+    # pre-lb4b /data/bots.enc files carry a "channels" list; membership is the filter now (delta plan)
+    _write_raw(path, key, {"version": 1, "bot": _raw(channels=legacy)})
+    cfg = store.load(path, key)
+    assert cfg == BotConfig(token=TOKEN, wake_url="https://w.example/h", wake_secret=SECRET)
+    assert not hasattr(cfg, "channels")
+
+
+def test_save_writes_no_channels_key(path, key):
+    import json
+    store.save(path, key, cfg())
+    doc = json.loads(Fernet(key.encode()).decrypt(open(path, "rb").read()))
+    assert doc == {"version": 1, "bot": {"token": TOKEN, "wake_url": "https://wake.example/hook",
+                                         "wake_secret": SECRET} }
 
 
 def test_http_wake_allowed_only_with_test_flag(path, key, monkeypatch):
diff --git a/tests/unit/test_wake.py b/tests/unit/test_wake.py
index 8b2067a..0728843 100644
--- a/tests/unit/test_wake.py
+++ b/tests/unit/test_wake.py
@@ -51,7 +51,7 @@ def rx(clk):
 
 
 def cfg(url=URL, secret=SECRET):
-    return BotConfig(token=TOKEN, wake_url=url, wake_secret=secret, channels=["a" * 26])
+    return BotConfig(token=TOKEN, wake_url=url, wake_secret=secret)
 
 
 def payload(post_id="p-1", bot_id="u-eddie"):
"""Encrypted store for the ONE live bot's config (ADR-0006): token, wake URL, wake secret. No channel list:
Mattermost membership decides which channel posts can wake the bot (delta plan 2026-10-27).

/data/bots.enc is the Fernet ciphertext of {"version": 1, "bot": {...} }, mode 0600, written atomically.
Key from env MMB_STORE_KEY; "new,old" is accepted (MultiFernet) for key rotation. Errors never carry
key material, token or secret. Loaded/saved token and secret are registered with the log redact filter.
A legacy `channels` key (pre-lb4b stores) is ignored on load and dropped on the next save.
"""
import httpx
import json
import os
import tempfile
from dataclasses import dataclass

from cryptography.fernet import Fernet, InvalidToken, MultiFernet

from app import logging as mlog

VERSION = 1
MIN_SECRET = 32


def path_from_env() -> str:
    return os.path.join(os.getenv("MMB_DATA_DIR", "/data"), "bots.enc")


class StoreError(Exception):
    """code: store_key_missing | store_unreadable | store_invalid (save-time validation). detail: field/reason."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__("%s: %s" % (code, detail) if detail else code)
        self.code, self.detail = code, detail


def _mask(s: str) -> str:
    return "****" + s[-4:] if len(s) > 8 else "****"


@dataclass
class BotConfig:
    token: str
    wake_url: str
    wake_secret: str
    version: int = VERSION

    def __repr__(self) -> str:  # never show token or secret
        return "BotConfig(token=%s, wake_url=%r, wake_secret=****, version=%d)" % (
            _mask(self.token), self.wake_url, self.version)

    __str__ = __repr__


def validate(cfg: BotConfig) -> None:
    """Raise ValueError(<field>: <reason>) unless cfg is a valid version-1 config (plan PR-6)."""
    if cfg.version != VERSION:
        raise ValueError("unsupported_version")
    for f in ("token", "wake_url", "wake_secret"):
        if not isinstance(getattr(cfg, f), str) or not getattr(cfg, f).strip():
            raise ValueError("%s: required" % f)
    if not https_ok(cfg.wake_url):
        raise ValueError("wake_url: must be https")
    if len(cfg.wake_secret) < MIN_SECRET:
        raise ValueError("wake_secret: must be at least %d characters" % MIN_SECRET)


def https_ok(url: str) -> bool:
    try:                                   # must also parse as the dispatcher will send it (review 4 P2)
        u = httpx.URL(url)
        if not u.host or (u.port is not None and not 0 < u.port < 65536):
            return False
    except (httpx.InvalidURL, ValueError, TypeError):
        return False
    if url.startswith("https://") and len(url) > 8:
        return True
    return os.getenv("LIVE_ALLOW_HTTP_WAKE", "").lower() == "true" and url.startswith("http://") and len(url) > 7


def _keys(key: str | None) -> list[Fernet]:
    keys = [k.strip() for k in (key or "").split(",") if k.strip()]
    if not keys:
        raise StoreError("store_key_missing")
    try:
        return [Fernet(k.encode()) for k in keys]
    except (ValueError, TypeError):
        raise StoreError("store_unreadable", "bad_key") from None


def _decode(plain: bytes) -> BotConfig:
    try:
        doc = json.loads(plain)
    except ValueError:
        raise StoreError("store_unreadable", "format") from None
    if not isinstance(doc, dict):
        raise StoreError("store_unreadable", "format")
    if doc.get("version") != VERSION:
        raise StoreError("store_unreadable", "unsupported_version")
    bot = doc.get("bot")
    if not isinstance(bot, dict):
        raise StoreError("store_unreadable", "bot: required")
    try:
        cfg = BotConfig(token=bot.get("token"), wake_url=bot.get("wake_url"), wake_secret=bot.get("wake_secret"),
                        version=doc["version"])
        validate(cfg)
    except ValueError as e:
        raise StoreError("store_unreadable", str(e)) from None
    return cfg


def _read(path: str, f: MultiFernet) -> tuple[bytes, BotConfig]:
    try:
        with open(path, "rb") as fh:
            blob = fh.read()
    except OSError:
        raise StoreError("store_unreadable", "file") from None
    try:
        plain = f.decrypt(blob)
    except InvalidToken:
        raise StoreError("store_unreadable", "decrypt") from None
    cfg = _decode(plain)
    _register(cfg)
    return blob, cfg


def _register(cfg: BotConfig) -> None:
    mlog.register_secret(cfg.token)
    mlog.register_secret(cfg.wake_secret)


def _write(path: str, data: bytes) -> None:
    """Atomic replace: 0600 temp file in the same dir, fsync, rename."""
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".bots.", suffix=".tmp")   # mkstemp creates 0600
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def load(path: str, key: str | None) -> BotConfig:
    return _read(path, MultiFernet(_keys(key)))[1]


def save(path: str, key: str | None, cfg: BotConfig) -> None:
    f = MultiFernet(_keys(key))
    try:
        validate(cfg)
    except ValueError as e:
        raise StoreError("store_invalid", str(e)) from None
    _register(cfg)
    doc = {"version": cfg.version, "bot": {"token": cfg.token, "wake_url": cfg.wake_url,
                                           "wake_secret": cfg.wake_secret} }
    _write(path, f.encrypt(json.dumps(doc).encode()))


def rotate(path: str, new_key: str | None, old_key: str | None) -> None:
    """Re-encrypt the store with the first new key (readable with new or old keys); validated first; atomic, 0600."""
    f = MultiFernet(_keys(new_key) + _keys(old_key))
    blob, _ = _read(path, f)
    _write(path, f.rotate(blob))
"""Which Mattermost websocket events wake the live bot (architecture Filter rules, REQ-A1/A2/A3).

Pure apart from the `event_invalid` log line: no I/O, no state. Drop own posts (A3), system posts (type set) and
group DMs (G); wake on DMs (D, A2) and every other post in open/private channels (A1). Membership is the channel
filter: Mattermost only sends the bot `posted` events for channels it is a member of, so there is no allow-list.
Thread replies are new posts and wake, carrying root_id. Malformed `posted` events drop and log `event_invalid`
(reason only; never the message text).
"""
import json
from dataclasses import dataclass

from app import logging as mlog


@dataclass(frozen=True)
class WakeIntent:
    post_id: str
    channel_id: str
    channel_type: str        # O | P | D
    user_id: str
    message: str
    create_at: int           # Mattermost ms
    root_id: str | None
    hints: dict              # event fields (channel_name, channel_display_name, sender_name, team_id) for fallbacks


def _invalid(reason: str) -> None:
    mlog.log.warning(json.dumps({"event": "event_invalid", "reason": reason}))


def _post(data: dict) -> dict | None:
    post = data.get("post")
    if isinstance(post, str):
        try:
            post = json.loads(post)
        except ValueError:
            return None
    return post if isinstance(post, dict) else None


def decide(event: dict, bot_user_id: str) -> WakeIntent | None:
    if not isinstance(event, dict):
        _invalid("not_object")
        return None
    if event.get("event") != "posted":
        return None
    data = event.get("data")
    if not isinstance(data, dict):
        _invalid("data")
        return None
    post = _post(data)
    if post is None:
        _invalid("post")
        return None
    for f in ("id", "channel_id", "user_id"):
        if not isinstance(post.get(f), str) or not post[f]:
            _invalid(f)
            return None
    create_at, message, ctype = post.get("create_at"), post.get("message", ""), data.get("channel_type")
    if not isinstance(create_at, int) or isinstance(create_at, bool):
        _invalid("create_at")
        return None
    if not isinstance(message, str):
        _invalid("message")
        return None
    if ctype not in ("O", "P", "D", "G"):
        _invalid("channel_type")
        return None

    if post["user_id"] == bot_user_id or post.get("type") or ctype == "G":
        return None
    hints = {k: data.get(k) for k in ("channel_name", "channel_display_name", "sender_name", "team_id")}
    return WakeIntent(post["id"], post["channel_id"], ctype, post["user_id"], message, create_at,
                      post.get("root_id") or None, hints)

exec
/bin/bash -lc "git diff cb4e71149cda690e854f165684c09565c12fac13 -- AGENTS.md OWNER-GUIDE.md CHANGELOG.md; rg 'cfg.channels|given_live_bot\\(|BotConfig\\(' app tests; ls .venv/bin/pytest; cat thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md" in /mnt/d/rob/projects/mmbridge
 succeeded in 53ms:
diff --git a/AGENTS.md b/AGENTS.md
index 9f5c46e..8534668 100644
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -17,9 +17,11 @@ Process: eng-process kit; canonical copy at `.eng/PROCESS.md` (phases, checkpoin
 The values live in `PROJECT_STATE.md` front matter (`implementer`, `planner`, `cross_review`, `push_permission`, `board`); `.eng/PROCESS.md` section 10 says what each means. Summary:
 - The **planner** agent plans, writes docs, keeps state and process. It does not write production code.
 - The **implementer** (default: Claude Code on the owner's PC) codes one slice at a time. When a slice is ready, the planner sends the owner the "ready to implement" message (`.eng/bin/eng-status` prints it), then afterwards picks up the implementer's handoff and runs `eng-verify` and `.eng/bin/eng-check`.
-- **Cross-model review** (Codex) is advisory, never a gate. See `.eng/PROCESS.md` section 10.
-- **Push:** follow `push_permission` (default `ask`: ask the owner before each push).
+- **Plan review is a gate for medium/large:** the mandatory cross-model plan review must be linked and clean before CP-C; slice and architecture cross-model reviews stay advisory. Detail in `.eng/PROCESS.md` section 10.
+- **Cross-model review** (Codex) of slices and architecture is advisory, never a gate (this does not cover the mandatory plan review above). See `.eng/PROCESS.md` section 10.
+- **Push:** follow `push_permission` (default `ask`). With `standing`, after eng-verify PASS you may push to `main` without asking. **Docs-only commits always push to `main` without asking** (both modes). Tags and force-push still ask. Never merge without the owner.
 - **Owner review notes** (`thoughts/shared/review-notes/`) belong to the owner. Agents never edit them until the owner says they are ready.
+- **Owner-facing updates:** brief status prose (or skip), then a labeled `**Action for Rob**` numbered list (one step per line; pasteable commands in their own fence) or `No action for you.`; end with the decision he owes. Never mix his todos into a status/findings paragraph. Never use `$TOKEN`-style shell placeholders in samples — use `PASTE_…_HERE` or paste-at-prompt. See `.eng/templates/owner-update.md` (LESSONS L-007). **Risk mitigations you uncovered:** name risk + friction/ops cost + narrower alternative; **Decision needed** before baking into design/architecture/plan (L-008).
 
 ## Commands
 - Install:  `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt`
@@ -39,6 +41,7 @@ The values live in `PROJECT_STATE.md` front matter (`implementer`, `planner`, `c
 - Durable decisions go in `docs/decisions/` (ADR). Deferred work goes in `TODOS.md`.
 - Don't touch: <paths / systems off-limits>
 
+
 ## Runtime facts
 - Container listens on **8080** (Coolify `SERVICE_FQDN_MMBRIDGE_8080`; local `docker run -p <host>:8080`), not 8000.
 - **Trusted proxy:** uvicorn honours X-Forwarded-For only from `FORWARDED_ALLOW_IPS` (Dockerfile default `127.0.0.1`). Never `*`. On Coolify set it to the Traefik source IP/subnet (TODO: real value from Rob). Until set, the anon rate limit keys on the proxy IP (shared bucket), which is safe but coarse.
diff --git a/CHANGELOG.md b/CHANGELOG.md
index 1582477..40c9701 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -2,6 +2,10 @@
 All notable changes to this project. Format: Keep a Changelog style; newest first.
 
 ## [Unreleased]
+<!-- id: CHANG-20261027-lb4b-drop-allowlist | owner_agent: unassigned | date: 2026-10-27 -->
+### Changed
+- Live bots: no channel allow-list. `python -m app.admin set-bot` takes only the token and wake URL (`--channels` is refused as no longer used; existing /data/bots.enc files with channel ids still load), and the bot wakes on every post by someone else in public or private channels it is a Mattermost member of, plus DMs; thread replies carry root_id. The bridge never joins channels.
+
 <!-- id: CHANG-20261027-lb2-state-db | owner_agent: unassigned | date: 2026-10-27 -->
 ### Added
 - Live bots: durable wake ledger and queue in /data/state.db (one wake per post, retries with 2-32 s backoff, crash-safe claims); `python -m app.admin failed [--retry POST_ID]` and `stats` for operators.
diff --git a/OWNER-GUIDE.md b/OWNER-GUIDE.md
index 3b63c22..e0948ee 100644
--- a/OWNER-GUIDE.md
+++ b/OWNER-GUIDE.md
@@ -30,4 +30,6 @@ Say "back up to discover" (or to any phase). That's normal, not a failure. The a
 - **ADR (Architecture Decision Record)**: a short numbered note of one durable decision and why, in `docs/decisions/`.
 - **Slice**: one small, end-to-end, demoable piece of work (about 100-200 changed lines).
 - **DoD (Definition of Done)**: the checklist every slice must pass (`docs/definition-of-done.md`).
+- **Runtime facts** (in `AGENTS.md`): short live values agents need (port, runtime pin, MCP restart after tool-list deploys). Project-specific numbers stay in that project's AGENTS; the section pattern comes from the kit.
+- **Push permission** (`push_permission` in PROJECT_STATE): `ask` (default) or `standing`. With standing, after eng-verify PASS agents may push to `main` without asking. **Docs-only commits always push without asking.** Tags and force-push still need you.
 
app/store.py:        return "BotConfig(token=%s, wake_url=%r, wake_secret=****, version=%d)" % (
app/store.py:        cfg = BotConfig(token=bot.get("token"), wake_url=bot.get("wake_url"), wake_secret=bot.get("wake_secret"),
tests/unit/test_wake.py:    return BotConfig(token=TOKEN, wake_url=url, wake_secret=secret)
app/admin.py:    cfg = store.BotConfig(token=token, wake_url=a.wake_url, wake_secret=secret)
tests/unit/test_store.py:    return BotConfig(**d)
tests/unit/test_store.py:    assert cfg == BotConfig(token=TOKEN, wake_url="https://w.example/h", wake_secret=SECRET)
tests/acceptance/dsl.py:    def given_live_bot(self, name="eddie"):
tests/acceptance/dsl.py:        self._d.given_live_bot(name)
tests/unit/test_listener.py:    cfg = BotConfig(token=w["bot"]["token"], wake_url="https://wake.example/hook", wake_secret="s" * 40)
tests/acceptance/specs/test_live_bots.py:    app.given_live_bot("eddie")
tests/acceptance/specs/test_live_bots.py:    app.given_live_bot("eddie")
tests/acceptance/specs/test_live_bots.py:    app.given_live_bot("eddie")
tests/acceptance/specs/test_live_bots.py:    app.given_live_bot("eddie")
tests/acceptance/specs/test_live_bots.py:    app.given_live_bot("eddie")
tests/acceptance/specs/test_live_bots.py:    app.given_live_bot("eddie")
tests/acceptance/specs/test_live_bots.py:    app.given_live_bot("eddie")
tests/acceptance/specs/test_live_bots.py:    app.given_live_bot("eddie")
tests/acceptance/specs/test_live_bots.py:    app.given_live_bot("eddie")
tests/acceptance/specs/test_live_bots.py:    app.given_live_bot("eddie")
tests/acceptance/specs/test_live_bots.py:    app.given_live_bot("eddie")
tests/acceptance/specs/test_live_bots.py:    app.given_live_bot("eddie")
tests/acceptance/specs/test_live_bots.py:    app.given_live_bot("eddie")
tests/acceptance/drivers/live.py:    def given_live_bot(self, name):
.venv/bin/pytest
---
id: SLICE-20261027-lb4b-drop-allowlist
type: slice
phase: implement
status: todo             # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md, thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md
plan_phase: 1
review: required (security: membership becomes the disclosure boundary) - thoughts/shared/verification/2026-10-27-lb4b-review.md
reqs: [REQ-A1, REQ-A2, REQ-A3, REQ-A7, REQ-A8]
specs: [tests/acceptance/specs/test_live_bots.py::test_mention_in_member_channel_wakes_bot_once, tests/acceptance/specs/test_live_bots.py::test_post_without_mention_in_member_channel_also_wakes_bot, tests/acceptance/specs/test_live_bots.py::test_channel_wide_mention_wakes_bot_once, tests/acceptance/specs/test_live_bots.py::test_reply_in_thread_bot_posted_in_wakes_bot_once, tests/acceptance/specs/test_live_bots.py::test_post_in_private_member_channel_wakes_bot_once, tests/acceptance/specs/test_live_bots.py::test_post_in_channel_bot_is_not_member_of_does_not_wake, tests/acceptance/specs/test_live_bots.py::test_dm_to_bot_wakes_bot_once, tests/acceptance/specs/test_live_bots.py::test_bots_own_post_never_wakes_itself, tests/acceptance/specs/test_live_bots.py::test_forged_wake_is_rejected, tests/acceptance/specs/test_live_bots.py::test_failed_wake_is_retried_then_visible_to_operator]
---
# Slice 4b: Drop the channel allow-list (re-lock specs)

Plan: [delta](../plans/2026-10-27-live-bots-delta-no-allowlist.md) Phase 1. Sequence: after lb4 CP-S, before lb5. **Security-relevant: gets the cross-model review.**
**Precondition:** CP-C for the delta logged by Rob with the new speclock hash. Until then this card stays todo.

## Outcome (user-visible, demoable)
`set-bot` takes token + wake URL only; in-process, the bot wakes once on any post (plain, @channel/@here/@all, thread reply naming the thread) in public or private channels it is a member of and on DMs; non-member channels never wake and are never joined.

## Acceptance criteria
- [ ] Re-lock: copy thoughts/shared/plans/drafts/2026-10-27-lb4b-test_live_bots.py.draft -> tests/acceptance/specs/test_live_bots.py and 2026-10-27-lb4b-dsl.py.draft -> tests/acceptance/dsl.py; `python3 .eng/bin/eng-spec lock .` prints exactly the hash Rob approved at CP-C (candidate sha256:ea6a99cbd5601d05); any difference -> stop, no commit
- [ ] app/store.py: no channels in BotConfig/validate; legacy `channels` key loads and is ignored (unit test)
- [ ] app/admin.py: no `--channels`; passing it -> `invalid_argument: channels no longer used`; show/set-bot output without channels
- [ ] app/live_filter.py: `decide(event, bot_user_id)`; O/P wake, D wake, own/system/G drop (unit tests incl. @channel, thread reply with root_id, non-member never reaches)
- [ ] tests/acceptance/drivers/live.py: given_channel(team, channel, members, private), reply in thread, membership check; no --channels; no join calls
- [ ] Wake payload carries root_id for thread replies

## Tasks
- [ ] Apply the re-lock (above) and confirm the specs: node ids fail for the right reason (red)
- [ ] Write failing unit tests, implement, go green
- [ ] Automated: `.venv/bin/pytest tests/unit -q` exit 0; `.venv/bin/pytest -q --channel live tests/acceptance/specs/test_live_bots.py::test_mention_in_member_channel_wakes_bot_once tests/acceptance/specs/test_live_bots.py::test_post_without_mention_in_member_channel_also_wakes_bot tests/acceptance/specs/test_live_bots.py::test_channel_wide_mention_wakes_bot_once tests/acceptance/specs/test_live_bots.py::test_reply_in_thread_bot_posted_in_wakes_bot_once tests/acceptance/specs/test_live_bots.py::test_post_in_private_member_channel_wakes_bot_once tests/acceptance/specs/test_live_bots.py::test_post_in_channel_bot_is_not_member_of_does_not_wake tests/acceptance/specs/test_live_bots.py::test_dm_to_bot_wakes_bot_once tests/acceptance/specs/test_live_bots.py::test_bots_own_post_never_wakes_itself tests/acceptance/specs/test_live_bots.py::test_forged_wake_is_rejected tests/acceptance/specs/test_live_bots.py::test_failed_wake_is_retried_then_visible_to_operator` exit 0 with 12 passed (10 functions; @channel/@here/@all parametrized); `.venv/bin/pytest tests/acceptance -q` (MCP regression) exit 0; `python3 .eng/bin/eng-spec status .` matches the new lock; `python3 .eng/bin/eng-check .` exit 0
- [ ] Manual (in-process demo, CP-S): with the fake MM, a plain post, an @channel post and a thread reply in a member channel each wake once (reply names the thread); a DM wakes; a post in a non-member private channel does not wake. Container suite + deployed demo stay in lb5.

## Size check
~150 lines + tests

## Progress log
<!-- date - agent - what changed (file:line) -->

## Blockers / deviations from plan
- Blocked on CP-C (Rob approves the delta and speclock hash).
- Drop/reconnect specs (test_post_during_connection_drop_..., test_post_during_drop_in_channel_on_another_team_...) and the token spec run in lb5.

exec
/bin/bash -lc '.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q' in /mnt/d/rob/projects/mmbridge
exec
/bin/bash -lc 'cat tests/acceptance/conftest.py | tail -65; cat .eng/prompts/code-review* 2>/dev/null | head -40; git diff --check cb4e71149cda690e854f165684c09565c12fac13' in /mnt/d/rob/projects/mmbridge
 succeeded in 442ms:
"""Acceptance-test wiring: channel option, driver fixture, markers. Not locked; edit freely."""
import os
import pytest

from dsl import Dsl


def pytest_addoption(parser):
    parser.addoption("--channel", default=os.environ.get("ACCEPTANCE_CHANNEL", "mcp"),
                     choices=["api", "ui", "mcp", "live"], help="protocol driver to run the specs through")


def pytest_configure(config):
    config.addinivalue_line("markers", "req(id): design-doc requirement this executable spec covers")
    config.addinivalue_line("markers", "channels(*names): channels this spec runs on (default: api)")


def pytest_collection_modifyitems(config, items):
    ch = config.getoption("--channel")
    here = os.path.dirname(os.path.abspath(__file__))
    for item in items:
        if not str(item.path).startswith(here + os.sep):
            continue  # only acceptance specs are channel-filtered (`pytest tests` must still run tests/unit)
        m = item.get_closest_marker("channels")
        if ch not in (m.args if m else ("api",)):
            item.add_marker(pytest.mark.skip(reason="not a %s-channel spec" % ch))


@pytest.fixture
def driver(request):
    ch = request.config.getoption("--channel")
    base = os.environ.get("ACCEPTANCE_BASE_URL", "http://127.0.0.1:8000")
    if ch == "api":
        from drivers.api import ApiDriver
        d = ApiDriver(base)
    elif ch == "ui":
        from drivers.ui import UiDriver
        d = UiDriver(base, page=request.getfixturevalue("page"))   # page fixture from pytest-playwright
    elif ch == "live":
        # Live bots (ADR-0010): container + fake MM websocket + wake receiver; built in slices 3-5.
        from drivers.live import LiveDriver
        d = LiveDriver()
    else:
        # In-process bridge (app.main:app) over Streamable HTTP + fake Mattermost; built in slice 1.
        from drivers.mcp import McpDriver
        d = McpDriver()
    yield d
    d.close()


@pytest.fixture
def app(driver):
    """The DSL every spec talks to."""
    return Dsl(driver)
---
prompt: code-review
prompt_version: 2
skill: eng-verify (Cross-model review section; PROCESS.md section 10)
writes: { {OUTPUT} }
---
You are the independent code reviewer for this repository (eng-process kit v{ {KIT_VERSION} }). You did not write this code. Do not edit any file.

Follow the cross-model review step of eng-verify (.claude/skills/eng-verify/SKILL.md) and .eng/PROCESS.md section 10.

Review the changes of { {SUBJECT} } (diff { {BASE} }...HEAD; slice card: { {SLICE_FILE} }; plan: { {PLAN} }) for correctness against the slice's acceptance criteria, missing or weak tests, security (auth, tenancy, secrets, injection), error handling, and maintainability.

Executable specs (v2.5): run `python .eng/bin/eng-spec status .`. Any change to locked specs or the DSL public interface is a [high] finding unless Rob re-approved it (new CP-C speclock row). For every changed DSL assertion step (assert_/then_/expect_/check_/verify_) name the step (e.g. `assert_order_placed`) in a finding and say whether the check got weaker. Driver changes are fine unless they hide failures (swallowed errors, retries that mask bugs, sleeps).

Output: a numbered list of findings, each as
  N. [severity] file:line - finding - suggested fix
with severity one of critical | high | medium | low. If you find nothing, write exactly "No findings."
Your final message is saved by eng-run to { {OUTPUT} } (a review-findings artifact). Findings are advisory; Rob decides.

exec
/bin/bash -lc 'cat .claude/skills/eng-verify/SKILL.md | tail -45; python3 .eng/bin/eng-spec status .; python3 .eng/bin/eng-check .' in /mnt/d/rob/projects/mmbridge
 succeeded in 1971ms:
---
name: eng-verify
description: Independently verify the implementation against the plan and the Definition of Done by re-running every check, and fold in the advisory cross-model review. Use after the implementer's handoff and review fixes, for each slice before CP-S and for the increment before shipping.
---
# eng-verify

Session: standard. **Start:** read only `PROJECT_STATE.md`, the latest handoff it links, and this skill's Inputs; run `.eng/bin/eng-check .` and stop and report if it fails for a reason this skill must not fix; stop if `pending_approvals` holds a checkpoint this skill needs. **Finish:** run eng-handoff (updates PROJECT_STATE phase / active_slice / pending_approvals / owner_agent / date / Next action / Blockers / Latest artifacts, writes the handoff, eng-check must pass, commits docs). Edge cases: `.eng/PROCESS.md` section 8. Scripts: `.eng/bin/eng-check`, `.eng/bin/eng-status`, `.eng/bin/eng-new`.

## Inputs (files only)
- Plan, slice cards, `docs/definition-of-done.md`, the implementer's latest handoff
- Review findings `thoughts/shared/verification/*-review.md` for the slice(s)
- `git diff <base>...HEAD`

## Outputs
- `thoughts/shared/verification/<date>-<slug>.md` (includes a **Cross-model review** section)
- Follow-ups in `TODOS.md`

## Steps
1. Run as the planner (or another agent), not the implementer. Pick up the implementer's handoff.
2. Re-execute every Automated Verification command and the full test/lint/build; record command + exit code.
3. Review the diff against the plan: deviations, missed items, edge/error paths, security; name every weakened test, timeout, skip, or suppression.
3a. **Executable specs (v2.5, when acceptance is enabled):** re-run the whole acceptance suite on every planned channel (`pytest tests/acceptance`, plus `--channel=ui` for large work), paste `python3 .eng/bin/eng-spec trace .` into the report's Executable specs table with results, and `eng-spec status .`. Any REQ without a passing spec, or a locked spec / DSL interface change without Rob's new CP-C speclock row, is a FAIL item; a changed DSL assertion step must be covered by the code review findings.
4. **Cross-model review:** medium/large: confirm the mandatory plan review is linked and clean (.eng/bin/eng-check). Slice diffs: confirm the Codex findings file exists for this diff (required for auth/tenancy/security slices; "skipped: small/docs-only" otherwise allowed). If missing and needed, ask Rob to run it before CP-S (`python3 .eng/bin/eng-run code-review <slice-id>`; Chet/Dave may run it on Rob's PC with his approval). eng-run refuses to let the implementer review its own slice; a `--allow-self-review` run must be named in the report. Whoever starts a headless code-review **stays attached** until exit (default), or uses a non-empty `code_review_on_complete` / `on_complete` plus an S 45m timeout on the `.running.md` PID marker (PROCESS.md section 10; L-006). Summarize it in the report section: reviewer, command, counts by severity, the resolution of each high finding. Advisory: never a FAIL by itself, but name any unresolved high finding in the Verdict.
5. Walk the DoD item by item: pass / fail / n.a.
6. Verdict PASS only if all criteria and DoD items pass; otherwise FAIL with the slice to reopen. Run `.eng/bin/eng-check .`.

## Exit criteria
Report complete with re-executed evidence, review summary and verdict.

## Approval stop (Rob)
Per slice: **CP-S** `CP-S: <slice path> - manual verification`. Increment: **CP-D** `CP-D: <report path> - approve done` with the Manual Verification checklist.

## Finish
Standard: end with eng-handoff.
lock approval: ok (2026-10-27)
specs and DSL interface match the lock
WARN  .eng/runners.toml: no on_complete hook configured ([hooks] empty or missing) - bots must stay attached to eng-run until exit; fire-and-forget needs a non-empty on_complete / <role>_on_complete (PROCESS.md section 10, LESSONS L-006)
WARN  PROJECT_STATE.md: ## Latest artifacts has 25 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 24 rows / 4221 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 107 artifact(s) checked

exec
/bin/bash -lc '.venv/bin/pytest tests/unit/test_listener.py -xq' in /mnt/d/rob/projects/mmbridge
 exited 1 in 3765ms:
.E
==================================== ERRORS ====================================
__________ ERROR at setup of test_qualifying_posts_land_once_in_state __________

self = <uvicorn.server.Server object at 0x77e92ce40530>, sockets = None

    async def startup(self, sockets: list[socket.socket] | None = None) -> None:
        await self.lifespan.startup()
        if self.lifespan.should_exit:
            self.should_exit = True
            return
    
        config = self.config
    
        def create_protocol(
            _loop: asyncio.AbstractEventLoop | None = None,
        ) -> asyncio.Protocol:
            return config.http_protocol_class(  # type: ignore[call-arg]
                config=config,
                server_state=self.server_state,
                app_state=self.lifespan.state,
                _loop=_loop,
            )
    
        loop = asyncio.get_running_loop()
    
        listeners: Sequence[socket.SocketType]
        if sockets is not None:  # pragma: full coverage
            # Explicitly passed a list of open sockets.
            # We use this when the server is run from a Gunicorn worker.
    
            def _share_socket(
                sock: socket.SocketType,
            ) -> socket.SocketType:  # pragma py-linux pragma: py-darwin
                # Windows requires the socket be explicitly shared across
                # multiple workers (processes).
                from socket import fromshare  # type: ignore[attr-defined]
    
                sock_data = sock.share(os.getpid())  # type: ignore[attr-defined]
                return fromshare(sock_data)
    
            self.servers: list[asyncio.base_events.Server] = []
            for sock in sockets:
                is_windows = platform.system() == "Windows"
                if config.workers > 1 and is_windows:  # pragma: py-not-win32
                    sock = _share_socket(sock)  # type: ignore[assignment]
                server = await loop.create_server(create_protocol, sock=sock, ssl=config.ssl, backlog=config.backlog)
                self.servers.append(server)
            listeners = sockets
    
        elif config.fd is not None:  # pragma: py-win32
            # Use an existing socket, from a file descriptor.
            sock = socket.fromfd(config.fd, socket.AF_UNIX, socket.SOCK_STREAM)
            server = await loop.create_server(create_protocol, sock=sock, ssl=config.ssl, backlog=config.backlog)
            assert server.sockets is not None  # mypy
            listeners = server.sockets
            self.servers = [server]
    
        elif config.uds is not None:  # pragma: py-win32
            # Create a socket using UNIX domain socket.
            uds_perms = 0o666
            if os.path.exists(config.uds):
                uds_perms = os.stat(config.uds).st_mode  # pragma: full coverage
            server = await loop.create_unix_server(
                create_protocol, path=config.uds, ssl=config.ssl, backlog=config.backlog
            )
            os.chmod(config.uds, uds_perms)
            assert server.sockets is not None  # mypy
            listeners = server.sockets
            self.servers = [server]
    
        else:
            # Standard case. Create a socket from a host/port pair.
            try:
>               server = await loop.create_server(
                    create_protocol,
                    host=config.host,
                    port=config.port,
                    ssl=config.ssl,
                    backlog=config.backlog,
                )

.venv/lib/python3.12/site-packages/uvicorn/server.py:163: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_UnixSelectorEventLoop running=False closed=False debug=False>
protocol_factory = <function Server.startup.<locals>.create_protocol at 0x77e92ce1ff60>
host = '127.0.0.1', port = 0, family = <AddressFamily.AF_UNSPEC: 0>
flags = <AddressInfo.AI_PASSIVE: 1>, sock = None, backlog = 2048, ssl = None
reuse_address = True, reuse_port = None, ssl_handshake_timeout = None
ssl_shutdown_timeout = None, start_serving = True

    async def create_server(
            self, protocol_factory, host=None, port=None,
            *,
            family=socket.AF_UNSPEC,
            flags=socket.AI_PASSIVE,
            sock=None,
            backlog=100,
            ssl=None,
            reuse_address=None,
            reuse_port=None,
            ssl_handshake_timeout=None,
            ssl_shutdown_timeout=None,
            start_serving=True):
        """Create a TCP server.
    
        The host parameter can be a string, in that case the TCP server is
        bound to host and port.
    
        The host parameter can also be a sequence of strings and in that case
        the TCP server is bound to all hosts of the sequence. If a host
        appears multiple times (possibly indirectly e.g. when hostnames
        resolve to the same IP address), the server is only bound once to that
        host.
    
        Return a Server object which can be used to stop the service.
    
        This method is a coroutine.
        """
        if isinstance(ssl, bool):
            raise TypeError('ssl argument must be an SSLContext or None')
    
        if ssl_handshake_timeout is not None and ssl is None:
            raise ValueError(
                'ssl_handshake_timeout is only meaningful with ssl')
    
        if ssl_shutdown_timeout is not None and ssl is None:
            raise ValueError(
                'ssl_shutdown_timeout is only meaningful with ssl')
    
        if sock is not None:
            _check_ssl_socket(sock)
    
        if host is not None or port is not None:
            if sock is not None:
                raise ValueError(
                    'host/port and sock can not be specified at the same time')
    
            if reuse_address is None:
                reuse_address = os.name == "posix" and sys.platform != "cygwin"
            sockets = []
            if host == '':
                hosts = [None]
            elif (isinstance(host, str) or
                  not isinstance(host, collections.abc.Iterable)):
                hosts = [host]
            else:
                hosts = host
    
            fs = [self._create_server_getaddrinfo(host, port, family=family,
                                                  flags=flags)
                  for host in hosts]
            infos = await tasks.gather(*fs)
            infos = set(itertools.chain.from_iterable(infos))
    
            completed = False
            try:
                for res in infos:
                    af, socktype, proto, canonname, sa = res
                    try:
                        sock = socket.socket(af, socktype, proto)
                    except socket.error:
                        # Assume it's a bad family/type/protocol combination.
                        if self._debug:
                            logger.warning('create_server() failed to create '
                                           'socket.socket(%r, %r, %r)',
                                           af, socktype, proto, exc_info=True)
                        continue
                    sockets.append(sock)
                    if reuse_address:
                        sock.setsockopt(
                            socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
                    # Since Linux 6.12.9, SO_REUSEPORT is not allowed
                    # on other address families than AF_INET/AF_INET6.
                    if reuse_port and af in (socket.AF_INET, socket.AF_INET6):
                        _set_reuseport(sock)
                    # Disable IPv4/IPv6 dual stack support (enabled by
                    # default on Linux) which makes a single socket
                    # listen on both address families.
                    if (_HAS_IPv6 and
                            af == socket.AF_INET6 and
                            hasattr(socket, 'IPPROTO_IPV6')):
                        sock.setsockopt(socket.IPPROTO_IPV6,
                                        socket.IPV6_V6ONLY,
                                        True)
                    try:
                        sock.bind(sa)
                    except OSError as err:
                        msg = ('error while attempting '
                               'to bind on address %r: %s'
                               % (sa, str(err).lower()))
                        if err.errno == errno.EADDRNOTAVAIL:
                            # Assume the family is not enabled (bpo-30945)
                            sockets.pop()
                            sock.close()
                            if self._debug:
                                logger.warning(msg)
                            continue
                        raise OSError(err.errno, msg) from None
    
                if not sockets:
>                   raise OSError('could not bind on any address out of %r'
                                  % ([info[4] for info in infos],))
E                                 OSError: could not bind on any address out of [('127.0.0.1', 0)]

/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py:1587: OSError

During handling of the above exception, another exception occurred:

self = <Coroutine test_qualifying_posts_land_once_in_state>

    def setup(self) -> None:
        runner_fixture_id = f"_{self._loop_scope}_scoped_runner"
        if runner_fixture_id not in self.fixturenames:
            self.fixturenames.append(runner_fixture_id)
        # When loop factories are configured, resolve the loop factory
        # fixture early so that a factory variant change cascades cache
        # invalidation before any async fixture checks its cache.
        hook_caller = self.config.hook.pytest_asyncio_loop_factories
        if hook_caller.get_hookimpls():
            _ = self._request.getfixturevalue(_asyncio_loop_factory.__name__)
>       return super().setup()
               ^^^^^^^^^^^^^^^

.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:559: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:945: in pytest_fixture_setup
    hook_result = yield
                  ^^^^^
.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:408: in _asyncgen_fixture_wrapper
    result = runner.run(setup(), context=context)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/runners.py:118: in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py:678: in run_until_complete
    self.run_forever()
/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py:645: in run_forever
    self._run_once()
/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py:1999: in _run_once
    handle._run()
/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/events.py:88: in _run
    self._context.run(self._callback, *self._args)
.venv/lib/python3.12/site-packages/uvicorn/server.py:70: in serve
    await self._serve(sockets)
.venv/lib/python3.12/site-packages/uvicorn/server.py:85: in _serve
    await self.startup(sockets=sockets)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <uvicorn.server.Server object at 0x77e92ce40530>, sockets = None

    async def startup(self, sockets: list[socket.socket] | None = None) -> None:
        await self.lifespan.startup()
        if self.lifespan.should_exit:
            self.should_exit = True
            return
    
        config = self.config
    
        def create_protocol(
            _loop: asyncio.AbstractEventLoop | None = None,
        ) -> asyncio.Protocol:
            return config.http_protocol_class(  # type: ignore[call-arg]
                config=config,
                server_state=self.server_state,
                app_state=self.lifespan.state,
                _loop=_loop,
            )
    
        loop = asyncio.get_running_loop()
    
        listeners: Sequence[socket.SocketType]
        if sockets is not None:  # pragma: full coverage
            # Explicitly passed a list of open sockets.
            # We use this when the server is run from a Gunicorn worker.
    
            def _share_socket(
                sock: socket.SocketType,
            ) -> socket.SocketType:  # pragma py-linux pragma: py-darwin
                # Windows requires the socket be explicitly shared across
                # multiple workers (processes).
                from socket import fromshare  # type: ignore[attr-defined]
    
                sock_data = sock.share(os.getpid())  # type: ignore[attr-defined]
                return fromshare(sock_data)
    
            self.servers: list[asyncio.base_events.Server] = []
            for sock in sockets:
                is_windows = platform.system() == "Windows"
                if config.workers > 1 and is_windows:  # pragma: py-not-win32
                    sock = _share_socket(sock)  # type: ignore[assignment]
                server = await loop.create_server(create_protocol, sock=sock, ssl=config.ssl, backlog=config.backlog)
                self.servers.append(server)
            listeners = sockets
    
        elif config.fd is not None:  # pragma: py-win32
            # Use an existing socket, from a file descriptor.
            sock = socket.fromfd(config.fd, socket.AF_UNIX, socket.SOCK_STREAM)
            server = await loop.create_server(create_protocol, sock=sock, ssl=config.ssl, backlog=config.backlog)
            assert server.sockets is not None  # mypy
            listeners = server.sockets
            self.servers = [server]
    
        elif config.uds is not None:  # pragma: py-win32
            # Create a socket using UNIX domain socket.
            uds_perms = 0o666
            if os.path.exists(config.uds):
                uds_perms = os.stat(config.uds).st_mode  # pragma: full coverage
            server = await loop.create_unix_server(
                create_protocol, path=config.uds, ssl=config.ssl, backlog=config.backlog
            )
            os.chmod(config.uds, uds_perms)
            assert server.sockets is not None  # mypy
            listeners = server.sockets
            self.servers = [server]
    
        else:
            # Standard case. Create a socket from a host/port pair.
            try:
                server = await loop.create_server(
                    create_protocol,
                    host=config.host,
                    port=config.port,
                    ssl=config.ssl,
                    backlog=config.backlog,
                )
            except OSError as exc:
                logger.error(exc)
                await self.lifespan.shutdown()
>               sys.exit(1)
E               SystemExit: 1

.venv/lib/python3.12/site-packages/uvicorn/server.py:173: SystemExit
---------------------------- Captured stderr setup -----------------------------
ERROR:    could not bind on any address out of [('127.0.0.1', 0)]
=============================== warnings summary ===============================
tests/unit/test_listener.py::test_qualifying_posts_land_once_in_state
  /mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/websockets/legacy/__init__.py:6: DeprecationWarning: websockets.legacy is deprecated; see https://websockets.readthedocs.io/en/stable/howto/upgrade.html for upgrade instructions
    warnings.warn(  # deprecated in 14.0 - 2024-11-09

tests/unit/test_listener.py::test_qualifying_posts_land_once_in_state
  /mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/uvicorn/protocols/websockets/websockets_impl.py:17: DeprecationWarning: websockets.server.WebSocketServerProtocol is deprecated
    from websockets.server import WebSocketServerProtocol

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
ERROR tests/unit/test_listener.py::test_qualifying_posts_land_once_in_state
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!Task exception was never retrieved
future: <Task finished name='Task-2' coro=<Server.serve() done, defined at /mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/uvicorn/server.py:68> exception=SystemExit(1)>
Traceback (most recent call last):
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/uvicorn/server.py", line 163, in startup
    server = await loop.create_server(
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py", line 1587, in create_server
    raise OSError('could not bind on any address out of %r'
OSError: could not bind on any address out of [('127.0.0.1', 0)]

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/runner.py", line 361, in from_call
    result: TResult | None = func()
                             ^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/runner.py", line 250, in <lambda>
    lambda: runtest_hook(item=item, **kwds),
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_caller.py", line 197, in __call__
    return self._hookexec(
           ^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_manager.py", line 183, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 195, in _multicall
    raise exception
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 167, in _multicall
    teardown.throw(exception)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/logging.py", line 858, in pytest_runtest_setup
    yield
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 167, in _multicall
    teardown.throw(exception)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/capture.py", line 895, in pytest_runtest_setup
    return (yield)
            ^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 147, in _multicall
    res = hook_impl.function(*args)
          ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/runner.py", line 170, in pytest_runtest_setup
    item.session._setupstate.setup(item)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/runner.py", line 536, in setup
    col.setup()
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py", line 559, in setup
    return super().setup()
           ^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/python.py", line 1710, in setup
    self._request._fillfixtures()
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 806, in _fillfixtures
    item.funcargs[argname] = self.getfixturevalue(argname)
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 630, in getfixturevalue
    fixturedef = self._get_active_fixturedef(argname)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 726, in _get_active_fixturedef
    fixturedef.execute(request=subrequest)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 1181, in execute
    fixturedef = request._get_active_fixturedef(argname)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 726, in _get_active_fixturedef
    fixturedef.execute(request=subrequest)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 1232, in execute
    result: FixtureValue = ihook.pytest_fixture_setup(
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_caller.py", line 197, in __call__
    return self._hookexec(
           ^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_manager.py", line 183, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 195, in _multicall
    raise exception
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 167, in _multicall
    teardown.throw(exception)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py", line 945, in pytest_fixture_setup
    hook_result = yield
                  ^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 167, in _multicall
    teardown.throw(exception)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 64, in run_old_style_hookwrapper
    return result.get_result()
           ^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_result.py", line 103, in get_result
    raise exc.with_traceback(tb)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 49, in run_old_style_hookwrapper
    res = yield
          ^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 167, in _multicall
    teardown.throw(exception)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/setuponly.py", line 36, in pytest_fixture_setup
    return (yield)
            ^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pluggy/_execution.py", line 147, in _multicall
    res = hook_impl.function(*args)
          ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 1328, in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/_pytest/fixtures.py", line 1005, in call_fixture_func
    fixture_result = fixturefunc(**kwargs)
                     ^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py", line 408, in _asyncgen_fixture_wrapper
    result = runner.run(setup(), context=context)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py", line 678, in run_until_complete
    self.run_forever()
  File "/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py", line 645, in run_forever
    self._run_once()
  File "/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py", line 1999, in _run_once
    handle._run()
  File "/home/rob/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/events.py", line 88, in _run
    self._context.run(self._callback, *self._args)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/uvicorn/server.py", line 85, in _serve
    await self.startup(sockets=sockets)
  File "/mnt/d/rob/projects/mmbridge/.venv/lib/python3.12/site-packages/uvicorn/server.py", line 173, in startup
    sys.exit(1)
SystemExit: 1

1 passed, 2 warnings, 1 error in 1.94s

codex
No actionable defects were identified. The changes consistently remove the allow-list while preserving legacy store loading and existing wake filters. Specification locks and repository checks pass; full test validation was limited by local server startup failures.
No actionable defects were identified. The changes consistently remove the allow-list while preserving legacy store loading and existing wake filters. Specification locks and repository checks pass; full test validation was limited by local server startup failures.
````
