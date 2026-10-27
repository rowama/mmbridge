---
id: RUN-2026-10-27-code-review-slice-20261027-lb1-bot-store-admin-cli
type: run-log
phase: verify
status: ok
owner_agent: eng-run
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md, thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md, thoughts/shared/verification/2026-10-27-slice-20261027-lb1-bot-store-admin-cli-review.md]
role: code-review
runner: codex
tool: codex
slice: SLICE-20261027-lb1-bot-store-admin-cli
plan: thoughts/shared/plans/2026-10-27-live-bots.md
base: 691f4ac
exit_code: 0
pid: 3449068
eng_run_pid: 3449067
started: 2026-10-27T01:26:49
prompt_template: code-review.md v2
---
# eng-run code-review slice-20261027-lb1-bot-store-admin-cli

## Summary
- role: code-review; runner: codex (codex); exit code: 0; started 2026-10-27 01:26:49
- review file: thoughts/shared/verification/2026-10-27-slice-20261027-lb1-bot-store-admin-cli-review.md - no numbered '[severity]' findings parsed; read the raw output and fill the Findings table by hand

## Command
````
codex review --base 691f4ac
````

## Prompt
````
You are the independent code reviewer for this repository (eng-process kit v2.5.6). You did not write this code. Do not edit any file.

Follow the cross-model review step of eng-verify (.claude/skills/eng-verify/SKILL.md) and .eng/PROCESS.md section 10.

Review the changes of slice SLICE-20261027-lb1-bot-store-admin-cli (diff 691f4ac...HEAD; slice card: thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md; plan: thoughts/shared/plans/2026-10-27-live-bots.md) for correctness against the slice's acceptance criteria, missing or weak tests, security (auth, tenancy, secrets, injection), error handling, and maintainability.

Executable specs (v2.5): run `python .eng/bin/eng-spec status .`. Any change to locked specs or the DSL public interface is a [high] finding unless Rob re-approved it (new CP-C speclock row). For every changed DSL assertion step (assert_/then_/expect_/check_/verify_) name the step (e.g. `assert_order_placed`) in a finding and say whether the check got weaker. Driver changes are fine unless they hide failures (swallowed errors, retries that mask bugs, sleeps).

Output: a numbered list of findings, each as
  N. [severity] file:line - finding - suggested fix
with severity one of critical | high | medium | low. If you find nothing, write exactly "No findings."
Your final message is saved by eng-run to thoughts/shared/verification/2026-10-27-slice-20261027-lb1-bot-store-admin-cli-review.md (a review-findings artifact). Findings are advisory; Rob decides.
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
session id: 01a17c0a-4414-7323-8c8e-6c532abfe99d
--------
user
changes against '691f4ac'
exec
/bin/bash -lc 'cat PROJECT_STATE.md; cat .eng/PROCESS.md; git status --short; git diff --stat 691f4ac50697a044175d0eab19f61e6aaffc8483' in /mnt/d/rob/projects/mmbridge
 succeeded in 668ms:
---
id: STATE
type: project-state
phase: implement
status: active
owner_agent: grok-bot
date: 2026-10-27
links: []
triage: large             # unset | small | medium | large
active_slice: SLICE-20261027-lb1-bot-store-admin-cli
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
[SLICE-20261027-lb1-bot-store-admin-cli](thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md) (todo). Previous: D hardening [done](thoughts/shared/slices/2026-10-26-d-hardening-xff-bearer.md))

## Next action
A Live bots: plan signed off (see Approval log). NEXT: implementer runs eng-run implement on lb1 (Merkle). Deploy prerequisites before enabling: Coolify volume /data (uid 10001), env MMB_STORE_KEY, replicas 1.

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
- Specs A: [tests/acceptance/specs/test_live_bots.py](tests/acceptance/specs/test_live_bots.py)
- Architecture A Live bots (approved): [docs/architecture/2026-10-26-live-bots.md](docs/architecture/2026-10-26-live-bots.md)
- Cross-model review A (awaiting Codex): [thoughts/shared/verification/2026-10-26-live-bots-arch-review.md](thoughts/shared/verification/2026-10-26-live-bots-arch-review.md)
- Architecture: [docs/architecture/2026-10-25-mmbridge-mcp.md](docs/architecture/2026-10-25-mmbridge-mcp.md)
- ADRs 0001-0010 (all accepted): [docs/decisions/](docs/decisions/)
- Latest handoff: [thoughts/shared/handoffs/2026-10-27_00-30-11_plan-drafted-awaiting-plan-review.md](thoughts/shared/handoffs/2026-10-27_00-30-11_plan-drafted-awaiting-plan-review.md)
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

?? thoughts/shared/inbox-local-bak-1793080755/
?? thoughts/shared/inbox.md
?? thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb1-bot-store-admin-cli.running.md
?? thoughts/shared/runs/2026-10-27-implement-slice-20261027-lb1-bot-store-admin-cli.running.md
 Dockerfile                                         |   3 +-
 app/admin.py                                       | 137 +++++++++++++++++
 app/logging.py                                     |  20 ++-
 app/store.py                                       | 163 +++++++++++++++++++++
 requirements.txt                                   |   1 +
 tests/unit/test_admin.py                           | 161 ++++++++++++++++++++
 tests/unit/test_store.py                           | 155 ++++++++++++++++++++
 .../slices/2026-10-27-lb1-bot-store-admin-cli.md   |   2 +-
 8 files changed, 637 insertions(+), 5 deletions(-)

exec
/bin/bash -lc 'cat thoughts/shared/handoffs/2026-10-27_00-30-11_plan-drafted-awaiting-plan-review.md; python3 .eng/bin/eng-check .; find . -name AGENTS.md -o -name AGENTS.override.md; git diff 691f4ac50697a044175d0eab19f61e6aaffc8483 -- app Dockerfile requirements.txt' in /mnt/d/rob/projects/mmbridge
 succeeded in 2709ms:
---
id: HANDO-20261027-plan-drafted-awaiting-plan-review
type: handoff
phase: plan
status: complete
owner_agent: grok-bot
date: 2026-10-27T00:30:11-05:00
links: []
git_commit: 808f988
branch: main
next_skill: <skill the next session should run>
---
# Handoff: Live bots plan drafted - awaiting mandatory Codex plan review, then CP-C

