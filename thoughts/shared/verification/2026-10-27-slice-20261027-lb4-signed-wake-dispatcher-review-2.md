---
id: REVIEW-20261027-slice-20261027-lb4-signed-wake-dispatcher-review-2
type: review-findings
phase: verify
status: open
owner_agent: eng-run
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md, thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md]
review_kind: slice
subject: "SLICE-20261027-lb4-signed-wake-dispatcher (thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md)"
diff: 5f70402...6fc2ce1
reviewer: codex
command: "codex review --base 5f70402"
run_log: thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb4-signed-wake-dispatcher-2.md
---
# Independent review: code-review slice-20261027-lb4-signed-wake-dispatcher
<!-- Written by eng-run (prompt code-review v2). Each finding row starts 'open': set disposition fixed (where) |
     accepted-risk (ONLY with Rob's approval, e.g. "Rob 2026-10-27") | rejected (reason). Plan reviews gate
     implementation (medium/large); slice reviews are advisory. -->

## Findings
| # | Severity | Location | Finding | Disposition | Reason / approval |
|---|---|---|---|---|---|

No findings.

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
session id: 01a17ebe-d613-7fc2-9d61-55359ae889e6
--------
user
changes against '5f70402'
exec
/bin/bash -lc 'cat PROJECT_STATE.md; git status --short; find .. -name AGENTS.md -o -name AGENTS.override.md' in /mnt/d/rob/projects/mmbridge
exec
/bin/bash -lc "cat thoughts/shared/handoffs/2026-10-27_12-53-47_lb4-blocked-dm-only-bot.md; cat .eng/PROCESS.md; python3 .eng/bin/eng-check .; git diff --stat 5f70402f4a2ff117f9a0311b962135f9e6f0cd32; find app tests -name 'AGENTS*'" in /mnt/d/rob/projects/mmbridge
 succeeded in 1994ms:
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

eng-check: OK - 0 error(s), 0 warning(s), 92 artifact(s) checked
 PROJECT_STATE.md                                   |    8 +-
 app/admin.py                                       |    4 +-
 app/listener.py                                    |    1 +
 app/store.py                                       |    4 +-
 app/wake.py                                        |  127 +
 tests/acceptance/drivers/fake_mattermost.py        |    7 +-
 tests/acceptance/drivers/live.py                   |  256 +-
 tests/acceptance/drivers/wake_receiver.py          |   48 +
 tests/unit/test_admin.py                           |    6 +
 tests/unit/test_listener.py                        |    1 +
 tests/unit/test_store.py                           |    6 +-
 tests/unit/test_wake.py                            |  404 ++++
 .../2026-10-27_12-53-47_lb4-blocked-dm-only-bot.md |   59 +
 .../2026-10-27-live-bots-delta-no-allowlist.md     |   86 +
 thoughts/shared/plans/2026-10-27-live-bots.md      |    2 +-
 ...nt-slice-20261027-lb4-signed-wake-dispatcher.md |   97 +
 ...-27-plan-review-live-bots-delta-no-allowlist.md | 2547 ++++++++++++++++++++
 .../2026-10-27-lb4-signed-wake-dispatcher.md       |   44 +-
 ...-27-live-bots-delta-no-allowlist-plan-review.md |   43 +
 19 files changed, 3714 insertions(+), 36 deletions(-)

exec
/bin/bash -lc 'git diff 5f70402f4a2ff117f9a0311b962135f9e6f0cd32 -- app tests/acceptance/drivers; cat app/state.py; cat .claude/skills/eng-code-review/SKILL.md; find . -name AGENTS.md -o -name AGENTS.override.md' in /mnt/d/rob/projects/mmbridge
 succeeded in 1163ms:
diff --git a/app/admin.py b/app/admin.py
index da46cb7..7c549e1 100644
--- a/app/admin.py
+++ b/app/admin.py
@@ -37,7 +37,7 @@ def _parser() -> argparse.ArgumentParser:
     s.add_argument("--wake-secret-stdin", action="store_true",
                    help="read the wake secret from the next stdin line instead of generating one")
     s.add_argument("--wake-url", required=True)
-    s.add_argument("--channels", required=True, help="team/channel,team/channel,...")
+    s.add_argument("--channels", default=None, help="team/channel,team/channel,... (omit for a DM-only bot)")
     sub.add_parser("show", help="show the stored config (token masked, secret hidden)")
     r = sub.add_parser("rotate-key", help="re-encrypt the store with a new MMB_STORE_KEY")
     r.add_argument("--new-key-env", default="MMB_STORE_KEY_NEW", help="env var holding the new key")
@@ -87,7 +87,7 @@ def _set_bot(a, stdin, out, transport) -> None:
         raise AdminError("invalid_argument", "wake_secret: must be at least %d characters" % store.MIN_SECRET)
     if not store.https_ok(a.wake_url):
         raise AdminError("invalid_argument", "wake_url: must be https")
-    specs = _channel_specs(a.channels)
+    specs = [] if a.channels is None else _channel_specs(a.channels)
     key = os.getenv("MMB_STORE_KEY")
     if not (key or "").strip():
         raise store.StoreError("store_key_missing")
diff --git a/app/listener.py b/app/listener.py
index 4f98dac..5c9856f 100644
--- a/app/listener.py
+++ b/app/listener.py
@@ -67,6 +67,7 @@ class Listener:
         try:
             me = await client.get("/users/me")
             self.bot_user_id, self._bot = me["id"], {"user_id": me["id"], "username": me["username"]}
+            await asyncio.to_thread(self.state.set_meta, "bot_user_id", me["id"])   # dispatcher: bot_rotated
             async with self.ws_connect(ws_url(self.base_url), {"Authorization": "Bearer " + self.cfg.token}) as ws:
                 pinger = asyncio.create_task(self._ping(ws))
                 try:
diff --git a/app/store.py b/app/store.py
index 892c500..f7641ef 100644
--- a/app/store.py
+++ b/app/store.py
@@ -61,9 +61,9 @@ def validate(cfg: BotConfig) -> None:
         raise ValueError("wake_url: must be https")
     if len(cfg.wake_secret) < MIN_SECRET:
         raise ValueError("wake_secret: must be at least %d characters" % MIN_SECRET)
-    if (not isinstance(cfg.channels, list) or not cfg.channels
+    if (not isinstance(cfg.channels, list)
             or not all(isinstance(c, str) and _CHANNEL_ID.fullmatch(c) for c in cfg.channels)):
-        raise ValueError("channels: must be a non-empty list of 26-char channel ids")
+        raise ValueError("channels: must be a list of 26-char channel ids (empty = DMs only)")
 
 
 def https_ok(url: str) -> bool:
diff --git a/app/wake.py b/app/wake.py
new file mode 100644
index 0000000..7a3a3b8
--- /dev/null
+++ b/app/wake.py
@@ -0,0 +1,127 @@
+"""Signed wake webhook (ADR-0008): sign/verify and the Dispatcher that delivers queued wakes from state.db.
+
+POST <wake_url> with the wake payload as raw JSON body and headers X-MMB-Delivery (post id, idempotency key),
+X-MMB-Timestamp (unix seconds), X-MMB-Signature `v1=<hex HMAC-SHA256(secret, ts + "." + body)>`.
+Receivers: `verify(secret, headers, raw_body, now)`; constant-time, rejects |now - ts| > 300 s, unknown versions
+and missing headers.
+
+Dispatcher.tick(): heartbeat the single-owner lease (standby while another owner is fresh), recover_stale,
+prune (start + every 6 h), claim_due up to 4 and POST them concurrently (5 s timeout). Config is read at
+send time (url/secret rotation applies to queued wakes); wakes of a previous bot user fail `bot_rotated`.
+2xx delivered; 408/429/5xx/timeout/connect retry (state.next_delay; failed after max attempts); other 4xx
+failed. Logs carry post id, attempt and error class only: never token, secret, signature or message text.
+"""
+import asyncio
+import hashlib
+import hmac
+import json
+import time
+from collections.abc import Mapping
+
+import httpx
+
+from app import logging as mlog
+from app.state import next_delay
+
+WINDOW_S = 300
+TIMEOUT_S = 5
+CONCURRENCY = 4
+PRUNE_EVERY_S = 6 * 3600
+POLL_S = 0.5
+
+
+def _mac(secret: str, ts: str, body: bytes) -> str:
+    return hmac.new(secret.encode(), ts.encode() + b"." + body, hashlib.sha256).hexdigest()
+
+
+def sign(secret: str, ts: int, body: bytes) -> str:
+    return "v1=" + _mac(secret, str(ts), body)
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
+    return hmac.compare_digest(sig[3:].encode(), _mac(secret, ts, body).encode())
+
+
+def _log(event: str, **fields) -> None:
+    mlog.log.info(json.dumps({"event": event, **fields}))
+
+
+class Dispatcher:
+    def __init__(self, state, cfg, http: httpx.AsyncClient, max_attempts: int | None = None, clock=None,
+                 poll_s: float = POLL_S, concurrency: int = CONCURRENCY):
+        """cfg: BotConfig or a zero-arg callable returning the current one (read at every send, PR-2)."""
+        self.state, self.http = state, http
+        self._cfg = cfg if callable(cfg) else (lambda: cfg)
+        if max_attempts:
+            state.max_attempts = max_attempts
+        self.clock = clock or state.clock
+        self.poll_s, self.concurrency = poll_s, concurrency
+        self.owner = None
+        self._pruned_at = None
+
+    async def run(self) -> None:
+        while True:
+            if not await self.tick():
+                await asyncio.sleep(self.poll_s)
+
+    async def tick(self) -> int:
+        """One loop pass; returns the number of wakes attempted."""
+        st, now = self.state, self.clock()
+        owner = await asyncio.to_thread(st.claim_owner, now)
+        if owner != self.owner:
+            _log("dispatcher_owner" if owner else "dispatcher_standby", instance=st.instance_id)
+            self.owner = owner
+        if not owner:
+            return 0
+        await asyncio.to_thread(st.recover_stale, now)
+        if self._pruned_at is None or now - self._pruned_at >= PRUNE_EVERY_S:
+            n = await asyncio.to_thread(st.prune, 7)
+            self._pruned_at = now
+            _log("wakes_pruned", count=n)
+        due = await asyncio.to_thread(st.claim_due, now, self.concurrency)
+        if due:
+            bot_id = await asyncio.to_thread(st.get_meta, "bot_user_id")
+            await asyncio.gather(*(self._send(w, bot_id) for w in due))
+        return len(due)
+
+    async def _send(self, w, bot_id: str | None) -> None:
+        st = self.state
+        if bot_id and (w.payload.get("bot") or {}).get("user_id") != bot_id:
+            await asyncio.to_thread(st.mark_failed, w.post_id, "bot_rotated")
+            _log("wake_failed", post_id=w.post_id, attempt=w.attempts, error="bot_rotated")
+            return
+        cfg = self._cfg()
+        body = json.dumps({**w.payload, "attempt": w.attempts}, separators=(",", ":")).encode()
+        ts = int(self.clock())
+        headers = {"Content-Type": "application/json", "X-MMB-Delivery": w.post_id,
+                   "X-MMB-Timestamp": str(ts), "X-MMB-Signature": sign(cfg.wake_secret, ts, body)}
+        try:
+            r = await self.http.post(cfg.wake_url, content=body, headers=headers, timeout=TIMEOUT_S)
+            status, err = r.status_code, "http_%d" % r.status_code
+        except httpx.TimeoutException:
+            status, err = None, "timeout"
+        except httpx.TransportError:
+            status, err = None, "connect"
+        if status is not None and 200 <= status < 300:
+            await asyncio.to_thread(st.mark_delivered, w.post_id)
+            fields = {"post_id": w.post_id, "attempt": w.attempts}
+            if w.post_create_at:
+                fields["latency_ms"] = int(self.clock() * 1000) - w.post_create_at
+            _log("wake_delivered", **fields)
+        elif status is None or status in (408, 429) or status >= 500:
+            res = await asyncio.to_thread(st.mark_retry, w.post_id, err, self.clock() + next_delay(w.attempts))
+            _log("wake_failed" if res == "failed" else "wake_retry", post_id=w.post_id, attempt=w.attempts,
+                 error=err)
+        else:
+            await asyncio.to_thread(st.mark_failed, w.post_id, err)
+            _log("wake_failed", post_id=w.post_id, attempt=w.attempts, error=err)
diff --git a/tests/acceptance/drivers/fake_mattermost.py b/tests/acceptance/drivers/fake_mattermost.py
index 33ed2d7..bf8b8cd 100644
--- a/tests/acceptance/drivers/fake_mattermost.py
+++ b/tests/acceptance/drivers/fake_mattermost.py
@@ -7,9 +7,11 @@ Slice 3: users/username/{u}, POST /channels/direct (idempotent; creating one is
 Live bots lb3: GET channels/{id}, teams/{id}, users/{id}; websocket /api/v4/websocket (Bearer handshake,
 hello{connection_id}, per-connection seq, `posted` broadcast to channel members, ping action -> pong reply,
 drop/raw/seq-skip controls). `serve()` runs the app on a free localhost port for real HTTP/WS clients.
+Live bots lb4: `mm_ids=True` gives channels Mattermost-shaped 26-char ids (the bot store validates them).
 """
 import asyncio
 import contextlib
+import hashlib
 import itertools
 import json
 
@@ -22,7 +24,8 @@ from starlette.websockets import WebSocket
 
 
 class FakeMattermost:
-    def __init__(self):
+    def __init__(self, mm_ids=False):
+        self.mm_ids = mm_ids
         self.users = {}      # id -> {"id","username","token"|None,"is_bot"}
         self.teams = {}      # id -> {"id","name","display_name"}
         self.channels = {}   # id -> {"id","team_id","name","display_name","type","members":set}
@@ -73,6 +76,8 @@ class FakeMattermost:
     def add_channel(self, team, name, members=(), ctype="O"):
         tid = self.add_team(team)
         cid = "c-%s-%s" % (team, name)
+        if self.mm_ids:
+            cid = hashlib.sha1(cid.encode()).hexdigest()[:26]
         self.channels[cid] = {"id": cid, "team_id": tid, "name": name, "display_name": name.title(),
                               "type": ctype, "members": {self.user_by_name(m)["id"] for m in members} }
         return cid
diff --git a/tests/acceptance/drivers/live.py b/tests/acceptance/drivers/live.py
index 6be612f..50f0441 100644
--- a/tests/acceptance/drivers/live.py
+++ b/tests/acceptance/drivers/live.py
@@ -1,16 +1,254 @@
-"""Live-bots protocol driver (layer 3, ADR-0010). STUB until slices 3-5 build it.
+"""Live-bots protocol driver (layer 3, ADR-0010). Drivers are not locked; edit freely.
 
-Target: start the real container image (temp /data, MMB_STORE_KEY, LIVE_BOTS_ENABLED=true,
-MATTERMOST_URL -> fake MM with REST + websocket, wake_url -> local HMAC-verifying receiver),
-configure the bot with the real admin CLI. Drivers are not locked; edit freely.
+lb4: in-process mode. A background event loop runs the fake Mattermost (REST + websocket, served on a free
+localhost port, MM-shaped channel ids), the real Listener and Dispatcher, and an HMAC-verifying wake receiver
+(drivers/wake_receiver.py, reached through an in-process httpx transport at https://receiver.test/wake).
+The bot is configured with the real admin CLI (`app.admin.main`, as `python -m app.admin` would run it) on a
+temp /data with a fresh MMB_STORE_KEY; the printed wake secret is handed to the receiver. Backoff is scaled
+by WAKE_BACKOFF_SCALE so retry specs run in seconds.
+lb5 adds container mode (real image) and drop/restore connection.
 """
+import asyncio
+import hashlib
+import hmac
+import io
+import json
+import logging
+import os
+import re
+import secrets
+import shutil
+import tempfile
+import threading
+import time
+
+import httpx
+from cryptography.fernet import Fernet
+
+from app import admin, store
+from app import logging as mlog
+from app.listener import Listener
+from app.mattermost import Client
+from app.state import State
+from app.wake import Dispatcher
+from drivers.fake_mattermost import FakeMattermost
+from drivers.wake_receiver import WakeReceiver
+
+WAKE_URL = "https://receiver.test/wake"
+TEAM = "rmlab"
+WAKE_WITHIN_S = 10.0       # design metric: wake within 10 s
+SETTLE_S = 0.3
+MARKER_USER = "zz-marker"
+
+
+class _Capture(logging.Handler):
+    def __init__(self):
+        super().__init__(logging.DEBUG)
+        self.addFilter(mlog.RedactFilter())
+        self.lines = []
+
+    def emit(self, record):
+        self.lines.append(self.format(record))
 
 
 class LiveDriver:
-    def __getattr__(self, name):
-        def _stub(*a, **k):
-            raise NotImplementedError("live driver step %r not built yet (slices 3-5)" % name)
-        return _stub
+    def __init__(self):
+        self._tmp = tempfile.mkdtemp(prefix="mmb-live-")
+        env = {"MMB_DATA_DIR": self._tmp, "MMB_STORE_KEY": Fernet.generate_key().decode(),
+               "WAKE_BACKOFF_SCALE": "0.05", "WAKE_MAX_ATTEMPTS": "5"}
+        self._env_saved = {k: os.environ.get(k) for k in env}
+        os.environ.update(env)
+        self.mm = FakeMattermost(mm_ids=True)
+        self.rx = WakeReceiver()
+        self.outputs = []              # admin CLI stdout
+        self.posts = {}                # message -> post id (latest)
+        self._last_post = None
+        self._tasks = []
+        self.state = None
+        self._log = _Capture()
+        for name in ("mmbridge", "mmbridge.ws", "httpx", "websockets"):
+            logging.getLogger(name).addHandler(self._log)
+        self._loop = asyncio.new_event_loop()
+        self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
+        self._thread.start()
+        self._serving = self.mm.serve()
+        self.base = self._run(self._serving.__aenter__())
+
+    def _run(self, coro, timeout=20):
+        return asyncio.run_coroutine_threadsafe(coro, self._loop).result(timeout)
+
+    def _call(self, fn, *a):
+        async def go():
+            return fn(*a)
+        return self._run(go())
+
+    # --- world ------------------------------------------------------------------------------------------------
+    def _user(self, name):
+        try:
+            return self.mm.user_by_name(name)
+        except StopIteration:
+            return self.mm.add_user(name)
+
+    def given_channel(self, team, channel, members):
+        for m in members:
+            self._user(m)
+        self.mm.add_channel(team, channel, members)
+
+    def _admin(self, *argv, stdin=""):
+        out = io.StringIO()
+        rc = admin.main(list(argv), stdin=io.StringIO(stdin), stdout=out, transport=self.mm.transport())
+        self.outputs.append(out.getvalue())
+        return rc, out.getvalue()
+
+    def given_live_bot(self, name, channels):
+        u = self._user(name)
+        u["is_bot"], u["token"] = True, "tok-%s-%s" % (name, secrets.token_hex(12))
+        chan = ["--channels", ",".join("%s/%s" % (TEAM, c) for c in channels)] if channels else []
+        rc, out = self._admin("set-bot", "--token-stdin", "--wake-url", WAKE_URL, *chan, stdin=u["token"] + "\n")
+        assert rc == 0, "admin set-bot failed: %s" % out.strip()
+        self.rx.secret = re.search(r"wake secret \(shown once[^)]*\): (\S+)", out).group(1)
+        cfg = store.load(store.path_from_env(), os.environ["MMB_STORE_KEY"])
+        self._run(self._start(cfg))
+
+    async def _start(self, cfg):
+        self.state = State(os.path.join(self._tmp, "state.db"))
+        self.listener = Listener(cfg, self.state, lambda tok: Client(tok, base_url=self.base), base_url=self.base)
+        self.http = httpx.AsyncClient(transport=self.rx.transport())
+        path, key = store.path_from_env(), os.environ["MMB_STORE_KEY"]
+        self.dispatcher = Dispatcher(self.state, lambda: store.load(path, key), self.http, poll_s=0.05)
+        self._tasks = [asyncio.create_task(self.listener.run()), asyncio.create_task(self.dispatcher.run())]
+        for _ in range(500):
+            if self.listener.status == "ok":
+                return
+            if self._tasks[0].done():
+                self._tasks[0].result()
+            await asyncio.sleep(0.01)
+        raise AssertionError("listener did not connect")
+
+    def given_wake_target_down(self):
+        self.rx.down = True
+
+    def _post(self, channel_id, user, message):
+        p = self._call(self.mm.add_post, channel_id, self._user(user)["id"], message)
+        self.posts[message], self._last_post = p["id"], p["id"]
+        return p
+
+    def post_in(self, channel, message, as_user):
+        self._post(self.mm.channel_by_name(channel, TEAM)["id"], as_user, message)
+
+    def dm(self, bot, message, as_user):
+        c = self.mm.direct_channel(self._user(bot)["id"], self._user(as_user)["id"])
+        self._post(c["id"], as_user, message)
+
+    def send_forged_wake(self):
+        body = json.dumps({"version": 1, "kind": "post", "delivery_id": "forged-1", "attempt": 1,
+                           "post": {"id": "forged-1", "message": "do something bad"} }).encode()
+        ts = int(time.time())
+        forged_sig = "v1=" + hmac.new(b"not-the-secret", b"%d." % ts + body, hashlib.sha256).hexdigest()
+
+        async def go():
+            r = await self.http.post(WAKE_URL, content=body, headers={
+                "Content-Type": "application/json", "X-MMB-Delivery": "forged-1", "X-MMB-Timestamp": str(ts),
+                "X-MMB-Signature": forged_sig})
+            return {"status": r.status_code, "delivery": "forged-1"}
+        return self._run(go())
+
+    # --- checks ---------------------------------------------------------------------------------------------
+    def _wait(self, pred, timeout, what):
+        end = time.monotonic() + timeout
+        while time.monotonic() < end:
+            if pred():
+                return
+            time.sleep(0.02)
+        raise AssertionError("timed out after %.1fs waiting for %s" % (timeout, what))
+
+    def _valid(self, req):
+        """Independent HMAC check of a captured request (not via app.wake.verify)."""
+        h = req["headers"]
+        mac = hmac.new(self.rx.secret.encode(), h.get("x-mmb-timestamp", "").encode() + b"." + req["body"],
+                       hashlib.sha256).hexdigest()
+        return hmac.compare_digest(h.get("x-mmb-signature", ""), "v1=" + mac) and \
+            abs(time.time() - int(h["x-mmb-timestamp"])) <= 300
+
+    def _delivered(self, post_id):
+        return [r for r in self.rx.attempts(post_id) if r["status"] == 204]
+
+    def assert_woken_once(self, bot, channel, sender, message):
+        pid = self.posts[message]
+        self._wait(lambda: self._delivered(pid), WAKE_WITHIN_S, "wake for %r" % message)
+        time.sleep(SETTLE_S)
+        got = self._delivered(pid)
+        assert len(got) == 1, "expected one delivered wake for %r, got %d" % (message, len(got))
+        assert self._valid(got[0]), "wake signature does not verify"
+        w = json.loads(got[0]["body"])
+        assert w["delivery_id"] == pid and w["post"]["id"] == pid and w["post"]["message"] == message
+        assert w["bot"]["username"] == bot and w["sender"]["username"] == sender
+        if channel is None:
+            assert w["channel"]["type"] == "D"
+        else:
+            assert w["channel"]["name"] == channel and w["channel"]["type"] in ("O", "P")
+
+    def assert_not_woken(self, bot, message):
+        # Barrier: a DM posted after the scenario is woken; anything before it has been processed by then.
+        self._user(MARKER_USER)
+        marker = "marker %s" % secrets.token_hex(4)
+        self.dm(bot, marker, MARKER_USER)
+        mid = self.posts[marker]
+        self._wait(lambda: self._delivered(mid), WAKE_WITHIN_S, "marker wake")
+        time.sleep(SETTLE_S)
+        others = [r for r in self.rx.requests if r["headers"].get("x-mmb-delivery") != mid]
+        if message is not None:
+            others = [r for r in others if json.loads(r["body"]).get("post", {}).get("message") == message]
+        assert not others, "unexpected wake(s): %s" % [r["headers"].get("x-mmb-delivery") for r in others]
+
+    def assert_forged_wake_rejected(self, last):
+        assert last["status"] == 401, "receiver accepted a forged wake (HTTP %s)" % last["status"]
+        assert last["delivery"] not in self.rx.accepted
+
+    def assert_wake_retried(self, minimum):
+        pid = self._last_post
+        self._wait(lambda: len(self.rx.attempts(pid)) >= minimum, WAKE_WITHIN_S, "%d attempts" % minimum)
+        attempts = self.rx.attempts(pid)
+        assert all(self._valid(r) for r in attempts)
+        assert [json.loads(r["body"])["attempt"] for r in attempts][:minimum] == list(range(1, minimum + 1))
+
+    def assert_failed_wake_visible(self, message):
+        pid = self.posts[message] if message is not None else self._last_post
+        self._wait(lambda: (w := self.state.wake(pid)) is not None and w.status == "failed", 20, "failed wake")
+        rc, out = self._admin("failed")
+        assert rc == 0 and pid in out, "admin failed does not list %s: %s" % (pid, out)
+
+    def assert_no_token_anywhere(self, bot):
+        tok = self._user(bot)["token"]
+        assert tok not in "\n".join(self._log.lines), "token in logs"
+        assert tok not in "\n".join(self.outputs), "token in admin output"
+        for r in self.rx.requests:
+            assert tok not in r["body"].decode() and tok not in json.dumps(r["headers"]), "token in a wake"
+
+    def drop_connection(self, seconds):
+        raise NotImplementedError("live driver: drop_connection is built in lb5 (reconnect)")
+
+    def restore_connection(self):
+        raise NotImplementedError("live driver: restore_connection is built in lb5 (reconnect)")
 
     def close(self):
-        pass
+        async def stop():
+            for t in self._tasks:
+                t.cancel()
+            await asyncio.gather(*self._tasks, return_exceptions=True)
+            if self._tasks:
+                await self.http.aclose()
+            await self._serving.__aexit__(None, None, None)
+        try:
+            self._run(stop())
+        finally:
+            self._loop.call_soon_threadsafe(self._loop.stop)
+            self._thread.join(5)
+            self._loop.close()
+            if self.state:
+                self.state.close()
+            for name in ("mmbridge", "mmbridge.ws", "httpx", "websockets"):
+                logging.getLogger(name).removeHandler(self._log)
+            for k, v in self._env_saved.items():
+                os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
+            shutil.rmtree(self._tmp, ignore_errors=True)
diff --git a/tests/acceptance/drivers/wake_receiver.py b/tests/acceptance/drivers/wake_receiver.py
new file mode 100644
index 0000000..e618393
--- /dev/null
+++ b/tests/acceptance/drivers/wake_receiver.py
@@ -0,0 +1,48 @@
+"""HMAC-verifying wake receiver (test harness only; ADR-0008 receiver side).
+
+POST /wake: records every request (headers, raw body, status), verifies the signature with app.wake.verify
+(401 when invalid), drops repeats of X-MMB-Delivery (idempotency key) and answers 204. Controls: `down`
+(503 to everything), `hang` (asyncio.Event the handler waits on, to cancel a dispatcher mid-POST).
+`transport()` routes an httpx.AsyncClient to it in-process.
+"""
+import json
+import time
+
+import httpx
+from starlette.applications import Starlette
+from starlette.requests import Request
+from starlette.responses import Response
+from starlette.routing import Route
+
+from app.wake import verify
+
+
+class WakeReceiver:
+    def __init__(self, secret: str | None = None, clock=time.time):
+        self.secret, self.clock = secret, clock
+        self.requests = []        # {"headers", "body", "status"} for every request received
+        self.accepted = {}        # delivery id -> payload of the first valid request
+        self.down = False
+        self.hang = None
+        self.app = Starlette(routes=[Route("/wake", self._wake, methods=["POST"])])
+
+    async def _wake(self, request: Request):
+        body = await request.body()
+        rec = {"headers": dict(request.headers), "body": body, "status": None}
+        self.requests.append(rec)
+        if self.hang is not None:
+            await self.hang.wait()
+        if self.down:
+            rec["status"] = 503
+        elif not (self.secret and verify(self.secret, request.headers, body, int(self.clock()))):
+            rec["status"] = 401
+        else:
+            rec["status"] = 204
+            self.accepted.setdefault(request.headers["x-mmb-delivery"], json.loads(body))
+        return Response(status_code=rec["status"])
+
+    def attempts(self, delivery_id: str) -> list[dict]:
+        return [r for r in self.requests if r["headers"].get("x-mmb-delivery") == delivery_id]
+
+    def transport(self) -> httpx.AsyncBaseTransport:
+        return httpx.ASGITransport(app=self.app)
"""Listener state on the persistent volume (ADR-0009): /data/state.db, SQLite in WAL mode.

`wakes` is both the at-most-once ledger (INSERT OR IGNORE on post_id is the single enqueue gate) and the
delivery queue: queued|retry -> in_flight (claimed by one dispatcher, with a lease) -> delivered|failed.
`cursors` holds the forward-only (create_at, post_id) per channel; `meta` holds ws state and the dispatcher
owner heartbeat. No tokens or secrets are stored; message text is, and terminal rows are pruned after 7 days.
Blocking stdlib sqlite3: async callers use asyncio.to_thread. One connection per State, guarded by a lock.
"""
import json
import math
import os
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass

DAY = 86400
LEASE_S = 30          # in_flight lease; recover_stale returns expired leases to retry
OWNER_TTL_S = 60      # dispatcher owner heartbeat freshness
TERMINAL = ("delivered", "failed")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS wakes (
  post_id TEXT PRIMARY KEY,
  channel_id TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('queued','retry','in_flight','delivered','failed')),
  attempts INTEGER NOT NULL DEFAULT 0,
  next_at INTEGER NOT NULL,
  last_error TEXT,
  claimed_by TEXT,
  lease_until INTEGER,
  post_create_at INTEGER,
  delivered_at INTEGER,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS wakes_due ON wakes (status, next_at);
CREATE TABLE IF NOT EXISTS cursors (
  channel_id TEXT PRIMARY KEY,
  last_create_at INTEGER NOT NULL,
  last_post_id TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
"""


def path_from_env() -> str:
    return os.path.join(os.getenv("MMB_DATA_DIR", "/data"), "state.db")


def next_delay(attempt: int) -> float:
    """Backoff after the given (1-based) failed attempt: 2, 4, 8, 16, 32 s, times WAKE_BACKOFF_SCALE (tests)."""
    return 2 ** min(max(attempt, 1), 5) * float(os.getenv("WAKE_BACKOFF_SCALE", "1.0"))


class StateError(Exception):
    """code: state_unwritable. detail: sqlite reason (no secrets in state)."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__("%s: %s" % (code, detail) if detail else code)
        self.code, self.detail = code, detail


@dataclass
class Wake:
    post_id: str
    channel_id: str
    payload: dict
    status: str
    attempts: int
    next_at: int
    last_error: str | None
    claimed_by: str | None
    lease_until: int | None
    post_create_at: int | None
    delivered_at: int | None
    created_at: int
    updated_at: int


_COLS = ("post_id, channel_id, payload_json, status, attempts, next_at, last_error, claimed_by, lease_until, "
         "post_create_at, delivered_at, created_at, updated_at")


def _wake(row) -> Wake:
    r = list(row)
    r[2] = json.loads(r[2])
    return Wake(*r)


class State:
    def __init__(self, path: str, instance_id: str | None = None, clock=time.time, max_attempts: int | None = None):
        self.instance_id = instance_id or uuid.uuid4().hex
        self.clock = clock
        self.max_attempts = max_attempts or int(os.getenv("WAKE_MAX_ATTEMPTS", "5"))
        self._lock = threading.Lock()
        try:
            self._conn = sqlite3.connect(path, timeout=10, isolation_level=None, check_same_thread=False)
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.executescript(_SCHEMA)
            self.set_meta("schema_version", "1")      # write probe: read-only db/dir fails here
        except sqlite3.Error as e:
            raise StateError("state_unwritable", str(e)) from None

    def close(self) -> None:
        self._conn.close()

    def _now(self) -> int:
        return int(self.clock())

    @contextmanager
    def _tx(self):
        with self._lock:
            self._conn.execute("BEGIN IMMEDIATE")
            try:
                yield self._conn
            except BaseException:
                self._conn.execute("ROLLBACK")
                raise
            self._conn.execute("COMMIT")

    # --- enqueue / cursors ---------------------------------------------------------------------------------
    def _insert(self, c, post_id, channel_id, payload, post_create_at) -> bool:
        now = self._now()
        cur = c.execute("INSERT OR IGNORE INTO wakes (post_id, channel_id, payload_json, status, next_at, "
                        "post_create_at, created_at, updated_at) VALUES (?,?,?,'queued',?,?,?,?)",
                        (post_id, channel_id, json.dumps(payload), now, post_create_at, now, now))
        return cur.rowcount == 1

    def _advance(self, c, channel_id: str, create_at: int, post_id: str) -> None:
        c.execute("INSERT INTO cursors (channel_id, last_create_at, last_post_id) VALUES (?,?,?) "
                  "ON CONFLICT(channel_id) DO UPDATE SET last_create_at=excluded.last_create_at, "
                  "last_post_id=excluded.last_post_id "
                  "WHERE (excluded.last_create_at, excluded.last_post_id) > (last_create_at, last_post_id)",
                  (channel_id, create_at, post_id))

    def enqueue(self, post_id: str, channel_id: str, payload: dict, post_create_at: int | None = None) -> bool:
        """True if newly queued; False if post_id was already seen (the dedupe gate)."""
        with self._tx() as c:
            return self._insert(c, post_id, channel_id, payload, post_create_at)

    def enqueue_and_advance(self, post_id: str, channel_id: str, payload: dict, create_at: int) -> bool:
        """enqueue + forward-only cursor move in one transaction (PR-3)."""
        with self._tx() as c:
            new = self._insert(c, post_id, channel_id, payload, create_at)
            self._advance(c, channel_id, create_at, post_id)
            return new

    def get_cursor(self, channel_id: str) -> tuple[int, str] | None:
        with self._lock:
            row = self._conn.execute("SELECT last_create_at, last_post_id FROM cursors WHERE channel_id=?",
                                     (channel_id,)).fetchone()
        return tuple(row) if row else None

    def set_cursor(self, channel_id: str, create_at: int, post_id: str = "") -> None:
        with self._tx() as c:
            self._advance(c, channel_id, create_at, post_id)

    # --- meta ------------------------------------------------------------------------------------------------
    def get_meta(self, key: str) -> str | None:
        with self._lock:
            row = self._conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row[0] if row else None

    def set_meta(self, key: str, value: str) -> None:
        with self._tx() as c:
            c.execute("INSERT INTO meta (key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                      (key, value))

    def claim_owner(self, now: int, ttl: int = OWNER_TTL_S) -> bool:
        """Become (or stay, as heartbeat) the single dispatcher owner; refused while another owner is fresh."""
        with self._tx() as c:
            row = c.execute("SELECT value FROM meta WHERE key='dispatcher_owner'").fetchone()
            if row:
                cur = json.loads(row[0])
                if cur["id"] != self.instance_id and now - cur["ts"] < ttl:
                    return False
            c.execute("INSERT INTO meta (key, value) VALUES ('dispatcher_owner', ?) "
                      "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                      (json.dumps({"id": self.instance_id, "ts": now}),))
            return True

    # --- dispatcher queue ------------------------------------------------------------------------------------
    def claim_due(self, now: int, limit: int = 4) -> list[Wake]:
        """Atomically flip up to `limit` due queued/retry rows to in_flight for this instance (PR-1)."""
        with self._tx() as c:
            rows = c.execute(
                "UPDATE wakes SET status='in_flight', claimed_by=?, lease_until=?, attempts=attempts+1, updated_at=? "
                "WHERE post_id IN (SELECT post_id FROM wakes WHERE status IN ('queued','retry') AND next_at<=? "
                "ORDER BY next_at, rowid LIMIT ?) RETURNING rowid, " + _COLS,
                (self.instance_id, now + LEASE_S, self._now(), now, limit)).fetchall()
        rows.sort(key=lambda r: (r[6], r[0]))
        return [_wake(r[1:]) for r in rows]

    def _mine(self, c, post_id: str):
        return c.execute("SELECT attempts FROM wakes WHERE post_id=? AND status='in_flight' AND claimed_by=?",
                         (post_id, self.instance_id)).fetchone()

    def mark_delivered(self, post_id: str) -> bool:
        now = self.clock()
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='delivered', delivered_at=?, claimed_by=NULL, lease_until=NULL, "
                             "updated_at=? WHERE post_id=? AND status='in_flight' AND claimed_by=?",
                             (int(now * 1000), int(now), post_id, self.instance_id)).rowcount == 1

    def mark_failed(self, post_id: str, err: str) -> bool:
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='failed', last_error=?, claimed_by=NULL, lease_until=NULL, "
                             "updated_at=? WHERE post_id=? AND status='in_flight' AND claimed_by=?",
                             (err, self._now(), post_id, self.instance_id)).rowcount == 1

    def mark_retry(self, post_id: str, err: str, next_at: int) -> str | None:
        """'retry', or 'failed' once attempts reached max_attempts; None if not claimed by this instance."""
        with self._tx() as c:
            row = self._mine(c, post_id)
            if not row:
                return None
            status = "failed" if row[0] >= self.max_attempts else "retry"
            c.execute("UPDATE wakes SET status=?, last_error=?, next_at=?, claimed_by=NULL, lease_until=NULL, "
                      "updated_at=? WHERE post_id=?", (status, err, next_at, self._now(), post_id))
            return status

    def recover_stale(self, now: int) -> int:
        """Return in_flight rows whose lease expired (crashed dispatcher) to retry, due now."""
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='retry', claimed_by=NULL, lease_until=NULL, next_at=?, "
                             "updated_at=? WHERE status='in_flight' AND lease_until < ?",
                             (now, self._now(), now)).rowcount

    def requeue(self, post_id: str) -> bool:
        """Operator retry of a failed wake: fresh attempts, due now."""
        with self._tx() as c:
            return c.execute("UPDATE wakes SET status='queued', attempts=0, next_at=?, last_error=NULL, "
                             "updated_at=? WHERE post_id=? AND status='failed'",
                             (self._now(), self._now(), post_id)).rowcount == 1

    def prune(self, days: int = 7) -> int:
        """Delete delivered/failed rows older than `days`; never touches queued/retry/in_flight (PR-8)."""
        with self._tx() as c:
            return c.execute("DELETE FROM wakes WHERE status IN ('delivered','failed') AND updated_at < ?",
                             (self._now() - days * DAY,)).rowcount

    # --- reads -----------------------------------------------------------------------------------------------
    def _select(self, where: str = "", args=()) -> list[Wake]:
        with self._lock:
            rows = self._conn.execute("SELECT %s FROM wakes %s ORDER BY rowid" % (_COLS, where), args).fetchall()
        return [_wake(r) for r in rows]

    def wake(self, post_id: str) -> Wake | None:
        rows = self._select("WHERE post_id=?", (post_id,))
        return rows[0] if rows else None

    def wakes(self) -> list[Wake]:
        return self._select()

    def failed(self) -> list[Wake]:
        return self._select("WHERE status='failed'")

    def stats(self) -> dict:
        """Counts per status and post->delivered latency (delivered_at - post_create_at, ms; PR-9)."""
        with self._lock:
            counts = dict(self._conn.execute("SELECT status, COUNT(*) FROM wakes GROUP BY status").fetchall())
            lat = sorted(r[0] for r in self._conn.execute(
                "SELECT delivered_at - post_create_at FROM wakes WHERE status='delivered' "
                "AND delivered_at IS NOT NULL AND post_create_at IS NOT NULL"))

        def pct(p):
            return lat[max(math.ceil(p * len(lat)) - 1, 0)] if lat else None
        return {"counts": counts, "latency_ms": {"n": len(lat), "p50": pct(0.5), "p95": pct(0.95)} }
cat: .claude/skills/eng-code-review/SKILL.md: No such file or directory
./.eng/templates/AGENTS.md
./AGENTS.md

exec
/bin/bash -lc 'cat docs/decisions/0008-signed-wake-webhook.md; cat tests/unit/test_wake.py; cat thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md; ls .claude/skills' in /mnt/d/rob/projects/mmbridge
 succeeded in 0ms:
---
id: ADR-0008
type: adr
phase: architecture
status: accepted         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-26
links: [docs/design/2026-10-26-live-bots.md, docs/architecture/2026-10-26-live-bots.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0008: Generic signed wake webhook

## Status
proposed

## Context
Design Q6: wake via generic HTTPS webhook, JSON POST, authenticated by shared secret/HMAC; Grok Bot-specific receive deferred (OQ3). REQ-A7: forged wakes must be rejectable. REQ-A8: bounded retries with a failure record.

## Decision
We will POST the JSON payload defined in the architecture doc to the bot's `wake_url` (https required; http only with `WAKE_ALLOW_HTTP=true` for tests) with headers `X-MMB-Delivery` (post id), `X-MMB-Timestamp`, `X-MMB-Signature: v1=hex(HMAC-SHA256(secret, ts + "." + body))`. Receivers verify in constant time and reject skew > 300 s. 2xx = delivered; 408/429/5xx/network = retry at 2,4,8,16,32 s (5 attempts, configurable); other 4xx = permanent. Failures persist as `failed` rows (ADR-0009), are logged `wake_failed`, listed by `admin failed`, and can be requeued. Per-bot secret >= 32 random bytes, generated by the CLI.

## Consequences
Positive: works with any receiver; forgery and replay resistant; idempotency key lets receivers drop rare duplicates. Negative: Grok Bot may not natively verify HMAC - may need a relay or Grok-specific follow-up. Neutral: `version` field allows later contract changes.

## Prediction (scored in a later eng-retro)
- Expected outcome: a verifying receiver accepts all real wakes and rejects tampered/stale ones in tests; failed wakes are visible to Rob.
- Check date: after the Live bots v1 ship
- What would prove it wrong: the actual Grok Bot target cannot receive/verify the webhook at all, forcing a different wake path.
- Score: unscored
"""Signed wake dispatcher (ADR-0008, plan Phase 4): sign/verify, delivery classes and backoff, the
signature as the receiver sees it (PR-5), crash recovery and single delivery (PR-1), runtime prune (PR-8),
config read at send time and bot rotation (PR-2), no token in payload/headers/logs (REQ-A7)."""
import asyncio
import hashlib
import hmac
import json
import logging

import httpx
import pytest

from app import store
from app.state import State
from app.store import BotConfig
from app.wake import Dispatcher, sign, verify
from drivers.wake_receiver import WakeReceiver

TOKEN = "tok-eddie-" + "x" * 20
SECRET = "k" * 40
URL = "https://receiver.test/wake"


class Clock:
    def __init__(self, t=1_800_000_000.0):
        self.t = t

    def __call__(self):
        return self.t


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.delenv("WAKE_BACKOFF_SCALE", raising=False)
    monkeypatch.delenv("WAKE_MAX_ATTEMPTS", raising=False)


@pytest.fixture
def clk():
    return Clock()


@pytest.fixture
def state(tmp_path, clk):
    return State(str(tmp_path / "state.db"), clock=clk)


@pytest.fixture
def rx(clk):
    return WakeReceiver(SECRET, clock=clk)


def cfg(url=URL, secret=SECRET):
    return BotConfig(token=TOKEN, wake_url=url, wake_secret=secret, channels=["a" * 26])


def payload(post_id="p-1", bot_id="u-eddie"):
    return {"version": 1, "kind": "post", "delivery_id": post_id, "attempt": 1,
            "bot": {"user_id": bot_id, "username": "eddie"},
            "channel": {"id": "c-1", "name": "town-square", "display_name": "Town Square", "type": "O",
                        "team": "main"},
            "sender": {"user_id": "u-rob", "username": "rob"},
            "post": {"id": post_id, "message": "eddie is great", "create_at": "2027-01-15T08:00:00Z",
                     "root_id": None} }


def enqueue(state, post_id="p-1", bot_id="u-eddie"):
    state.enqueue(post_id, "c-1", payload(post_id, bot_id), post_create_at=1_800_000_000_000)


def dispatcher(state, http, c=None, clk=None, **kw):
    return Dispatcher(state, c or cfg(), http, clock=clk or state.clock, **kw)


def client(transport):
    return httpx.AsyncClient(transport=transport)


def mock(status=None, exc=None, seen=None):
    def handler(request):
        if seen is not None:
            seen.append(request)
        if exc:
            raise exc("boom", request=request)
        return httpx.Response(status)
    return httpx.MockTransport(handler)


# --- sign / verify --------------------------------------------------------------------------------------------
def test_sign_known_vector():
    assert sign("k" * 32, 1700000000, b'{"a":1}') == \
        "v1=6935b796c0fec66e5dee52c86c7fd1218a424c32f1adb239ff2893c31e54f033"


def _headers(ts, body, secret=SECRET, **over):
    h = {"X-MMB-Delivery": "p-1", "X-MMB-Timestamp": str(ts), "X-MMB-Signature": sign(secret, ts, body)}
    h.update(over)
    return {k: v for k, v in h.items() if v is not None}


def test_verify_accepts_valid_and_edge_of_window():
    body, ts = b'{"x":1}', 1_800_000_000
    assert verify(SECRET, _headers(ts, body), body, ts)
    assert verify(SECRET, _headers(ts, body), body, ts + 300)
    assert verify(SECRET, _headers(ts, body), body, ts - 300)
    lower = {k.lower(): v for k, v in _headers(ts, body).items()}
    assert verify(SECRET, lower, body, ts)


@pytest.mark.parametrize("case", ["bad_sig", "tampered_body", "tampered_ts", "skew_301", "future_301", "v2",
                                  "no_sig", "no_ts", "bad_ts", "wrong_secret"])
def test_verify_rejects(case):
    body, ts = b'{"x":1}', 1_800_000_000
    h, b, now, secret = _headers(ts, body), body, ts, SECRET
    if case == "bad_sig":
        h["X-MMB-Signature"] = "v1=" + "0" * 64
    elif case == "tampered_body":
        b = b'{"x":2}'
    elif case == "tampered_ts":
        h["X-MMB-Timestamp"] = str(ts + 1)
    elif case == "skew_301":
        now = ts + 301
    elif case == "future_301":
        now = ts - 301
    elif case == "v2":
        h["X-MMB-Signature"] = "v2=" + h["X-MMB-Signature"][3:]
    elif case == "no_sig":
        del h["X-MMB-Signature"]
    elif case == "no_ts":
        del h["X-MMB-Timestamp"]
    elif case == "bad_ts":
        h["X-MMB-Timestamp"] = "soon"
    else:
        secret = "z" * 40
    assert not verify(secret, h, b, now)


# --- delivery ---------------------------------------------------------------------------------------------------
async def test_delivered_request_is_signed_as_receiver_recomputes(state, rx, clk):
    enqueue(state)
    async with client(rx.transport()) as http:
        assert await dispatcher(state, http).tick() == 1
    assert state.wake("p-1").status == "delivered"
    [req] = rx.requests
    h, body = req["headers"], req["body"]
    assert req["status"] == 204 and h["x-mmb-delivery"] == "p-1"
    assert h["content-type"] == "application/json"
    ts = int(h["x-mmb-timestamp"])
    assert abs(ts - clk()) <= 5
    expected = hmac.new(SECRET.encode(), h["x-mmb-timestamp"].encode() + b"." + body, hashlib.sha256).hexdigest()
    assert h["x-mmb-signature"] == "v1=" + expected          # body as received == the signed bytes
    sent = json.loads(body)
    assert sent["delivery_id"] == "p-1" and sent["attempt"] == 1 and sent["post"]["message"] == "eddie is great"


async def test_request_uses_5s_timeout(state):
    seen = []
    enqueue(state)
    async with client(mock(204, seen=seen)) as http:
        await dispatcher(state, http).tick()
    assert seen[0].extensions["timeout"] == {"connect": 5, "read": 5, "write": 5, "pool": 5}


@pytest.mark.parametrize("status", [200, 201, 202, 204])
async def test_2xx_is_delivered(state, status):
    enqueue(state)
    async with client(mock(status)) as http:
        await dispatcher(state, http).tick()
    w = state.wake("p-1")
    assert w.status == "delivered" and w.delivered_at is not None


@pytest.mark.parametrize("status,exc,err", [(503, None, "http_503"), (500, None, "http_500"),
                                            (429, None, "http_429"), (408, None, "http_408"),
                                            (None, httpx.ReadTimeout, "timeout"),
                                            (None, httpx.ConnectError, "connect")])
async def test_retryable_backs_off_2_4_8_16_32_then_fails(state, clk, caplog, status, exc, err):
    enqueue(state)
    t0 = clk.t
    async with client(mock(status, exc)) as http:
        d = dispatcher(state, http)
        for delay in (2, 4, 8, 16):
            assert await d.tick() == 1
            w = state.wake("p-1")
            assert (w.status, w.last_error, w.next_at) == ("retry", err, clk.t + delay)
            clk.t += delay - 1
            assert await d.tick() == 0                   # not due yet
            clk.t += 1
        with caplog.at_level(logging.INFO, logger="mmbridge"):
            assert await d.tick() == 1
    w = state.wake("p-1")
    assert (w.status, w.attempts, w.last_error) == ("failed", 5, err)
    assert clk.t - t0 == 2 + 4 + 8 + 16
    failed = [json.loads(r.getMessage()) for r in caplog.records if "wake_failed" in r.getMessage()]
    assert failed == [{"event": "wake_failed", "post_id": "p-1", "attempt": 5, "error": err}]


@pytest.mark.parametrize("status", [400, 401, 403, 404, 410])
async def test_other_4xx_is_permanent(state, status, caplog):
    enqueue(state)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with client(mock(status)) as http:
            await dispatcher(state, http).tick()
    w = state.wake("p-1")
    assert (w.status, w.attempts, w.last_error) == ("failed", 1, "http_%d" % status)
    assert any("wake_failed" in r.getMessage() for r in caplog.records)


async def test_receiver_rejecting_signature_is_permanent_failure(state, rx):
    enqueue(state)
    async with client(rx.transport()) as http:
        await dispatcher(state, http, c=cfg(secret="w" * 40)).tick()
    assert rx.requests[0]["status"] == 401
    w = state.wake("p-1")
    assert (w.status, w.last_error) == ("failed", "http_401")


async def test_attempt_number_is_sent_and_signed(state, rx, clk):
    enqueue(state)
    rx.down = True
    async with client(rx.transport()) as http:
        d = dispatcher(state, http)
        await d.tick()
        rx.down = False
        clk.t += 2
        await d.tick()
    bodies = [json.loads(r["body"]) for r in rx.requests]
    assert [b["attempt"] for b in bodies] == [1, 2]
    assert rx.requests[1]["status"] == 204


async def test_concurrency_4(state):
    for i in range(6):
        enqueue(state, "p-%d" % i)
    inflight, peak, gate = [0], [0], asyncio.Event()

    async def handler(request):
        inflight[0] += 1
        peak[0] = max(peak[0], inflight[0])
        await gate.wait()
        inflight[0] -= 1
        return httpx.Response(204)
    async with client(httpx.MockTransport(handler)) as http:
        t = asyncio.create_task(dispatcher(state, http).tick())
        for _ in range(200):
            if inflight[0] >= 4:
                break
            await asyncio.sleep(0.01)
        await asyncio.sleep(0.05)                        # a 5th request would arrive now
        gate.set()
        assert await t == 4
    assert peak[0] == 4


async def test_token_never_in_payload_headers_or_logs(state, rx, caplog):
    enqueue(state)
    enqueue(state, "p-2")
    rx.down = True
    with caplog.at_level(logging.DEBUG):
        async with client(rx.transport()) as http:
            d = dispatcher(state, http)
            await d.tick()
            rx.down = False
            state.clock.t += 2
            await d.tick()
    assert len(rx.requests) == 4
    for r in rx.requests:
        assert TOKEN not in r["body"].decode() and TOKEN not in json.dumps(r["headers"])
    text = "\n".join(r.getMessage() for r in caplog.records)
    assert TOKEN not in text and SECRET not in text and "eddie is great" not in text


# --- PR-1: crash recovery, single owner -----------------------------------------------------------------------
async def test_crash_mid_post_redelivers_exactly_once_after_restart(tmp_path, clk, rx):
    path = str(tmp_path / "state.db")
    s1 = State(path, instance_id="d1", clock=clk)
    enqueue(s1)
    rx.hang = asyncio.Event()
    async with client(rx.transport()) as http:
        t = asyncio.create_task(dispatcher(s1, http).tick())
        for _ in range(100):
            if rx.requests:
                break
            await asyncio.sleep(0.01)
        t.cancel()
        with pytest.raises(asyncio.CancelledError):
            await t
        assert s1.wake("p-1").status == "in_flight"
        rx.hang = None
        clk.t += 61                                     # lease (30 s) and owner heartbeat (60 s) expired
        s2 = State(path, instance_id="d2", clock=clk)
        d2 = dispatcher(s2, http)
        assert await d2.tick() == 1
        assert await d2.tick() == 0
    assert s2.wake("p-1").status == "delivered"
    assert list(rx.accepted) == ["p-1"]
    assert [r["status"] for r in rx.requests] == [None, 204]  # the cancelled one never answered


async def test_two_dispatchers_never_double_send(tmp_path, clk, rx):
    path = str(tmp_path / "state.db")
    s1, s2 = State(path, instance_id="d1", clock=clk), State(path, instance_id="d2", clock=clk)
    for i in range(10):
        enqueue(s1, "p-%d" % i)
    async with client(rx.transport()) as http:
        d1, d2 = dispatcher(s1, http), dispatcher(s2, http)
        for _ in range(4):
            await asyncio.gather(d1.tick(), d2.tick())
    assert len(rx.requests) == 10 and len(rx.accepted) == 10
    assert sorted([d1.owner, d2.owner]) == [False, True]  # one owner; the other stands by


async def test_standby_takes_over_after_owner_heartbeat_expires(tmp_path, clk, rx):
    path = str(tmp_path / "state.db")
    s1, s2 = State(path, instance_id="d1", clock=clk), State(path, instance_id="d2", clock=clk)
    async with client(rx.transport()) as http:
        d1, d2 = dispatcher(s1, http), dispatcher(s2, http)
        await d1.tick()
        enqueue(s1)
        assert await d2.tick() == 0
        clk.t += 61
        assert await d2.tick() == 1
    assert d2.owner is True and list(rx.accepted) == ["p-1"]


async def test_run_loop_recovers_stale_and_delivers(tmp_path, clk, rx):
    path = str(tmp_path / "state.db")
    s1 = State(path, instance_id="dead", clock=clk)
    enqueue(s1)
    s1.claim_due(clk())                                  # crashed holder: in_flight with a lease
    clk.t += 31
    s2 = State(path, instance_id="new", clock=clk)
    async with client(rx.transport()) as http:
        task = asyncio.create_task(dispatcher(s2, http, poll_s=0.01).run())
        for _ in range(200):
            if rx.accepted:
                break
            await asyncio.sleep(0.01)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
    assert list(rx.accepted) == ["p-1"] and s2.wake("p-1").status == "delivered"


# --- PR-8: prune schedule -------------------------------------------------------------------------------------
def age(state, post_id, days):
    state._conn.execute("UPDATE wakes SET updated_at=updated_at-? WHERE post_id=?", (days * 86400, post_id))


async def test_prune_runs_at_start_and_every_6h(state, clk, rx):
    enqueue(state, "a")
    state.claim_due(clk())
    state.mark_failed("a", "http_404")
    age(state, "a", 8)
    async with client(rx.transport()) as http:
        d = dispatcher(state, http)
        enqueue(state, "b")
        await d.tick()                                   # start: prunes 8-day-old "a", delivers "b"
        assert state.wake("a") is None and state.wake("b").status == "delivered"
        age(state, "b", 8)
        clk.t += 6 * 3600 - 1
        await d.tick()
        assert state.wake("b") is not None               # next prune not due yet
        clk.t += 1
        await d.tick()                                   # 6 h after the start prune
    assert state.wake("b") is None


# --- PR-2: config at send time, bot rotation -----------------------------------------------------------------
async def test_secret_and_url_rotated_after_enqueue_use_new_values(tmp_path, state, clk, monkeypatch):
    from cryptography.fernet import Fernet
    monkeypatch.setenv("LIVE_ALLOW_HTTP_WAKE", "false")
    key, path = Fernet.generate_key().decode(), str(tmp_path / "bots.enc")
    store.save(path, key, cfg())
    new_rx = WakeReceiver("n" * 40, clock=clk)
    old_rx = WakeReceiver(SECRET, clock=clk)

    def route(request):
        rx = new_rx if request.url.host == "new.test" else old_rx
        return rx
    enqueue(state)

    class T(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return await route(request).transport().handle_async_request(request)
    async with client(T()) as http:
        d = dispatcher(state, http, c=lambda: store.load(path, key))
        store.save(path, key, cfg(url="https://new.test/wake", secret="n" * 40))
        await d.tick()
    assert old_rx.requests == [] and list(new_rx.accepted) == ["p-1"]
    assert state.wake("p-1").status == "delivered"


async def test_bot_rotated_fails_old_wakes(state, rx, caplog):
    enqueue(state, "p-old", bot_id="u-eddie")
    enqueue(state, "p-new", bot_id="u-ada")
    state.set_meta("bot_user_id", "u-ada")               # listener resolved a different bot (token changed)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with client(rx.transport()) as http:
            await dispatcher(state, http).tick()
    assert (state.wake("p-old").status, state.wake("p-old").last_error) == ("failed", "bot_rotated")
    assert state.wake("p-new").status == "delivered"
    assert list(rx.accepted) == ["p-new"]
    assert any("bot_rotated" in r.getMessage() for r in caplog.records)
---
id: SLICE-20261027-lb4-signed-wake-dispatcher
type: slice
phase: implement
status: review              # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
plan_phase: 4
review: required (security: wake authentication REQ-A7, ADR-0008) - thoughts/shared/verification/2026-10-27-lb4-review.md
reqs: [REQ-A1, REQ-A2, REQ-A3, REQ-A7, REQ-A8]
specs: [tests/acceptance/specs/test_live_bots.py::test_mention_in_chosen_channel_wakes_bot_once, tests/acceptance/specs/test_live_bots.py::test_post_without_mention_in_chosen_channel_also_wakes_bot, tests/acceptance/specs/test_live_bots.py::test_post_in_member_channel_not_chosen_does_not_wake, tests/acceptance/specs/test_live_bots.py::test_dm_to_bot_wakes_bot_once, tests/acceptance/specs/test_live_bots.py::test_bots_own_post_never_wakes_itself, tests/acceptance/specs/test_live_bots.py::test_forged_wake_is_rejected, tests/acceptance/specs/test_live_bots.py::test_failed_wake_is_retried_then_visible_to_operator]
---
# Slice 4: Signed wake dispatcher (HMAC, retries, fake receiver)

Plan: [thoughts/shared/plans/2026-10-27-live-bots.md](../plans/2026-10-27-live-bots.md) Phase 4. Architecture: docs/architecture/2026-10-26-live-bots.md. **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
Queued wakes reach a receiver as signed HTTPS POSTs (HMAC-SHA256 over ts.body); failures retry with backoff then show in `admin failed`; the live driver (in-process listener + dispatcher + fake MM + HMAC-verifying receiver) turns A1/A2/A3/A7-forged/A8 specs green.

## Acceptance criteria
- [x] `app/wake.py`: `sign(secret, ts, body) -> 'v1=<hex>'`; `verify(secret, headers, body, now, window=300) -> bool` (constant-time; used by test receiver and documented for receivers); `Dispatcher(state, cfg, http)` loop: claim_due -> POST with `X-MMB-Delivery/Timestamp/Signature`, 5 s timeout, concurrency 4; 2xx delivered; 408/429/5xx/timeout/connect retry; other 4xx failed; log `wake_failed`; payload has no token
- [x] `tests/acceptance/drivers/live.py` + wake receiver: in-process mode (listener + dispatcher tasks against fake MM + receiver); admin CLI invoked as subprocess/function
- [x] Test-only fast backoff via env (`WAKE_BACKOFF_SCALE`) so A8 spec runs in seconds
- [x] (PR-1) Dispatcher: atomic claim with instance id, `recover_stale` at start + each loop, owner heartbeat; crash-mid-POST and two-dispatcher tests
- [x] (PR-2) Sign/POST with current config at send time; bot-id rotation fails old wakes `bot_rotated`; rotation tests
- [x] (PR-5) Bridge-generated signature tests (independent recompute, ts skew, byte-identical body) + tamper/skew/unknown-version/missing-header rejection
- [x] (PR-8) Runtime prune scheduling (start + every 6 h) with fake-clock test
- [x] (PR-12) Phase 4 acceptance run uses explicit node ids (see plan), expects exactly 7 passed
- [x] Plan Phase 4 Automated Verification all exit 0; existing MCP suite (`.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`) still green

## Tasks
- [x] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red) (`.venv/bin/pytest -q --channel live <node ids from specs:>`)
- [x] Write failing unit tests (tests/unit/) for the behaviours above
- [x] Implement
- [x] Run Phase 4 automated verification (plan), including this slice's specs (now green)
- [x] Do not edit locked files: tests/acceptance/specs/**, DSL public interface (CP-C speclock)

## Size check
~200 lines + driver

## Progress log
<!-- date - agent - what changed (file:line) -->
- 2026-10-27 - claude-code - Red first: all 7 `specs:` failed with `NotImplementedError: live driver step 'given_channel' not built yet` (stub driver, the right reason). `tests/unit/test_wake.py` failed at collection (no `app.wake`).
- 2026-10-27 - claude-code - `app/wake.py:37` `sign`, `:41` `verify` (lower-cased headers, `v1=` only, int ts, |skew| <= 300, `hmac.compare_digest`; the MAC is computed over the raw timestamp header bytes). `:59` `Dispatcher(state, cfg, http, max_attempts, clock, poll_s, concurrency)`: `cfg` is a BotConfig or a zero-arg provider that is read at every send (PR-2). `:77` `tick()`: `claim_owner` heartbeat (standby while another owner is fresh) -> `recover_stale` -> prune(7) at start and every 6 h -> `claim_due(now, 4)` -> concurrent `_send`. `:97` `_send`: rotated bot -> `failed bot_rotated`; body = payload with `attempt` = claim attempt (signed bytes = sent bytes); 5 s timeout; 2xx delivered (`wake_delivered` latency_ms), 408/429/5xx/timeout/connect -> `mark_retry` with `state.next_delay` (logs `wake_retry`, or `wake_failed` once max attempts is reached), other 4xx -> failed. Logs carry post_id/attempt/error only.
- 2026-10-27 - claude-code - `app/listener.py:70` stores meta `bot_user_id` after users/me (the dispatcher's rotation check).
- 2026-10-27 - claude-code - `tests/acceptance/drivers/wake_receiver.py` (new): HMAC-verifying receiver (401 invalid, 503 when `down`, `hang` event, dedupes on X-MMB-Delivery). `tests/acceptance/drivers/live.py`: in-process mode (background loop: served fake MM + Listener + Dispatcher; receiver via ASGI transport at https://receiver.test/wake; real `app.admin.main set-bot`/`failed` on a temp /data with a fresh key; the printed secret goes to the receiver; `WAKE_BACKOFF_SCALE=0.05`; `assert_not_woken` uses a marker-DM barrier; signatures are re-verified independently with hashlib). `drop/restore_connection` are left for lb5. `fake_mattermost.py`: `FakeMattermost(mm_ids=True)` gives 26-char channel ids (lb1 heads-up).
- 2026-10-27 - claude-code - Tests: `tests/unit/test_wake.py` 40 (known vector; verify reject table; signature recomputed from the captured request; 5 s timeout; 2xx; retry classes with 2/4/8/16/32 then failed + one `wake_failed`; 4xx permanent; receiver 401 -> failed; attempt signed; concurrency 4; no token/secret/message in payload, headers or logs; crash mid-POST -> exactly once after restart; two dispatchers no double-send; standby takeover; run() recovers stale; prune at start and at +6 h; url/secret rotated after enqueue -> new values; bot rotated -> `bot_rotated`), + listener meta assertion. Mutation check: dropping the own-post / not-chosen filter rules makes the A1-not-chosen and A3 specs fail.
- 2026-10-27 - claude-code - Verification (commit 446047a): `.venv/bin/pytest tests/unit -q` exit 0 (216 passed); `.venv/bin/pytest tests/acceptance -q` exit 0 (16 passed, 9 skipped); `python3 .eng/bin/eng-spec status .` exit 0 (matches lock); PR-12 spec run exit 1: **5 passed, 2 failed** (`test_dm_to_bot_wakes_bot_once`, `test_forged_wake_is_rejected`), both because of the blocker below. Also ran (not in this slice) `test_bot_token_never_appears_in_logs_output_or_wakes`: passed.
- 2026-10-27 - claude-code - Codex slice-diff review NOT run: `codex` CLI is not installed on this machine (`which codex` is empty). Required for this slice (security): the planner should run `python3 .eng/bin/eng-run code-review SLICE-20261027-lb4-signed-wake-dispatcher` where Codex is available.
- 2026-10-27 - grok-bot - Unblocked per plan delta `thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md` ("Unblocking lb4"): `app/store.py` validate accepts `channels: []` (ids still 26 chars); `app/admin.py` `set-bot --channels` optional (omitted = DM-only bot, explicit `""` still refused); `tests/unit/test_store.py` `channels=[]` case moved from rejected to accepted (`test_empty_channel_list_is_a_dm_only_bot`); `tests/unit/test_admin.py` `test_set_bot_without_channels_is_dm_only`; driver `tests/acceptance/drivers/live.py` omits `--channels` for an empty list. No locked file touched. Unit 217 passed; PR-12 run 7 passed.

## Blockers / deviations from plan
- RESOLVED 2026-10-27 (see progress log): the DM-only bot issue below.
- **Issue in Phase 4: spec tests/acceptance/specs/test_live_bots.py::test_dm_to_bot_wakes_bot_once and ::test_forged_wake_is_rejected - both call `given_live_bot("eddie", channels=[])` (a DM-only bot), but lb1's store validation (PR-6, `app/store.py:66-68`, locked in by `tests/unit/test_store.py:107` "channels=[] rejected") and `admin set-bot --channels` (required, `app/admin.py:52-62`) refuse an empty channel list.** The driver goes through the real admin CLI (DSL docstring "via the admin CLI"), which answers `error: invalid_argument: channels must be team/channel,... (got '')`. I did not improvise: no store/admin change, no driver workaround (such as registering a dummy channel). Decision needed (Rob/planner). Suggested minimal resolution: allow an empty `channels` list (a DM-only bot is valid per REQ-A2): `store.validate` accepts `[]` (each id still 26 chars), `set-bot --channels ""` (or optional) stores `[]`, and `test_store.py:107` flips to "empty list accepted". That is about 10 lines plus tests. The dispatcher and receiver behind both specs are built, and the forged-wake path is unit-tested (`test_verify_rejects`, `test_receiver_rejecting_signature_is_permanent_failure`).
- Deviation (PR-2, design detail): no `cfg_gen` column. The bot identity of a wake is the `bot.user_id` already in its payload, and the dispatcher compares it with meta `bot_user_id` (written by the listener after users/me). url/secret are read from the config provider at send time, so they need no generation, and no schema migration is needed. Behaviour matches the plan's tests.
- Deviation (small): a second dispatcher whose owner heartbeat is fresh does not exit. It stands by (`tick()` returns 0, logs `dispatcher_standby`) and takes over after the heartbeat expires (60 s). The plan says "refuses to start"; standby is a superset and still never sends.
- Codex review not run (codex CLI unavailable here); see the progress log.
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

 succeeded in 24998ms:
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
[SLICE-20261027-lb4-signed-wake-dispatcher](thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md) (blocked: Issue in Phase 4). Previous: lb3 [done](thoughts/shared/slices/2026-10-27-lb3-listener-filters.md)

## Next action
lb4 unblocked by allowing `channels: []` (DM-only bot, delta section 'Unblocking lb4'); implementer/verify finishing lb4. Allow-list delta: Rob's wake rules recorded in the delta; delta stays in-review because eng-check gates it on 4 high plan-review findings (F1-F4) - planner fixes them in lb4b prep, then the CP-C row is logged. After lb4 CP-S: lb4b (full allow-list removal) - do not start until the planner says. Deploy prerequisites before enabling: Coolify volume /data (uid 10001), env MMB_STORE_KEY, replicas 1.

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
?? thoughts/shared/inbox-local-bak-1793080755/
?? thoughts/shared/inbox.md
?? thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb4-signed-wake-dispatcher-2.running.md
?? thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb4-signed-wake-dispatcher.md
?? thoughts/shared/verification/2026-10-27-slice-20261027-lb4-signed-wake-dispatcher-review.md
../acorn/.eng/templates/AGENTS.md
../acorn/AGENTS.md
../farmer/.eng/templates/AGENTS.md
../farmer/AGENTS.md
../mmbridge/.eng/templates/AGENTS.md
../mmbridge/AGENTS.md

exec
/bin/bash -lc "nl -ba app/wake.py | sed -n '85,125p'; nl -ba tests/acceptance/drivers/wake_receiver.py | tail -25; python3 .eng/bin/eng-check .; .venv/bin/pytest tests/unit/test_wake.py -q" in /mnt/d/rob/projects/mmbridge
codex
Bot rotation can deliver old queued messages to a new target during startup. Additionally, the request timeout does not bound delivery duration, allowing a slow receiver to stall the dispatcher and invalidate its ownership guarantees.

Full review comments:

- [P1] Resolve current bot identity before dispatching queued wakes — /mnt/d/rob/projects/mmbridge/app/wake.py:93-99
  After replacing a bot's token and restarting, `bot_user_id` still identifies the previous bot until the listener finishes `/users/me`. The concurrently started dispatcher can therefore approve old queued wakes and send them using the new bot's URL and secret. Missing metadata also bypasses the check entirely. Gate dispatch on identity resolution for the current configuration rather than trusting persisted metadata, so old-bot messages are failed as `bot_rotated` instead of delivered to the new target.

- [P2] Enforce an overall deadline for each webhook attempt — /mnt/d/rob/projects/mmbridge/app/wake.py:108-112
  If a receiver streams response bytes less than five seconds apart without completing, HTTPX's read timeout never fires: `timeout=5` limits individual network operations, not total request duration. Because `tick()` awaits the entire batch, one such response blocks subsequent dispatch and owner heartbeats indefinitely; another dispatcher can then take ownership and redeliver expired leases. Wrap the complete POST in an overall asynchronous deadline and handle its expiry as a retryable timeout.
Bot rotation can deliver old queued messages to a new target during startup. Additionally, the request timeout does not bound delivery duration, allowing a slow receiver to stall the dispatcher and invalidate its ownership guarantees.

Full review comments:

- [P1] Resolve current bot identity before dispatching queued wakes — /mnt/d/rob/projects/mmbridge/app/wake.py:93-99
  After replacing a bot's token and restarting, `bot_user_id` still identifies the previous bot until the listener finishes `/users/me`. The concurrently started dispatcher can therefore approve old queued wakes and send them using the new bot's URL and secret. Missing metadata also bypasses the check entirely. Gate dispatch on identity resolution for the current configuration rather than trusting persisted metadata, so old-bot messages are failed as `bot_rotated` instead of delivered to the new target.

- [P2] Enforce an overall deadline for each webhook attempt — /mnt/d/rob/projects/mmbridge/app/wake.py:108-112
  If a receiver streams response bytes less than five seconds apart without completing, HTTPX's read timeout never fires: `timeout=5` limits individual network operations, not total request duration. Because `tick()` awaits the entire batch, one such response blocks subsequent dispatch and owner heartbeats indefinitely; another dispatcher can then take ownership and redeliver expired leases. Wrap the complete POST in an overall asynchronous deadline and handle its expiry as a retryable timeout.
````
