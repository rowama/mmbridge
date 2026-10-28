---
id: RUN-2026-10-27-code-review-slice-20261027-lb4b-drop-allowlist-2
type: run-log
phase: verify
status: ok
owner_agent: eng-run
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md, thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md, thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review-2.md]
role: code-review
runner: codex
tool: codex
slice: SLICE-20261027-lb4b-drop-allowlist
plan: thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md
base: cb4e711
exit_code: 0
pid: 55104
eng_run_pid: 55102
started: 2026-10-27T22:30:27
prompt_template: code-review.md v2
---
# eng-run code-review slice-20261027-lb4b-drop-allowlist

## Summary
- role: code-review; runner: codex (codex); exit code: 0; started 2026-10-27 22:30:27
- review file: thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review-2.md - No findings.

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
Your final message is saved by eng-run to thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review-2.md (a review-findings artifact). Findings are advisory; Rob decides.
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
session id: 01a1808f-2903-7c63-95c5-2ada66936e89
--------
user
changes against 'cb4e711'
exec
/bin/bash -lc 'cat PROJECT_STATE.md; cat AGENTS.md; python3 .eng/bin/eng-check .' in /mnt/d/rob/projects/mmbridge
 succeeded in 1578ms:
---
id: STATE
type: project-state
phase: implement
status: active
owner_agent: claude-code
date: 2026-10-27
links: []
triage: large             # unset | small | medium | large
active_slice: SLICE-20261027-lb4b-drop-allowlist
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
[SLICE-20261027-lb4b-drop-allowlist](thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md) (review: implemented at 14ecd18, Codex review no findings). Previous: lb4 [done](thoughts/shared/slices/2026-10-27-lb4-signed-wake-dispatcher.md)

## Next action
lb4 done (see Approval log; README wake-receiver/tamper demo deferred until set-bot + wake secret exist). Allow-list delta: CP-A amendment + CP-C speclock rows in the Approval log; re-locked specs/DSL applied (new live specs red until lb4b implements). F8 dispositioned (live-only per ADR-0010). lb4b implemented at 14ecd18 (unit 234 passed; lb4b specs 12 passed; review no findings). Next: planner runs eng-verify for lb4b, then requests CP-S (in-process demo); then lb5. Deploy prerequisites before enabling: Coolify volume /data (uid 10001), env MMB_STORE_KEY, replicas 1.

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
- Latest handoff: [thoughts/shared/handoffs/2026-10-27_22-25-35_lb4b-implemented-awaiting-verify.md](thoughts/shared/handoffs/2026-10-27_22-25-35_lb4b-implemented-awaiting-verify.md)
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
- **Plan review is a gate for medium/large:** the mandatory cross-model plan review must be linked and clean before CP-C; slice and architecture cross-model reviews stay advisory. Detail in `.eng/PROCESS.md` section 10.
- **Cross-model review** (Codex) of slices and architecture is advisory, never a gate (this does not cover the mandatory plan review above). See `.eng/PROCESS.md` section 10.
- **Push:** follow `push_permission` (default `ask`). With `standing`, after eng-verify PASS you may push to `main` without asking. **Docs-only commits always push to `main` without asking** (both modes). Tags and force-push still ask. Never merge without the owner.
- **Owner review notes** (`thoughts/shared/review-notes/`) belong to the owner. Agents never edit them until the owner says they are ready.
- **Owner-facing updates:** brief status prose (or skip), then a labeled `**Action for Rob**` numbered list (one step per line; pasteable commands in their own fence) or `No action for you.`; end with the decision he owes. Never mix his todos into a status/findings paragraph. Never use `$TOKEN`-style shell placeholders in samples — use `PASTE_…_HERE` or paste-at-prompt. See `.eng/templates/owner-update.md` (LESSONS L-007). **Risk mitigations you uncovered:** name risk + friction/ops cost + narrower alternative; **Decision needed** before baking into design/architecture/plan (L-008).

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
WARN  .eng/runners.toml: no on_complete hook configured ([hooks] empty or missing) - bots must stay attached to eng-run until exit; fire-and-forget needs a non-empty on_complete / <role>_on_complete (PROCESS.md section 10, LESSONS L-006)
WARN  PROJECT_STATE.md: ## Latest artifacts has 26 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 24 rows / 4221 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 110 artifact(s) checked

exec
/bin/bash -lc 'cat thoughts/shared/handoffs/2026-10-27_22-25-35_lb4b-implemented-awaiting-verify.md; cat .claude/skills/eng-review/SKILL.md; cat .eng/PROCESS.md | head -100; git diff cb4e71149cda690e854f165684c09565c12fac13 --stat; find . -name AGENTS.md -o -name AGENTS.override.md' in /mnt/d/rob/projects/mmbridge
 succeeded in 1713ms:
---
id: HANDO-20261027-lb4b-implemented-awaiting-verify
type: handoff
phase: implement
status: complete
owner_agent: claude-code
date: 2026-10-27T22:25:35-05:00
links: [thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md, thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md]
git_commit: 14ecd18
branch: main
next_skill: eng-verify
---
# Handoff: lb4b implemented, awaiting verify
<!-- Session handoff (agent to agent, one session). A standing orientation for a new implementer is a project brief: .eng/bin/eng-new brief. -->

## Task(s)
- SLICE-20261027-lb4b-drop-allowlist (delta plan Phase 1): **completed, status review**. Test-first; all automated criteria green. Codex slice review: no findings.

## Critical References
- thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md (Progress log with exit codes)
- thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md Phase 1
- thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review.md

## Recent changes
- app/live_filter.py:41 `decide(event, bot_user_id)`; :70 drops own/system/G only; O/P always wake (membership is the filter)
- app/store.py:40 `BotConfig` without `channels`; `validate` drops the channels rule; :88 `_decode` ignores a legacy `channels` key; :150 `save` writes no `channels`
- app/admin.py:20 `FIELDS` without channels; :48 `_username` (replaces `_resolve`, no channel lookups); :57 hidden `--channels` -> `invalid_argument: channels no longer used ...` before any Mattermost call; :87 `show` without channels; set-bot output `bot @x stored: wake_url ...`
- app/listener.py:108 `decide(ev, self.bot_user_id)`
- tests/acceptance/drivers/live.py:94 `given_channel(..., private=False)`, :144 `reply_in_thread`, :199 `assert_woken_once(thread=)` checks `post.root_id`, :215 `assert_not_member`
- tests/unit/test_live_filter.py, test_store.py, test_admin.py, test_listener.py, test_wake.py updated (see slice Progress log)
- CHANGELOG.md Unreleased "Changed" entry
- Commit 14ecd18 (code); docs commit follows

## Learnings
- The planner had already applied the re-lock in 6148856 (specs/DSL byte-identical to the drafts, eng-spec status ok), so this slice only needed the code/driver side.
- The fake Mattermost already broadcasts `posted` only to channel members (drivers/fake_mattermost.py `add_post`), so the non-member spec exercises the real "membership is the filter" behaviour without driver tricks.
- argparse: keeping `--channels` as a hidden (`help=SUPPRESS`) option gives the planned clear error instead of argparse's generic "unrecognized arguments" exit 2.
- The Codex reviewer sandbox cannot bind local ports, so uvicorn-backed listener tests error there; this does not reflect the local run.

## Artifacts
- app/live_filter.py, app/store.py, app/admin.py, app/listener.py
- tests/acceptance/drivers/live.py
- tests/unit/test_live_filter.py, tests/unit/test_store.py, tests/unit/test_admin.py, tests/unit/test_listener.py, tests/unit/test_wake.py
- CHANGELOG.md
- thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md (status review)
- thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md (Phase 1 automated boxes ticked)
- thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review.md (addressed, no findings)
- thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb4b-drop-allowlist.md
- PROJECT_STATE.md

## Approvals
- Requested (via the planner after eng-verify): CP-S for lb4b - in-process demo (Manual Verification in the slice card).
- None granted this session.

## Action Items & Next Steps
1. Planner: eng-verify lb4b at 14ecd18 (unit, the 12-case lb4b spec command, default acceptance, eng-spec status, eng-check).
2. Planner: request CP-S from Rob with the in-process demo steps; push per `push_permission: standing` after verify PASS.
3. Then lb5 (drop/reconnect + catch-up across member channels on all teams; the 2 drop specs currently fail with `NotImplementedError` by design).
4. Docs that still mention channel lists (README / architecture text, if any remain) are planner territory; not touched here.