## Done (grok-bot, 2026-10-27)
- Plan: thoughts/shared/plans/2026-10-27-live-bots.md (status draft; 5 phases = Rob-approved slice order; research claims re-verified at 808f988).
- Slice cards (todo, owner claude-code, all security-review required): thoughts/shared/slices/2026-10-27-lb1..lb5-*.md.
- Specs: tests/acceptance/specs/test_live_bots.py (9 specs: A1x3, A2, A3, A4, A7x2, A8; channel `live`), DSL live steps in tests/acceptance/dsl.py, conftest `--channel live`, stub drivers/live.py. Live specs red (NotImplementedError) on `--channel live`, skipped by default; existing suite 16 passed.
- Speclock: `approved speclock sha256:3108f1fe6a93cfae` (eng-check warns lock differs from 2026-10-26 approval until CP-C row logged - expected).
- Plan review stub: thoughts/shared/verification/2026-10-27-live-bots-plan-review.md (AWAITING Codex; plan_review: set).

## Next (exact)
1. Rob, repo root on his PC: `git pull && python3 .eng/bin/eng-run plan-review thoughts/shared/plans/2026-10-27-live-bots.md` (or the `codex exec ... -o thoughts/shared/verification/2026-10-27-live-bots-plan-review.md` command in the stub / `.eng/bin/eng-status`).
2. Planner (Eddie/grok-bot): restore front matter + Findings table, disposition each row (fixed/rejected with evidence/accepted-risk only with Rob), update plan/cards; if specs change, re-run `eng-spec lock` and update sha. eng-check.
3. Only then ask Rob: `CP-C: thoughts/shared/plans/2026-10-27-live-bots.md - approve plan` and log `| <date> | CP-C | thoughts/shared/plans/2026-10-27-live-bots.md | approved speclock sha256:<hex> |`; set plan approved, phase implement, active_slice lb1; `python3 .eng/bin/eng-run implement thoughts/shared/plans/2026-10-27-live-bots.md SLICE-20261027-lb1-bot-store-admin-cli`.

## Open / risks
- Codex plan review NOT done; CP-C waits on it.
- Advisory arch review (2026-10-26-live-bots-arch-review.md) still awaiting, optional.
eng-check: OK - 0 error(s), 0 warning(s), 71 artifact(s) checked
./.eng/templates/AGENTS.md
./AGENTS.md
diff --git a/Dockerfile b/Dockerfile
index 557abb4..57e19fb 100644
--- a/Dockerfile
+++ b/Dockerfile
@@ -8,7 +8,8 @@ RUN pip install --no-cache-dir -r requirements.txt
 
 COPY app ./app
 
-RUN useradd --create-home --uid 10001 appuser
+# /data: persistent volume for the encrypted bot store (ADR-0006); owned by the app user, private.
+RUN useradd --create-home --uid 10001 appuser && mkdir -p /data && chown 10001:10001 /data && chmod 700 /data
 USER appuser
 
 # Trusted proxy for X-Forwarded-For: uvicorn reads FORWARDED_ALLOW_IPS natively.
