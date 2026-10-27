---
id: REVIEW-20261027-slice-20261027-lb3-listener-filters-review
type: review-findings
phase: verify
status: addressed
owner_agent: eng-run
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md, thoughts/shared/slices/2026-10-27-lb3-listener-filters.md]
review_kind: slice
subject: "SLICE-20261027-lb3-listener-filters (thoughts/shared/slices/2026-10-27-lb3-listener-filters.md)"
diff: 8bd8d68...c170d0d
reviewer: codex
command: "codex review --base 8bd8d68"
run_log: thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb3-listener-filters.md
---
# Independent review: code-review slice-20261027-lb3-listener-filters
<!-- Written by eng-run (prompt code-review v2). Each finding row starts 'open': set disposition fixed (where) |
     accepted-risk (ONLY with Rob's approval, e.g. "Rob 2026-10-27") | rejected (reason). Plan reviews gate
     implementation (medium/large); slice reviews are advisory. -->

## Findings
| # | Severity | Location | Finding | Disposition | Reason / approval |
|---|---|---|---|---|---|

No findings.

Implementer note (claude-code 2026-10-27): Codex's validation was partial - its sandbox could not bind a localhost port, so the 13 websocket tests in tests/unit/test_listener.py errored at uvicorn startup there (environment, not code). They pass locally: `.venv/bin/pytest tests/unit -q` 176 passed, 3 consecutive runs. The verifier should re-run them outside a socket-restricted sandbox.

## Reviewer raw output
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
session id: 01a17c3e-6fb7-7282-831f-7e8474ed9e96
--------
user
changes against '8bd8d68'
exec
/bin/bash -lc 'cat PROJECT_STATE.md; git status --short; python3 .eng/bin/eng-check .; git diff --stat 8bd8d680a83f56b0972a8fcb7d26f722937c42bb' in /mnt/d/rob/projects/mmbridge
 succeeded in 2205ms:
---
id: STATE
type: project-state
phase: implement
status: active
owner_agent: claude-code
date: 2026-10-27
links: []
triage: large             # unset | small | medium | large
active_slice: SLICE-20261027-lb3-listener-filters
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
[SLICE-20261027-lb3-listener-filters](thoughts/shared/slices/2026-10-27-lb3-listener-filters.md) (todo). Previous: lb2 [done](thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md)

## Next action
lb2 done (CP-S logged; empty-DB admin check deferred). NEXT: implementer runs eng-run implement on lb3 (SLICE-20261027-lb3-listener-filters), then planner runs eng-verify. Deploy prerequisites before enabling: Coolify volume /data (uid 10001), env MMB_STORE_KEY, replicas 1.

## Blockers
none

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
- Latest handoff: [thoughts/shared/handoffs/2026-10-27_02-07-31_lb2-implemented-awaiting-verify.md](thoughts/shared/handoffs/2026-10-27_02-07-31_lb2-implemented-awaiting-verify.md)
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
 M thoughts/shared/slices/2026-10-27-lb3-listener-filters.md
?? thoughts/shared/inbox-local-bak-1793080755/
?? thoughts/shared/inbox.md
?? thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb3-listener-filters.running.md
?? thoughts/shared/runs/2026-10-27-implement-slice-20261027-lb3-listener-filters.running.md
eng-check: OK - 0 error(s), 0 warning(s), 81 artifact(s) checked
 app/listener.py                                    | 152 +++++++++++++++
 app/live_filter.py                                 |  75 ++++++++
 app/ws_spike.py                                    |  71 +++++++
 requirements.txt                                   |   1 +
 tests/acceptance/drivers/fake_mattermost.py        | 150 ++++++++++++++-
 tests/unit/test_listener.py                        | 212 +++++++++++++++++++++
 tests/unit/test_live_filter.py                     |  93 +++++++++
 .../slices/2026-10-27-lb3-listener-filters.md      |   2 +-
 8 files changed, 750 insertions(+), 6 deletions(-)

exec
/bin/bash -lc 'cat thoughts/shared/handoffs/2026-10-27_02-07-31_lb2-implemented-awaiting-verify.md .eng/PROCESS.md .claude/skills/eng-review/SKILL.md; find . -name AGENTS.md -o -name AGENTS.override.md; git diff 8bd8d680a83f56b0972a8fcb7d26f722937c42bb -- app requirements.txt' in /mnt/d/rob/projects/mmbridge
 succeeded in 1103ms:
---
id: HANDO-20261027-lb2-implemented-awaiting-verify
type: handoff
phase: implement
status: complete
owner_agent: claude-code
date: 2026-10-27T02:07:31-05:00
links: [thoughts/shared/plans/2026-10-27-live-bots.md, thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md]
git_commit: dc9efe0
branch: main
next_skill: eng-verify
---
# Handoff: lb2 implemented, awaiting verify
<!-- Session handoff (agent to agent, one session). A standing orientation for a new implementer is a project brief: .eng/bin/eng-new brief. -->

## Task(s)
- SLICE-20261027-lb2-state-db-wake-queue (plan Phase 2): **completed, status review**. Test-first; all Phase 2 automated verification exit 0. Manual verification (CP-S) pending Rob.

## Critical References
- thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md (progress log, deviations)
- thoughts/shared/plans/2026-10-27-live-bots.md Phase 2
- docs/decisions/0009-listener-state-persistence.md

## Recent changes
- app/state.py:26 schema (wakes with status `queued|retry|in_flight|delivered|failed`, claimed_by, lease_until, post_create_at, delivered_at; cursors `(last_create_at, last_post_id)`; meta), :54 `next_delay`, :95 `State.__init__` (WAL, write probe -> `StateError('state_unwritable')`), :115 `_tx` (BEGIN IMMEDIATE under a lock), :133 `_advance` forward-only row-value compare, :145 `enqueue_and_advance`, :173 `claim_owner` (dispatcher heartbeat), :187 `claim_due` (UPDATE ... RETURNING, attempts+1 at claim), :202-224 claimer-checked `mark_*`, :226 `recover_stale`, :233 `requeue`, :240 `prune` terminal-only, :262 `stats`
- app/admin.py:121 `failed [--retry]`, :138 `stats`; StateError handled in `main`
- tests/unit/test_state.py (20 tests), tests/unit/test_admin.py (+4 tests); commits 6551dd9, dc9efe0

## Learnings
- Plan signature block vs PR-3/PR-1 text disagree (cursor int vs `(create_at, post_id)`; statuses vs architecture CHECK). Followed the later PR text; recorded as deviations in the slice card.
- `attempts` increments at claim, so a `Wake` from `claim_due` carries the attempt number for the lb4 payload `attempt` field; `mark_retry` returns 'failed' once attempts >= `max_attempts`.
- `mark_failed` is claimer-checked: lb4's `bot_rotated` (failing unclaimed queued rows) needs a separate method.
- `codex` is not on the non-login PATH from Claude Code (lives in ~/.nvm/versions/node/*/bin); logged in process-feedback.
- eng-run's review parser missed Codex's `[P2]` finding ("No findings"); transcribed by hand.

## Artifacts
- app/state.py, app/admin.py, CHANGELOG.md (Unreleased Added)
- tests/unit/test_state.py, tests/unit/test_admin.py
- thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md, thoughts/shared/plans/2026-10-27-live-bots.md (Phase 2 automated boxes ticked)
- thoughts/shared/verification/2026-10-27-slice-20261027-lb2-state-db-wake-queue-review.md (1 finding, fixed; addressed)
- thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb2-state-db-wake-queue.md
- thoughts/shared/process-feedback.md (codex PATH entry)

## Approvals
- Pending (planner to request): `CP-S: thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md - manual verification` (`python -m app.admin failed` and `stats` on an empty DB print "no failed wakes" / "no wakes yet").
- None granted this session.

## Action Items & Next Steps
1. Planner: eng-verify on lb2 (re-run Phase 2 automated checks; review the deviations in the slice card).
2. Request CP-S from Rob with the manual step. Do not start lb3 before CP-S.
3. Not pushed (push_permission standing applies only after eng-verify PASS).

## Other Notes
- Untracked files left as found: thoughts/shared/inbox.md, thoughts/shared/inbox-local-bak-1793080755/, the eng-run `.running.md` marker.
<!-- Copy of eng-process kit v2.5.6 PROCESS.md, vendored by eng-init. Do not edit here. -->
# Engineering Process (canonical, kit v2.1)

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
`docs/definition-of-done.md` (project may extend, never weaken). Core: criteria re-executed in the verifying session; tests incl. regression; no weakened gates; docs, CHANGELOG, ADRs, TODOS updated; verification PASS; state + handoff written.

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
- If the next agent must ask "what was I doing?", the handoff is defective. Log it in `process-feedback.md`.
- Session handoff and **project brief** are different: the handoff passes one session to the next; a brief (`.eng/bin/eng-new brief`) orients a new implementer or reviewer and points at the plan and state.

## 9. Rules for every agent
Recommend; Rob decides. Never weaken a gate or use `--no-verify`. A report is a claim until re-executed. Stop and report on plan/code mismatch ("Issue in Phase N") instead of improvising. No fix without root cause; after 3 failed fixes, stop and hand off. Log process friction in `thoughts/shared/process-feedback.md` as you hit it.

## 10. Working agreements (standard; values in PROJECT_STATE front matter)
| Field | Default | Meaning |
|---|---|---|
| `implementer` | `claude-code` | Who writes code: Claude Code on the owner's own PC. Never name it in design docs; reference this field. |
| `planner` | `grok-bot` | Grok Bot assistants plan, write docs, keep state and process. They don't write production code. |
| `cross_review` | `codex-advisory` | Independent cross-model review; advisory, never a gate. `none` disables. |
| `push_permission` | `ask` | `ask` = ask the owner before each push; `standing` = may push the slice branch without asking (never merge). |
| `board` | `none` | Optional Kanban (e.g. self-hosted Vikunja, deferred). If used: board only, one card per slice linking to the repo plan/slice card. The repo stays the single source of truth; never record decisions on the board. |

**Implementer hand-off loop.**
1. When a slice is ready (plan approved with its mandatory plan review clean (M/L), slice is next in PROJECT_STATE `active_slice` with `status: todo`, `pending_approvals` empty, `.eng/bin/eng-check` OK), the planner **starts** implementation on the owner's PC: `python3 .eng/bin/eng-run implement <plan> <slice-id>` (or `eng run implement ...` with the global CLI), then tells Rob once, as FYI, with the standard message from `.eng/templates/ready-to-implement.md` (`.eng/bin/eng-status` prints it filled). Bots run eng-run on Rob's PC only with Rob's approval; his CP-C / slice-ready approval covers starting implement unless he said otherwise (if PROJECT_STATE has no standing note, a one-line "start implement?" is enough). **Fallback:** if eng-run or the Claude CLI is unavailable, or Rob wants to drive Claude interactively, send the paste prompt from the same message: `Run eng-resume, then eng-implement-slice for <slice> per <plan>`. Work keeps running until Rob interjects or a real decision is due: CP-S, a push when `push_permission: ask`, eng-check failures, locked-spec issues, open critical/high plan-review findings, blockers. **Completion signal:** whoever starts `eng-run implement` owns its completion. Stay on the run (or resume when the process exits), then read the new run log in `thoughts/shared/runs/` plus the latest handoff / PROJECT_STATE, and either continue (eng-verify, request CP-S) or surface the blocker to Rob. No fire-and-forget: Rob should never have to paste the handoff filename back. If the starter cannot stay attached, configure the opt-in `[hooks] implement_on_complete` in `.eng/runners.toml` (e.g. curl a planner routine webhook) so the planner is woken on every exit, ok or failed. Same rule for headless plan-review / code-review runs; see "Wake pair + PID harness" below.
2. The implementer runs the slice on the owner's PC, ends with eng-handoff.
3. **Independent review (advisory):** before eng-verify, the cross-model review runs on the slice diff. Findings go to `thoughts/shared/verification/<date>-<slice>-review.md` (`.eng/bin/eng-new review <slug>`). The implementer fixes or answers each finding, then eng-verify runs.
4. The planner picks up the implementer's handoff and runs `eng-verify` and `.eng/bin/eng-check`, then requests CP-S.

**Mandatory plan review (medium and large; small exempt).** After the plan and slice cards are drafted and before CP-C, Codex reviews them non-interactively from the repo root on the owner's machine:
`codex exec "review <plan path> and the slice cards <slice glob> against <design doc> (REQ ids), <architecture doc> and <ADR range> for gaps, wrong ordering, missing tests, and security holes; output a numbered list of findings with severity" -o thoughts/shared/verification/<date>-<slug>-plan-review.md`
`.eng/bin/eng-status` prints this command with the real paths while CP-C is pending. **Codex output always goes straight to a file in the repo, never only the terminal:** `-o`/`--output-last-message <path>` writes the final review to the review file. Then turn that file into the findings artifact in place: add the review-findings front matter and Findings table (from `templates/review-findings.md`) above the raw output, which stays under "Reviewer raw output". Link it it from the plan's `plan_review:` field. Each finding gets a severity (critical/high/medium/low) and a disposition: `fixed` (where), `accepted-risk` (only with Rob's approval, recorded in the row), or `rejected` (with a reason). `.eng/bin/eng-check` fails, for medium/large triage, if a slice is in-progress or the phase is implement/verify/ship without a linked plan review, or with any critical/high finding still `open`. **Grandfathered plans** (approved before the review was mandatory): before the next slice starts, either run the review retroactively (same command, link it in `plan_review:`, fix/disposition findings), or record Rob's waiver in the Approval log: `| <date> | CP-C | <plan path> | waiver: plan review - approved by Rob |`. eng-check's error names both routes. This is the one review that is a gate; slice-diff and architecture reviews stay advisory.

**Cross-model review (Codex), advisory.** Run it on every slice diff before Rob approves the slice (always for auth, tenancy or security work), and on architecture docs for large work (plans: see the mandatory review above). Skip it for small or docs-only changes (write "skipped: <reason>" in the verification report). In Claude Code, gstack's `/codex` calls the real Codex CLI (diffs: `codex review --base <base> > thoughts/shared/verification/<date>-<slice-slug>-review.md`; documents: `codex exec "<prompt>" -o thoughts/shared/verification/<date>-<slug>-review.md`; always written into the repo). That needs `npm install -g @openai/codex` and `codex login` once on the owner's PC. Findings are recorded in the findings file and summarized in the verification report's "Cross-model review" section. They are advice: Rob decides, and no finding blocks by itself.

**Windows owner machines.**
- Line endings: set per command, not globally: `git -c core.autocrlf=false <cmd>` (or `input`). Kit files are LF.
- Encoding: write files as UTF-8 **without BOM** (PowerShell 5: `Out-File -Encoding utf8` adds a BOM; use `[IO.File]::WriteAllText` or PowerShell 7 `utf8NoBOM`). The scripts tolerate a BOM and print ASCII only.
- Archiving a repo to move it: include dotfiles and `.git` (`tar -czf repo.tgz -C <parent> <repo>`; Explorer's "Send to zip" can skip them).

**Headless agent runs (`eng-run`, v2.3).** From the repo root: `python3 .eng/bin/eng-run plan-review <plan>`, `... implement <plan> <slice-id>`, `... code-review <slice-id | --base REF>`. Prompts are `.eng/prompts/<role>.md` (kit-owned); the runner per role is `.eng/runners.toml` (project-owned, created once; defaults implement=claude, plan-review/code-review=codex), overridable by `ENG_RUNNER_<ROLE>` or `--runner` (`claude`, `codex`, or a `[runners.<name>]` `command` runner). Rules: every run writes a run log `thoughts/shared/runs/<date>-<role>-<target>.md` (command, prompt, output, exit code); every review also writes a review-findings file in `thoughts/shared/verification/` with rows `open` until dispositioned; review output never lives only in the terminal. Plan reviews set an empty `plan_review:` so eng-check's gate applies. eng-run refuses a review by the same runner that implemented the slice (run log, else PROJECT_STATE `implementer`) unless `--allow-self-review`, which must be named in the verification report. `--dry-run` prints the exact command without running. Bots (Chet, Dave) may run eng-run on Rob's PC only with Rob's approval for that run.

**Wake pair + PID harness (every autonomous eng-run role, v2.5.4).** Applies to `plan-review`, `implement` and `code-review` alike; the starter still owns completion and fire-and-forget stays forbidden. Set up both halves when you start a run you will not watch:
- (A) **Callback:** opt-in `[hooks]` in `.eng/runners.toml`. Role-specific `implement_on_complete` / `plan_review_on_complete` / `code_review_on_complete` wins; else the general `on_complete` fires for any role. Runs on every exit (ok or failed) after the run log is written; env `ENG_ROLE ENG_EXIT_CODE ENG_STATUS ENG_RUN_LOG ENG_REPO ENG_PLAN ENG_SLICE ENG_HANDOFF ENG_PID ENG_ENG_RUN_PID`.
- (B) **Effort-based timeout routine** as backup. Starting points by effort: S 45m, M 2h, L 4h (reviews are usually S, implement M or L).
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
diff --git a/app/listener.py b/app/listener.py
new file mode 100644
index 0000000..4f98dac
--- /dev/null
+++ b/app/listener.py
@@ -0,0 +1,152 @@
+"""Mattermost websocket listener for the ONE live bot (ADR-0007).
+
+run(): GET /users/me -> WS /api/v4/websocket with `Authorization: Bearer` -> hello{connection_id} -> for each
+`posted` event, live_filter.decide -> wake payload (ADR-0008 schema, no token; channel/team/sender lookups
+cached) -> state.enqueue_and_advance (dedupe gate + forward-only cursor, PR-3). Tracks seq (gaps logged as
+ws_seq_gap); sends the Mattermost `ping` action every PING_S and treats IDLE_S without any frame as dead.
+One connection per run(): reconnect, resume and catch-up are slice 5. Never joins channels or posts.
+"""
+import asyncio
+import itertools
+import json
+import logging
+import time
+from datetime import datetime, timezone
+
+import websockets
+from websockets.exceptions import ConnectionClosed
+
+from app import logging as mlog
+from app.live_filter import WakeIntent, decide
+from app.mattermost import MATTERMOST_URL, MMError
+
+PING_S = 30
+IDLE_S = 60
+
+# websockets logs handshake headers (incl. Authorization) and frames at DEBUG: own logger, redacted, INFO.
+_ws_log = logging.getLogger("mmbridge.ws")
+_ws_log.setLevel(logging.INFO)
+_ws_log.addFilter(mlog.RedactFilter())
+
+
+def ws_url(base_url: str) -> str:
+    base = base_url.rstrip("/")
+    return ("wss://" + base[8:] if base.startswith("https://") else "ws://" + base.removeprefix("http://")) \
+        + "/api/v4/websocket"
+
+
+def connect(url: str, headers: dict):
+    """Default ws_connect: protocol-level keepalive off (the listener pings at application level)."""
+    return websockets.connect(url, additional_headers=headers, ping_interval=None, open_timeout=10, logger=_ws_log)
+
+
+def _log(event: str, **fields) -> None:
+    mlog.log.info(json.dumps({"event": event, **fields}))
+
+
+def _iso(ms: int) -> str:
+    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
+
+
+class Listener:
+    def __init__(self, cfg, state, client_factory, ws_connect=connect, clock=time.time,
+                 base_url: str = MATTERMOST_URL, ping_s: float = PING_S, idle_s: float = IDLE_S):
+        self.cfg, self.state, self.client_factory, self.ws_connect = cfg, state, client_factory, ws_connect
+        self.clock, self.base_url, self.ping_s, self.idle_s = clock, base_url, ping_s, idle_s
+        self.status = "off"                   # off | connecting | ok
+        self.bot_user_id = self.connection_id = self.last_seq = None
+        self._bot: dict = {}
+        self._channels: dict = {}
+        self._teams: dict = {}
+        self._users: dict = {}
+
+    async def run(self) -> None:
+        mlog.register_secret(self.cfg.token)
+        client = self.client_factory(self.cfg.token)
+        self.status = "connecting"
+        try:
+            me = await client.get("/users/me")
+            self.bot_user_id, self._bot = me["id"], {"user_id": me["id"], "username": me["username"]}
+            async with self.ws_connect(ws_url(self.base_url), {"Authorization": "Bearer " + self.cfg.token}) as ws:
+                pinger = asyncio.create_task(self._ping(ws))
+                try:
+                    await self._read(ws, client)
+                finally:
+                    pinger.cancel()
+        finally:
+            self.status = "off"
+
+    async def _read(self, ws, client) -> None:
+        while True:
+            try:
+                raw = await asyncio.wait_for(ws.recv(), self.idle_s)
+            except TimeoutError:
+                _log("ws_idle", seconds=self.idle_s)
+                return
+            except ConnectionClosed:
+                _log("ws_closed", connection_id=self.connection_id)
+                return
+            try:
+                ev = json.loads(raw)
+            except ValueError:
+                mlog.log.warning(json.dumps({"event": "event_invalid", "reason": "json"}))
+                continue
+            if not isinstance(ev, dict) or "event" not in ev:
+                continue                      # ping replies ({"status","seq_reply"}) and other non-events
+            self._track_seq(ev)
+            if ev["event"] == "hello":
+                self.connection_id = (ev.get("data") or {}).get("connection_id")
+                await asyncio.to_thread(self.state.set_meta, "ws_connection_id", self.connection_id or "")
+                self.status = "ok"
+                _log("ws_connected", connection_id=self.connection_id,
+                     server_version=(ev.get("data") or {}).get("server_version"))
+                continue
+            intent = decide(ev, self.bot_user_id, set(self.cfg.channels))
+            if intent:
+                payload = await self._payload(intent, client)
+                new = await asyncio.to_thread(self.state.enqueue_and_advance, intent.post_id, intent.channel_id,
+                                              payload, intent.create_at)
+                _log("wake_queued", post_id=intent.post_id, channel_id=intent.channel_id, new=new)
+
+    def _track_seq(self, ev: dict) -> None:
+        seq = ev.get("seq")
+        if not isinstance(seq, int):
+            return
+        if ev["event"] != "hello" and self.last_seq is not None and seq != self.last_seq + 1:
+            _log("ws_seq_gap", expected=self.last_seq + 1, got=seq)
+        self.last_seq = seq
+
+    async def _ping(self, ws) -> None:
+        for n in itertools.count(1):
+            await asyncio.sleep(self.ping_s)
+            try:
+                await ws.send(json.dumps({"action": "ping", "seq": n}))
+            except ConnectionClosed:
+                return
+
+    async def _get(self, client, cache: dict, key: str, path: str) -> dict | None:
+        """Cached REST lookup; None (not cached) on Mattermost errors so the event hints are used instead."""
+        if key not in cache:
+            try:
+                cache[key] = await client.get(path)
+            except MMError as e:
+                _log("lookup_failed", path=path.split("/")[1], code=e.code)
+                return None
+        return cache[key]
+
+    async def _payload(self, w: WakeIntent, client) -> dict:
+        h = w.hints
+        ch = await self._get(client, self._channels, w.channel_id, "/channels/" + w.channel_id) or {}
+        team_id = ch.get("team_id", h.get("team_id")) or ""
+        team = await self._get(client, self._teams, team_id, "/teams/" + team_id) if team_id else None
+        user = await self._get(client, self._users, w.user_id, "/users/" + w.user_id) or {}
+        return {
+            "version": 1, "kind": "post", "delivery_id": w.post_id, "attempt": 1,
+            "bot": dict(self._bot),
+            "channel": {"id": w.channel_id, "name": ch.get("name", h.get("channel_name")),
+                        "display_name": ch.get("display_name", h.get("channel_display_name")),
+                        "type": w.channel_type, "team": (team or {}).get("name")},
+            "sender": {"user_id": w.user_id,
+                       "username": user.get("username") or (h.get("sender_name") or "").lstrip("@") or None},
+            "post": {"id": w.post_id, "message": w.message, "create_at": _iso(w.create_at), "root_id": w.root_id},
+        }
diff --git a/app/live_filter.py b/app/live_filter.py
new file mode 100644
index 0000000..c662aee
--- /dev/null
+++ b/app/live_filter.py
@@ -0,0 +1,75 @@
+"""Which Mattermost websocket events wake the live bot (architecture Filter rules, REQ-A1/A2/A3).
+
+Pure apart from the `event_invalid` log line: no I/O, no state. Drop own posts (A3), system posts (type set),
+group DMs (G) and open/private channels not chosen (A1); wake on DMs (D, A2) and chosen channels. Thread
+replies are new posts and wake, carrying root_id. Malformed `posted` events drop and log `event_invalid`
+(reason only; never the message text).
+"""
+import json
+from dataclasses import dataclass
+
+from app import logging as mlog
+
+
+@dataclass(frozen=True)
+class WakeIntent:
+    post_id: str
+    channel_id: str
+    channel_type: str        # O | P | D
+    user_id: str
+    message: str
+    create_at: int           # Mattermost ms
+    root_id: str | None
+    hints: dict              # event fields (channel_name, channel_display_name, sender_name, team_id) for fallbacks
+
+
+def _invalid(reason: str) -> None:
+    mlog.log.warning(json.dumps({"event": "event_invalid", "reason": reason}))
+
+
+def _post(data: dict) -> dict | None:
+    post = data.get("post")
+    if isinstance(post, str):
+        try:
+            post = json.loads(post)
+        except ValueError:
+            return None
+    return post if isinstance(post, dict) else None
+
+
+def decide(event: dict, bot_user_id: str, chosen: set[str]) -> WakeIntent | None:
+    if not isinstance(event, dict):
+        _invalid("not_object")
+        return None
+    if event.get("event") != "posted":
+        return None
+    data = event.get("data")
+    if not isinstance(data, dict):
+        _invalid("data")
+        return None
+    post = _post(data)
+    if post is None:
+        _invalid("post")
+        return None
+    for f in ("id", "channel_id", "user_id"):
+        if not isinstance(post.get(f), str) or not post[f]:
+            _invalid(f)
+            return None
+    create_at, message, ctype = post.get("create_at"), post.get("message", ""), data.get("channel_type")
+    if not isinstance(create_at, int) or isinstance(create_at, bool):
+        _invalid("create_at")
+        return None
+    if not isinstance(message, str):
+        _invalid("message")
+        return None
+    if ctype not in ("O", "P", "D", "G"):
+        _invalid("channel_type")
+        return None
+
+    if post["user_id"] == bot_user_id or post.get("type") or ctype == "G":
+        return None
+    if ctype in ("O", "P") and post["channel_id"] not in chosen:
+        return None
+    hints = {k: data.get(k) for k in ("channel_name", "channel_display_name", "sender_name", "team_id")}
+    return WakeIntent(post["id"], post["channel_id"], ctype, post["user_id"], message, create_at,
+                      post.get("root_id") or None, hints)
diff --git a/app/ws_spike.py b/app/ws_spike.py
new file mode 100644
index 0000000..0c01fe8
--- /dev/null
+++ b/app/ws_spike.py
@@ -0,0 +1,71 @@
+"""OQ1 spike (slice lb3 manual check): print the shape of Mattermost's websocket hello, ping reply and first
+`posted` event, to confirm the listener's contract against the real server version.
+
+    echo "$TOKEN" | python -m app.ws_spike [--timeout 120]
+
+Token from stdin only, never printed. Output is key -> type shapes plus seq/channel_type/connection_id;
+message text is not printed.
+"""
+import argparse
+import asyncio
+import json
+import sys
+
+from app import logging as mlog
+from app.listener import connect, ws_url
+from app.mattermost import MATTERMOST_URL
+
+
+def shape(v):
+    if isinstance(v, dict):
+        return {k: shape(x) for k, x in sorted(v.items())}
+    return type(v).__name__
+
+
+async def spike(token: str, base_url: str, timeout: float, out=print, ws_connect=connect) -> int:
+    async with ws_connect(ws_url(base_url), {"Authorization": "Bearer " + token}) as ws:
+        hello = json.loads(await asyncio.wait_for(ws.recv(), 10))
+        out("hello: event=%s seq=%s connection_id=%s server_version=%s" % (
+            hello.get("event"), hello.get("seq"), bool((hello.get("data") or {}).get("connection_id")),
+            (hello.get("data") or {}).get("server_version")))
+        out("hello shape: " + json.dumps(shape(hello)))
+        await ws.send(json.dumps({"action": "ping", "seq": 1}))
+        out("waiting up to %ds for a post in any channel the bot is in ..." % timeout)
+        loop = asyncio.get_running_loop()
+        deadline = loop.time() + timeout
+        while (left := deadline - loop.time()) > 0:
+            try:
+                ev = json.loads(await asyncio.wait_for(ws.recv(), left))
+            except TimeoutError:
+                break
+            if "seq_reply" in ev:
+                out("ping reply shape: " + json.dumps(shape(ev)))
+            elif ev.get("event") == "posted":
+                data = dict(ev["data"])
+                post = json.loads(data["post"]) if isinstance(data.get("post"), str) else data.get("post")
+                data["post"] = "<json string>" if isinstance(ev["data"].get("post"), str) else "<object>"
+                out("posted: seq=%s channel_type=%s" % (ev.get("seq"), data.get("channel_type")))
+                out("posted shape: " + json.dumps(shape({**ev, "data": data})))
+                out("post shape: " + json.dumps(shape(post)))
+                return 0
+            else:
+                out("other event: %s seq=%s" % (ev.get("event"), ev.get("seq")))
+    out("no posted event within %ds" % timeout)
+    return 1
+
+
+def main(argv=None) -> int:
+    p = argparse.ArgumentParser(prog="python -m app.ws_spike")
+    p.add_argument("--timeout", type=float, default=120)
+    a = p.parse_args(argv)
+    token = sys.stdin.readline().strip()
+    if not token:
+        print("token required on stdin", file=sys.stderr)
+        return 2
+    mlog.setup()
+    mlog.register_secret(token)
+    return asyncio.run(spike(token, MATTERMOST_URL, a.timeout))
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/requirements.txt b/requirements.txt
index fec4b37..521ce83 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -2,4 +2,5 @@ fastapi==0.115.6
 uvicorn[standard]==0.34.0
 mcp==1.30.0
 httpx==0.28.1
+websockets==17.3
 cryptography==50.0.2

exec
/bin/bash -lc 'cat app/mattermost.py; cat tests/unit/test_listener.py; git diff 8bd8d680a83f56b0972a8fcb7d26f722937c42bb -- tests/acceptance/drivers/fake_mattermost.py; cat thoughts/shared/slices/2026-10-27-lb3-listener-filters.md; ls .claude/skills' in /mnt/d/rob/projects/mmbridge
 succeeded in 15ms:
"""Mattermost REST client (ADR-0002): one httpx client per call, using the caller's own token.

Reached only over the private stack network (MATTERMOST_URL, default http://mattermost:8065).
Retry policy: post() never retried; get() retried exactly once on httpx.ConnectError only.
"""
import os

import httpx

MATTERMOST_URL = os.getenv("MATTERMOST_URL", "http://mattermost:8065")
TIMEOUT_S = 10.0


class MMError(Exception):
    def __init__(self, code: str, status: int | None = None):
        super().__init__(code if status is None else "%s (HTTP %s)" % (code, status))
        self.code, self.status = code, status


class Client:
    def __init__(self, token: str, base_url: str = MATTERMOST_URL, transport: httpx.AsyncBaseTransport | None = None):
        self._token = token
        self._base = base_url.rstrip("/") + "/api/v4"
        self._transport = transport
        self.last_status: int | None = None

    def __repr__(self) -> str:  # never show the token
        return "Client(%s)" % self._base

    async def _send(self, method: str, path: str, **kw) -> httpx.Response:
        async with httpx.AsyncClient(transport=self._transport, timeout=TIMEOUT_S) as c:
            return await c.request(method, self._base + path, headers={"Authorization": "Bearer " + self._token}, **kw)

    async def get(self, path: str, **params) -> dict | list:
        try:
            try:
                r = await self._send("GET", path, params=params or None)
            except httpx.ConnectError:
                r = await self._send("GET", path, params=params or None)  # exactly one retry
        except (httpx.TransportError, httpx.TimeoutException):
            raise MMError("mattermost_unavailable") from None
        return self._result(r)

    async def post(self, path: str, json: dict | list) -> dict | list:
        try:
            r = await self._send("POST", path, json=json)
        except (httpx.TransportError, httpx.TimeoutException):
            raise MMError("mattermost_unavailable") from None
        return self._result(r)

    def _result(self, r: httpx.Response):
        self.last_status = r.status_code
        s = r.status_code
        if s < 400:
            return r.json()
        if s >= 500:
            raise MMError("mattermost_unavailable", s)
        if s == 401:
            raise MMError("unauthorized", s)
        if s == 404:
            raise MMError("not_found", s)
        raise MMError("mattermost_error", s)
"""Listener against the fake Mattermost REST + websocket (served by uvicorn on a free port): users/me,
Bearer handshake, hello/seq, ping/idle, posted -> filter -> state.db (enqueue_and_advance)."""
import asyncio
import json
import logging

import pytest

from app.listener import Listener, ws_url
from app.mattermost import Client
from app.state import State
from app.store import BotConfig
from drivers.fake_mattermost import FakeMattermost


@pytest.fixture
def world():
    m = FakeMattermost()
    bot = m.add_user("eddie", bot=True)
    rob = m.add_user("rob")
    m.add_team("main")
    chosen = m.add_channel("main", "town-square", ["eddie", "rob"])
    other = m.add_channel("main", "off-topic", ["eddie", "rob"])
    group = m.add_channel("main", "gdm", ["eddie", "rob"], ctype="G")
    dm = m.direct_channel(bot["id"], rob["id"])["id"]
    return m, {"bot": bot, "rob": rob, "chosen": chosen, "other": other, "group": group, "dm": dm}


@pytest.fixture
async def served(world):
    m, w = world
    async with m.serve() as base_url:
        yield m, w, base_url


def make(served, tmp_path, **kw):
    m, w, base = served
    cfg = BotConfig(token=w["bot"]["token"], wake_url="https://wake.example/hook", wake_secret="s" * 40,
                    channels=[w["chosen"]])
    state = State(str(tmp_path / "state.db"))
    lis = Listener(cfg, state, lambda tok: Client(tok, base_url=base), base_url=base, **kw)
    return lis, state


async def until(pred, timeout=5.0):
    for _ in range(int(timeout / 0.02)):
        if pred():
            return
        await asyncio.sleep(0.02)
    raise AssertionError("condition not met in %.1fs" % timeout)


@pytest.fixture
async def running(served, tmp_path):
    lis, state = make(served, tmp_path)
    task = asyncio.create_task(lis.run())
    await until(lambda: lis.status == "ok")
    yield served[0], served[1], lis, state
    served[0].ws_drop()
    await asyncio.wait_for(task, 5)


def test_ws_url():
    assert ws_url("http://mattermost:8065") == "ws://mattermost:8065/api/v4/websocket"
    assert ws_url("https://chat.example/") == "wss://chat.example/api/v4/websocket"


async def test_qualifying_posts_land_once_in_state(running):
    m, w, lis, state = running
    rob, bot = w["rob"]["id"], w["bot"]["id"]
    wake1 = m.add_post(w["chosen"], rob, "eddie is great")
    m.add_post(w["other"], rob, "not chosen")
    m.add_post(w["chosen"], bot, "my own post")
    m.add_post(w["chosen"], rob, "rob joined", type="system_join_channel")
    m.add_post(w["group"], rob, "group dm")
    wake2 = m.add_post(w["dm"], rob, "ping")
    reply = m.add_post(w["chosen"], rob, "a reply", root_id=wake1["id"])
    m.ws_resend_last()                      # duplicate delivery of the reply event: dedupe gate
    marker = m.add_post(w["dm"], rob, "marker")
    await until(lambda: state.wake(marker["id"]) is not None)
    assert [x.post_id for x in state.wakes()] == [wake1["id"], wake2["id"], reply["id"], marker["id"]]
    assert all(x.status == "queued" for x in state.wakes())
    assert state.get_cursor(w["chosen"]) == (reply["create_at"], reply["id"])
    assert state.get_cursor(w["dm"]) == (marker["create_at"], marker["id"])
    assert state.wake(reply["id"]).payload["post"]["root_id"] == wake1["id"]
    assert state.wake(wake1["id"]).post_create_at == wake1["create_at"]


async def test_payload_matches_wake_contract(running):
    m, w, lis, state = running
    p = m.add_post(w["chosen"], w["rob"]["id"], "eddie is great")
    d = m.add_post(w["dm"], w["rob"]["id"], "ping")
    await until(lambda: state.wake(d["id"]) is not None)
    assert state.wake(p["id"]).payload == {
        "version": 1, "kind": "post", "delivery_id": p["id"], "attempt": 1,
        "bot": {"user_id": w["bot"]["id"], "username": "eddie"},
        "channel": {"id": w["chosen"], "name": "town-square", "display_name": "Town-Square", "type": "O",
                    "team": "main"},
        "sender": {"user_id": w["rob"]["id"], "username": "rob"},
        "post": {"id": p["id"], "message": "eddie is great", "create_at": "2023-11-14T22:13:20Z", "root_id": None} }
    dm = state.wake(d["id"]).payload
    assert dm["channel"]["type"] == "D" and dm["channel"]["team"] is None and dm["sender"]["username"] == "rob"


async def test_lookups_are_cached(running):
    m, w, lis, state = running
    for i in range(3):
        last = m.add_post(w["chosen"], w["rob"]["id"], "msg %d" % i)
    await until(lambda: state.wake(last["id"]) is not None)
    paths = [c[1] for c in m.calls]
    assert paths.count("/api/v4/channels/%s" % w["chosen"]) == 1
    assert paths.count("/api/v4/users/%s" % w["rob"]["id"]) == 1
    assert paths.count("/api/v4/teams/t-main") == 1


async def test_bearer_header_on_handshake_and_rest(running):
    m, w, lis, state = running
    tok = w["bot"]["token"]
    assert ("GET", "/api/v4/users/me", tok) in m.calls
    assert ("WS", "/api/v4/websocket", tok) in m.calls
    assert lis.connection_id and state.get_meta("ws_connection_id") == lis.connection_id
    assert lis.bot_user_id == w["bot"]["id"]


@pytest.mark.parametrize("ws_level", [None, logging.DEBUG], ids=["default", "ws-debug"])
async def test_token_absent_from_logs_and_state(served, tmp_path, caplog, ws_level):
    m, w, _ = served
    with caplog.at_level(logging.DEBUG), caplog.at_level(ws_level or logging.INFO, logger="mmbridge.ws"):
        lis, state = make(served, tmp_path)
        task = asyncio.create_task(lis.run())
        await until(lambda: lis.status == "ok")
        p = m.add_post(w["chosen"], w["rob"]["id"], "hello")
        await until(lambda: state.wake(p["id"]) is not None)
        m.ws_drop()
        await asyncio.wait_for(task, 5)
    tok = w["bot"]["token"]
    assert "wake_queued" in caplog.text and "ws_connected" in caplog.text
    assert tok not in caplog.text
    assert tok not in json.dumps([x.payload for x in state.wakes()])
    state.close()
    for f in tmp_path.iterdir():
        assert tok.encode() not in f.read_bytes()


async def test_malformed_event_is_skipped_and_listener_keeps_going(running, caplog):
    m, w, lis, state = running
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        m.ws_send_raw("{not json")
        m.ws_send_raw({"event": "posted", "data": {"channel_type": "O", "post": "{broken"} })
        p = m.add_post(w["chosen"], w["rob"]["id"], "still listening")
        await until(lambda: state.wake(p["id"]) is not None)
    assert caplog.text.count("event_invalid") == 2
    assert [x.post_id for x in state.wakes()] == [p["id"]]


async def test_seq_is_tracked_and_gap_logged(running, caplog):
    m, w, lis, state = running
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        a = m.add_post(w["chosen"], w["rob"]["id"], "one")
        await until(lambda: state.wake(a["id"]) is not None)
        assert lis.last_seq == 1
        m.ws_skip_seq(2)
        b = m.add_post(w["chosen"], w["rob"]["id"], "two")
        await until(lambda: state.wake(b["id"]) is not None)
    assert lis.last_seq == 4
    assert '"event": "ws_seq_gap"' in caplog.text and '"expected": 2' in caplog.text


async def test_pings_keep_a_quiet_connection_alive(served, tmp_path):
    m, w, _ = served
    lis, state = make(served, tmp_path, ping_s=0.05, idle_s=0.3)
    task = asyncio.create_task(lis.run())
    await until(lambda: lis.status == "ok")
    await asyncio.sleep(1.0)
    assert not task.done() and m.ws_pings >= 5
    m.ws_drop()
    await asyncio.wait_for(task, 5)
    assert lis.status == "off"


async def test_idle_connection_is_treated_as_dead(served, tmp_path, caplog):
    m, w, _ = served
    m.ws_answer_pings = False
    lis, state = make(served, tmp_path, ping_s=0.05, idle_s=0.3)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        await asyncio.wait_for(lis.run(), 5)
    assert lis.status == "off" and "ws_idle" in caplog.text


async def test_listener_never_joins_or_posts(running):
    m, w, lis, state = running
    p = m.add_post(w["chosen"], w["rob"]["id"], "hi")
    await until(lambda: state.wake(p["id"]) is not None)
    assert m.changes == []
    assert all(c[0] in ("GET", "WS") for c in m.calls)


async def test_ws_spike_prints_shapes_without_token_or_text(served):
    from app.ws_spike import spike
    m, w, base = served
    lines = []

    async def post_soon():
        await until(lambda: m.ws_pings)   # ping reply is queued before the posted event
        m.add_post(w["chosen"], w["rob"]["id"], "m-private-text")
    poster = asyncio.create_task(post_soon())
    assert await spike(w["bot"]["token"], base, 5, out=lines.append) == 0
    await poster
    text = "\n".join(lines)
    assert "hello: event=hello seq=0 connection_id=True" in text
    assert "ping reply shape" in text and "posted: seq=1 channel_type=O" in text
    assert w["bot"]["token"] not in text and "m-private-text" not in text
diff --git a/tests/acceptance/drivers/fake_mattermost.py b/tests/acceptance/drivers/fake_mattermost.py
index 031ff89..33ed2d7 100644
--- a/tests/acceptance/drivers/fake_mattermost.py
+++ b/tests/acceptance/drivers/fake_mattermost.py
@@ -4,14 +4,21 @@ Injected into the bridge via httpx.ASGITransport. Records every call as (method,
 Slice 1: users/me, users/me/teams, users/me/teams/{id}/channels.
 Slice 2: channel by name, members/me, POST /posts, channel posts, POST /users/ids.
 Slice 3: users/username/{u}, POST /channels/direct (idempotent; creating one is a world change).
+Live bots lb3: GET channels/{id}, teams/{id}, users/{id}; websocket /api/v4/websocket (Bearer handshake,
+hello{connection_id}, per-connection seq, `posted` broadcast to channel members, ping action -> pong reply,
+drop/raw/seq-skip controls). `serve()` runs the app on a free localhost port for real HTTP/WS clients.
 """
+import asyncio
+import contextlib
 import itertools
+import json
 
 import httpx
 from starlette.applications import Starlette
 from starlette.requests import Request
 from starlette.responses import JSONResponse
-from starlette.routing import Route
+from starlette.routing import Route, WebSocketRoute
+from starlette.websockets import WebSocket
 
 
 class FakeMattermost:
@@ -26,6 +33,11 @@ class FakeMattermost:
         self._ids = itertools.count(1)
         self.down = False
         self.fail_status = None   # force every response to this HTTP status
+        self.server_version = "10.11.0"
+        self.ws_sessions = []     # open websocket sessions (_WsSession)
+        self.ws_answer_pings = True
+        self.ws_pings = 0
+        self._ws_ids = itertools.count(1)
         self.app = Starlette(routes=[
             Route("/api/v4/users/me", self._me),
             Route("/api/v4/users/me/teams", self._teams),
@@ -37,6 +49,10 @@ class FakeMattermost:
             Route("/api/v4/users/ids", self._users_by_ids, methods=["POST"]),
             Route("/api/v4/users/username/{username}", self._user_by_username),
             Route("/api/v4/channels/direct", self._direct, methods=["POST"]),
+            Route("/api/v4/channels/{channel_id}", self._channel),
+            Route("/api/v4/teams/{team_id}", self._team),
+            Route("/api/v4/users/{user_id}", self._user),
+            WebSocketRoute("/api/v4/websocket", self._ws),
         ])
 
     # --- world setup -------------------------------------------------------------
@@ -76,11 +92,60 @@ class FakeMattermost:
     def direct_channels(self, user_a, user_b):
         return [c for c in self.channels.values() if c["type"] == "D" and c["members"] == {user_a, user_b}]
 
-    def add_post(self, channel_id, user_id, message):
+    def add_post(self, channel_id, user_id, message, type="", root_id=""):
+        """Create a post and broadcast `posted` to the channel members' websocket sessions (as Mattermost does,
+        including the author's own sessions)."""
         pid = "p-%d" % next(self._ids)
-        self.posts[pid] = {"id": pid, "channel_id": channel_id, "user_id": user_id, "message": message,
-                           "create_at": next(self._clock)}
-        return self.posts[pid]
+        self.posts[pid] = p = {"id": pid, "channel_id": channel_id, "user_id": user_id, "message": message,
+                               "create_at": next(self._clock), "type": type, "root_id": root_id}
+        c = self.channels[channel_id]
+        event = {"event": "posted", "broadcast": {"channel_id": channel_id, "team_id": "", "user_id": ""},
+                 "data": {"channel_display_name": c["display_name"], "channel_name": c["name"],
+                          "channel_type": c["type"], "sender_name": "@" + self.users[user_id]["username"],
+                          "team_id": c["team_id"], "post": json.dumps(p)} }
+        for s in self.ws_sessions:
+            if s.user_id in c["members"]:
+                s.push(event)
+        return p
+
+    # --- websocket controls -------------------------------------------------------
+    def ws_send_raw(self, event):
+        """Send a raw frame (dict -> JSON with the session seq; str -> as is) to every open session."""
+        for s in self.ws_sessions:
+            s.push(event) if isinstance(event, dict) else s.q.put_nowait(event)
+
+    def ws_resend_last(self):
+        """Re-send each session's last event with a fresh seq (duplicate delivery)."""
+        for s in self.ws_sessions:
+            s.push({k: v for k, v in s.last.items() if k != "seq"})
+
+    def ws_skip_seq(self, n=1):
+        for s in self.ws_sessions:
+            s.seq += n
+
+    def ws_drop(self):
+        """Close every open websocket session (connection drop)."""
+        for s in self.ws_sessions:
+            s.q.put_nowait(None)
+
+    @contextlib.asynccontextmanager
+    async def serve(self):
+        """Serve REST + websocket on 127.0.0.1:<free port>; yields the base URL (http://127.0.0.1:<port>)."""
+        import uvicorn
+        server = uvicorn.Server(uvicorn.Config(self.app, host="127.0.0.1", port=0, log_level="warning",
+                                               lifespan="off", ws="websockets"))
+        task = asyncio.create_task(server.serve())
+        while not server.started:
+            if task.done():
+                task.result()
+            await asyncio.sleep(0.01)
+        port = server.servers[0].sockets[0].getsockname()[1]
+        try:
+            yield "http://127.0.0.1:%d" % port
+        finally:
+            self.ws_drop()
+            server.should_exit = True
+            await task
 
     def channel_posts(self, channel_id):
         """Posts of a channel, oldest first."""
@@ -200,6 +265,67 @@ class FakeMattermost:
             return JSONResponse({"message": "not found"}, status_code=404)
         return JSONResponse({"id": x["id"], "username": x["username"], "is_bot": x["is_bot"]})
 
+    async def _channel(self, request):
+        u, err = self._auth(request)
+        if err:
+            return err
+        c, err = self._member_channel(u, request.path_params["channel_id"])
+        if err:
+            return err
+        return JSONResponse({k: v for k, v in c.items() if k != "members"})
+
+    async def _team(self, request):
+        u, err = self._auth(request)
+        if err:
+            return err
+        t = self.teams.get(request.path_params["team_id"])
+        return JSONResponse(t) if t else JSONResponse({"message": "not found"}, status_code=404)
+
+    async def _user(self, request):
+        u, err = self._auth(request)
+        if err:
+            return err
+        x = self.users.get(request.path_params["user_id"])
+        if not x:
+            return JSONResponse({"message": "not found"}, status_code=404)
+        return JSONResponse({"id": x["id"], "username": x["username"], "is_bot": x["is_bot"]})
+
+    async def _ws(self, ws: WebSocket):
+        tok = _tok(ws.headers)
+        self.calls.append(("WS", ws.url.path, tok))
+        user = next((u for u in self.users.values() if tok and u["token"] == tok), None)
+        if not user or self.fail_status:
+            await ws.close(code=1008)          # before accept: the handshake is refused (HTTP 403)
+            return
+        await ws.accept()
+        s = _WsSession(user["id"], "conn-%d" % next(self._ws_ids))
+        s.push({"event": "hello", "data": {"connection_id": s.connection_id, "server_version": self.server_version},
+                "broadcast": {"user_id": user["id"]} })
+        self.ws_sessions.append(s)
+
+        async def writer():
+            while (m := await s.q.get()) is not None:
+                await ws.send_text(m if isinstance(m, str) else json.dumps(m))
+
+        async def reader():
+            while True:
+                msg = json.loads(await ws.receive_text())
+                if msg.get("action") == "ping":
+                    self.ws_pings += 1
+                    if self.ws_answer_pings:
+                        s.q.put_nowait({"status": "OK", "seq_reply": msg.get("seq"),
+                                        "data": {"text": "pong", "version": self.server_version} })
+        tasks = [asyncio.create_task(writer()), asyncio.create_task(reader())]
+        try:
+            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
+        finally:
+            for t in tasks:
+                t.cancel()
+            await asyncio.gather(*tasks, return_exceptions=True)
+            self.ws_sessions.remove(s)
+            with contextlib.suppress(Exception):
+                await ws.close()
+
     async def _direct(self, request):
         u, err = self._auth(request)
         if err:
@@ -214,6 +340,20 @@ class FakeMattermost:
         return JSONResponse({k: v for k, v in c.items() if k != "members"}, status_code=200 if existed else 201)
 
 
+class _WsSession:
+    """One websocket connection: outgoing queue (None closes it) and the per-connection seq (hello is 0)."""
+
+    def __init__(self, user_id, connection_id):
+        self.user_id, self.connection_id = user_id, connection_id
+        self.q = asyncio.Queue()
+        self.seq, self.last = 0, None
+
+    def push(self, event):
+        self.last = {**event, "seq": self.seq}
+        self.seq += 1
+        self.q.put_nowait(self.last)
+
+
 def _tok(headers):
     a = headers.get("authorization", "")
     return a[7:] if a.startswith("Bearer ") else None
---
id: SLICE-20261027-lb3-listener-filters
type: slice
phase: implement
status: in-progress           # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
plan_phase: 3
review: required (long-lived network component, ADR-0007) - thoughts/shared/verification/2026-10-27-lb3-review.md
reqs: [REQ-A1, REQ-A2, REQ-A3]
specs: none - wakes are only observable at a receiver after slice 4; this slice proves filter + listener->state.db with unit tests and an integration test against the fake MM websocket (specs for A1/A2/A3 turn green in slice 4)
---
# Slice 3: Listener + filters (fake MM websocket)

Plan: [thoughts/shared/plans/2026-10-27-live-bots.md](../plans/2026-10-27-live-bots.md) Phase 3. Architecture: docs/architecture/2026-10-26-live-bots.md. **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
Against a fake Mattermost websocket, the listener authenticates, tracks seq, and puts exactly the qualifying posts (chosen channels + DMs, not own/system/group posts) into the wake queue.

## Acceptance criteria
- [ ] `app/live_filter.py`: pure `decide(event: dict, bot_user_id: str, chosen: set[str]) -> WakeIntent | None` (rules from architecture Filter rules; malformed -> None + `event_invalid`)
- [ ] `app/listener.py`: `Listener(cfg, state, client_factory, ws_connect)`; `run()` = GET /users/me -> WS connect `Authorization: Bearer` -> hello(connection_id) -> on `posted` decide -> build payload (channel/sender lookups cached) -> `state.enqueue` + cursor; seq tracking, ping 30 s/idle 60 s; no reconnect/catch-up yet (slice 5)
- [ ] Spike (OQ1): confirm hello/seq/posted shape against Rob's Mattermost version; record result in progress log
- [ ] `tests/acceptance/drivers/fake_mattermost.py`: websocket endpoint (hello, seq, posted, drop) - reusable by the live driver
- [ ] `requirements.txt`: pin `websockets` explicitly (ADR-0007)
- [ ] (PR-3) Listener persists via `state.enqueue_and_advance`
- [ ] Plan Phase 3 Automated Verification all exit 0; existing MCP suite (`.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`) still green

## Tasks
- [ ] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red) - n/a, see specs:
- [ ] Write failing unit tests (tests/unit/) for the behaviours above
- [ ] Implement
- [ ] Run Phase 3 automated verification (plan), including this slice's specs (now green)
- [ ] Do not edit locked files: tests/acceptance/specs/**, DSL public interface (CP-C speclock)

## Size check
~200 lines + tests (split filter/listener if larger)

## Progress log
<!-- date - agent - what changed (file:line) -->

## Blockers / deviations from plan
none
eng-architecture-review
eng-discover
eng-handoff
eng-implement-slice
eng-inbox
eng-plan
eng-project-init
eng-research
eng-resume
eng-retro
eng-scope-review
eng-ship
eng-triage
eng-verify

exec
/bin/bash -lc ".venv/bin/python -c 'import websockets; print(websockets.__version__)'; .venv/bin/pytest tests/unit -q" in /mnt/d/rob/projects/mmbridge
exec
/bin/bash -lc 'cat app/logging.py; cat docs/decisions/0007-mattermost-websocket-listener.md; cat tests/unit/test_live_filter.py; cat AGENTS.md' in /mnt/d/rob/projects/mmbridge
 succeeded in 0ms:
"""Structured JSON call logs (ADR-0005) with a redaction filter. Never log headers, tokens or bodies.

The filter also redacts registered literals (stored bot token and wake secret, ADR-0006)."""
import json
import logging
import re
import sys

_PATTERNS = [re.compile(r"(?i)bearer\s+\S+"), re.compile(r"(?i)(authorization['\"]?\s*[:=]\s*['\"]?)[^'\",}\s]+")]
_SECRETS: set[str] = set()   # stored bot token / wake secret (ADR-0006), redacted as literals


def register_secret(value: str) -> None:
    if isinstance(value, str) and len(value) >= 8:
        _SECRETS.add(value)


def _literals(s: str) -> str:
    for v in sorted(_SECRETS, key=len, reverse=True):
        s = s.replace(v, "[REDACTED]")
    return s


class RedactFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        for p in _PATTERNS:
            msg = p.sub(lambda m: (m.group(1) if m.groups() else "Bearer ") + "[REDACTED]", msg)
        record.msg, record.args = _literals(msg), None
        if record.exc_info:
            record.exc_text = _redact(logging.Formatter().formatException(record.exc_info))
            record.exc_info = None
        return True


def _redact(s: str) -> str:
    for p in _PATTERNS:
        s = p.sub("[REDACTED]", s)
    return _literals(s)


log = logging.getLogger("mmbridge")
calls = logging.getLogger("mmbridge.calls")


def setup() -> None:
    if getattr(log, "_mmb_setup", False):
        return
    log.setLevel(logging.INFO)
    f = RedactFilter()
    log.addFilter(f)
    calls.addFilter(f)
    h = logging.StreamHandler(sys.stdout)
    h.addFilter(f)
    log.addHandler(h)
    log._mmb_setup = True


def call_line(**fields) -> None:
    calls.info(json.dumps(fields, sort_keys=True))
---
id: ADR-0007
type: adr
phase: architecture
status: accepted         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-26
links: [docs/design/2026-10-26-live-bots.md, docs/architecture/2026-10-26-live-bots.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0007: Mattermost websocket listener inside the bridge process

## Status
proposed

## Context
REQ-A1/A2/A4 need real-time post events. Research: no background task or WS client exists; single uvicorn process (Dockerfile:19); `websockets` arrives only transitively via `uvicorn[standard]` (OQ4). Mattermost exposes `/api/v4/websocket` with header auth, `hello{connection_id}`, per-event `seq`, and resume via `connection_id` + `sequence_number` query params (OQ1).

## Decision
We will run one asyncio listener task from the FastAPI lifespan, gated by `LIVE_BOTS_ENABLED`, using the `websockets` library pinned explicitly in requirements.txt. Auth with `Authorization: Bearer` on the handshake. Track `seq`; on reconnect pass `connection_id` and next sequence; if the hello brings a new connection_id (or a seq gap) run a REST catch-up of chosen + DM channels since the stored cursor, bounded by `LIVE_CATCHUP_MINUTES` (default 15). Ping every 30 s, treat 60 s silence as dead; backoff 1 s doubling to 60 s with jitter. Exactly one listener per deployment (replicas=1 plus SQLite lease, ADR-0009). Rejected: separate worker container (two deploys, shared volume); MM outgoing webhooks (no DMs); polling (latency).

## Consequences
Positive: one deploy, real-time, reuses existing MM REST client. Negative: bridge becomes stateful; listener bugs share the process with MCP tools (mitigated: task exceptions caught and restarted, flag to disable). Neutral: Mattermost version-specific behaviour verified in the first slice.

## Prediction (scored in a later eng-retro)
- Expected outcome: >=95% of wakes within 10 s over 7 days; a 30 s connection drop yields exactly one wake per gap post.
- Check date: 7 days after v1 is enabled
- What would prove it wrong: reconnect loops, missed posts after MM restarts, or MCP tool latency regressions caused by the listener.
- Score: unscored
"""live_filter.decide: architecture Filter rules (REQ-A1 chosen channels, A2 DMs, A3 own posts)."""
import json
import logging

import pytest

from app.live_filter import WakeIntent, decide

BOT = "u-eddie"
CHOSEN = {"c-main-town-square"}


def posted(channel_id="c-main-town-square", ctype="O", user_id="u-rob", ptype="", root_id="", message="hi",
           post_as_str=True, **post_extra):
    post = {"id": "p-1", "channel_id": channel_id, "user_id": user_id, "message": message, "type": ptype,
            "create_at": 1_700_000_000_000, "root_id": root_id, **post_extra}
    return {"event": "posted", "seq": 3,
            "data": {"channel_type": ctype, "channel_name": "town-square", "channel_display_name": "Town Square",
                     "sender_name": "@rob", "team_id": "t-main", "post": json.dumps(post) if post_as_str else post},
            "broadcast": {"channel_id": channel_id} }


def test_chosen_channel_wakes():
    w = decide(posted(), BOT, CHOSEN)
    assert isinstance(w, WakeIntent)
    assert (w.post_id, w.channel_id, w.channel_type, w.user_id, w.message, w.create_at, w.root_id) == (
        "p-1", "c-main-town-square", "O", "u-rob", "hi", 1_700_000_000_000, None)


@pytest.mark.parametrize("ctype", ["O", "P"])
def test_non_chosen_open_or_private_channel_drops(ctype):
    assert decide(posted(channel_id="c-main-other", ctype=ctype), BOT, CHOSEN) is None


def test_chosen_private_channel_wakes():
    assert decide(posted(ctype="P"), BOT, CHOSEN) is not None


def test_dm_wakes_without_being_chosen():
    w = decide(posted(channel_id="d-u-eddie__u-rob", ctype="D"), BOT, CHOSEN)
    assert w is not None and w.channel_type == "D"


def test_group_dm_drops_even_if_chosen():
    assert decide(posted(ctype="G"), BOT, CHOSEN) is None


@pytest.mark.parametrize("ctype", ["O", "D"])
def test_own_post_drops(ctype):
    assert decide(posted(ctype=ctype, user_id=BOT), BOT, CHOSEN) is None


@pytest.mark.parametrize("ptype", ["system_join_channel", "system_add_to_channel", "system_header_change"])
def test_system_post_drops(ptype):
    assert decide(posted(ptype=ptype), BOT, CHOSEN) is None


def test_thread_reply_wakes_with_root_id():
    w = decide(posted(root_id="p-root"), BOT, CHOSEN)
    assert w is not None and w.root_id == "p-root"


def test_post_given_as_dict_is_accepted():
    assert decide(posted(post_as_str=False), BOT, CHOSEN) is not None


def test_non_posted_event_is_ignored_silently(caplog):
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        assert decide({"event": "typing", "data": {}, "seq": 2}, BOT, CHOSEN) is None
    assert "event_invalid" not in caplog.text


def _broken():
    e = posted(message="m-private-text")
    yield "no data", {"event": "posted", "seq": 1}
    yield "post not json", {**e, "data": {**e["data"], "post": "{not json"} }
    yield "post not object", {**e, "data": {**e["data"], "post": "[1, 2]"} }
    p = json.loads(e["data"]["post"])
    for field in ("id", "channel_id", "user_id", "create_at"):
        q = {k: v for k, v in p.items() if k != field}
        yield "missing " + field, {**e, "data": {**e["data"], "post": json.dumps(q)} }
    yield "create_at not int", {**e, "data": {**e["data"], "post": json.dumps({**p, "create_at": "x"})} }
    yield "message not str", {**e, "data": {**e["data"], "post": json.dumps({**p, "message": None})} }
    yield "no channel_type", {**e, "data": {k: v for k, v in e["data"].items() if k != "channel_type"} }
    yield "not a dict", ["posted"]


@pytest.mark.parametrize("label,event", list(_broken()), ids=[x[0] for x in _broken()])
def test_malformed_event_drops_and_logs_event_invalid(label, event, caplog):
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        assert decide(event, BOT, CHOSEN) is None
    assert "event_invalid" in caplog.text
    assert "m-private-text" not in caplog.text   # message text never logged
---
id: AGENTS
type: conventions
phase: any
status: active
owner_agent: Eddie
date: 2026-10-25
links: [PROJECT_STATE.md, docs/definition-of-done.md]
---
# Agent conventions

**Start here:** read `PROJECT_STATE.md`, then the latest handoff it links. Do not rely on chat history.
Process: eng-process kit; canonical copy at `.eng/PROCESS.md` (phases, checkpoints, skill for each phase in section 3, session convention in section 8). Run `.eng/bin/eng-check .` before and after each session.
**The kit is vendored in this repo:** skills are in `.claude/skills/eng-*/SKILL.md` (Claude Code loads them as project skills; other agents read them as files) and the scripts are in `.eng/bin/` (plain Python 3, run through the interpreter from the repo root: `python3 .eng/bin/eng-check .`; native Windows: `python .eng/bin/eng-check .` or `py .eng/bin/eng-check .`). Do not look for the kit elsewhere; if `.eng/bin` or `.claude/skills` is missing, ask the planner to run `<kit>/bin/eng-init <repo> --upgrade`.

## Working agreements
The values live in `PROJECT_STATE.md` front matter (`implementer`, `planner`, `cross_review`, `push_permission`, `board`); `.eng/PROCESS.md` section 10 says what each means. Summary:
- The **planner** agent plans, writes docs, keeps state and process. It does not write production code.
- The **implementer** (default: Claude Code on the owner's PC) codes one slice at a time. When a slice is ready, the planner sends the owner the "ready to implement" message (`.eng/bin/eng-status` prints it), then afterwards picks up the implementer's handoff and runs `eng-verify` and `.eng/bin/eng-check`.
- **Cross-model review** (Codex) is advisory, never a gate. See `.eng/PROCESS.md` section 10.
- **Push:** follow `push_permission` (default `ask`: ask the owner before each push).
- **Owner review notes** (`thoughts/shared/review-notes/`) belong to the owner. Agents never edit them until the owner says they are ready.

## Commands
- Install:  `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt`
- Build:    `docker build -t mmbridge .`
- Test:     `.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`
- Lint/typecheck: none yet
- Run locally: `MATTERMOST_URL=http://localhost:8065 .venv/bin/uvicorn app.main:app --port 8080`

## Architecture map
<top-level dirs and what lives there, 5-10 lines>

## Code style / conventions
<only rules an agent cannot infer from the code>

## Rules
- Never weaken a test, timeout, or check to make it pass; never use `--no-verify`.
- Durable decisions go in `docs/decisions/` (ADR). Deferred work goes in `TODOS.md`.
- Don't touch: <paths / systems off-limits>

## Runtime facts
- Container listens on **8080** (Coolify `SERVICE_FQDN_MMBRIDGE_8080`; local `docker run -p <host>:8080`), not 8000.
- **Trusted proxy:** uvicorn honours X-Forwarded-For only from `FORWARDED_ALLOW_IPS` (Dockerfile default `127.0.0.1`). Never `*`. On Coolify set it to the Traefik source IP/subnet (TODO: real value from Rob). Until set, the anon rate limit keys on the proxy IP (shared bucket), which is safe but coarse.
- Lint: ruff not in the gate yet (TODO, TODOS P3: needs ruff in requirements-dev + a clean run).
- Dev venv uses **Python 3.12** to match the Dockerfile: `uv venv -p 3.12` (3.14 install fails).
- After a redeploy that changes the MCP tool list, restart the Grok Bot MCP servers before manual checks (clients cache tool lists).

## Gotchas

 exited 1 in 12942ms:
17.3
........................................................................ [ 40%]
..................EEEEEEEEEEEE.......................................... [ 81%]
................................                                         [100%]
==================================== ERRORS ====================================
__________ ERROR at setup of test_qualifying_posts_land_once_in_state __________

self = <uvicorn.server.Server object at 0x7393f992e840>, sockets = None

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
protocol_factory = <function Server.startup.<locals>.create_protocol at 0x7393f9a36c00>
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

self = <uvicorn.server.Server object at 0x7393f992e840>, sockets = None

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
_____________ ERROR at setup of test_payload_matches_wake_contract _____________

self = <Coroutine test_payload_matches_wake_contract>

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
E       AssertionError

.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:559: AssertionError
__________________ ERROR at setup of test_lookups_are_cached ___________________

self = <Coroutine test_lookups_are_cached>

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
E       AssertionError

.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:559: AssertionError
__________ ERROR at setup of test_bearer_header_on_handshake_and_rest __________

self = <Coroutine test_bearer_header_on_handshake_and_rest>

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
E       AssertionError

.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:559: AssertionError
_______ ERROR at setup of test_token_absent_from_logs_and_state[default] _______

self = <Coroutine test_token_absent_from_logs_and_state[default]>

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
E       AssertionError

.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:559: AssertionError
______ ERROR at setup of test_token_absent_from_logs_and_state[ws-debug] _______

self = <Coroutine test_token_absent_from_logs_and_state[ws-debug]>

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
E       AssertionError

.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:559: AssertionError
__ ERROR at setup of test_malformed_event_is_skipped_and_listener_keeps_going __

self = <Coroutine test_malformed_event_is_skipped_and_listener_keeps_going>

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
E       AssertionError

.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:559: AssertionError
_____________ ERROR at setup of test_seq_is_tracked_and_gap_logged _____________

self = <Coroutine test_seq_is_tracked_and_gap_logged>

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
E       AssertionError

.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:559: AssertionError
__________ ERROR at setup of test_pings_keep_a_quiet_connection_alive __________

self = <Coroutine test_pings_keep_a_quiet_connection_alive>

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
E       AssertionError

.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:559: AssertionError
__________ ERROR at setup of test_idle_connection_is_treated_as_dead ___________

self = <Coroutine test_idle_connection_is_treated_as_dead>

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
E       AssertionError

.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:559: AssertionError
_____________ ERROR at setup of test_listener_never_joins_or_posts _____________

self = <Coroutine test_listener_never_joins_or_posts>

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
E       AssertionError

.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:559: AssertionError
_____ ERROR at setup of test_ws_spike_prints_shapes_without_token_or_text ______

self = <Coroutine test_ws_spike_prints_shapes_without_token_or_text>

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
E       AssertionError

.venv/lib/python3.12/site-packages/pytest_asyncio/plugin.py:559: AssertionError
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
ERROR tests/unit/test_listener.py::test_payload_matches_wake_contract - Asser...
ERROR tests/unit/test_listener.py::test_lookups_are_cached - AssertionError
ERROR tests/unit/test_listener.py::test_bearer_header_on_handshake_and_rest
ERROR tests/unit/test_listener.py::test_token_absent_from_logs_and_state[default]
ERROR tests/unit/test_listener.py::test_token_absent_from_logs_and_state[ws-debug]
ERROR tests/unit/test_listener.py::test_malformed_event_is_skipped_and_listener_keeps_going
ERROR tests/unit/test_listener.py::test_seq_is_tracked_and_gap_logged - Asser...
ERROR tests/unit/test_listener.py::test_pings_keep_a_quiet_connection_alive
ERROR tests/unit/test_listener.py::test_idle_connection_is_treated_as_dead - ...
ERROR tests/unit/test_listener.py::test_listener_never_joins_or_posts - Asser...
ERROR tests/unit/test_listener.py::test_ws_spike_prints_shapes_without_token_or_text
164 passed, 2 warnings, 12 errors in 9.43s

exec
/bin/bash -lc '.venv/bin/pytest tests/acceptance -q; python3 .eng/bin/eng-check .' in /mnt/d/rob/projects/mmbridge
exec
/bin/bash -lc '.venv/bin/pytest tests/unit/test_listener.py -xq 2>&1 | tail -65' in /mnt/d/rob/projects/mmbridge
 succeeded in 3598ms:
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

1 passed, 2 warnings, 1 error in 1.87s

exec
/bin/bash -lc 'python3 .eng/bin/eng-check .' in /mnt/d/rob/projects/mmbridge
 succeeded in 1217ms:
eng-check: OK - 0 error(s), 0 warning(s), 81 artifact(s) checked

2026-10-27T07:24:51.463959Z ERROR codex_core::session: failed to record rollout items: thread 01a17c3e-71b4-7fe1-af6a-a75d6659ae55 not found
codex
No actionable defects were identified in the changes. Validation was partial: 164 unit tests passed, while websocket tests encountered server-startup failures in the restricted environment; eng-check passed.
No actionable defects were identified in the changes. Validation was partial: 164 unit tests passed, while websocket tests encountered server-startup failures in the restricted environment; eng-check passed.
````