## Other Notes
- Verification at 14ecd18: unit 234 passed (exit 0); lb4b spec command 12 passed (exit 0); default acceptance 16 passed / 15 skipped (exit 0); full `--channel live` 13 passed / 2 failed (lb5 drop specs only); eng-spec status matches lock; eng-check OK (3 pre-existing warnings).
- No locked spec, DSL interface or DSL assertion step body edited.
- Not pushed. Left untouched as found: uncommitted AGENTS.md / OWNER-GUIDE.md edits, untracked receiver.py, thoughts/shared/inbox.md, thoughts/shared/inbox-local-bak-1793080755/, the eng-run `.running.md` marker.
- Inbox: thoughts/shared/inbox.md exists (untracked); not processed.
cat: .claude/skills/eng-review/SKILL.md: No such file or directory
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

 AGENTS.md                                          |    7 +-
 CHANGELOG.md                                       |    4 +
 OWNER-GUIDE.md                                     |    2 +
 PROJECT_STATE.md                                   |    9 +-
 app/admin.py                                       |   52 +-
 app/listener.py                                    |    2 +-
 app/live_filter.py                                 |   11 +-
 app/store.py                                       |   18 +-
 tests/acceptance/drivers/live.py                   |   37 +-
 tests/unit/test_admin.py                           |   51 +-
 tests/unit/test_listener.py                        |   13 +-
 tests/unit/test_live_filter.py                     |   51 +-
 tests/unit/test_store.py                           |   25 +-
 tests/unit/test_wake.py                            |    2 +-
 ...27_22-25-35_lb4b-implemented-awaiting-verify.md |   65 +
 .../2026-10-27-live-bots-delta-no-allowlist.md     |    4 +-
 ...de-review-slice-20261027-lb4b-drop-allowlist.md | 2134 ++++++++++++++++++++
 .../slices/2026-10-27-lb4b-drop-allowlist.md       |   28 +-
 ...27-slice-20261027-lb4b-drop-allowlist-review.md | 2113 +++++++++++++++++++
 19 files changed, 4486 insertions(+), 142 deletions(-)
./.eng/templates/AGENTS.md
./AGENTS.md

exec
/bin/bash -lc 'git diff cb4e71149cda690e854f165684c09565c12fac13 -- app tests; cat app/live_filter.py app/store.py app/admin.py' in /mnt/d/rob/projects/mmbridge
 succeeded in 152ms:
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
"""Operator CLI for the live bot (ADR-0006/0009): `python -m app.admin set-bot | show | rotate-key | failed | stats`.

Run inside the container (Coolify terminal). The token is read from stdin only and never printed or logged;
the wake secret is printed once when generated, never by `show`. No channel list: Mattermost membership decides
which channel posts wake the bot, and the bridge never joins (REQ-7); `--channels` is refused as no longer used.
`failed`/`stats` read state.db and never print message text.
"""
import argparse
import asyncio
import json
import os
import secrets
import sys
import time

from app import logging as mlog
from app import state, store
from app.mattermost import MATTERMOST_URL, Client, MMError

FIELDS = ("token", "wake_url", "wake_secret")


class AdminError(Exception):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(code)
        self.code, self.detail = code, detail


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m app.admin", description="mmbridge live bot admin")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("set-bot", help="store the bot token and wake URL (token read from stdin)")
    s.add_argument("--token-stdin", action="store_true", required=True, help="read the bot token from stdin")
    s.add_argument("--wake-secret-stdin", action="store_true",
                   help="read the wake secret from the next stdin line instead of generating one")
    s.add_argument("--wake-url", required=True)
    s.add_argument("--channels", default=None, help=argparse.SUPPRESS)   # removed: refused with a clear error
    sub.add_parser("show", help="show the stored config (token masked, secret hidden)")
    r = sub.add_parser("rotate-key", help="re-encrypt the store with a new MMB_STORE_KEY")
    r.add_argument("--new-key-env", default="MMB_STORE_KEY_NEW", help="env var holding the new key")
    r.add_argument("--old-key-env", default="MMB_STORE_KEY", help="env var holding the current key(s)")
    f = sub.add_parser("failed", help="list failed wakes, or requeue one")
    f.add_argument("--retry", metavar="POST_ID", help="requeue this failed wake for delivery")
    sub.add_parser("stats", help="wake counts and post->delivered latency")
    return p


async def _username(token: str, transport) -> str:
    try:
        return (await Client(token, MATTERMOST_URL, transport=transport).get("/users/me"))["username"]
    except MMError as e:
        detail = "Mattermost rejected the bot token" if e.code == "unauthorized" else ""
        raise AdminError(e.code, detail) from None


def _set_bot(a, stdin, out, transport) -> None:
    if a.channels is not None:
        raise AdminError("invalid_argument", "channels no longer used (the bot wakes in channels it is a member of)")
    lines = stdin.read().splitlines()
    token = lines[0].strip() if lines else ""
    if not token:
        raise AdminError("invalid_argument", "no token on stdin")
    supplied = a.wake_secret_stdin
    secret = (lines[1].strip() if len(lines) > 1 else "") if supplied else secrets.token_urlsafe(32)
    if supplied and len(secret) < store.MIN_SECRET:
        raise AdminError("invalid_argument", "wake_secret: must be at least %d characters" % store.MIN_SECRET)
    if not store.https_ok(a.wake_url):
        raise AdminError("invalid_argument", "wake_url: must be https")
    key = os.getenv("MMB_STORE_KEY")
    if not (key or "").strip():
        raise store.StoreError("store_key_missing")
    username = asyncio.run(_username(token, transport))
    path = store.path_from_env()
    try:
        prev = store.load(path, key)
    except store.StoreError:
        prev = None
    cfg = store.BotConfig(token=token, wake_url=a.wake_url, wake_secret=secret)
    store.save(path, key, cfg)
    changed = [f for f in FIELDS if prev is None or getattr(prev, f) != getattr(cfg, f)]
    mlog.log.info(json.dumps({"event": "store_updated", "fields": changed}))
    print("bot @%s stored: wake_url %s" % (username, cfg.wake_url), file=out)
    if not supplied:
        print("wake secret (shown once; give it to the receiver): %s" % secret, file=out)