diff --git a/app/admin.py b/app/admin.py
new file mode 100644
index 0000000..4914a0d
--- /dev/null
+++ b/app/admin.py
@@ -0,0 +1,137 @@
+"""Operator CLI for the live bot (ADR-0006): `python -m app.admin set-bot | show | rotate-key`.
+
+Run inside the container (Coolify terminal). The token is read from stdin only and never printed or logged;
+the wake secret is printed once when generated, never by `show`. Channels are resolved by name to ids with the
+bot's own token and must already include the bot (REQ-7: never joins).
+"""
+import argparse
+import asyncio
+import json
+import os
+import secrets
+import sys
+
+from app import logging as mlog
+from app import store
+from app.errors import ToolError
+from app.mattermost import MATTERMOST_URL, Client, MMError
+from app.service import _member_channel
+from app.validate import identifier
+
+FIELDS = ("token", "wake_url", "wake_secret", "channels")
+
+
+class AdminError(Exception):
+    def __init__(self, code: str, detail: str = ""):
+        super().__init__(code)
+        self.code, self.detail = code, detail
+
+
+def _parser() -> argparse.ArgumentParser:
+    p = argparse.ArgumentParser(prog="python -m app.admin", description="mmbridge live bot admin")
+    sub = p.add_subparsers(dest="cmd", required=True)
+    s = sub.add_parser("set-bot", help="store the bot token, wake URL and channels (token read from stdin)")
+    s.add_argument("--token-stdin", action="store_true", required=True, help="read the bot token from stdin")
+    s.add_argument("--wake-secret-stdin", action="store_true",
+                   help="read the wake secret from the next stdin line instead of generating one")
+    s.add_argument("--wake-url", required=True)
+    s.add_argument("--channels", required=True, help="team/channel,team/channel,...")
+    sub.add_parser("show", help="show the stored config (token masked, secret hidden)")
+    r = sub.add_parser("rotate-key", help="re-encrypt the store with a new MMB_STORE_KEY")
+    r.add_argument("--new-key-env", default="MMB_STORE_KEY_NEW", help="env var holding the new key")
+    r.add_argument("--old-key-env", default="MMB_STORE_KEY", help="env var holding the current key(s)")
+    return p
+
+
+def _channel_specs(raw: str) -> list[tuple[str, str]]:
+    out = []
+    for item in raw.split(","):
+        parts = item.strip().split("/")
+        if len(parts) != 2:
+            raise AdminError("invalid_argument", "channels must be team/channel,... (got %r)" % item.strip())
+        try:
+            out.append((identifier("team", parts[0]), identifier("channel", parts[1])))
+        except ToolError as e:
+            raise AdminError("invalid_argument", e.message) from None
+    return out
+
+
+async def _resolve(token: str, specs: list[tuple[str, str]], transport) -> tuple[str, list[str]]:
+    c = Client(token, MATTERMOST_URL, transport=transport)
+    try:
+        me = await c.get("/users/me")
+        ids = []
+        for team, channel in specs:
+            ids.append((await _member_channel(c, team, channel))["id"])
+    except ToolError as e:
+        raise AdminError(e.code, e.message) from None
+    except MMError as e:
+        detail = "Mattermost rejected the bot token" if e.code == "unauthorized" else ""
+        raise AdminError(e.code, detail) from None
+    return me["username"], list(dict.fromkeys(ids))
+
+
+def _set_bot(a, stdin, out, transport) -> None:
+    lines = stdin.read().splitlines()
+    token = lines[0].strip() if lines else ""
+    if not token:
+        raise AdminError("invalid_argument", "no token on stdin")
+    supplied = a.wake_secret_stdin
+    secret = (lines[1].strip() if len(lines) > 1 else "") if supplied else secrets.token_urlsafe(32)
+    if supplied and len(secret) < store.MIN_SECRET:
+        raise AdminError("invalid_argument", "wake_secret: must be at least %d characters" % store.MIN_SECRET)
+    if not store.https_ok(a.wake_url):
+        raise AdminError("invalid_argument", "wake_url: must be https")
+    specs = _channel_specs(a.channels)
+    key = os.getenv("MMB_STORE_KEY")
+    if not (key or "").strip():
+        raise store.StoreError("store_key_missing")
+    username, ids = asyncio.run(_resolve(token, specs, transport))
+    path = store.path_from_env()
+    try:
+        prev = store.load(path, key)
+    except store.StoreError:
+        prev = None
+    cfg = store.BotConfig(token=token, wake_url=a.wake_url, wake_secret=secret, channels=ids)
+    store.save(path, key, cfg)
+    changed = [f for f in FIELDS if prev is None or getattr(prev, f) != getattr(cfg, f)]
+    mlog.log.info(json.dumps({"event": "store_updated", "fields": changed}))
+    print("bot @%s stored: wake_url %s, channels %s" % (username, cfg.wake_url, ",".join(ids)), file=out)
+    if not supplied:
+        print("wake secret (shown once; give it to the receiver): %s" % secret, file=out)
+
+
+def _show(out) -> None:
+    cfg = store.load(store.path_from_env(), os.getenv("MMB_STORE_KEY"))
+    print("version: %d\ntoken: ****%s\nwake_url: %s\nwake_secret: set (hidden)\nchannels: %s" % (
+        cfg.version, cfg.token[-4:], cfg.wake_url, ",".join(cfg.channels)), file=out)
+
+
+def _rotate_key(a, out) -> None:
+    store.rotate(store.path_from_env(), os.getenv(a.new_key_env), os.getenv(a.old_key_env))
+    mlog.log.info(json.dumps({"event": "store_updated", "fields": ["key"]}))
+    print("store re-encrypted with %s; set MMB_STORE_KEY to that key" % a.new_key_env, file=out)
+
+
+def main(argv=None, stdin=None, stdout=None, transport=None) -> int:
+    mlog.setup()
+    stdin, out = stdin or sys.stdin, stdout or sys.stdout
+    a = _parser().parse_args(argv)
+    try:
+        if a.cmd == "set-bot":
+            _set_bot(a, stdin, out, transport)
+        elif a.cmd == "show":
+            _show(out)
+        else:
+            _rotate_key(a, out)
+    except (AdminError, store.StoreError) as e:
+        print("error: %s%s" % (e.code, ": " + e.detail if e.detail else ""), file=out)
+        return 1
+    except OSError as e:
+        print("error: store_unwritable: %s" % e.strerror, file=out)
+        return 1
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/app/logging.py b/app/logging.py
index 9cee0d6..8e43060 100644
--- a/app/logging.py
+++ b/app/logging.py
@@ -1,10 +1,24 @@
-"""Structured JSON call logs (ADR-0005) with a redaction filter. Never log headers, tokens or bodies."""
+"""Structured JSON call logs (ADR-0005) with a redaction filter. Never log headers, tokens or bodies.
+
+The filter also redacts registered literals (stored bot token and wake secret, ADR-0006)."""
 import json
 import logging
 import re
 import sys
 
 _PATTERNS = [re.compile(r"(?i)bearer\s+\S+"), re.compile(r"(?i)(authorization['\"]?\s*[:=]\s*['\"]?)[^'\",}\s]+")]
+_SECRETS: set[str] = set()   # stored bot token / wake secret (ADR-0006), redacted as literals
+
+
+def register_secret(value: str) -> None:
+    if isinstance(value, str) and len(value) >= 8:
+        _SECRETS.add(value)
+
+
+def _literals(s: str) -> str:
+    for v in sorted(_SECRETS, key=len, reverse=True):
+        s = s.replace(v, "[REDACTED]")
+    return s
 
 
 class RedactFilter(logging.Filter):
@@ -12,7 +26,7 @@ class RedactFilter(logging.Filter):
         msg = record.getMessage()
         for p in _PATTERNS:
             msg = p.sub(lambda m: (m.group(1) if m.groups() else "Bearer ") + "[REDACTED]", msg)
-        record.msg, record.args = msg, None
+        record.msg, record.args = _literals(msg), None
         if record.exc_info:
             record.exc_text = _redact(logging.Formatter().formatException(record.exc_info))
             record.exc_info = None
@@ -22,7 +36,7 @@ class RedactFilter(logging.Filter):
 def _redact(s: str) -> str:
     for p in _PATTERNS:
         s = p.sub("[REDACTED]", s)
-    return s
+    return _literals(s)
 
 
 log = logging.getLogger("mmbridge")
