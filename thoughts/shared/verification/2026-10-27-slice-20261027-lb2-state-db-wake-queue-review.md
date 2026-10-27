---
id: REVIEW-20261027-slice-20261027-lb2-state-db-wake-queue-review
type: review-findings
phase: verify
status: addressed
owner_agent: eng-run
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md, thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md]
review_kind: slice
subject: "SLICE-20261027-lb2-state-db-wake-queue (thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md)"
diff: 37e7131...6551dd9
reviewer: codex
command: "codex review --base 37e7131"
run_log: thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb2-state-db-wake-queue.md
---
# Independent review: code-review slice-20261027-lb2-state-db-wake-queue
<!-- Written by eng-run (prompt code-review v2). Each finding row starts 'open': set disposition fixed (where) |
     accepted-risk (ONLY with Rob's approval, e.g. "Rob 2026-10-27") | rejected (reason). Plan reviews gate
     implementation (medium/large); slice reviews are advisory. -->

## Findings
| # | Severity | Location | Finding | Disposition | Reason / approval |
|---|---|---|---|---|---|
| 1 | P2 (medium) | tests/unit/test_state.py:242 | `os.geteuid` in skipif decorator raises AttributeError at collection on native Windows | fixed (dc9efe0: `os.name != "posix" or os.geteuid() == 0`) | short-circuits before geteuid; Windows chmod can't enforce dir perms anyway |

eng-run's parser reported "No findings"; finding 1 transcribed by hand from the raw output below.

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
session id: 01a17c2e-4204-70c2-97c4-b3644fec87fa
--------
user
changes against '37e7131'
exec
/bin/bash -lc 'cat PROJECT_STATE.md; cat .eng/PROCESS.md; git status --short; git diff --stat 37e7131bbc19003e1fbacca710f23773a9567ec2' in /mnt/d/rob/projects/mmbridge
 succeeded in 595ms:
---
id: STATE
type: project-state
phase: implement
status: active
owner_agent: claude-code
date: 2026-10-27
links: []
triage: large             # unset | small | medium | large
active_slice: SLICE-20261027-lb2-state-db-wake-queue
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
[SLICE-20261027-lb2-state-db-wake-queue](thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md) (todo). Previous: lb1 [done](thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md)

## Next action
lb1 done (CP-S logged; live container check deferred until redeploy). NEXT: implementer runs eng-run implement on lb2 (SLICE-20261027-lb2-state-db-wake-queue), then planner runs eng-verify. Deploy prerequisites before enabling: Coolify volume /data (uid 10001), env MMB_STORE_KEY, replicas 1.

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
- Latest handoff: [thoughts/shared/handoffs/2026-10-27_01-37-10_lb1-implemented-awaiting-verify.md](thoughts/shared/handoffs/2026-10-27_01-37-10_lb1-implemented-awaiting-verify.md)
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
?? thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb2-state-db-wake-queue.running.md
?? thoughts/shared/runs/2026-10-27-implement-slice-20261027-lb2-state-db-wake-queue.running.md
 CHANGELOG.md                                       |   4 +
 app/admin.py                                       |  47 +++-
 app/state.py                                       | 272 +++++++++++++++++++++
 tests/unit/test_admin.py                           |  47 ++++
 tests/unit/test_state.py                           | 258 +++++++++++++++++++
 .../slices/2026-10-27-lb2-state-db-wake-queue.md   |   2 +-
 6 files changed, 624 insertions(+), 6 deletions(-)

exec
/bin/bash -lc 'cat thoughts/shared/handoffs/2026-10-27_01-37-10_lb1-implemented-awaiting-verify.md; python3 .eng/bin/eng-check .; find . -name AGENTS.md -o -name AGENTS.override.md; git diff 37e7131bbc19003e1fbacca710f23773a9567ec2 -- app tests/unit' in /mnt/d/rob/projects/mmbridge
 succeeded in 2404ms:
---
id: HANDO-20261027-lb1-implemented-awaiting-verify
type: handoff
phase: implement
status: complete
owner_agent: claude-code
date: 2026-10-27T01:37:10-05:00
links: [thoughts/shared/plans/2026-10-27-live-bots.md, thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md]
git_commit: cf78905
branch: main
next_skill: eng-verify
---
# Handoff: lb1 implemented, awaiting verify
<!-- Session handoff (agent to agent, one session). -->

## Task(s)
- SLICE-20261027-lb1-bot-store-admin-cli (plan Phase 1): **completed, status review**. Test-first; all Phase 1 automated verification exit 0. Manual verification (CP-S) pending Rob.

## Critical References
- thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md (progress log, deviations)
- thoughts/shared/plans/2026-10-27-live-bots.md Phase 1
- docs/decisions/0006-encrypted-token-store.md

## Recent changes
- app/store.py:39 `BotConfig` (masked `__repr__`), :53 `validate` (PR-6), :75 `_keys` (comma list -> MultiFernet), :126 `_write` (mkstemp 0600 + fsync + os.replace), :143 `load`, :147 `save`, :159 `rotate` (PR-7)
- app/admin.py:74 `set-bot` (token from stdin, optional `--wake-secret-stdin` second line, https check before any MM call, resolves via `app/service._member_channel` = never joins, logs `store_updated` field names), :104 `show`, :110 `rotate-key`, :116 `main(argv, stdin, stdout, transport)`
- app/logging.py `register_secret` + literal redaction in `RedactFilter`/`_redact`
- requirements.txt `cryptography==50.0.2`; Dockerfile `/data` 700 owned by 10001
- tests/unit/test_store.py, tests/unit/test_admin.py (43 tests); commit cf78905

## Learnings
- `FakeMattermost` channel ids (`c-team-name`) fail the PR-6 26-char id rule; test_admin re-ids channels locally. lb4 live driver (admin CLI setup against the fake) will need 26-char ids in the fake.
- Store registers the token/secret with the log redact filter on every load/save, so any later component that loads the store (listener, dispatcher) gets redaction for free.

## Artifacts
- app/store.py, app/admin.py, app/logging.py, requirements.txt, Dockerfile, CHANGELOG.md (Unreleased Added)
- tests/unit/test_store.py, tests/unit/test_admin.py
- thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md, thoughts/shared/plans/2026-10-27-live-bots.md (Phase 1 automated boxes ticked)
- thoughts/shared/verification/2026-10-27-slice-20261027-lb1-bot-store-admin-cli-review.md (Codex: no findings; addressed)
- thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb1-bot-store-admin-cli.md

## Approvals
- Pending (planner to request): `CP-S: thoughts/shared/slices/2026-10-27-lb1-bot-store-admin-cli.md - manual verification` (set-bot with real token -> show masked; `xxd /data/bots.enc` no plaintext).
- None granted this session.

## Action Items & Next Steps
1. Planner: eng-verify on lb1 (re-run Phase 1 automated checks; review the minor deviations in the slice card: `store_invalid` code, `--wake-secret-stdin` instead of argv flag, rotate-key env defaults).
2. Request CP-S from Rob with the manual step. Do not start lb2 before CP-S.
3. Not pushed (push_permission standing applies only after eng-verify PASS).

## Other Notes
- Untracked files left as found: thoughts/shared/inbox.md (empty Open/Deferred), thoughts/shared/inbox-local-bak-1793080755/.
eng-check: OK - 0 error(s), 0 warning(s), 76 artifact(s) checked
./.eng/templates/AGENTS.md
./AGENTS.md
diff --git a/app/admin.py b/app/admin.py
index 4914a0d..da46cb7 100644
--- a/app/admin.py
+++ b/app/admin.py
@@ -1,8 +1,9 @@
-"""Operator CLI for the live bot (ADR-0006): `python -m app.admin set-bot | show | rotate-key`.
+"""Operator CLI for the live bot (ADR-0006/0009): `python -m app.admin set-bot | show | rotate-key | failed | stats`.
 
 Run inside the container (Coolify terminal). The token is read from stdin only and never printed or logged;
 the wake secret is printed once when generated, never by `show`. Channels are resolved by name to ids with the
-bot's own token and must already include the bot (REQ-7: never joins).
+bot's own token and must already include the bot (REQ-7: never joins). `failed`/`stats` read state.db and
+never print message text.
 """
 import argparse
 import asyncio
@@ -10,9 +11,10 @@ import json
 import os
 import secrets
 import sys
+import time
 
 from app import logging as mlog
-from app import store
+from app import state, store
 from app.errors import ToolError
 from app.mattermost import MATTERMOST_URL, Client, MMError
 from app.service import _member_channel
@@ -40,6 +42,9 @@ def _parser() -> argparse.ArgumentParser:
     r = sub.add_parser("rotate-key", help="re-encrypt the store with a new MMB_STORE_KEY")
     r.add_argument("--new-key-env", default="MMB_STORE_KEY_NEW", help="env var holding the new key")
     r.add_argument("--old-key-env", default="MMB_STORE_KEY", help="env var holding the current key(s)")
+    f = sub.add_parser("failed", help="list failed wakes, or requeue one")
+    f.add_argument("--retry", metavar="POST_ID", help="requeue this failed wake for delivery")
+    sub.add_parser("stats", help="wake counts and post->delivered latency")
     return p
 
 
@@ -113,6 +118,34 @@ def _rotate_key(a, out) -> None:
     print("store re-encrypted with %s; set MMB_STORE_KEY to that key" % a.new_key_env, file=out)
 
 
+def _failed(a, out) -> None:
+    st = state.State(state.path_from_env())
+    if a.retry:
+        if not st.requeue(a.retry):
+            raise AdminError("not_found", "no failed wake %s" % a.retry)
+        mlog.log.info(json.dumps({"event": "wake_requeued", "post_id": a.retry}))
+        print("requeued %s" % a.retry, file=out)
+        return
+    rows = st.failed()
+    if not rows:
+        print("no failed wakes", file=out)
+    for w in rows:
+        at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(w.updated_at))
+        print("%s  channel %s  attempts %d  error %s  at %s" % (w.post_id, w.channel_id, w.attempts,
+                                                              w.last_error or "-", at), file=out)
+
+
+def _stats(out) -> None:
+    s = state.State(state.path_from_env()).stats()
+    if not s["counts"]:
+        print("no wakes yet", file=out)
+        return
+    for k in sorted(s["counts"]):
+        print("%s: %d" % (k, s["counts"][k]), file=out)
+    lat = s["latency_ms"]
+    print("latency post->delivered (ms): n=%d p50=%s p95=%s" % (lat["n"], lat["p50"], lat["p95"]), file=out)
+
+
 def main(argv=None, stdin=None, stdout=None, transport=None) -> int:
     mlog.setup()
     stdin, out = stdin or sys.stdin, stdout or sys.stdout
@@ -122,9 +155,13 @@ def main(argv=None, stdin=None, stdout=None, transport=None) -> int:
             _set_bot(a, stdin, out, transport)
         elif a.cmd == "show":
             _show(out)
-        else:
+        elif a.cmd == "rotate-key":
             _rotate_key(a, out)
-    except (AdminError, store.StoreError) as e:
+        elif a.cmd == "failed":
+            _failed(a, out)
+        else:
+            _stats(out)
+    except (AdminError, store.StoreError, state.StateError) as e:
         print("error: %s%s" % (e.code, ": " + e.detail if e.detail else ""), file=out)
         return 1
     except OSError as e:
diff --git a/app/state.py b/app/state.py
new file mode 100644
index 0000000..c164945
--- /dev/null
+++ b/app/state.py
@@ -0,0 +1,272 @@
+"""Listener state on the persistent volume (ADR-0009): /data/state.db, SQLite in WAL mode.
+
+`wakes` is both the at-most-once ledger (INSERT OR IGNORE on post_id is the single enqueue gate) and the
+delivery queue: queued|retry -> in_flight (claimed by one dispatcher, with a lease) -> delivered|failed.
+`cursors` holds the forward-only (create_at, post_id) per channel; `meta` holds ws state and the dispatcher
+owner heartbeat. No tokens or secrets are stored; message text is, and terminal rows are pruned after 7 days.
+Blocking stdlib sqlite3: async callers use asyncio.to_thread. One connection per State, guarded by a lock.
+"""
+import json
+import math
+import os
+import sqlite3
+import threading
+import time
+import uuid
+from contextlib import contextmanager
+from dataclasses import dataclass
+
+DAY = 86400
+LEASE_S = 30          # in_flight lease; recover_stale returns expired leases to retry
+OWNER_TTL_S = 60      # dispatcher owner heartbeat freshness
+TERMINAL = ("delivered", "failed")
+
+_SCHEMA = """
+CREATE TABLE IF NOT EXISTS wakes (
+  post_id TEXT PRIMARY KEY,
+  channel_id TEXT NOT NULL,
+  payload_json TEXT NOT NULL,
+  status TEXT NOT NULL CHECK (status IN ('queued','retry','in_flight','delivered','failed')),
+  attempts INTEGER NOT NULL DEFAULT 0,
+  next_at INTEGER NOT NULL,
+  last_error TEXT,
+  claimed_by TEXT,
+  lease_until INTEGER,
+  post_create_at INTEGER,
+  delivered_at INTEGER,
+  created_at INTEGER NOT NULL,
+  updated_at INTEGER NOT NULL
+);
+CREATE INDEX IF NOT EXISTS wakes_due ON wakes (status, next_at);
+CREATE TABLE IF NOT EXISTS cursors (
+  channel_id TEXT PRIMARY KEY,
+  last_create_at INTEGER NOT NULL,
+  last_post_id TEXT NOT NULL
+);
+CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
+"""
+
+
+def path_from_env() -> str:
+    return os.path.join(os.getenv("MMB_DATA_DIR", "/data"), "state.db")
+
+
+def next_delay(attempt: int) -> float:
+    """Backoff after the given (1-based) failed attempt: 2, 4, 8, 16, 32 s, times WAKE_BACKOFF_SCALE (tests)."""
+    return 2 ** min(max(attempt, 1), 5) * float(os.getenv("WAKE_BACKOFF_SCALE", "1.0"))
+
+
+class StateError(Exception):
+    """code: state_unwritable. detail: sqlite reason (no secrets in state)."""
+
+    def __init__(self, code: str, detail: str = ""):
+        super().__init__("%s: %s" % (code, detail) if detail else code)
+        self.code, self.detail = code, detail
+
+
+@dataclass
+class Wake:
+    post_id: str
+    channel_id: str
+    payload: dict
+    status: str
+    attempts: int
+    next_at: int
+    last_error: str | None
+    claimed_by: str | None
+    lease_until: int | None
+    post_create_at: int | None
+    delivered_at: int | None
+    created_at: int
+    updated_at: int
+
+
+_COLS = ("post_id, channel_id, payload_json, status, attempts, next_at, last_error, claimed_by, lease_until, "
+         "post_create_at, delivered_at, created_at, updated_at")
+
+
+def _wake(row) -> Wake:
+    r = list(row)
+    r[2] = json.loads(r[2])
+    return Wake(*r)
+
+
+class State:
+    def __init__(self, path: str, instance_id: str | None = None, clock=time.time, max_attempts: int | None = None):
+        self.instance_id = instance_id or uuid.uuid4().hex
+        self.clock = clock
+        self.max_attempts = max_attempts or int(os.getenv("WAKE_MAX_ATTEMPTS", "5"))
+        self._lock = threading.Lock()
+        try:
+            self._conn = sqlite3.connect(path, timeout=10, isolation_level=None, check_same_thread=False)
+            self._conn.execute("PRAGMA journal_mode=WAL")
+            self._conn.executescript(_SCHEMA)
+            self.set_meta("schema_version", "1")      # write probe: read-only db/dir fails here
+        except sqlite3.Error as e:
+            raise StateError("state_unwritable", str(e)) from None
+
+    def close(self) -> None:
+        self._conn.close()
+
+    def _now(self) -> int:
+        return int(self.clock())
+
+    @contextmanager
+    def _tx(self):
+        with self._lock:
+            self._conn.execute("BEGIN IMMEDIATE")
+            try:
+                yield self._conn
+            except BaseException:
+                self._conn.execute("ROLLBACK")
+                raise
+            self._conn.execute("COMMIT")
+
+    # --- enqueue / cursors ---------------------------------------------------------------------------------
+    def _insert(self, c, post_id, channel_id, payload, post_create_at) -> bool:
+        now = self._now()
+        cur = c.execute("INSERT OR IGNORE INTO wakes (post_id, channel_id, payload_json, status, next_at, "
+                        "post_create_at, created_at, updated_at) VALUES (?,?,?,'queued',?,?,?,?)",
+                        (post_id, channel_id, json.dumps(payload), now, post_create_at, now, now))
+        return cur.rowcount == 1
+
+    def _advance(self, c, channel_id: str, create_at: int, post_id: str) -> None:
+        c.execute("INSERT INTO cursors (channel_id, last_create_at, last_post_id) VALUES (?,?,?) "
+                  "ON CONFLICT(channel_id) DO UPDATE SET last_create_at=excluded.last_create_at, "
+                  "last_post_id=excluded.last_post_id "
+                  "WHERE (excluded.last_create_at, excluded.last_post_id) > (last_create_at, last_post_id)",
+                  (channel_id, create_at, post_id))
+
+    def enqueue(self, post_id: str, channel_id: str, payload: dict, post_create_at: int | None = None) -> bool:
+        """True if newly queued; False if post_id was already seen (the dedupe gate)."""
+        with self._tx() as c:
+            return self._insert(c, post_id, channel_id, payload, post_create_at)
+
+    def enqueue_and_advance(self, post_id: str, channel_id: str, payload: dict, create_at: int) -> bool:
+        """enqueue + forward-only cursor move in one transaction (PR-3)."""
+        with self._tx() as c:
+            new = self._insert(c, post_id, channel_id, payload, create_at)
+            self._advance(c, channel_id, create_at, post_id)
+            return new
+
+    def get_cursor(self, channel_id: str) -> tuple[int, str] | None:
+        with self._lock:
+            row = self._conn.execute("SELECT last_create_at, last_post_id FROM cursors WHERE channel_id=?",
+                                     (channel_id,)).fetchone()
+        return tuple(row) if row else None
+
+    def set_cursor(self, channel_id: str, create_at: int, post_id: str = "") -> None:
+        with self._tx() as c:
+            self._advance(c, channel_id, create_at, post_id)
+
+    # --- meta ------------------------------------------------------------------------------------------------
+    def get_meta(self, key: str) -> str | None:
+        with self._lock:
+            row = self._conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
+        return row[0] if row else None
+
+    def set_meta(self, key: str, value: str) -> None:
+        with self._tx() as c:
+            c.execute("INSERT INTO meta (key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
+                      (key, value))
+
+    def claim_owner(self, now: int, ttl: int = OWNER_TTL_S) -> bool:
+        """Become (or stay, as heartbeat) the single dispatcher owner; refused while another owner is fresh."""
+        with self._tx() as c:
+            row = c.execute("SELECT value FROM meta WHERE key='dispatcher_owner'").fetchone()
+            if row:
+                cur = json.loads(row[0])
+                if cur["id"] != self.instance_id and now - cur["ts"] < ttl:
+                    return False
+            c.execute("INSERT INTO meta (key, value) VALUES ('dispatcher_owner', ?) "
+                      "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
+                      (json.dumps({"id": self.instance_id, "ts": now}),))
+            return True
+
+    # --- dispatcher queue ------------------------------------------------------------------------------------
+    def claim_due(self, now: int, limit: int = 4) -> list[Wake]:
+        """Atomically flip up to `limit` due queued/retry rows to in_flight for this instance (PR-1)."""
+        with self._tx() as c:
+            rows = c.execute(
+                "UPDATE wakes SET status='in_flight', claimed_by=?, lease_until=?, attempts=attempts+1, updated_at=? "
+                "WHERE post_id IN (SELECT post_id FROM wakes WHERE status IN ('queued','retry') AND next_at<=? "
+                "ORDER BY next_at, rowid LIMIT ?) RETURNING rowid, " + _COLS,
+                (self.instance_id, now + LEASE_S, self._now(), now, limit)).fetchall()
+        rows.sort(key=lambda r: (r[6], r[0]))
+        return [_wake(r[1:]) for r in rows]
+
+    def _mine(self, c, post_id: str):
+        return c.execute("SELECT attempts FROM wakes WHERE post_id=? AND status='in_flight' AND claimed_by=?",
+                         (post_id, self.instance_id)).fetchone()
+
+    def mark_delivered(self, post_id: str) -> bool:
+        now = self.clock()
+        with self._tx() as c:
+            return c.execute("UPDATE wakes SET status='delivered', delivered_at=?, claimed_by=NULL, lease_until=NULL, "
+                             "updated_at=? WHERE post_id=? AND status='in_flight' AND claimed_by=?",
+                             (int(now * 1000), int(now), post_id, self.instance_id)).rowcount == 1
+
+    def mark_failed(self, post_id: str, err: str) -> bool:
+        with self._tx() as c:
+            return c.execute("UPDATE wakes SET status='failed', last_error=?, claimed_by=NULL, lease_until=NULL, "
+                             "updated_at=? WHERE post_id=? AND status='in_flight' AND claimed_by=?",
+                             (err, self._now(), post_id, self.instance_id)).rowcount == 1
+
+    def mark_retry(self, post_id: str, err: str, next_at: int) -> str | None:
+        """'retry', or 'failed' once attempts reached max_attempts; None if not claimed by this instance."""
+        with self._tx() as c:
+            row = self._mine(c, post_id)
+            if not row:
+                return None
+            status = "failed" if row[0] >= self.max_attempts else "retry"
+            c.execute("UPDATE wakes SET status=?, last_error=?, next_at=?, claimed_by=NULL, lease_until=NULL, "
+                      "updated_at=? WHERE post_id=?", (status, err, next_at, self._now(), post_id))
+            return status
+
+    def recover_stale(self, now: int) -> int:
+        """Return in_flight rows whose lease expired (crashed dispatcher) to retry, due now."""
+        with self._tx() as c:
+            return c.execute("UPDATE wakes SET status='retry', claimed_by=NULL, lease_until=NULL, next_at=?, "
+                             "updated_at=? WHERE status='in_flight' AND lease_until < ?",
+                             (now, self._now(), now)).rowcount
+
+    def requeue(self, post_id: str) -> bool:
+        """Operator retry of a failed wake: fresh attempts, due now."""
+        with self._tx() as c:
+            return c.execute("UPDATE wakes SET status='queued', attempts=0, next_at=?, last_error=NULL, "
+                             "updated_at=? WHERE post_id=? AND status='failed'",
+                             (self._now(), self._now(), post_id)).rowcount == 1
+
+    def prune(self, days: int = 7) -> int:
+        """Delete delivered/failed rows older than `days`; never touches queued/retry/in_flight (PR-8)."""
+        with self._tx() as c:
+            return c.execute("DELETE FROM wakes WHERE status IN ('delivered','failed') AND updated_at < ?",
+                             (self._now() - days * DAY,)).rowcount
+
+    # --- reads -----------------------------------------------------------------------------------------------
+    def _select(self, where: str = "", args=()) -> list[Wake]:
+        with self._lock:
+            rows = self._conn.execute("SELECT %s FROM wakes %s ORDER BY rowid" % (_COLS, where), args).fetchall()
+        return [_wake(r) for r in rows]
+
+    def wake(self, post_id: str) -> Wake | None:
+        rows = self._select("WHERE post_id=?", (post_id,))
+        return rows[0] if rows else None
+
+    def wakes(self) -> list[Wake]:
+        return self._select()
+
+    def failed(self) -> list[Wake]:
+        return self._select("WHERE status='failed'")
+
+    def stats(self) -> dict:
+        """Counts per status and post->delivered latency (delivered_at - post_create_at, ms; PR-9)."""
+        with self._lock:
+            counts = dict(self._conn.execute("SELECT status, COUNT(*) FROM wakes GROUP BY status").fetchall())
+            lat = sorted(r[0] for r in self._conn.execute(
+                "SELECT delivered_at - post_create_at FROM wakes WHERE status='delivered' "
+                "AND delivered_at IS NOT NULL AND post_create_at IS NOT NULL"))
+
+        def pct(p):
+            return lat[max(math.ceil(p * len(lat)) - 1, 0)] if lat else None
+        return {"counts": counts, "latency_ms": {"n": len(lat), "p50": pct(0.5), "p95": pct(0.95)} }
diff --git a/tests/unit/test_admin.py b/tests/unit/test_admin.py
index e8cafcc..7fa3d94 100644
--- a/tests/unit/test_admin.py
+++ b/tests/unit/test_admin.py
@@ -159,3 +159,50 @@ def test_rotate_key_missing_env(mm, env):
     set_bot(mm)
     rc, out = run(mm, "rotate-key", "--new-key-env", "NOPE_UNSET", "--old-key-env", "MMB_STORE_KEY")
     assert rc != 0 and "store_key_missing" in out
+
+
+# --- lb2: failed / stats (state.db) ---
+
+def _state(env):
+    from app.state import State
+    import os
+    return State(os.path.join(os.path.dirname(env["path"]), "state.db"), instance_id="d1")
+
+
+def test_failed_and_stats_on_empty_db(mm, env):
+    rc, out = run(mm, "failed")
+    assert rc == 0 and "no failed wakes" in out
+    rc, out = run(mm, "stats")
+    assert rc == 0 and "no wakes yet" in out
+
+
+def test_failed_lists_and_retry_requeues(mm, env):
+    s = _state(env)
+    s.enqueue("postfailed1", TOWN, {"message": "hello there"})
+    s.enqueue("postok", TOWN, {})
+    s.claim_due(2_000_000_000)
+    s.mark_failed("postfailed1", "http_401")
+    rc, out = run(mm, "failed")
+    assert rc == 0 and "postfailed1" in out and "http_401" in out and TOWN in out
+    assert "postok" not in out and "hello there" not in out          # message text not echoed
+    rc, out = run(mm, "failed", "--retry", "postfailed1")
+    assert rc == 0 and "requeued postfailed1" in out
+    assert s.wake("postfailed1").status == "queued"
+    rc, out = run(mm, "failed", "--retry", "postfailed1")
+    assert rc == 1 and "not_found" in out
+
+
+def test_stats_counts_and_latency(mm, env):
+    s = _state(env)
+    s.enqueue("a", TOWN, {}, post_create_at=0)
+    s.enqueue("b", TOWN, {})
+    s.claim_due(2_000_000_000)
+    s.mark_delivered("a")
+    rc, out = run(mm, "stats")
+    assert rc == 0 and "delivered: 1" in out and "in_flight: 1" in out and "p95" in out
+
+
+def test_failed_unwritable_data_dir(mm, env, monkeypatch, tmp_path):
+    monkeypatch.setenv("MMB_DATA_DIR", str(tmp_path / "missing"))
+    rc, out = run(mm, "failed")
+    assert rc == 1 and "state_unwritable" in out
diff --git a/tests/unit/test_state.py b/tests/unit/test_state.py
new file mode 100644
index 0000000..7b24ffa
--- /dev/null
+++ b/tests/unit/test_state.py
@@ -0,0 +1,258 @@
+import os
+import sqlite3
+import stat
+import threading
+
+import pytest
+
+from app import state
+from app.state import State, StateError
+
+DAY = 86400
+CH = "townsquareid0000000000000a"
+
+
+@pytest.fixture
+def clock():
+    class Clock:
+        t = 1_800_000_000.0
+
+        def __call__(self):
+            return self.t
+    return Clock()
+
+
+@pytest.fixture
+def db(tmp_path, clock):
+    return State(str(tmp_path / "state.db"), instance_id="d1", clock=clock)
+
+
+def now(clock):
+    return int(clock())
+
+
+def test_enqueue_dedupes_on_post_id(db):
+    assert db.enqueue("p1", CH, {"message": "hi"}) is True
+    assert db.enqueue("p1", CH, {"message": "other"}) is False
+    rows = db.wakes()
+    assert len(rows) == 1 and rows[0].payload == {"message": "hi"} and rows[0].status == "queued"
+
+
+def test_wal_and_schema_has_no_secret_columns(db, tmp_path):
+    con = sqlite3.connect(str(tmp_path / "state.db"))
+    assert con.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
+    tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
+    assert {"wakes", "cursors", "meta"} <= set(tables)
+    for t in tables:
+        for col in con.execute("PRAGMA table_info(%s)" % t):
+            assert "token" not in col[1].lower() and "secret" not in col[1].lower()
+
+
+def test_claim_due_respects_next_at_and_marks_in_flight(db, clock):
+    db.enqueue("p1", CH, {})
+    db.enqueue("p2", CH, {})
+    assert [w.post_id for w in db.claim_due(now(clock))] == ["p1", "p2"]
+    w = db.wake("p1")
+    assert w.status == "in_flight" and w.claimed_by == "d1" and w.lease_until == now(clock) + state.LEASE_S
+    assert w.attempts == 1
+    assert db.claim_due(now(clock)) == []                        # in_flight not re-claimable
+    db.mark_retry("p1", "http_503", now(clock) + 2)
+    assert db.claim_due(now(clock)) == []                        # not due yet
+    assert [w.post_id for w in db.claim_due(now(clock) + 2)] == ["p1"]
+
+
+def test_claim_due_limit(db, clock):
+    for i in range(6):
+        db.enqueue("p%d" % i, CH, {})
+    assert len(db.claim_due(now(clock), limit=4)) == 4
+    assert len(db.claim_due(now(clock), limit=4)) == 2
+
+
+def test_retry_then_failed_after_max_attempts(tmp_path, clock):
+    db = State(str(tmp_path / "s.db"), instance_id="d1", clock=clock, max_attempts=3)
+    db.enqueue("p1", CH, {})
+    t = now(clock)
+    for _ in range(2):
+        (w,) = db.claim_due(t)
+        assert db.mark_retry("p1", "http_503", t) == "retry"
+    (w,) = db.claim_due(t)
+    assert w.attempts == 3
+    assert db.mark_retry("p1", "http_503", t) == "failed"
+    w = db.wake("p1")
+    assert w.status == "failed" and w.last_error == "http_503" and w.claimed_by is None
+    assert db.claim_due(t + 999) == []
+
+
+def test_mark_failed_and_requeue(db, clock):
+    db.enqueue("p1", CH, {})
+    db.claim_due(now(clock))
+    assert db.mark_failed("p1", "http_401") is True
+    assert [w.post_id for w in db.failed()] == ["p1"]
+    assert db.requeue("p1") is True
+    w = db.wake("p1")
+    assert w.status == "queued" and w.attempts == 0 and w.next_at <= now(clock)
+    assert db.failed() == []
+    assert db.requeue("p1") is False                              # only failed rows
+    assert db.requeue("nope") is False
+
+
+def test_mark_with_wrong_claimer_is_noop(db, tmp_path, clock):
+    other = State(str(tmp_path / "state.db"), instance_id="d2", clock=clock)
+    db.enqueue("p1", CH, {})
+    db.claim_due(now(clock))
+    assert other.mark_delivered("p1") is False
+    assert other.mark_failed("p1", "x") is False
+    assert other.mark_retry("p1", "x", 0) is None
+    assert db.wake("p1").status == "in_flight"
+    assert db.mark_delivered("p1") is True
+    assert db.wake("p1").status == "delivered"
+
+
+def test_concurrent_claimers_never_share_a_post(tmp_path, clock):
+    path = str(tmp_path / "state.db")
+    State(path, clock=clock).close()
+    seed = State(path, clock=clock)
+    for i in range(200):
+        seed.enqueue("p%03d" % i, CH, {})
+    got: dict[str, list[str]] = {"a": [], "b": [], "c": []}
+
+    def worker(name):
+        s = State(path, instance_id=name, clock=clock)
+        while True:
+            batch = s.claim_due(now(clock), limit=3)
+            if not batch:
+                break
+            got[name].extend(w.post_id for w in batch)
+        s.close()
+    ts = [threading.Thread(target=worker, args=(n,)) for n in got]
+    for t in ts:
+        t.start()
+    for t in ts:
+        t.join()
+    allp = got["a"] + got["b"] + got["c"]
+    assert len(allp) == 200 and len(set(allp)) == 200
+    for name, ids in got.items():
+        assert all(seed.wake(p).claimed_by == name for p in ids)
+
+
+def test_recover_stale_returns_expired_leases_only(db, clock):
+    db.enqueue("old", CH, {})
+    db.claim_due(now(clock))
+    clock.t += 20
+    db.enqueue("new", CH, {})
+    db.claim_due(now(clock))
+    assert db.recover_stale(now(clock) + 15) == 1                  # old lease ended at t0+30, new at t0+50
+    old, new = db.wake("old"), db.wake("new")
+    assert old.status == "retry" and old.claimed_by is None and old.next_at <= now(clock) + 15
+    assert new.status == "in_flight" and new.claimed_by == "d1"
+    assert db.mark_delivered("old") is False                       # lease lost
+    assert [w.post_id for w in db.claim_due(now(clock) + 15)] == ["old"]
+
+
+def test_dispatcher_owner_heartbeat(tmp_path, clock):
+    path = str(tmp_path / "state.db")
+    a = State(path, instance_id="A", clock=clock)
+    b = State(path, instance_id="B", clock=clock)
+    t = now(clock)
+    assert a.claim_owner(t) is True
+    assert b.claim_owner(t + 10) is False                          # A's heartbeat fresh
+    assert a.claim_owner(t + 50) is True                           # heartbeat
+    assert b.claim_owner(t + 50 + state.OWNER_TTL_S - 1) is False
+    assert b.claim_owner(t + 50 + state.OWNER_TTL_S) is True       # expired -> taken over
+    assert a.claim_owner(t + 50 + state.OWNER_TTL_S + 1) is False
+
+
+def test_enqueue_and_advance_is_atomic(db, monkeypatch):
+    assert db.enqueue_and_advance("p1", CH, {}, 1000) is True
+    assert db.get_cursor(CH) == (1000, "p1")
+
+    def boom(*a, **k):
+        raise RuntimeError("injected")
+    monkeypatch.setattr(db, "_advance", boom)
+    with pytest.raises(RuntimeError):
+        db.enqueue_and_advance("p2", CH, {}, 2000)
+    assert db.wake("p2") is None and db.get_cursor(CH) == (1000, "p1")
+
+
+def test_cursor_only_moves_forward(db):
+    assert db.get_cursor(CH) is None
+    db.set_cursor(CH, 2000, "pb")
+    db.set_cursor(CH, 1000, "pz")                                  # older: ignored
+    assert db.get_cursor(CH) == (2000, "pb")
+    db.set_cursor(CH, 2000, "pa")                                  # same ts, smaller id: ignored
+    assert db.get_cursor(CH) == (2000, "pb")
+    db.set_cursor(CH, 2000, "pc")                                  # same ts, larger id: advances
+    assert db.get_cursor(CH) == (2000, "pc")
+    assert db.enqueue_and_advance("pold", CH, {}, 500) is True     # late post still enqueued, cursor kept
+    assert db.get_cursor(CH) == (2000, "pc")
+
+
+def test_meta(db):
+    assert db.get_meta("connection_id") is None
+    db.set_meta("connection_id", "abc")
+    db.set_meta("connection_id", "def")
+    assert db.get_meta("connection_id") == "def"
+
+
+def test_prune_terminal_only(db, clock):
+    for p in ("del", "fail", "r", "inf"):
+        db.enqueue(p, CH, {})
+    db.claim_due(now(clock), limit=10)
+    db.enqueue("q", CH, {})
+    db.mark_delivered("del")
+    db.mark_failed("fail", "x")
+    db.mark_retry("r", "x", now(clock))
+    clock.t += 6 * DAY
+    assert db.prune(7) == 0
+    clock.t += DAY + 1
+    assert db.prune(7) == 2
+    assert sorted(w.post_id for w in db.wakes()) == ["inf", "q", "r"]
+
+
+def test_delivered_latency_from_post_create_at(db, clock):
+    t_ms = int(clock() * 1000)
+    db.enqueue("p1", CH, {}, post_create_at=t_ms - 3000)
+    db.enqueue("p2", CH, {}, post_create_at=t_ms - 1000)
+    clock.t += 100                                                  # enqueue time must not matter
+    db.claim_due(now(clock))
+    db.mark_delivered("p1")
+    db.mark_delivered("p2")
+    assert db.wake("p1").delivered_at == int(clock() * 1000)
+    s = db.stats()
+    assert s["counts"] == {"delivered": 2}
+    assert s["latency_ms"] == {"n": 2, "p50": 101000, "p95": 103000}
+
+
+def test_stats_empty(db):
+    assert db.stats() == {"counts": {}, "latency_ms": {"n": 0, "p50": None, "p95": None} }
+
+
+def test_next_delay(monkeypatch):
+    assert [state.next_delay(a) for a in range(1, 6)] == [2, 4, 8, 16, 32]
+    monkeypatch.setenv("WAKE_BACKOFF_SCALE", "0.5")
+    assert state.next_delay(3) == 4
+
+
+def test_max_attempts_env(tmp_path, monkeypatch):
+    assert State(str(tmp_path / "a.db")).max_attempts == 5
+    monkeypatch.setenv("WAKE_MAX_ATTEMPTS", "7")
+    assert State(str(tmp_path / "b.db")).max_attempts == 7
+
+
+@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory permissions")
+def test_unwritable_dir(tmp_path):
+    ro = tmp_path / "ro"
+    ro.mkdir()
+    ro.chmod(stat.S_IRUSR | stat.S_IXUSR)
+    try:
+        with pytest.raises(StateError) as e:
+            State(str(ro / "state.db"))
+        assert e.value.code == "state_unwritable"
+    finally:
+        ro.chmod(0o700)
+
+
+def test_missing_dir(tmp_path):
+    with pytest.raises(StateError) as e:
+        State(str(tmp_path / "nope" / "state.db"))
+    assert e.value.code == "state_unwritable"

exec
/bin/bash -lc "cat thoughts/shared/slices/2026-10-27-lb2-state-db-wake-queue.md; cat docs/decisions/0009-listener-state-persistence.md; cat .claude/skills/eng-resume/SKILL.md; cat AGENTS.md; rg 'geteuid|recover_stale|claim_due' tests app; ls .venv/bin/python*" in /mnt/d/rob/projects/mmbridge
 succeeded in 0ms:
---
id: SLICE-20261027-lb2-state-db-wake-queue
type: slice
phase: implement
status: in-progress      # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
plan_phase: 2
review: required (persistence/dedupe correctness, ADR-0009) - thoughts/shared/verification/2026-10-27-lb2-review.md
reqs: [REQ-A4, REQ-A8]
specs: none - no event source/receiver yet; at-most-once ledger and retry bookkeeping proven by unit tests; specs for A4/A8 turn green in slices 4-5
---
# Slice 2: State DB + wake queue

Plan: [thoughts/shared/plans/2026-10-27-live-bots.md](../plans/2026-10-27-live-bots.md) Phase 2. Architecture: docs/architecture/2026-10-26-live-bots.md. **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
`app/state.py` gives a SQLite (WAL) ledger: enqueue a wake once per post id, claim due wakes, mark delivered/retry/failed, cursors, meta; `admin failed`/`admin stats` read it.

## Acceptance criteria
- [x] `app/state.py`: `State(path)`; schema per architecture (`wakes`, `cursors`, `meta`); `enqueue(post_id, channel_id, payload) -> bool` (INSERT OR IGNORE: the single dedupe gate); `claim_due(now, limit) -> list[Wake]`; `mark_delivered`, `mark_retry(post_id, err, next_at)`, `mark_failed(post_id, err)`; `requeue(post_id)`; `get/set_cursor`; `get/set_meta`; `prune(older_than_days=7)`; no tokens/secrets columns
- [x] Backoff helper `next_delay(attempt) -> 2,4,8,16,32 s`, `WAKE_MAX_ATTEMPTS` default 5
- [x] `app/admin.py`: `failed [--retry POST_ID]`, `stats` (counts, p95 enqueue->delivered latency)
- [x] Unwritable /data -> `StateError('state_unwritable')`
- [x] (PR-1) Atomic `claim_due` (BEGIN IMMEDIATE + in_flight + claimed_by + lease), `recover_stale`, claimer-checked `mark_*`, `meta.dispatcher_owner` heartbeat; concurrency/crash tests per plan Phase 2
- [x] (PR-3) `enqueue_and_advance` atomic enqueue+cursor, cursor `(create_at, post_id)` forward-only
- [x] (PR-9) store `post_create_at`/`delivered_at`; `stats` latency = delivered_at - post_create_at
- [x] (PR-8) `prune(7)` terminal-only; tests keep non-terminal rows
- [x] Plan Phase 2 Automated Verification all exit 0; existing MCP suite (`.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`) still green

## Tasks
- [x] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red) - n/a, see specs:
- [x] Write failing unit tests (tests/unit/) for the behaviours above
- [x] Implement
- [x] Run Phase 2 automated verification (plan), including this slice's specs (now green)
- [x] Do not edit locked files: tests/acceptance/specs/**, DSL public interface (CP-C speclock)

## Size check
~170 lines + tests

## Progress log
<!-- date - agent - what changed (file:line) -->
- 2026-10-27 - claude-code - specs: none (n/a). Wrote tests first: tests/unit/test_state.py (20 tests) + 4 admin tests in tests/unit/test_admin.py; red = `ImportError: cannot import name 'state'` / argparse exit 2 for `failed`/`stats`.
- 2026-10-27 - claude-code - app/state.py (new): schema + WAL + write probe (`State.__init__`, StateError('state_unwritable')); `enqueue` INSERT OR IGNORE; `enqueue_and_advance` + `_advance` forward-only `(create_at, post_id)` row-value compare; `claim_due` BEGIN IMMEDIATE + `UPDATE ... RETURNING` (in_flight, claimed_by, lease_until=now+30, attempts+1); claimer-checked `mark_delivered|mark_failed|mark_retry` (mark_retry -> 'failed' at max_attempts); `recover_stale`; `requeue` (failed only); `claim_owner` (meta.dispatcher_owner heartbeat, TTL 60 s); `prune` terminal-only; `stats` counts + p50/p95 of delivered_at - post_create_at (ms); `next_delay` 2..32 s x WAKE_BACKOFF_SCALE; WAKE_MAX_ATTEMPTS default 5.
- 2026-10-27 - claude-code - app/admin.py: `failed [--retry POST_ID]` (never prints message text; unknown/non-failed -> `not_found`), `stats` ("no wakes yet" on empty DB); StateError -> `error: state_unwritable`. Commit 6551dd9.
- 2026-10-27 - claude-code - Phase 2 automated verification: `.venv/bin/pytest tests/unit -q` exit 0 (138 passed); `.venv/bin/pytest tests/acceptance -q` exit 0 (16 passed, 9 live skipped); `python3 .eng/bin/eng-check .` exit 0; `python3 .eng/bin/eng-spec status .` matches lock. Concurrency/owner/stale tests run 5x, stable.

## Blockers / deviations from plan
- Status values follow plan PR-1 (`queued|retry|in_flight|delivered|failed`), not the older architecture CHECK (`pending|delivered|failed`).
- Cursor API follows PR-3 (`(create_at, post_id)`) rather than the plan's earlier key signature: `get_cursor -> (create_at, post_id) | None`, `set_cursor(channel_id, create_at, post_id="")`.
- Additions not named in the plan signature block: `State(path, instance_id=None, clock=time.time, max_attempts=None)`; `enqueue(..., post_create_at=None)`; `claim_owner(now, ttl=60)` for the dispatcher heartbeat; read helpers `wake`, `wakes`, `failed`, `stats`; `mark_retry` returns 'retry'|'failed'|None.
- `attempts` is incremented at claim time (so the claimed Wake carries the attempt number for the lb4 payload); a stale lease recovered by `recover_stale` counts as an attempt.
- `mark_failed` is claimer-checked; lb4's `bot_rotated` (failing queued rows not claimed) will need its own method.
- Size: app/state.py ~250 lines (estimate ~170) because of PR-1/3/8/9 additions.
---
id: ADR-0009
type: adr
phase: architecture
status: accepted         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-26
links: [docs/design/2026-10-26-live-bots.md, docs/architecture/2026-10-26-live-bots.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0009: Listener state in SQLite on a persistent volume

## Status
proposed

## Context
REQ-A4 needs at-most-once delivery and catch-up across reconnects and restarts; REQ-A8 needs a durable failure record. Today all state is in memory and no volume exists (research Q5, OQ2).

## Decision
We will keep `/data/state.db` (stdlib `sqlite3`, WAL, via `asyncio.to_thread`) with tables `wakes` (post_id PK = dedupe ledger + delivery queue), `cursors` (per-channel last create_at) and `meta` (connection_id, seq, single-listener lease). `INSERT OR IGNORE` on post_id is the only enqueue gate for both socket and catch-up. Terminal rows pruned after 7 days. A Coolify persistent volume at `/data` writable by uid 10001 is a required deploy prerequisite; without it the listener refuses to start (MCP unaffected). Rejected: Postgres/Redis (extra service), in-memory (loses dedupe on restart).

## Consequences
Positive: zero new services; durable dedupe and queue. Negative: needs a volume; single writer means one replica. Neutral: residual duplicate if the process dies between receiver 2xx and marking delivered - mitigated by the `X-MMB-Delivery` idempotency key.

## Prediction (scored in a later eng-retro)
- Expected outcome: 0 duplicate wakes from the bridge over 7 days including at least one restart.
- Check date: 7 days after v1 is enabled
- What would prove it wrong: SQLite lock errors under load, or duplicate wakes logged after restarts.
- Score: unscored
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
app/state.py:LEASE_S = 30          # in_flight lease; recover_stale returns expired leases to retry
app/state.py:    def claim_due(self, now: int, limit: int = 4) -> list[Wake]:
app/state.py:    def recover_stale(self, now: int) -> int:
tests/unit/test_admin.py:    s.claim_due(2_000_000_000)
tests/unit/test_admin.py:    s.claim_due(2_000_000_000)
tests/unit/test_state.py:def test_claim_due_respects_next_at_and_marks_in_flight(db, clock):
tests/unit/test_state.py:    assert [w.post_id for w in db.claim_due(now(clock))] == ["p1", "p2"]
tests/unit/test_state.py:    assert db.claim_due(now(clock)) == []                        # in_flight not re-claimable
tests/unit/test_state.py:    assert db.claim_due(now(clock)) == []                        # not due yet
tests/unit/test_state.py:    assert [w.post_id for w in db.claim_due(now(clock) + 2)] == ["p1"]
tests/unit/test_state.py:def test_claim_due_limit(db, clock):
tests/unit/test_state.py:    assert len(db.claim_due(now(clock), limit=4)) == 4
tests/unit/test_state.py:    assert len(db.claim_due(now(clock), limit=4)) == 2
tests/unit/test_state.py:        (w,) = db.claim_due(t)
tests/unit/test_state.py:    (w,) = db.claim_due(t)
tests/unit/test_state.py:    assert db.claim_due(t + 999) == []
tests/unit/test_state.py:    db.claim_due(now(clock))
tests/unit/test_state.py:    db.claim_due(now(clock))
tests/unit/test_state.py:            batch = s.claim_due(now(clock), limit=3)
tests/unit/test_state.py:def test_recover_stale_returns_expired_leases_only(db, clock):
tests/unit/test_state.py:    db.claim_due(now(clock))
tests/unit/test_state.py:    db.claim_due(now(clock))
tests/unit/test_state.py:    assert db.recover_stale(now(clock) + 15) == 1                  # old lease ended at t0+30, new at t0+50
tests/unit/test_state.py:    assert [w.post_id for w in db.claim_due(now(clock) + 15)] == ["old"]
tests/unit/test_state.py:    db.claim_due(now(clock), limit=10)
tests/unit/test_state.py:    db.claim_due(now(clock))
tests/unit/test_state.py:@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory permissions")
.venv/bin/python
.venv/bin/python3
.venv/bin/python3.12

exec
/bin/bash -lc "nl -ba .eng/PROCESS.md | sed -n '170,190p'; nl -ba tests/unit/test_state.py | tail -25; .venv/bin/pytest tests/unit -q; python3 .eng/bin/eng-check ." in /mnt/d/rob/projects/mmbridge
 succeeded in 10608ms:
   170	
   171	## 13. Executable specifications (v2.5; Dave Farley's ATDD four-layer model)
   172	**Two kinds of "spec", one direction.** *Design-side specs* (the design doc, the architecture doc, ADRs) say **what**
   173	to build and **how** to build it; they are the authority. *Executable specs* are the **test-side** expression of the
   174	design doc's requirements (REQ-n) and its plain-language acceptance examples: pytest tests in domain language under
   175	`tests/acceptance/specs/`, each pointing back at its requirement with `@pytest.mark.req("REQ-n")` (the design doc's
   176	id). They never introduce requirements; a spec without a REQ, or a REQ without a spec, is a gap to fix in the design
   177	doc or the specs.
   178	
   179	**Four layers** (`.eng/templates/acceptance/`, copied by `eng-spec init`):
   180	1. **Specs** (`specs/`): what, never how; no URLs, selectors, status codes or sleeps; each creates its own data.
   181	2. **DSL** (`dsl.py`): the shared domain vocabulary; aliases names per run (functional and temporal isolation).
   182	3. **Protocol drivers** (`drivers/`): `api` (httpx), `ui` (Playwright), `mcp`. All system knowledge lives here.
   183	4. **System under test**: deployed like production, started outside the tests; external systems stubbed at its boundary.
   184	
   185	**By size.** Small: unchanged (unit/regression tests; no executable specs). Medium: specs on the API channel.
   186	Large: API channel plus one Playwright web journey (`@pytest.mark.channels("api", "ui")`), with an ADR from
   187	`.eng/templates/adr-acceptance-tests.md`.
   188	
   189	**Approvals.**
   190	- **CP-A:** Rob approves the plain-language Given/When/Then examples in the design doc's "Acceptance examples".
   234	
   235	
   236	def test_max_attempts_env(tmp_path, monkeypatch):
   237	    assert State(str(tmp_path / "a.db")).max_attempts == 5
   238	    monkeypatch.setenv("WAKE_MAX_ATTEMPTS", "7")
   239	    assert State(str(tmp_path / "b.db")).max_attempts == 7
   240	
   241	
   242	@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory permissions")
   243	def test_unwritable_dir(tmp_path):
   244	    ro = tmp_path / "ro"
   245	    ro.mkdir()
   246	    ro.chmod(stat.S_IRUSR | stat.S_IXUSR)
   247	    try:
   248	        with pytest.raises(StateError) as e:
   249	            State(str(ro / "state.db"))
   250	        assert e.value.code == "state_unwritable"
   251	    finally:
   252	        ro.chmod(0o700)
   253	
   254	
   255	def test_missing_dir(tmp_path):
   256	    with pytest.raises(StateError) as e:
   257	        State(str(tmp_path / "nope" / "state.db"))
   258	    assert e.value.code == "state_unwritable"
........................................................................ [ 52%]
..................................................................       [100%]
138 passed in 5.88s
eng-check: OK - 0 error(s), 0 warning(s), 76 artifact(s) checked

exec
/bin/bash -lc "nl -ba AGENTS.md | sed -n '11,15p'" in /mnt/d/rob/projects/mmbridge
 succeeded in 0ms:
    11	
    12	**Start here:** read `PROJECT_STATE.md`, then the latest handoff it links. Do not rely on chat history.
    13	Process: eng-process kit; canonical copy at `.eng/PROCESS.md` (phases, checkpoints, skill for each phase in section 3, session convention in section 8). Run `.eng/bin/eng-check .` before and after each session.
    14	**The kit is vendored in this repo:** skills are in `.claude/skills/eng-*/SKILL.md` (Claude Code loads them as project skills; other agents read them as files) and the scripts are in `.eng/bin/` (plain Python 3, run through the interpreter from the repo root: `python3 .eng/bin/eng-check .`; native Windows: `python .eng/bin/eng-check .` or `py .eng/bin/eng-check .`). Do not look for the kit elsewhere; if `.eng/bin` or `.claude/skills` is missing, ask the planner to run `<kit>/bin/eng-init <repo> --upgrade`.
    15	

codex
The new test breaks unit-test collection on native Windows. On Linux, all 138 unit tests passed and eng-check reported no errors or warnings.

Review comment:

- [P2] Guard the Unix-only permission test on Windows — /mnt/d/rob/projects/mmbridge/tests/unit/test_state.py:242-242
  On native Windows, `os.geteuid` does not exist, so evaluating this decorator raises `AttributeError` during collection and prevents the unit suite from running. Native Windows is an explicitly supported workflow ([AGENTS.md:14](AGENTS.md#L14)). Skip this Unix permission test on Windows using a platform guard that short-circuits before calling `os.geteuid`; Windows `chmod` also cannot enforce the directory permissions this test requires.
The new test breaks unit-test collection on native Windows. On Linux, all 138 unit tests passed and eng-check reported no errors or warnings.

Review comment:

- [P2] Guard the Unix-only permission test on Windows — /mnt/d/rob/projects/mmbridge/tests/unit/test_state.py:242-242
  On native Windows, `os.geteuid` does not exist, so evaluating this decorator raises `AttributeError` during collection and prevents the unit suite from running. Native Windows is an explicitly supported workflow ([AGENTS.md:14](AGENTS.md#L14)). Skip this Unix permission test on Windows using a platform guard that short-circuits before calling `os.geteuid`; Windows `chmod` also cannot enforce the directory permissions this test requires.
````