def _show(out) -> None:
    cfg = store.load(store.path_from_env(), os.getenv("MMB_STORE_KEY"))
    print("version: %d\ntoken: ****%s\nwake_url: %s\nwake_secret: set (hidden)" % (
        cfg.version, cfg.token[-4:], cfg.wake_url), file=out)


def _rotate_key(a, out) -> None:
    store.rotate(store.path_from_env(), os.getenv(a.new_key_env), os.getenv(a.old_key_env))
    mlog.log.info(json.dumps({"event": "store_updated", "fields": ["key"]}))
    print("store re-encrypted with %s; set MMB_STORE_KEY to that key" % a.new_key_env, file=out)


def _failed(a, out) -> None:
    st = state.State(state.path_from_env())
    if a.retry:
        if not st.requeue(a.retry):
            raise AdminError("not_found", "no failed wake %s" % a.retry)
        mlog.log.info(json.dumps({"event": "wake_requeued", "post_id": a.retry}))
        print("requeued %s" % a.retry, file=out)
        return
    rows = st.failed()
    if not rows:
        print("no failed wakes", file=out)
    for w in rows:
        at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(w.updated_at))
        print("%s  channel %s  attempts %d  error %s  at %s" % (w.post_id, w.channel_id, w.attempts,
                                                              w.last_error or "-", at), file=out)


def _stats(out) -> None:
    s = state.State(state.path_from_env()).stats()
    if not s["counts"]:
        print("no wakes yet", file=out)
        return
    for k in sorted(s["counts"]):
        print("%s: %d" % (k, s["counts"][k]), file=out)
    lat = s["latency_ms"]
    print("latency post->delivered (ms): n=%d p50=%s p95=%s" % (lat["n"], lat["p50"], lat["p95"]), file=out)


def main(argv=None, stdin=None, stdout=None, transport=None) -> int:
    mlog.setup()
    stdin, out = stdin or sys.stdin, stdout or sys.stdout
    a = _parser().parse_args(argv)
    try:
        if a.cmd == "set-bot":
            _set_bot(a, stdin, out, transport)
        elif a.cmd == "show":
            _show(out)
        elif a.cmd == "rotate-key":
            _rotate_key(a, out)
        elif a.cmd == "failed":
            _failed(a, out)
        else:
            _stats(out)
    except (AdminError, store.StoreError, state.StateError) as e:
        print("error: %s%s" % (e.code, ": " + e.detail if e.detail else ""), file=out)
        return 1
    except OSError as e:
        print("error: store_unwritable: %s" % e.strerror, file=out)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

exec
/bin/bash -lc "rg '\\.channels|BotConfig\\(|decide\\(' app; cat app/listener.py; ls .claude/skills | grep review; .venv/bin/pytest tests/unit/test_admin.py tests/unit/test_store.py tests/unit/test_live_filter.py tests/unit/test_wake.py -q" in /mnt/d/rob/projects/mmbridge
exec
/bin/bash -lc 'git diff cb4e71149cda690e854f165684c09565c12fac13 -- tests/unit/test_admin.py tests/unit/test_listener.py tests/unit/test_live_filter.py; python3 .eng/bin/eng-check .' in /mnt/d/rob/projects/mmbridge
 succeeded in 1637ms:
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
WARN  .eng/runners.toml: no on_complete hook configured ([hooks] empty or missing) - bots must stay attached to eng-run until exit; fire-and-forget needs a non-empty on_complete / <role>_on_complete (PROCESS.md section 10, LESSONS L-006)
WARN  PROJECT_STATE.md: ## Latest artifacts has 26 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 24 rows / 4221 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 110 artifact(s) checked

2026-10-28T03:31:24.649825Z ERROR codex_core::session: failed to record rollout items: thread 01a1808f-2ddc-7912-9bc3-d5bcbe392485 not found
codex
The changes consistently remove the channel allow-list from configuration, administration, and event filtering while preserving legacy-store compatibility. No actionable regressions were identified in the diff.
The changes consistently remove the channel allow-list from configuration, administration, and event filtering while preserving legacy-store compatibility. No actionable regressions were identified in the diff.
````