diff --git a/app/store.py b/app/store.py
new file mode 100644
index 0000000..892c500
--- /dev/null
+++ b/app/store.py
@@ -0,0 +1,163 @@
+"""Encrypted store for the ONE live bot's config (ADR-0006): token, wake URL, wake secret, channel ids.
+
+/data/bots.enc is the Fernet ciphertext of {"version": 1, "bot": {...} }, mode 0600, written atomically.
+Key from env MMB_STORE_KEY; "new,old" is accepted (MultiFernet) for key rotation. Errors never carry
+key material, token or secret. Loaded/saved token and secret are registered with the log redact filter.
+"""
+import json
+import os
+import re
+import tempfile
+from dataclasses import dataclass
+
+from cryptography.fernet import Fernet, InvalidToken, MultiFernet
+
+from app import logging as mlog
+
+VERSION = 1
+MIN_SECRET = 32
+_CHANNEL_ID = re.compile(r"[a-z0-9]{26}")
+
+
+def path_from_env() -> str:
+    return os.path.join(os.getenv("MMB_DATA_DIR", "/data"), "bots.enc")
+
+
+class StoreError(Exception):
+    """code: store_key_missing | store_unreadable | store_invalid (save-time validation). detail: field/reason."""
+
+    def __init__(self, code: str, detail: str = ""):
+        super().__init__("%s: %s" % (code, detail) if detail else code)
+        self.code, self.detail = code, detail
+
+
+def _mask(s: str) -> str:
+    return "****" + s[-4:] if len(s) > 8 else "****"
+
+
+@dataclass
+class BotConfig:
+    token: str
+    wake_url: str
+    wake_secret: str
+    channels: list[str]
+    version: int = VERSION
+
+    def __repr__(self) -> str:  # never show token or secret
+        return "BotConfig(token=%s, wake_url=%r, wake_secret=****, channels=%r, version=%d)" % (
+            _mask(self.token), self.wake_url, self.channels, self.version)
+
+    __str__ = __repr__
+
+
+def validate(cfg: BotConfig) -> None:
+    """Raise ValueError(<field>: <reason>) unless cfg is a valid version-1 config (plan PR-6)."""
+    if cfg.version != VERSION:
+        raise ValueError("unsupported_version")
+    for f in ("token", "wake_url", "wake_secret"):
+        if not isinstance(getattr(cfg, f), str) or not getattr(cfg, f).strip():
+            raise ValueError("%s: required" % f)
+    if not https_ok(cfg.wake_url):
+        raise ValueError("wake_url: must be https")
+    if len(cfg.wake_secret) < MIN_SECRET:
+        raise ValueError("wake_secret: must be at least %d characters" % MIN_SECRET)
+    if (not isinstance(cfg.channels, list) or not cfg.channels
+            or not all(isinstance(c, str) and _CHANNEL_ID.fullmatch(c) for c in cfg.channels)):
+        raise ValueError("channels: must be a non-empty list of 26-char channel ids")
+
+
+def https_ok(url: str) -> bool:
+    if url.startswith("https://") and len(url) > 8:
+        return True
+    return os.getenv("LIVE_ALLOW_HTTP_WAKE", "").lower() == "true" and url.startswith("http://") and len(url) > 7
+
+
+def _keys(key: str | None) -> list[Fernet]:
+    keys = [k.strip() for k in (key or "").split(",") if k.strip()]
+    if not keys:
+        raise StoreError("store_key_missing")
+    try:
+        return [Fernet(k.encode()) for k in keys]
+    except (ValueError, TypeError):
+        raise StoreError("store_unreadable", "bad_key") from None
+
+
+def _decode(plain: bytes) -> BotConfig:
+    try:
+        doc = json.loads(plain)
+    except ValueError:
+        raise StoreError("store_unreadable", "format") from None
+    if not isinstance(doc, dict):
+        raise StoreError("store_unreadable", "format")
+    if doc.get("version") != VERSION:
+        raise StoreError("store_unreadable", "unsupported_version")
+    bot = doc.get("bot")
+    if not isinstance(bot, dict):
+        raise StoreError("store_unreadable", "bot: required")
+    try:
+        cfg = BotConfig(token=bot.get("token"), wake_url=bot.get("wake_url"), wake_secret=bot.get("wake_secret"),
+                        channels=bot.get("channels"), version=doc["version"])
+        validate(cfg)
+    except ValueError as e:
+        raise StoreError("store_unreadable", str(e)) from None
+    return cfg
+
+
+def _read(path: str, f: MultiFernet) -> tuple[bytes, BotConfig]:
+    try:
+        with open(path, "rb") as fh:
+            blob = fh.read()
+    except OSError:
+        raise StoreError("store_unreadable", "file") from None
+    try:
+        plain = f.decrypt(blob)
+    except InvalidToken:
+        raise StoreError("store_unreadable", "decrypt") from None
+    cfg = _decode(plain)
+    _register(cfg)
+    return blob, cfg
+
+
+def _register(cfg: BotConfig) -> None:
+    mlog.register_secret(cfg.token)
+    mlog.register_secret(cfg.wake_secret)
+
+
+def _write(path: str, data: bytes) -> None:
+    """Atomic replace: 0600 temp file in the same dir, fsync, rename."""
+    d = os.path.dirname(os.path.abspath(path))
+    fd, tmp = tempfile.mkstemp(dir=d, prefix=".bots.", suffix=".tmp")   # mkstemp creates 0600
+    try:
+        with os.fdopen(fd, "wb") as fh:
+            fh.write(data)
+            fh.flush()
+            os.fsync(fh.fileno())
+        os.chmod(tmp, 0o600)
+        os.replace(tmp, path)
+    except BaseException:
+        if os.path.exists(tmp):
+            os.unlink(tmp)
+        raise
+
+
+def load(path: str, key: str | None) -> BotConfig:
+    return _read(path, MultiFernet(_keys(key)))[1]
+
+
+def save(path: str, key: str | None, cfg: BotConfig) -> None:
+    f = MultiFernet(_keys(key))
+    try:
+        validate(cfg)
+    except ValueError as e:
+        raise StoreError("store_invalid", str(e)) from None
+    _register(cfg)
+    doc = {"version": cfg.version, "bot": {"token": cfg.token, "wake_url": cfg.wake_url,
+                                           "wake_secret": cfg.wake_secret, "channels": list(cfg.channels)} }
+    _write(path, f.encrypt(json.dumps(doc).encode()))
+
+
+def rotate(path: str, new_key: str | None, old_key: str | None) -> None:
+    """Re-encrypt the store with the first new key (readable with new or old keys); validated first; atomic, 0600."""
+    f = MultiFernet(_keys(new_key) + _keys(old_key))
+    blob, _ = _read(path, f)
+    _write(path, f.rotate(blob))
diff --git a/requirements.txt b/requirements.txt
index 6d6dcaf..fec4b37 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -2,3 +2,4 @@ fastapi==0.115.6
 uvicorn[standard]==0.34.0
 mcp==1.30.0
 httpx==0.28.1
+cryptography==50.0.2

exec
/bin/bash -lc 'cat app/mattermost.py; cat tests/unit/test_admin.py; cat tests/unit/test_store.py; cat .claude/skills/eng-resume/SKILL.md; cat AGENTS.md' in /mnt/d/rob/projects/mmbridge
 succeeded in 0ms:
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
import io
import logging
import os

import pytest
from cryptography.fernet import Fernet

from app import admin, store
from drivers.fake_mattermost import FakeMattermost

TOWN = "townsquareid0000000000000a"   # 26-char ids, as real Mattermost uses
DEV = "devchannelid00000000000000"
OPS = "opschannelid00000000000000"


def _reid(mm, cid, new):
    c = mm.channels.pop(cid)
    c["id"] = new
    mm.channels[new] = c


@pytest.fixture
def mm():
    m = FakeMattermost()
    m.add_user("eddie", bot=True)
    m.add_user("ada", bot=True)
    _reid(m, m.add_channel("main", "town-square", ["eddie"]), TOWN)
    _reid(m, m.add_channel("main", "dev", ["eddie"], ctype="P"), DEV)
    _reid(m, m.add_channel("main", "ops", ["ada"]), OPS)
    return m


@pytest.fixture
def env(tmp_path, monkeypatch):
    key = Fernet.generate_key().decode()
    monkeypatch.setenv("MMB_STORE_KEY", key)
    monkeypatch.setenv("MMB_DATA_DIR", str(tmp_path))
    monkeypatch.delenv("LIVE_ALLOW_HTTP_WAKE", raising=False)
    return {"key": key, "path": str(tmp_path / "bots.enc")}


def run(mm, *argv, stdin=""):
    out = io.StringIO()
    rc = admin.main(list(argv), stdin=io.StringIO(stdin), stdout=out, transport=mm.transport())
    return rc, out.getvalue()


def tok(mm, name="eddie"):
    return mm.user_by_name(name)["token"]


def set_bot(mm, channels="main/town-square,main/dev", url="https://wake.example/hook", stdin=None):
    return run(mm, "set-bot", "--token-stdin", "--wake-url", url, "--channels", channels,
               stdin=stdin if stdin is not None else tok(mm) + "\n")


def test_set_bot_stores_resolved_ids_and_prints_secret_once(mm, env, caplog):
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        rc, out = set_bot(mm)
    assert rc == 0, out
    cfg = store.load(env["path"], env["key"])
    assert cfg.token == tok(mm) and cfg.channels == [TOWN, DEV] and cfg.wake_url == "https://wake.example/hook"
    assert len(cfg.wake_secret) >= 32 and out.count(cfg.wake_secret) == 1
    assert tok(mm) not in out and tok(mm) not in caplog.text and cfg.wake_secret not in caplog.text
    assert "store_updated" in caplog.text
    for f in ("token", "wake_url", "wake_secret", "channels"):
        assert f in caplog.text
    assert not [c for c in mm.changes]   # never joins / changes the world


def test_show_masks_token_never_prints_secret(mm, env):
    set_bot(mm)
    cfg = store.load(env["path"], env["key"])
    rc, out = run(mm, "show")
    assert rc == 0
    assert tok(mm) not in out and cfg.wake_secret not in out
    assert tok(mm)[-4:] in out and TOWN in out and DEV in out and "https://wake.example/hook" in out


def test_non_member_channel_refused_without_join(mm, env):
    rc, out = set_bot(mm, channels="main/town-square,main/ops")
    assert rc != 0 and "not_member" in out
    assert not os.path.exists(env["path"])
    assert not [c for c in mm.calls if c[0] == "POST"] and mm.changes == []


def test_unknown_channel_refused(mm, env):
    rc, out = set_bot(mm, channels="main/nope")
    assert rc != 0 and "unknown_channel" in out and not os.path.exists(env["path"])


@pytest.mark.parametrize("ch", ["town-square", "main/", "/x", "a/b/c", ""])
def test_bad_channel_spec_refused(mm, env, ch):
    rc, out = set_bot(mm, channels=ch)
    assert rc != 0 and not os.path.exists(env["path"])


def test_http_wake_url_refused(mm, env):
    rc, out = set_bot(mm, url="http://wake.example/hook")
    assert rc != 0 and "https" in out and not os.path.exists(env["path"])
    assert mm.calls == []   # refused before touching Mattermost


def test_http_wake_url_allowed_with_test_flag(mm, env, monkeypatch):
    monkeypatch.setenv("LIVE_ALLOW_HTTP_WAKE", "true")
    rc, out = set_bot(mm, url="http://wake.example/hook")
    assert rc == 0, out


def test_bad_token_refused(mm, env):
    rc, out = set_bot(mm, stdin="wrong-token-xxxxxxxxxxxx\n")
    assert rc != 0 and "unauthorized" in out and "wrong-token" not in out
    assert not os.path.exists(env["path"])


def test_missing_key_refused(mm, env, monkeypatch):
    monkeypatch.delenv("MMB_STORE_KEY")
    rc, out = set_bot(mm)
    assert rc != 0 and "store_key_missing" in out and not os.path.exists(env["path"])


def test_supplied_wake_secret(mm, env):
    secret = "k" * 40
    rc, out = run(mm, "set-bot", "--token-stdin", "--wake-secret-stdin", "--wake-url", "https://w.example/h",
                  "--channels", "main/town-square", stdin="%s\n%s\n" % (tok(mm), secret))
    assert rc == 0, out
    assert store.load(env["path"], env["key"]).wake_secret == secret and secret not in out


def test_short_wake_secret_refused(mm, env):
    rc, out = run(mm, "set-bot", "--token-stdin", "--wake-secret-stdin", "--wake-url", "https://w.example/h",
                  "--channels", "main/town-square", stdin="%s\n%s\n" % (tok(mm), "k" * 31))
    assert rc != 0 and "wake_secret" in out and not os.path.exists(env["path"])


def test_show_without_store(mm, env):
    rc, out = run(mm, "show")
    assert rc != 0 and "store_unreadable" in out


def test_show_wrong_key(mm, env, monkeypatch):
    set_bot(mm)
    monkeypatch.setenv("MMB_STORE_KEY", Fernet.generate_key().decode())
    rc, out = run(mm, "show")
    assert rc != 0 and "store_unreadable" in out and tok(mm) not in out


def test_rotate_key_cli(mm, env, monkeypatch):
    set_bot(mm)
    new = Fernet.generate_key().decode()
    monkeypatch.setenv("NEWK", new)
    rc, out = run(mm, "rotate-key", "--new-key-env", "NEWK", "--old-key-env", "MMB_STORE_KEY")
    assert rc == 0, out
    assert new not in out and env["key"] not in out
    assert store.load(env["path"], new).token == tok(mm)


def test_rotate_key_missing_env(mm, env):
    set_bot(mm)
    rc, out = run(mm, "rotate-key", "--new-key-env", "NOPE_UNSET", "--old-key-env", "MMB_STORE_KEY")
    assert rc != 0 and "store_key_missing" in out
import logging
import os
import stat

import pytest
from cryptography.fernet import Fernet

from app import store
from app.store import BotConfig, StoreError

CH = "abcdefghijklmnopqrstuvwxyz"   # 26-char Mattermost id
TOKEN = "mmtoken-abcdefghijklmnop-9876"
SECRET = "s" * 43


def cfg(**kw):
    d = dict(token=TOKEN, wake_url="https://wake.example/hook", wake_secret=SECRET, channels=[CH])
    d.update(kw)
    return BotConfig(**d)


@pytest.fixture
def key():
    return Fernet.generate_key().decode()


@pytest.fixture
def path(tmp_path):
    return str(tmp_path / "bots.enc")


def _code(fn, *a):
    with pytest.raises(StoreError) as e:
        fn(*a)
    return e.value


def test_roundtrip(path, key):
    store.save(path, key, cfg())
    assert store.load(path, key) == cfg()


def test_file_is_ciphertext_mode_0600(path, key):
    store.save(path, key, cfg())
    raw = open(path, "rb").read()
    assert TOKEN.encode() not in raw and SECRET.encode() not in raw and b"wake.example" not in raw
    assert stat.S_IMODE(os.stat(path).st_mode) == 0o600
    assert os.listdir(os.path.dirname(path)) == ["bots.enc"]   # no tmp left behind


def test_wrong_key_unreadable(path, key):
    store.save(path, key, cfg())
    assert _code(store.load, path, Fernet.generate_key().decode()).code == "store_unreadable"


@pytest.mark.parametrize("k", [None, "", "  "])
def test_missing_key(path, key, k):
    store.save(path, key, cfg())
    assert _code(store.load, path, k).code == "store_key_missing"


def test_malformed_key_unreadable(path, key):
    store.save(path, key, cfg())
    assert _code(store.load, path, "not-a-fernet-key").code == "store_unreadable"


def test_missing_file_unreadable(path, key):
    assert _code(store.load, path, key).code == "store_unreadable"


def test_tamper_unreadable(path, key):
    store.save(path, key, cfg())
    raw = bytearray(open(path, "rb").read())
    raw[40] = ord("A") if raw[40] != ord("A") else ord("B")
    open(path, "wb").write(bytes(raw))
    assert _code(store.load, path, key).code == "store_unreadable"


def test_repr_masks_token_and_secret():
    r = repr(cfg()) + str(cfg())
    assert TOKEN not in r and SECRET not in r and "9876" in r


def test_store_error_carries_no_key_material(path, key):
    store.save(path, key, cfg())
    e = _code(store.load, path, Fernet.generate_key().decode())
    assert key not in str(e) and TOKEN not in str(e)


def _write_raw(path, key, obj):
    import json
    open(path, "wb").write(Fernet(key.encode()).encrypt(json.dumps(obj).encode()))


def _raw(**bot):
    b = {"token": TOKEN, "wake_url": "https://w.example/h", "wake_secret": SECRET, "channels": [CH]}
    b.update(bot)
    return b


@pytest.mark.parametrize("obj,detail", [
    ({"version": 2, "bot": _raw()}, "unsupported_version"),
    ({"version": 1, "bot": {k: v for k, v in _raw().items() if k != "token"} }, "token"),
    ({"version": 1, "bot": _raw(wake_secret="short")}, "wake_secret"),
    ({"version": 1, "bot": _raw(wake_url="http://w.example/h")}, "wake_url"),
    ({"version": 1, "bot": _raw(channels=["town-square"])}, "channels"),
    ({"version": 1, "bot": _raw(channels=[])}, "channels"),
    ({"version": 1}, "bot"),
    ([1, 2], "format"),
])
def test_load_validates(path, key, obj, detail):
    _write_raw(path, key, obj)
    e = _code(store.load, path, key)
    assert e.code == "store_unreadable" and detail in e.detail


def test_http_wake_allowed_only_with_test_flag(path, key, monkeypatch):
    _write_raw(path, key, {"version": 1, "bot": _raw(wake_url="http://w.example/h")})
    monkeypatch.setenv("LIVE_ALLOW_HTTP_WAKE", "true")
    assert store.load(path, key).wake_url == "http://w.example/h"


def test_save_validates_and_writes_nothing(path, key):
    e = _code(store.save, path, key, cfg(wake_secret="x" * 31))
    assert e.code == "store_invalid" and not os.path.exists(path)


# --- PR-7 key rotation (MultiFernet, ADR-0006) -------------------------------------
def test_rotate_key_roundtrip(path):
    old, new = Fernet.generate_key().decode(), Fernet.generate_key().decode()
    store.save(path, old, cfg())
    assert store.load(path, "%s,%s" % (new, old)) == cfg()       # MMB_STORE_KEY=new,old reads old file
    store.rotate(path, new, old)
    assert store.load(path, new) == cfg()
    assert _code(store.load, path, old).code == "store_unreadable"
    assert stat.S_IMODE(os.stat(path).st_mode) == 0o600


def test_rotate_with_wrong_old_key_leaves_file(path):
    old, new = Fernet.generate_key().decode(), Fernet.generate_key().decode()
    store.save(path, old, cfg())
    before = open(path, "rb").read()
    assert _code(store.rotate, path, new, Fernet.generate_key().decode()).code == "store_unreadable"
    assert open(path, "rb").read() == before


# --- REQ-A7: redaction of the stored token/secret in logs ---------------------------
def test_loaded_token_and_secret_redacted_in_logs(path, key, caplog):
    from app import logging as mlog
    mlog.setup()
    store.save(path, key, cfg())
    store.load(path, key)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        mlog.log.info("oops token=%s secret=%s", TOKEN, SECRET)
    assert TOKEN not in caplog.text and SECRET not in caplog.text and "[REDACTED]" in caplog.text
---
name: eng-resume
description: Cold-start any agent on a project. Use at the beginning of every session, before any other eng-* skill, or when taking over work from another agent.
---
# eng-resume

This skill is the standard session Start (`.eng/PROCESS.md` section 8). It ends by running the Next action's skill or eng-handoff; it doesn't call itself.

## Inputs (files only)
- `PROJECT_STATE.md`; the latest handoff it links; only that handoff's Critical References

## Outputs
- No new artifact; updates `PROJECT_STATE.md` (`owner_agent`, `date`) and Blockers if discrepancies are found

## Steps
1. Run `.eng/bin/eng-status .` and `.eng/bin/eng-check .`. Note the `readiness:` line and the working agreements (are you the planner or the implementer?).
2. Read PROJECT_STATE fully, then the latest handoff fully. Read its Critical References directly.
3. Verify the handoff's Recent changes exist (`git log`, `git status`, open the cited file:line).
4. If a pending approval is one the next skill needs, or readiness is NOT READY: report to Rob and stop (suggest eng-triage readiness check).
5. If `thoughts/shared/inbox.md` has items under `## Open` or `## Deferred`, mention the count to Rob ("N inbox items; say process incoming to go through them"). Do not process them unless asked (eng-inbox).
6. State: phase, next skill, discrepancies. Then run that skill in this session only if context is still small.

## Exit criteria
Agent can state the phase, next skill, and blockers from files alone; discrepancies recorded.

## Approval stop (Rob)
Stops if needed approvals are pending or the handoff contradicts the repo.
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

exec
/bin/bash -lc "cat thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md; cat docs/decisions/0006-encrypted-token-store.md; grep -n -E 'set-bot|wake.secret|overwrite|bot account|is_bot|rotation' docs/architecture/2026-10-26-live-bots.md thoughts/shared/plans/2026-10-27-live-bots.md; ls .venv/bin/python*; .venv/bin/pytest tests/unit -q" in /mnt/d/rob/projects/mmbridge
 succeeded in 11814ms:
---
id: SLICE-20261027-lb1-bot-store-admin-cli
type: slice
phase: implement
status: in-progress      # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
plan_phase: 1
review: required (security: stored token, ADR-0006) - thoughts/shared/verification/2026-10-27-lb1-review.md
reqs: [REQ-A7]
specs: none - no listener yet; REQ-A7 token-secrecy for store/CLI proven by unit tests, end-to-end spec test_bot_token_never_appears_in_logs_output_or_wakes turns green in slice 5
---
# Slice 1: Encrypted bot store + admin CLI

Plan: [thoughts/shared/plans/2026-10-27-live-bots.md](../plans/2026-10-27-live-bots.md) Phase 1. Architecture: docs/architecture/2026-10-26-live-bots.md. **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
Operator can `python -m app.admin set-bot/show` inside the container; config sits Fernet-encrypted at /data/bots.enc and the token never appears in output or logs.

## Acceptance criteria
- [x] `app/store.py`: `BotConfig` dataclass (token, wake_url, wake_secret, channels:list[str] ids, version=1); `load(path, key) -> BotConfig`, `save(path, key, cfg)` atomic (tmp+rename, mode 0600); `StoreError(code)` codes `store_key_missing`, `store_unreadable`; `__repr__` masks token+secret
- [x] `app/admin.py` (`python -m app.admin`): `set-bot --token-stdin --wake-url URL --channels team/chan,...` resolves names to ids via existing `app/mattermost.Client` (`/users/me`, channel by name, `members/me`) and refuses non-member channels (never joins); generates 32-byte wake secret printed once unless `--wake-secret-stdin`; `show` masks token to last 4, never prints secret; `wake_url` must be https (http only if `LIVE_ALLOW_HTTP_WAKE=true`, for tests)
- [x] Logs `store_updated` with field names only; `app/logging.py` redact filter extended to the stored token/secret
- [x] `requirements.txt`: pin `cryptography`; Dockerfile creates /data owned by uid 10001
- [x] No listener, no state DB, no HTTP surface change; `/health` unchanged
- [x] (PR-7) `admin rotate-key` via MultiFernet (ADR-0006); `MMB_STORE_KEY` accepts `new,old`; tests per plan Phase 1
- [x] (PR-6) Config validation on load/set-bot: version==1, required fields, https wake_url, channel id format, wake secret >= 32 chars; tests per plan Phase 1
- [x] Plan Phase 1 Automated Verification all exit 0; existing MCP suite (`.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`) still green

## Tasks
- [x] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red) - n/a, see specs:
- [x] Write failing unit tests (tests/unit/) for the behaviours above
- [x] Implement
- [x] Run Phase 1 automated verification (plan), including this slice's specs (now green)
- [x] Do not edit locked files: tests/acceptance/specs/**, DSL public interface (CP-C speclock)

## Size check
~180 lines + tests (actual: store 163 + admin 137 + logging +16; tests 330)

## Progress log
<!-- date - agent - what changed (file:line) -->
- 2026-10-27 - claude-code - red first: tests/unit/test_store.py + test_admin.py failed at collection (no app.store/app.admin).
- 2026-10-27 - claude-code - app/store.py (new, BotConfig/validate/load/save/rotate, MultiFernet, atomic 0600 via mkstemp+fsync+os.replace); app/admin.py (new, set-bot/show/rotate-key; reuses app/service._member_channel so never joins); app/logging.py register_secret + literal redaction; requirements.txt cryptography==50.0.2; Dockerfile /data 700 uid 10001. Commit cf78905.
- 2026-10-27 - claude-code - verification: `pytest tests/unit -q` 114 passed (exit 0; 43 new); `pytest tests/acceptance -q` 16 passed 9 skipped (exit 0); `eng-check .` OK exit 0; `eng-spec status .` matches lock; `docker build -t mmbridge:lb1 .` exit 0. Container smoke: /data drwx------ appuser; `admin show` with no store -> `store_unreadable: file`; http wake URL refused; saved file 0600, no plaintext.

## Blockers / deviations from plan
- Minor (detail-level, no plan conflict): `StoreError` has a third code `store_invalid` for save-time validation (load-time failures stay `store_unreadable: <reason>`); `StoreError.detail` carries the field/reason. Supplied wake secret comes in via `--wake-secret-stdin` (second stdin line) as in the card/architecture, not a `--wake-secret` argv flag (plan PR-6 wording), so it never lands in shell history. `rotate-key` defaults: `--new-key-env MMB_STORE_KEY_NEW`, `--old-key-env MMB_STORE_KEY`.
- Heads-up for lb4/lb5: PR-6 requires 26-char channel ids, but `FakeMattermost.add_channel` makes ids like `c-rmlab-dev`; test_admin re-ids channels locally. The live driver (admin CLI setup against the fake) will need 26-char ids in the fake.
---
id: ADR-0006
type: adr
phase: architecture
status: accepted         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-26
links: [docs/design/2026-10-26-live-bots.md, docs/architecture/2026-10-26-live-bots.md, docs/decisions/0001-credential-handoff-bearer-per-call.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0006: Encrypted token store (partially supersedes ADR-0001)

## Status
proposed

## Context
Design Q7 (Rob 2026-10-26): the Live bots listener must hold the bot's Mattermost token continuously, outside any MCP call, and changing the bot must not need a redeploy. ADR-0001 says tokens are never stored. That remains true for the MCP tool path; it cannot hold for the listener.

## Decision
We will store the one bot's config (token, wake URL, wake secret, chosen channel ids) in `/data/bots.enc`, a Fernet ciphertext (AES-128-CBC + HMAC-SHA256, `cryptography` package, new pinned dep) on the persistent volume, mode 0600. The key comes from env `MMB_STORE_KEY` (Coolify secret), never written to disk. Written only by the admin CLI (`python -m app.admin`) inside the container; no HTTP admin endpoint. Decrypted config is held in memory only; the token is never logged, returned, or placed in wake payloads. Key rotation: `admin rotate-key` re-encrypts (MultiFernet). This supersedes ADR-0001 only for the listener; the MCP path stays per-call bearer, never stored. On acceptance ADR-0001 gets a note "partially superseded by ADR-0006 (listener)".

## Consequences
Positive: no redeploy to change the bot; volume/backups leak only ciphertext. Negative: a long-lived secret now exists in the bridge; key+volume compromise exposes the token; operator needs container shell. Neutral: one bot in v1; format has `version` and a `bot` object so A6 can widen it to a list.

## Prediction (scored in a later eng-retro)
- Expected outcome: token never appears in logs, /health, tool output or wake payloads (tested); token rotation via CLI takes effect within 60 s without redeploy.
- Check date: after the Live bots v1 ship
- What would prove it wrong: a token string found in any log/output; Rob needs a redeploy to change the bot; key management proves too awkward in Coolify.
- Score: unscored
docs/architecture/2026-10-26-live-bots.md:18:| Token/bot store | app/store.py | encrypted file holding the ONE bot config: token, wake URL, wake secret, chosen channel ids (ADR-0006) |
docs/architecture/2026-10-26-live-bots.md:46:{"version":1,"bot":{"token":"<mm bot token>","wake_url":"https://...","wake_secret":"<32+ random bytes b64>","channels":["<channel_id>"]} }
docs/architecture/2026-10-26-live-bots.md:51:- `python -m app.admin set-bot --token-stdin --wake-url URL --channels team/chan,...` (wake secret generated and printed once, or `--wake-secret-stdin`)
docs/architecture/2026-10-26-live-bots.md:70:- `X-MMB-Signature: v1=<hex HMAC-SHA256(wake_secret, timestamp + "." + raw_body)>`
docs/architecture/2026-10-26-live-bots.md:179:3. Container terminal: `python -m app.admin set-bot ...` with bot token, wake URL, channels.
thoughts/shared/plans/2026-10-27-live-bots.md:28:With volume `/data`, `MMB_STORE_KEY`, bot set via `python -m app.admin set-bot`, and `LIVE_BOTS_ENABLED=true`: a post in a chosen channel or a DM to the bot produces exactly one signed wake at the configured URL within 10 s; own posts never wake; drops heal via resume or 15-min REST catch-up with no duplicates; receiver failures retry (5 attempts, 2-32 s) then appear in `admin failed`; no token in logs/output/payloads. Verified by `.venv/bin/pytest tests/acceptance --channel live -q` (9 specs) green against the container plus the existing 16 MCP specs and unit tests, and a live CP-S demo.
thoughts/shared/plans/2026-10-27-live-bots.md:50:class BotConfig: token: str; wake_url: str; wake_secret: str; channels: list[str]; version: int = 1
thoughts/shared/plans/2026-10-27-live-bots.md:92:- `app/admin.py` (new): `set-bot`, `show`; resolves `team/channel` to ids with `app/mattermost.Client`, refuses non-member channels, https-only wake URL, secret generated + printed once.
thoughts/shared/plans/2026-10-27-live-bots.md:93:- `app/logging.py`: redact stored token and wake secret; `store_updated` logs field names only.
thoughts/shared/plans/2026-10-27-live-bots.md:96:- (PR-6) Validation on `load` and `set-bot`: `version == 1` (else `store_unreadable: unsupported_version`), required fields non-empty, `wake_url` https (unless `LIVE_ALLOW_HTTP_WAKE`), `channels` list of 26-char ids, `wake_secret` >= 32 bytes of entropy (generated secrets 32 random bytes urlsafe; supplied `--wake-secret` < 32 chars refused).
thoughts/shared/plans/2026-10-27-live-bots.md:99:- [x] `.venv/bin/pytest tests/unit -q` exit 0 incl. new `tests/unit/test_store.py` (roundtrip, wrong key -> store_unreadable, missing key, tamper, file mode 0600, repr masks) and `tests/unit/test_admin.py` (show masks to last 4, secret never printed after set, non-member channel refused with zero join calls, http wake URL refused, token absent from captured logs/stdout); (PR-7) rotate-key roundtrip: old-key file readable with `new,old`, after rotate readable with new only, old alone -> store_unreadable, file mode stays 0600; (PR-6) load rejects version 2, missing field, short secret, http url, malformed channel id; set-bot refuses `--wake-secret` shorter than 32
thoughts/shared/plans/2026-10-27-live-bots.md:104:- [ ] Rob (local or Coolify terminal): `set-bot` with a real bot token -> `show` displays masked token and channel ids; `xxd /data/bots.enc | head` shows no plaintext.
thoughts/shared/plans/2026-10-27-live-bots.md:194:2. Container terminal: `echo "$TOKEN" | python -m app.admin set-bot --token-stdin --wake-url https://<receiver> --channels main/town-square`; note the printed wake secret into the receiver.
.venv/bin/python
.venv/bin/python3
.venv/bin/python3.12
........................................................................ [ 63%]
..........................................                               [100%]
114 passed in 7.12s

exec
/bin/bash -lc '.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q; python3 .eng/bin/eng-check .; git diff 691f4ac50697a044175d0eab19f61e6aaffc8483 -- tests/unit/test_store.py tests/unit/test_admin.py >/tmp/mmbridge-review-tests.diff' in /mnt/d/rob/projects/mmbridge
exec
/bin/bash -lc 'python3 .eng/bin/eng-check .' in /mnt/d/rob/projects/mmbridge
 succeeded in 1122ms:
eng-check: OK - 0 error(s), 0 warning(s), 71 artifact(s) checked

codex
No actionable regressions were identified in the changes. All 114 unit tests passed, and the repository checks completed without errors or warnings.
No actionable regressions were identified in the changes. All 114 unit tests passed, and the repository checks completed without errors or warnings.
````
