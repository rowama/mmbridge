---
id: RUN-2026-10-28-code-review-slice-20261027-lb5-wireup-reconnect-acceptance-4
type: run-log
phase: verify
status: ok
owner_agent: eng-run
date: 2026-10-28
links: [thoughts/shared/plans/2026-10-27-live-bots.md, thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md, thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-4.md]
role: code-review
runner: codex
tool: codex
slice: SLICE-20261027-lb5-wireup-reconnect-acceptance
plan: thoughts/shared/plans/2026-10-27-live-bots.md
base: 3ed94b4
exit_code: 0
pid: 619894
eng_run_pid: 619893
started: 2026-10-28T13:09:21
prompt_template: code-review.md v2
---
# eng-run code-review slice-20261027-lb5-wireup-reconnect-acceptance

## Summary
- role: code-review; runner: codex (codex); exit code: 0; started 2026-10-28 13:09:21
- review file: thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-4.md - No findings.

## Command
```
codex review --base 3ed94b4
```

## Prompt
```
You are the independent code reviewer for this repository (eng-process kit v2.5.9). You did not write this code. Do not edit any file.

Follow the cross-model review step of eng-verify (.claude/skills/eng-verify/SKILL.md) and .eng/PROCESS.md section 10.

Review the changes of slice SLICE-20261027-lb5-wireup-reconnect-acceptance (diff 3ed94b4...HEAD; slice card: thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md; plan: thoughts/shared/plans/2026-10-27-live-bots.md) for correctness against the slice's acceptance criteria, missing or weak tests, security (auth, tenancy, secrets, injection), error handling, and maintainability.

Executable specs (v2.5): run `python .eng/bin/eng-spec status .`. Any change to locked specs or the DSL public interface is a [high] finding unless Rob re-approved it (new CP-C speclock row). For every changed DSL assertion step (assert_/then_/expect_/check_/verify_) name the step (e.g. `assert_order_placed`) in a finding and say whether the check got weaker. Driver changes are fine unless they hide failures (swallowed errors, retries that mask bugs, sleeps).

Output: a numbered list of findings, each as
  N. [severity] file:line - finding - suggested fix
with severity one of critical | high | medium | low. If you find nothing, write exactly "No findings."
Your final message is saved by eng-run to thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-4.md (a review-findings artifact). Findings are advisory; Rob decides.
```

## Output
```
OpenAI Codex v0.164.0
--------
workdir: /mnt/d/rob/projects/mmbridge
model: gpt-6.1-sol
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR]
reasoning effort: none
reasoning summaries: none
session id: 01a183b3-ce85-73c2-94b4-21c890f3c98f
--------
user
changes against '3ed94b4'
exec
/bin/bash -lc 'cat PROJECT_STATE.md; cat AGENTS.md; git status --short; git diff --stat 3ed94b421d7367292510790ff6f73598eee94237' in /mnt/d/rob/projects/mmbridge
 succeeded in 968ms:
---
id: STATE
type: project-state
phase: implement
status: active
owner_agent: claude-code
date: 2026-10-28
links: []
triage: large             # unset | small | medium | large
active_slice: SLICE-20261027-lb5-wireup-reconnect-acceptance
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
[SLICE-20261027-lb5-wireup-reconnect-acceptance](thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md) (review: implemented b5926c6, all Phase 5 automated checks exit 0 incl. container live suite). Previous: lb4b [done](thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md)

## Next action
lb4b done (CP-S 2026-10-28; live Mattermost->receiver e2e and wake posts deferred until lb5 wires listener/dispatcher into main). lb5 implemented (b5926c6, status review). Next: advisory Codex slice review (codex CLI missing on the implementer shell; run `eng-run code-review` where available), planner eng-verify (incl. PR-11 eng-spec trace), OWNER-GUIDE pointer, then CP-S lb5 (live e2e demo, Mattermost restart mid-demo). Deploy prerequisites before enabling: Coolify volume /data (uid 10001), env MMB_STORE_KEY, replicas 1.

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
- Verification lb4b (PASS): [thoughts/shared/verification/2026-10-27-lb4b-drop-allowlist.md](thoughts/shared/verification/2026-10-27-lb4b-drop-allowlist.md)
- Latest handoff: [thoughts/shared/handoffs/2026-10-28_12-50-17_lb5-implemented-awaiting-review.md](thoughts/shared/handoffs/2026-10-28_12-50-17_lb5-implemented-awaiting-review.md)
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
| 2026-10-28 | CP-S | thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md | approved (verify PASS 14ecd18; demo set-bot + --channels reject; live Mattermost->receiver e2e deferred until listener/dispatcher wired in lb5) |
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
 M AGENTS.md
 M OWNER-GUIDE.md
?? receiver.py
?? thoughts/shared/inbox-local-bak-1793080755/
?? thoughts/shared/inbox.md
?? thoughts/shared/runs/2026-10-28-code-review-slice-20261027-lb5-wireup-reconnect-acceptance-2.md
?? thoughts/shared/runs/2026-10-28-code-review-slice-20261027-lb5-wireup-reconnect-acceptance-3.md
?? thoughts/shared/runs/2026-10-28-code-review-slice-20261027-lb5-wireup-reconnect-acceptance-4.running.md
?? thoughts/shared/runs/2026-10-28-code-review-slice-20261027-lb5-wireup-reconnect-acceptance.md
?? thoughts/shared/runs/2026-10-28-implement-slice-20261027-lb5-wireup-reconnect-acceptance.md
?? thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-2.md
?? thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-3.md
?? thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review.md
 AGENTS.md                                          |   7 +-
 CHANGELOG.md                                       |   4 +
 OWNER-GUIDE.md                                     |   2 +
 PROJECT_STATE.md                                   |   8 +-
 README.md                                          |  21 ++
 app/listener.py                                    | 379 ++++++++++++++++++---
 app/live.py                                        | 176 ++++++++++
 app/main.py                                        |  15 +-
 app/state.py                                       |  33 +-
 tests/acceptance/drivers/fake_mattermost.py        | 114 +++++--
 tests/acceptance/drivers/live.py                   | 253 +++++++++-----
 tests/acceptance/drivers/wake_receiver.py          |  23 +-
 tests/unit/test_app.py                             |   2 +-
 tests/unit/test_listener.py                        |  15 +-
 tests/unit/test_main_live.py                       | 297 ++++++++++++++++
 tests/unit/test_reconnect.py                       | 369 ++++++++++++++++++++
 ...-28_12-50-17_lb5-implemented-awaiting-review.md |  63 ++++
 thoughts/shared/plans/2026-10-27-live-bots.md      |   6 +-
 .../2026-10-27-lb5-wireup-reconnect-acceptance.md  |  43 ++-
 19 files changed, 1645 insertions(+), 185 deletions(-)

exec
/bin/bash -lc 'cat thoughts/shared/handoffs/2026-10-28_12-50-17_lb5-implemented-awaiting-review.md; cat .eng/PROCESS.md >/dev/null; cat .claude/skills/eng-code-review/SKILL.md; python3 .eng/bin/eng-check .; find app tests -name AGENTS.md -o -name AGENTS.override.md; git diff 3ed94b421d7367292510790ff6f73598eee94237 -- app' in /mnt/d/rob/projects/mmbridge
 succeeded in 1750ms:
---
id: HANDO-20261028-lb5-implemented-awaiting-review
type: handoff
phase: implement
status: complete
owner_agent: claude-code
date: 2026-10-28T12:50:17-05:00
links: [thoughts/shared/plans/2026-10-27-live-bots.md, thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md]
git_commit: b5926c6
branch: main
next_skill: eng-verify
---
# Handoff: lb5 implemented, awaiting Codex review + verify
<!-- Session handoff (agent to agent, one session). A standing orientation for a new implementer is a project brief: .eng/bin/eng-new brief. -->

## Task(s)
- SLICE-20261027-lb5-wireup-reconnect-acceptance (plan Phase 5): **completed, status review**. Test-first. All Phase 5 automated criteria exit 0, including the full live suite against the real container. Open: the advisory Codex slice review was not run (no `codex` CLI here), OWNER-GUIDE pointer, PR-11 trace (planner).

## Critical References
- thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md (Progress log with exit codes; deviations)
- thoughts/shared/plans/2026-10-27-live-bots.md Phase 5
- docs/architecture/2026-10-26-live-bots.md 'catch-up channel discovery' + failure modes

## Recent changes
- app/live.py:35 `ConfigHolder` (mtime reload, `store_reload_failed` keeps old config, `store_updated` field names only); :84 `supervise` (task_crashed, 1->60 s restart, `crashed` set -> health degraded); :108 `LiveRuntime` (:125 start gating flag/store/state -> disabled/off; :171 health)
- app/main.py:27 lifespan `live.start()`/`stop()`; :37 `/health` = `{"ok", "listener", "wake_failed_24h"}`; `create_app(live=)` for tests
- app/listener.py:135 `run()` reconnect loop (Unauthorized -> degraded + 5 min retry, LeaseHeld -> idle, errors -> backoff :123); :163 `connect_once()` (lease, users/me, resume query); :235 hello: resumed vs new id -> seq reset + `_catch_up`; seq gap -> catch-up; :308 `_refresh_members` (all teams paged + cursors + seen); :328 membership events; :340 `_catch_up` (pending survives failures, keeps its start); :384 `_since` paged; :112 `config_changed` (new token -> reconnect, no resume)
- app/state.py:162 `delete_cursor`, :166 `cursor_channels`, :181 `claim_owner(key=)`, :194 `release_owner`, :277 `failed_count`
- tests/acceptance/drivers/live.py:69 `_InProcess`, :106 `_Container` (ADR-0010 layer 4), :218 `given_live_bot` waits for /health ok, :341 drop/restore
- tests/acceptance/drivers/fake_mattermost.py: `clock=`, `since`, paging, D/G in team channel lists, `ws_refuse`, resumable dead queue, `ws_event`; drivers/wake_receiver.py `serve()`
- tests/unit/test_reconnect.py (14), tests/unit/test_main_live.py (12); test_listener.py single-connection tests use `connect_once()`; test_app.py health fields
- README.md "Live bots (deploy)"; CHANGELOG.md Unreleased Added

## Learnings
- `run()` no longer returns on a drop: unit tests that need one connection call `connect_once()`; fixtures cancel `run()`.
- A test helper `until(lambda: coro())` is always truthy: await the result if it is a coroutine (caught in test_main_live.py, fixed before commit).
- Catch-up must remember where it started: if it fails, the next hello's "last alive" is later than the outage start. `_catchup_from` is kept while `_catchup_pending`, and meta `last_event_at` is not written while pending.
- Fake drop must refuse REST too (`ws_refuse` -> 503), or users/me succeeds and the 403 handshake looks like a bad token (Unauthorized -> 5 min wait).
- Docker here is a native engine in WSL; `--network host` works, so the fakes stay on 127.0.0.1. One-off `docker run --rm -i ... python -m app.admin set-bot` on the named volume before the server starts mirrors the operator flow (set-bot, then flag on).
- `docker logs` shows every bridge log line twice (stdout handler + propagation). This happened before lb5 and is not touched here; worth a TODO.

## Artifacts
- app/live.py (new), app/main.py, app/listener.py, app/state.py
- tests/unit/test_reconnect.py (new), tests/unit/test_main_live.py (new), tests/unit/test_listener.py, tests/unit/test_app.py
- tests/acceptance/drivers/live.py, tests/acceptance/drivers/fake_mattermost.py, tests/acceptance/drivers/wake_receiver.py
- README.md, CHANGELOG.md
- thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md (status review)
- thoughts/shared/plans/2026-10-27-live-bots.md (Phase 5 automated boxes ticked)
- PROJECT_STATE.md

## Approvals
- None requested or granted this session. Next: CP-S lb5 (Coolify demo incl. Mattermost restart mid-demo), requested by the planner after eng-verify.

## Action Items & Next Steps
1. Planner/Rob: run the advisory Codex slice review where `codex` is installed (security-relevant slice): `python3 .eng/bin/eng-run code-review SLICE-20261027-lb5-wireup-reconnect-acceptance`; implementer answers findings.
2. Planner: eng-verify lb5 at b5926c6: `docker build -t mmbridge:lb5 .`, `.venv/bin/pytest tests/unit -q`, `.venv/bin/pytest tests/acceptance --channel live -q` (container; `LIVE_MODE=inprocess` for the fast path), `.venv/bin/pytest tests/acceptance -q`, `eng-spec status .`, `eng-spec trace .` (PR-11: REQ-A* show "(not in an approved design)", which is the design-amendment approval tracking, to be resolved by the planner), `eng-check .`.
3. Planner: add an OWNER-GUIDE pointer to README "Live bots (deploy)" (OWNER-GUIDE.md has someone else's uncommitted edits, not touched).
4. Then CP-S lb5 on Coolify per the plan Demo script; check the fake-drift points (resume hello shape, `since` semantics) against real Mattermost.

## Other Notes
- No locked spec, DSL public interface or DSL assertion step body edited (`eng-spec status` matches lock). The driver's `assert_no_token_anywhere` now also asserts the log capture is non-empty (it contains `wake_queued`), which makes that check stricter.
- Not pushed (push_permission standing applies only after eng-verify PASS). Left untouched as found: uncommitted AGENTS.md / OWNER-GUIDE.md edits, untracked receiver.py, thoughts/shared/inbox.md (6 lines, not processed), thoughts/shared/inbox-local-bak-1793080755/, the eng-run `.running.md` marker.
- Docker image `mmbridge:lb5` is built locally; test containers and volumes are named `mmb-live-*` and removed at driver close (verified none left).
cat: .claude/skills/eng-code-review/SKILL.md: No such file or directory
WARN  .eng/runners.toml: no on_complete hook configured ([hooks] empty or missing) - bots must stay attached to eng-run until exit; fire-and-forget needs a non-empty on_complete / <role>_on_complete (PROCESS.md section 10, LESSONS L-006)
WARN  PROJECT_STATE.md: ## Latest artifacts has 27 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 25 rows / 4448 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 121 artifact(s) checked
diff --git a/app/listener.py b/app/listener.py
index 19eed23..e90e9d0 100644
--- a/app/listener.py
+++ b/app/listener.py
@@ -2,19 +2,29 @@
 
 run(): GET /users/me -> WS /api/v4/websocket with `Authorization: Bearer` -> hello{connection_id} -> for each
 `posted` event, live_filter.decide -> wake payload (ADR-0008 schema, no token; channel/team/sender lookups
-cached) -> state.enqueue_and_advance (dedupe gate + forward-only cursor, PR-3). Tracks seq (gaps logged as
-ws_seq_gap); sends the Mattermost `ping` action every PING_S and treats IDLE_S without any frame as dead.
-One connection per run(): reconnect, resume and catch-up are slice 5. Never joins channels or posts.
+cached) -> state.enqueue_and_advance (dedupe gate + forward-only cursor, PR-3). Tracks seq; sends the
+Mattermost `ping` action every PING_S and treats IDLE_S without any frame as dead. Never joins channels or posts.
+
+lb5: run() reconnects forever (backoff 1->60 s with jitter) and asks to resume with
+`?connection_id&sequence_number`. Same connection_id in hello = resumed (missed events are replayed). A new id,
+or a seq gap, runs REST catch-up: membership across all teams (+ D channels, channels with a cursor, channels
+seen on the socket), then per channel `GET /channels/{id}/posts` paged back by post id (`before=`; never
+`since`, which Mattermost does not page), ascending (create_at, post_id),
+each post through decide() and enqueue_and_advance (the ledger dedupes). Channels without a cursor start at meta
+`last_event_at` (last alive); posts older than LIVE_CATCHUP_MINUTES are skipped (`catchup_skipped`). 401 ->
+`degraded`, retry every 5 min or on a config change. One listener per state.db (meta lease `listener_owner`).
 """
 import asyncio
 import itertools
 import json
 import logging
+import os
+import random
 import time
 from datetime import datetime, timezone
 
 import websockets
-from websockets.exceptions import ConnectionClosed
+from websockets.exceptions import ConnectionClosed, InvalidHandshake, InvalidStatus
 
 from app import logging as mlog
 from app.live_filter import WakeIntent, decide
@@ -23,6 +33,12 @@ from app.wake import token_fp
 
 PING_S = 30
 IDLE_S = 60
+BACKOFF_S, MAX_BACKOFF_S = 1.0, 60.0
+AUTH_RETRY_S = 300
+LEASE_TTL_S = 60
+PER_PAGE = 200
+MAX_PAGES = 50
+ALIVE_EVERY_S = 5
 
 # websockets logs handshake headers (incl. Authorization) and frames at DEBUG: own logger, redacted, INFO.
 _ws_log = logging.getLogger("mmbridge.ws")
@@ -49,85 +65,364 @@ def _iso(ms: int) -> str:
     return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
 
 
+class Unauthorized(Exception):
+    """users/me or the websocket handshake refused the bot token."""
+
+
+class LeaseHeld(Exception):
+    """Another listener holds the state.db lease."""
+
+
 class Listener:
     def __init__(self, cfg, state, client_factory, ws_connect=connect, clock=time.time,
-                 base_url: str = MATTERMOST_URL, ping_s: float = PING_S, idle_s: float = IDLE_S):
-        self.cfg, self.state, self.client_factory, self.ws_connect = cfg, state, client_factory, ws_connect
+                 base_url: str = MATTERMOST_URL, ping_s: float = PING_S, idle_s: float = IDLE_S,
+                 backoff_s: float = BACKOFF_S, max_backoff_s: float = MAX_BACKOFF_S,
+                 auth_retry_s: float = AUTH_RETRY_S, lease_retry_s: float = LEASE_TTL_S / 2,
+                 catchup_minutes: float | None = None, refresh_s: float | None = None, per_page: int = PER_PAGE,
+                 rand=random.random):
+        """cfg: BotConfig or a zero-arg callable returning the current one (ConfigHolder.get, PR-2)."""
+        self._cfg = cfg if callable(cfg) else (lambda: cfg)
+        self.state, self.client_factory, self.ws_connect = state, client_factory, ws_connect
         self.clock, self.base_url, self.ping_s, self.idle_s = clock, base_url, ping_s, idle_s
-        self.status = "off"                   # off | connecting | ok
+        self.backoff_s, self.max_backoff_s, self.rand = backoff_s, max_backoff_s, rand
+        self.auth_retry_s, self.lease_retry_s, self.per_page = auth_retry_s, lease_retry_s, per_page
+        self.window_ms = int(60_000 * (catchup_minutes if catchup_minutes is not None
+                                       else float(os.getenv("LIVE_CATCHUP_MINUTES", "15"))))
+        self.refresh_s = refresh_s if refresh_s is not None else float(os.getenv("LIVE_MEMBERSHIP_REFRESH_S", "300"))
+        self.status = "off"                   # off | connecting | ok | degraded (401)
         self.bot_user_id = self.connection_id = self.last_seq = None
+        self.members: dict = {}               # channel id -> channel (O/P/D), catch-up set
+        self._seen: dict = {}                 # channel id -> type, seen on the socket since start
         self._bot: dict = {}
         self._channels: dict = {}
         self._teams: dict = {}
         self._users: dict = {}
+        self._alive_at = None                 # ms, last frame received (meta last_event_at)
+        self._alive_written = 0.0
+        self._refreshed_at = 0.0
+        self._catchup_pending = False
+        self._catchup_from = None
+        self._resume_id = None
+        self._ws = None
+        self._wake = asyncio.Event()
+
+    @property
+    def cfg(self):
+        return self._cfg()
+
+    def config_changed(self, old, new) -> None:
+        """ConfigHolder subscriber: a new token reconnects at once (no resume across tokens, fresh lookups)."""
+        if new.token == old.token:
+            return
+        mlog.register_secret(new.token)
+        self.connection_id = None
+        self._channels, self._teams, self._users = {}, {}, {}
+        self._wake.set()
+        if self._ws is not None:
+            asyncio.ensure_future(self._ws.close())
+
+    def _backoff(self, attempt: int) -> float:
+        d = min(self.max_backoff_s, self.backoff_s * 2 ** (max(attempt, 1) - 1))
+        return d * (0.5 + 0.5 * self.rand())
+
+    async def _pause(self, seconds: float) -> None:
+        """Sleep, cut short by a config change."""
+        self._wake.clear()
+        try:
+            await asyncio.wait_for(self._wake.wait(), seconds)
+        except TimeoutError:
+            pass
 
     async def run(self) -> None:
-        mlog.register_secret(self.cfg.token)
-        client = self.client_factory(self.cfg.token)
+        """Reconnect forever (cancel to stop)."""
+        attempt = 0
+        try:
+            while True:
+                try:
+                    ok = await self.connect_once()
+                    attempt = 0 if ok else attempt + 1
+                except Unauthorized:
+                    self.status = "degraded"
+                    mlog.log.warning(json.dumps({"event": "mm_unauthorized", "retry_s": self.auth_retry_s}))
+                    await self._pause(self.auth_retry_s)
+                    continue
+                except LeaseHeld:
+                    _log("listener_lease_held", instance=self.state.instance_id)
+                    await self._pause(self.lease_retry_s)
+                    continue
+                except (OSError, TimeoutError, MMError, InvalidHandshake, ConnectionClosed) as e:
+                    attempt += 1
+                    _log("ws_connect_failed", error=getattr(e, "code", None) or type(e).__name__)
+                delay = self._backoff(attempt)
+                self.status = "connecting"
+                _log("ws_reconnect", attempt=attempt, delay=round(delay, 2))
+                await self._pause(delay)
+        finally:
+            self.status = "off"
+            await asyncio.to_thread(self.state.release_owner, "listener_owner")
+
+    async def connect_once(self) -> bool:
+        """One connection; True if it reached hello (then dropped/idled). Raises Unauthorized / LeaseHeld."""
+        cfg = self.cfg
+        mlog.register_secret(cfg.token)
+        client = self.client_factory(cfg.token)
         self.status = "connecting"
+        reached = False
         try:
-            me = await client.get("/users/me")
+            if not await asyncio.to_thread(self.state.claim_owner, self.clock(), LEASE_TTL_S, "listener_owner"):
+                self.status = "off"
+                raise LeaseHeld()
+            if self._alive_at is None:
+                v = await asyncio.to_thread(self.state.get_meta, "last_event_at")
+                self._alive_at = int(v) if v else None
+            try:
+                me = await client.get("/users/me")
+            except MMError as e:
+                if e.code == "unauthorized":
+                    raise Unauthorized() from None
+                raise
+            if me["id"] != self.bot_user_id:
+                self.connection_id, self.members, self._seen = None, {}, {}
             self.bot_user_id, self._bot = me["id"], {"user_id": me["id"], "username": me["username"]}
             await asyncio.to_thread(self.state.set_meta, "bot_user_id", me["id"])   # dispatcher: bot_rotated
             await asyncio.to_thread(self.state.set_meta, "bot_identity",              # id + token as one row
-                                    token_fp(self.cfg.token) + ":" + me["id"])
-            async with self.ws_connect(ws_url(self.base_url), {"Authorization": "Bearer " + self.cfg.token}) as ws:
+                                    token_fp(cfg.token) + ":" + me["id"])
+            url = ws_url(self.base_url)
+            self._resume_id = self.connection_id
+            if self.connection_id and self.last_seq is not None:
+                url += "?connection_id=%s&sequence_number=%d" % (self.connection_id, self.last_seq + 1)
+            try:
+                conn = self.ws_connect(url, {"Authorization": "Bearer " + cfg.token})
+                ws = await conn.__aenter__()
+            except InvalidStatus as e:
+                if e.response.status_code in (401, 403):
+                    raise Unauthorized() from None
+                raise
+            self._ws = ws
+            try:
                 pinger = asyncio.create_task(self._ping(ws))
                 try:
-                    await self._read(ws, client)
+                    reached = await self._read(ws, client)
                 finally:
                     pinger.cancel()
+            finally:
+                self._ws = None
+                await conn.__aexit__(None, None, None)
         finally:
-            self.status = "off"
+            if self.status != "degraded":
+                self.status = "off"
+        return reached
 
-    async def _read(self, ws, client) -> None:
+    async def _read(self, ws, client) -> bool:
+        reached = False
         while True:
             try:
                 raw = await asyncio.wait_for(ws.recv(), self.idle_s)
             except TimeoutError:
                 _log("ws_idle", seconds=self.idle_s)
-                return
+                return reached
             except ConnectionClosed:
                 _log("ws_closed", connection_id=self.connection_id)
-                return
+                return reached
+            prev_alive = self._alive_at
+            self._alive_at = int(self.clock() * 1000)   # persisted only once the frame is handled
             try:
-                ev = json.loads(raw)
-            except ValueError:
-                mlog.log.warning(json.dumps({"event": "event_invalid", "reason": "json"}))
-                continue
-            if not isinstance(ev, dict) or "event" not in ev:
-                continue                      # ping replies ({"status","seq_reply"}) and other non-events
-            self._track_seq(ev)
-            if ev["event"] == "hello":
-                self.connection_id = (ev.get("data") or {}).get("connection_id")
-                await asyncio.to_thread(self.state.set_meta, "ws_connection_id", self.connection_id or "")
-                self.status = "ok"
-                _log("ws_connected", connection_id=self.connection_id,
-                     server_version=(ev.get("data") or {}).get("server_version"))
-                continue
-            intent = decide(ev, self.bot_user_id)
-            if intent:
-                payload = await self._payload(intent, client)
-                new = await asyncio.to_thread(self.state.enqueue_and_advance, intent.post_id, intent.channel_id,
-                                              payload, intent.create_at)
-                _log("wake_queued", post_id=intent.post_id, channel_id=intent.channel_id, new=new)
-
-    def _track_seq(self, ev: dict) -> None:
+                if await self._frame(raw, client, prev_alive):
+                    reached = True
+            except BaseException:
+                self._alive_at = prev_alive   # not handled: a later catch-up must still start before this frame
+                raise
+            await self._mark_alive()
+
+    async def _frame(self, raw, client, prev_alive: int | None) -> bool:
+        """Handle one frame; True when it was a hello (connection established). Raises leave last_seq and
+        meta last_event_at untouched, so a reconnect resumes/catches up from before this frame."""
+        try:
+            ev = json.loads(raw)
+        except ValueError:
+            mlog.log.warning(json.dumps({"event": "event_invalid", "reason": "json"}))
+            return False
+        if not isinstance(ev, dict) or "event" not in ev:
+            return False                      # ping replies ({"status","seq_reply"}) and other non-events
+        if ev["event"] == "hello":
+            cid = (ev.get("data") or {}).get("connection_id")
+            resumed = bool(cid) and cid == self._resume_id
+            self.connection_id = cid
+            await asyncio.to_thread(self.state.set_meta, "ws_connection_id", cid or "")
+            if not resumed:
+                self.last_seq = ev.get("seq") if isinstance(ev.get("seq"), int) else 0
+            _log("ws_connected", connection_id=cid, resumed=resumed,
+                 server_version=(ev.get("data") or {}).get("server_version"))
+            if not resumed or self._catchup_pending:
+                await self._catch_up(client, "new_connection" if not resumed else "pending", prev_alive)
+            elif time.monotonic() - self._refreshed_at >= self.refresh_s:
+                await self._refresh_soft(client)
+            self.status = "ok"
+            return True
+        seq = ev.get("seq")
+        if self._seq_gap(ev):
+            await self._catch_up(client, "seq_gap", prev_alive)
+        if time.monotonic() - self._refreshed_at >= self.refresh_s:
+            await self._refresh_soft(client)
+        await self._membership_event(ev, client)
+        intent = decide(ev, self.bot_user_id)
+        if intent:
+            self._seen.setdefault(intent.channel_id, {"id": intent.channel_id, "type": intent.channel_type})
+            await self._enqueue(intent, client)
+        if isinstance(seq, int):
+            self.last_seq = seq           # only after the event is committed (a raise above replays it)
+        return False
+
+    async def _enqueue(self, intent: WakeIntent, client) -> bool:
+        payload = await self._payload(intent, client)
+        new = await asyncio.to_thread(self.state.enqueue_and_advance, intent.post_id, intent.channel_id,
+                                      payload, intent.create_at)
+        _log("wake_queued", post_id=intent.post_id, channel_id=intent.channel_id, new=new)
+        return new
+
+    def _seq_gap(self, ev: dict) -> bool:
+        """True on a seq gap (missed events). Does not advance last_seq (_frame does, after the commit)."""
         seq = ev.get("seq")
         if not isinstance(seq, int):
-            return
-        if ev["event"] != "hello" and self.last_seq is not None and seq != self.last_seq + 1:
+            return False
+        gap = self.last_seq is not None and seq != self.last_seq + 1
+        if gap:
             _log("ws_seq_gap", expected=self.last_seq + 1, got=seq)
-        self.last_seq = seq
+        return gap
+
+    async def _mark_alive(self) -> None:
+        """Persist the last-alive time of a fully handled frame (never mid catch-up: a restart then still
+        starts cursor-less channels at the catch-up's own start)."""
+        if self._alive_at is None or self._catchup_pending:
+            return
+        if time.monotonic() - self._alive_written >= ALIVE_EVERY_S:
+            self._alive_written = time.monotonic()
+            await asyncio.to_thread(self.state.set_meta, "last_event_at", str(self._alive_at))
 
     async def _ping(self, ws) -> None:
         for n in itertools.count(1):
             await asyncio.sleep(self.ping_s)
+            if not await asyncio.to_thread(self.state.claim_owner, self.clock(), LEASE_TTL_S, "listener_owner"):
+                _log("listener_lease_lost", instance=self.state.instance_id)
+                await ws.close()
+                return
             try:
                 await ws.send(json.dumps({"action": "ping", "seq": n}))
             except ConnectionClosed:
                 return
 
+    # --- membership + catch-up (architecture 'catch-up channel discovery') -------------------------------------
+    async def _paged(self, client, path: str) -> list:
+        out, ids = [], set()
+        for page in range(MAX_PAGES):
+            batch = await client.get(path, page=page, per_page=self.per_page)
+            new = [x for x in batch if isinstance(x, dict) and x.get("id") not in ids]
+            ids.update(x["id"] for x in new)
+            out += new
+            if len(batch) < self.per_page or not new:
+                break
+        return out
+
+    async def _refresh_members(self, client) -> None:
+        found = {}
+        for t in await self._paged(client, "/users/me/teams"):
+            for c in await self._paged(client, "/users/me/teams/%s/channels" % t["id"]):
+                if c.get("type") in ("O", "P", "D"):
+                    found[c["id"]] = c
+        for cid in await asyncio.to_thread(self.state.cursor_channels):
+            found.setdefault(cid, self.members.get(cid) or {"id": cid})
+        for cid, c in self._seen.items():
+            found.setdefault(cid, c)
+        self.members, self._refreshed_at = found, time.monotonic()
+
+    async def _refresh_soft(self, client) -> None:
+        """Periodic/event refresh: a Mattermost error keeps the old set (catch-up refreshes again)."""
+        try:
+            await self._refresh_members(client)
+        except MMError as e:
+            self._refreshed_at = time.monotonic()
+            _log("membership_refresh_failed", code=e.code)
+
+    async def _membership_event(self, ev: dict, client) -> None:
+        kind, data, bc = ev["event"], ev.get("data") or {}, ev.get("broadcast") or {}
+        if kind in ("user_added", "added_to_team") and data.get("user_id") == self.bot_user_id:
+            await self._refresh_soft(client)
+        elif kind == "user_removed" and self.bot_user_id in (data.get("user_id"), bc.get("user_id")):
+            cid = data.get("channel_id") or bc.get("channel_id")
+            if cid:
+                self.members.pop(cid, None)
+                self._seen.pop(cid, None)
+                await asyncio.to_thread(self.state.delete_cursor, cid)
+                _log("channel_removed", channel_id=cid)
+
+    async def _catch_up(self, client, reason: str, alive_at: int | None) -> None:
+        """REST catch-up of every member channel; raises (and stays pending, keeping its start) on MM errors."""
+        if not self._catchup_pending:
+            self._catchup_pending, self._catchup_from = True, alive_at
+        alive_at = self._catchup_from
+        await self._refresh_members(client)
+        floor = int(self.clock() * 1000) - self.window_ms
+        n_posts = n_skipped = 0
+        for cid, ch in list(self.members.items()):
+            cur = await asyncio.to_thread(self.state.get_cursor, cid)
+            if cur is None:
+                if alive_at is None:
+                    continue                  # first start ever: no backfill of history
+                cur = (alive_at, "")
+            try:                              # skipped posts are counted at most one window further back
+                posts = await self._since(client, cid, max(cur[0], floor - self.window_ms))
+            except MMError as e:
+                if e.code == "not_found" or e.status == 403:
+                    _log("channel_unavailable", channel_id=cid, code=e.code)
+                    self.members.pop(cid, None)
+                    continue
+                raise
+            ctype = ch.get("type") or (await self._get(client, self._channels, cid, "/channels/" + cid) or {}).get("type")
+            for p in sorted(posts, key=lambda p: (p.get("create_at", 0), p.get("id", ""))):
+                at = p.get("create_at")
+                if not isinstance(at, int) or at < cur[0] or p.get("delete_at"):
+                    continue                  # equal create_at is re-offered: the ledger dedupes (PR-3)
+                if at < floor:
+                    n_skipped += 1
+                    await asyncio.to_thread(self.state.set_cursor, cid, at, p["id"])
+                    continue
+                ev = {"event": "posted", "data": {"channel_type": ctype, "channel_name": ch.get("name"),
+                                                  "channel_display_name": ch.get("display_name"),
+                                                  "team_id": ch.get("team_id"), "post": p} }
+                intent = decide(ev, self.bot_user_id)
+                if intent:
+                    n_posts += await self._enqueue(intent, client)
+                else:
+                    await asyncio.to_thread(self.state.set_cursor, cid, at, p["id"])
+        self._catchup_pending = False
+        _log("catchup", reason=reason, channels=len(self.members), posts=n_posts, skipped=n_skipped)
+        if n_skipped:
+            _log("catchup_skipped", n=n_skipped, window_minutes=self.window_ms // 60_000)
+
+    async def _since(self, client, cid: str, since_ms: int) -> list:
+        """Every post with create_at >= since_ms. Mattermost ignores page/per_page when `since` is given (and caps
+        the result), so this pages by post id instead: the newest page, then `before=<oldest id seen>` until a
+        page reaches back past since_ms or runs out. MAX_PAGES (x per_page posts in one channel inside the
+        catch-up window) is the only bound; reaching it is logged (`catchup_truncated`)."""
+        posts: dict = {}
+        before = ""
+        for _ in range(MAX_PAGES):
+            q = {"page": 0, "per_page": self.per_page}
+            if before:
+                q["before"] = before
+            r = await client.get("/channels/%s/posts" % cid, **q)
+            batch = [r["posts"][i] for i in r.get("order", []) if i in r.get("posts", {})]
+            new = [p for p in batch if p["id"] not in posts]
+            posts.update((p["id"], p) for p in new)
+            if len(batch) < self.per_page or not new:
+                return list(posts.values())
+            oldest = batch[-1]                # Mattermost order is newest first
+            if oldest.get("create_at", 0) < since_ms:
+                return list(posts.values())
+            before = oldest["id"]
+        _log("catchup_truncated", channel_id=cid, pages=MAX_PAGES)
+        return list(posts.values())
+
     async def _get(self, client, cache: dict, key: str, path: str) -> dict | None:
         """Cached REST lookup; None (not cached) on Mattermost errors so the event hints are used instead."""
         if key not in cache:
diff --git a/app/live.py b/app/live.py
new file mode 100644
index 0000000..111fc41
--- /dev/null
+++ b/app/live.py
@@ -0,0 +1,176 @@
+"""Live-bots runtime started from the FastAPI lifespan (slice lb5, ADR-0007/0009; plan Phase 5).
+
+LiveRuntime.start(): LIVE_BOTS_ENABLED must be "true" (else health `disabled`), the store must decrypt
+(MMB_STORE_KEY; else `off`, log store_unreadable) and /data/state.db must be writable (else `off`, log
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
+        delay = min(max_s, base_s * 2 ** (attempt - 1))
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
+            return
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
+        self._tasks = [
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
diff --git a/app/main.py b/app/main.py
index 1615082..141dc09 100644
--- a/app/main.py
+++ b/app/main.py
@@ -1,6 +1,7 @@
 """mmbridge: MCP bridge between Grok Bots and self-hosted Mattermost.
 
-/health (public liveness) and /mcp (Bearer auth, MCP Streamable HTTP). Everything else 404.
+/health (public liveness + live-bots listener state, no ids) and /mcp (Bearer auth, MCP Streamable HTTP).
+Everything else 404. The lifespan also starts the live-bots runtime (app/live.py) when LIVE_BOTS_ENABLED=true.
 """
 import contextlib
 
@@ -9,26 +10,32 @@ from fastapi import FastAPI
 from app import logging as mlog
 from app import mcp as mcp_server
 from app.auth import BearerAuth
+from app.live import LiveRuntime
 from app.ratelimit import RateLimiter
 
 
-def create_app(mm_transport=None, limiter: RateLimiter | None = None) -> FastAPI:
+def create_app(mm_transport=None, limiter: RateLimiter | None = None, live: LiveRuntime | None = None) -> FastAPI:
     mlog.setup()
     limiter = limiter or RateLimiter()
+    live = live or LiveRuntime()
     server = mcp_server.build(limiter, mm_transport=mm_transport)
     mcp_app = server.streamable_http_app()
 
     @contextlib.asynccontextmanager
     async def lifespan(_):
         async with server.session_manager.run():
-            yield
+            await live.start()
+            try:
+                yield
+            finally:
+                await live.stop()
 
     app = FastAPI(title="mmbridge", version="0.2.0", lifespan=lifespan,
                   docs_url=None, redoc_url=None, openapi_url=None)
 
     @app.get("/health")
     async def health() -> dict:
-        return {"ok": True}
+        return {"ok": True, **await live.health()}
 
     app.router.routes.extend(mcp_app.routes)
     app.add_middleware(BearerAuth, limiter=limiter)
diff --git a/app/state.py b/app/state.py
index c164945..4040f3e 100644
--- a/app/state.py
+++ b/app/state.py
@@ -159,6 +159,14 @@ class State:
         with self._tx() as c:
             self._advance(c, channel_id, create_at, post_id)
 
+    def delete_cursor(self, channel_id: str) -> None:
+        with self._tx() as c:
+            c.execute("DELETE FROM cursors WHERE channel_id=?", (channel_id,))
+
+    def cursor_channels(self) -> list[str]:
+        with self._lock:
+            return [r[0] for r in self._conn.execute("SELECT channel_id FROM cursors ORDER BY channel_id")]
+
     # --- meta ------------------------------------------------------------------------------------------------
     def get_meta(self, key: str) -> str | None:
         with self._lock:
@@ -170,19 +178,26 @@ class State:
             c.execute("INSERT INTO meta (key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                       (key, value))
 
-    def claim_owner(self, now: int, ttl: int = OWNER_TTL_S) -> bool:
-        """Become (or stay, as heartbeat) the single dispatcher owner; refused while another owner is fresh."""
+    def claim_owner(self, now: int, ttl: int = OWNER_TTL_S, key: str = "dispatcher_owner") -> bool:
+        """Become (or stay, as heartbeat) the single owner of `key` (dispatcher_owner | listener_owner);
+        refused while another owner is fresh."""
         with self._tx() as c:
-            row = c.execute("SELECT value FROM meta WHERE key='dispatcher_owner'").fetchone()
+            row = c.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
             if row:
                 cur = json.loads(row[0])
                 if cur["id"] != self.instance_id and now - cur["ts"] < ttl:
                     return False
-            c.execute("INSERT INTO meta (key, value) VALUES ('dispatcher_owner', ?) "
-                      "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
-                      (json.dumps({"id": self.instance_id, "ts": now}),))
+            c.execute("INSERT INTO meta (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
+                      (key, json.dumps({"id": self.instance_id, "ts": now})))
             return True
 
+    def release_owner(self, key: str = "dispatcher_owner") -> None:
+        """Clean shutdown: drop our lease so a restarted process takes over at once."""
+        with self._tx() as c:
+            row = c.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
+            if row and json.loads(row[0])["id"] == self.instance_id:
+                c.execute("DELETE FROM meta WHERE key=?", (key,))
+
     # --- dispatcher queue ------------------------------------------------------------------------------------
     def claim_due(self, now: int, limit: int = 4) -> list[Wake]:
         """Atomically flip up to `limit` due queued/retry rows to in_flight for this instance (PR-1)."""
@@ -259,6 +274,12 @@ class State:
     def failed(self) -> list[Wake]:
         return self._select("WHERE status='failed'")
 
+    def failed_count(self, since: int) -> int:
+        """Failed wakes whose last update is at or after `since` (unix s): /health wake_failed_24h."""
+        with self._lock:
+            return self._conn.execute("SELECT COUNT(*) FROM wakes WHERE status='failed' AND updated_at >= ?",
+                                      (since,)).fetchone()[0]
+
     def stats(self) -> dict:
         """Counts per status and post->delivered latency (delivered_at - post_create_at, ms; PR-9)."""
         with self._lock:

exec
/bin/bash -lc "nl -ba app/listener.py | sed -n '230,330p'; cat app/mattermost.py | head -140; ls .claude/skills; git diff 3ed94b4 -- tests/acceptance/drivers/fake_mattermost.py; cat tests/unit/test_reconnect.py" in /mnt/d/rob/projects/mmbridge
 succeeded in 21ms:
   230	                if await self._frame(raw, client, prev_alive):
   231	                    reached = True
   232	            except BaseException:
   233	                self._alive_at = prev_alive   # not handled: a later catch-up must still start before this frame
   234	                raise
   235	            await self._mark_alive()
   236	
   237	    async def _frame(self, raw, client, prev_alive: int | None) -> bool:
   238	        """Handle one frame; True when it was a hello (connection established). Raises leave last_seq and
   239	        meta last_event_at untouched, so a reconnect resumes/catches up from before this frame."""
   240	        try:
   241	            ev = json.loads(raw)
   242	        except ValueError:
   243	            mlog.log.warning(json.dumps({"event": "event_invalid", "reason": "json"}))
   244	            return False
   245	        if not isinstance(ev, dict) or "event" not in ev:
   246	            return False                      # ping replies ({"status","seq_reply"}) and other non-events
   247	        if ev["event"] == "hello":
   248	            cid = (ev.get("data") or {}).get("connection_id")
   249	            resumed = bool(cid) and cid == self._resume_id
   250	            self.connection_id = cid
   251	            await asyncio.to_thread(self.state.set_meta, "ws_connection_id", cid or "")
   252	            if not resumed:
   253	                self.last_seq = ev.get("seq") if isinstance(ev.get("seq"), int) else 0
   254	            _log("ws_connected", connection_id=cid, resumed=resumed,
   255	                 server_version=(ev.get("data") or {}).get("server_version"))
   256	            if not resumed or self._catchup_pending:
   257	                await self._catch_up(client, "new_connection" if not resumed else "pending", prev_alive)
   258	            elif time.monotonic() - self._refreshed_at >= self.refresh_s:
   259	                await self._refresh_soft(client)
   260	            self.status = "ok"
   261	            return True
   262	        seq = ev.get("seq")
   263	        if self._seq_gap(ev):
   264	            await self._catch_up(client, "seq_gap", prev_alive)
   265	        if time.monotonic() - self._refreshed_at >= self.refresh_s:
   266	            await self._refresh_soft(client)
   267	        await self._membership_event(ev, client)
   268	        intent = decide(ev, self.bot_user_id)
   269	        if intent:
   270	            self._seen.setdefault(intent.channel_id, {"id": intent.channel_id, "type": intent.channel_type})
   271	            await self._enqueue(intent, client)
   272	        if isinstance(seq, int):
   273	            self.last_seq = seq           # only after the event is committed (a raise above replays it)
   274	        return False
   275	
   276	    async def _enqueue(self, intent: WakeIntent, client) -> bool:
   277	        payload = await self._payload(intent, client)
   278	        new = await asyncio.to_thread(self.state.enqueue_and_advance, intent.post_id, intent.channel_id,
   279	                                      payload, intent.create_at)
   280	        _log("wake_queued", post_id=intent.post_id, channel_id=intent.channel_id, new=new)
   281	        return new
   282	
   283	    def _seq_gap(self, ev: dict) -> bool:
   284	        """True on a seq gap (missed events). Does not advance last_seq (_frame does, after the commit)."""
   285	        seq = ev.get("seq")
   286	        if not isinstance(seq, int):
   287	            return False
   288	        gap = self.last_seq is not None and seq != self.last_seq + 1
   289	        if gap:
   290	            _log("ws_seq_gap", expected=self.last_seq + 1, got=seq)
   291	        return gap
   292	
   293	    async def _mark_alive(self) -> None:
   294	        """Persist the last-alive time of a fully handled frame (never mid catch-up: a restart then still
   295	        starts cursor-less channels at the catch-up's own start)."""
   296	        if self._alive_at is None or self._catchup_pending:
   297	            return
   298	        if time.monotonic() - self._alive_written >= ALIVE_EVERY_S:
   299	            self._alive_written = time.monotonic()
   300	            await asyncio.to_thread(self.state.set_meta, "last_event_at", str(self._alive_at))
   301	
   302	    async def _ping(self, ws) -> None:
   303	        for n in itertools.count(1):
   304	            await asyncio.sleep(self.ping_s)
   305	            if not await asyncio.to_thread(self.state.claim_owner, self.clock(), LEASE_TTL_S, "listener_owner"):
   306	                _log("listener_lease_lost", instance=self.state.instance_id)
   307	                await ws.close()
   308	                return
   309	            try:
   310	                await ws.send(json.dumps({"action": "ping", "seq": n}))
   311	            except ConnectionClosed:
   312	                return
   313	
   314	    # --- membership + catch-up (architecture 'catch-up channel discovery') -------------------------------------
   315	    async def _paged(self, client, path: str) -> list:
   316	        out, ids = [], set()
   317	        for page in range(MAX_PAGES):
   318	            batch = await client.get(path, page=page, per_page=self.per_page)
   319	            new = [x for x in batch if isinstance(x, dict) and x.get("id") not in ids]
   320	            ids.update(x["id"] for x in new)
   321	            out += new
   322	            if len(batch) < self.per_page or not new:
   323	                break
   324	        return out
   325	
   326	    async def _refresh_members(self, client) -> None:
   327	        found = {}
   328	        for t in await self._paged(client, "/users/me/teams"):
   329	            for c in await self._paged(client, "/users/me/teams/%s/channels" % t["id"]):
   330	                if c.get("type") in ("O", "P", "D"):
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
diff --git a/tests/acceptance/drivers/fake_mattermost.py b/tests/acceptance/drivers/fake_mattermost.py
index bf8b8cd..4cdb67c 100644
--- a/tests/acceptance/drivers/fake_mattermost.py
+++ b/tests/acceptance/drivers/fake_mattermost.py
@@ -8,12 +8,19 @@ Live bots lb3: GET channels/{id}, teams/{id}, users/{id}; websocket /api/v4/webs
 hello{connection_id}, per-connection seq, `posted` broadcast to channel members, ping action -> pong reply,
 drop/raw/seq-skip controls). `serve()` runs the app on a free localhost port for real HTTP/WS clients.
 Live bots lb4: `mm_ids=True` gives channels Mattermost-shaped 26-char ids (the bot store validates them).
+Live bots lb5: `clock` (seconds callable, e.g. time.time) stamps posts with real ms (catch-up windows); channel
+posts: `since` as Mattermost (paging ignored, capped at `since_cap`), else newest-first pages with `before`/`after`
+post-id anchors (fix cycle: catch-up pages by id); /users/me/teams and team channels page (`page`/`per_page`) and team channel lists include
+the user's D/G channels (as Mattermost does); `ws_refuse` (REST 503 + websocket handshake 503, an MM restart);
+resume: a dropped session stays resumable (`ws_drop(resumable=True)`), keeps receiving its events in a dead
+queue, and a reconnect with `?connection_id&sequence_number` gets hello (same id, no seq) + the missed events.
 """
 import asyncio
 import contextlib
 import hashlib
 import itertools
 import json
+from urllib.parse import parse_qs
 
 import httpx
 from starlette.applications import Starlette
@@ -24,8 +31,8 @@ from starlette.websockets import WebSocket
 
 
 class FakeMattermost:
-    def __init__(self, mm_ids=False):
-        self.mm_ids = mm_ids
+    def __init__(self, mm_ids=False, clock=None):
+        self.mm_ids, self.clock = mm_ids, clock
         self.users = {}      # id -> {"id","username","token"|None,"is_bot"}
         self.teams = {}      # id -> {"id","name","display_name"}
         self.channels = {}   # id -> {"id","team_id","name","display_name","type","members":set}
@@ -40,6 +47,11 @@ class FakeMattermost:
         self.ws_sessions = []     # open websocket sessions (_WsSession)
         self.ws_answer_pings = True
         self.ws_pings = 0
+        self.ws_refuse = False    # Mattermost unreachable: REST 503, websocket handshake 503
+        self.ws_dead = {}         # connection_id -> resumable dropped _WsSession (dead queue)
+        self.ws_resumes = 0
+        self.since_cap = 1000     # Mattermost caps `GET /channels/{id}/posts?since=` (and ignores paging there)
+        self.posts_queries = []   # (channel_id, query dict) of every channel posts call
         self._ws_ids = itertools.count(1)
         self.app = Starlette(routes=[
             Route("/api/v4/users/me", self._me),
@@ -97,22 +109,35 @@ class FakeMattermost:
     def direct_channels(self, user_a, user_b):
         return [c for c in self.channels.values() if c["type"] == "D" and c["members"] == {user_a, user_b}]
 
-    def add_post(self, channel_id, user_id, message, type="", root_id=""):
+    def _now_ms(self):
+        if self.clock is None:
+            return next(self._clock)
+        self._last_ms = max(int(self.clock() * 1000), getattr(self, "_last_ms", 0) + 1)
+        return self._last_ms
+
+    def add_post(self, channel_id, user_id, message, type="", root_id="", create_at=None):
         """Create a post and broadcast `posted` to the channel members' websocket sessions (as Mattermost does,
-        including the author's own sessions)."""
+        including the author's own sessions; dead resumable sessions queue it)."""
         pid = "p-%d" % next(self._ids)
         self.posts[pid] = p = {"id": pid, "channel_id": channel_id, "user_id": user_id, "message": message,
-                               "create_at": next(self._clock), "type": type, "root_id": root_id}
+                               "create_at": self._now_ms() if create_at is None else create_at, "type": type,
+                               "root_id": root_id}
         c = self.channels[channel_id]
         event = {"event": "posted", "broadcast": {"channel_id": channel_id, "team_id": "", "user_id": ""},
                  "data": {"channel_display_name": c["display_name"], "channel_name": c["name"],
                           "channel_type": c["type"], "sender_name": "@" + self.users[user_id]["username"],
                           "team_id": c["team_id"], "post": json.dumps(p)} }
-        for s in self.ws_sessions:
+        for s in self.ws_sessions + list(self.ws_dead.values()):
             if s.user_id in c["members"]:
                 s.push(event)
         return p
 
+    def ws_event(self, user_id, event, data, broadcast=None):
+        """Send a non-post event (user_added, added_to_team, user_removed, ...) to the user's sessions."""
+        for s in self.ws_sessions:
+            if s.user_id == user_id:
+                s.push({"event": event, "data": data, "broadcast": broadcast or {"user_id": user_id} })
+
     # --- websocket controls -------------------------------------------------------
     def ws_send_raw(self, event):
         """Send a raw frame (dict -> JSON with the session seq; str -> as is) to every open session."""
@@ -125,13 +150,17 @@ class FakeMattermost:
             s.push({k: v for k, v in s.last.items() if k != "seq"})
 
     def ws_skip_seq(self, n=1):
-        for s in self.ws_sessions:
+        for s in self.ws_sessions + list(self.ws_dead.values()):
             s.seq += n
 
-    def ws_drop(self):
-        """Close every open websocket session (connection drop)."""
+    def ws_drop(self, resumable=False):
+        """Close every open websocket session (connection drop). resumable: the server keeps each session's
+        dead queue so a reconnect with its connection_id resumes; otherwise reconnects get a new id."""
         for s in self.ws_sessions:
+            s.resumable = resumable
             s.q.put_nowait(None)
+        if not resumable:
+            self.ws_dead.clear()
 
     @contextlib.asynccontextmanager
     async def serve(self):
@@ -153,8 +182,9 @@ class FakeMattermost:
             await task
 
     def channel_posts(self, channel_id):
-        """Posts of a channel, oldest first."""
-        return sorted((p for p in self.posts.values() if p["channel_id"] == channel_id), key=lambda p: p["create_at"])
+        """Posts of a channel, oldest first (create_at, then creation order)."""
+        return sorted((p for p in self.posts.values() if p["channel_id"] == channel_id),
+                      key=lambda p: (p["create_at"], int(p["id"][2:])))
 
     def transport(self):
         fake = self
@@ -175,6 +205,8 @@ class FakeMattermost:
     def _auth(self, request: Request):
         tok = _tok(request.headers)
         self.calls.append((request.method, request.url.path, tok))
+        if self.ws_refuse:
+            return None, JSONResponse({"message": "unavailable"}, status_code=503)
         if self.fail_status:
             return None, JSONResponse({"message": "forced"}, status_code=self.fail_status)
         user = next((u for u in self.users.values() if tok and u["token"] == tok), None)
@@ -193,15 +225,16 @@ class FakeMattermost:
         if err:
             return err
         tids = {c["team_id"] for c in self.channels.values() if u["id"] in c["members"] and c["team_id"]}
-        return JSONResponse([self.teams[t] for t in sorted(tids)])
+        return JSONResponse(_page(request, [self.teams[t] for t in sorted(tids)]))
 
     async def _team_channels(self, request):
         u, err = self._auth(request)
         if err:
             return err
         tid = request.path_params["team_id"]
-        return JSONResponse([{k: v for k, v in c.items() if k != "members"}
-                             for c in self.channels.values() if c["team_id"] == tid and u["id"] in c["members"]])
+        return JSONResponse(_page(request, [{k: v for k, v in c.items() if k != "members"}
+                                            for c in self.channels.values()
+                                            if c["team_id"] in (tid, "") and u["id"] in c["members"]]))
 
     def _member_channel(self, u, cid):
         c = self.channels.get(cid)
@@ -238,8 +271,22 @@ class FakeMattermost:
         c, err = self._member_channel(u, request.path_params["channel_id"])
         if err:
             return err
-        page, per_page = int(request.query_params.get("page", 0)), int(request.query_params.get("per_page", 60))
-        newest = list(reversed(self.channel_posts(c["id"])))[page * per_page:(page + 1) * per_page]
+        q = request.query_params
+        self.posts_queries.append((c["id"], dict(q)))
+        page, per_page = int(q.get("page", 0)), int(q.get("per_page", 60))
+        newest = list(reversed(self.channel_posts(c["id"])))
+        if "since" in q:                      # as Mattermost: page/per_page ignored, result capped
+            since = int(q["since"])
+            newest = [p for p in newest if p["create_at"] > since][:self.since_cap]
+        else:
+            ids = [p["id"] for p in newest]
+            if q.get("before"):
+                newest = newest[ids.index(q["before"]) + 1:] if q["before"] in ids else []
+            elif q.get("after"):          # the per_page posts right after the anchor, still newest first
+                later = list(reversed(newest[:ids.index(q["after"])])) if q["after"] in ids else []
+                newest = list(reversed(later[page * per_page:(page + 1) * per_page]))
+            if not q.get("after"):
+                newest = newest[page * per_page:(page + 1) * per_page]
         return JSONResponse({"order": [p["id"] for p in newest], "posts": {p["id"]: p for p in newest} })
 
     async def _create_post(self, request):
@@ -299,13 +346,29 @@ class FakeMattermost:
         tok = _tok(ws.headers)
         self.calls.append(("WS", ws.url.path, tok))
         user = next((u for u in self.users.values() if tok and u["token"] == tok), None)
+        if self.ws_refuse:
+            await ws.send_denial_response(JSONResponse({"message": "unavailable"}, status_code=503))
+            return
         if not user or self.fail_status:
             await ws.close(code=1008)          # before accept: the handshake is refused (HTTP 403)
             return
         await ws.accept()
-        s = _WsSession(user["id"], "conn-%d" % next(self._ws_ids))
-        s.push({"event": "hello", "data": {"connection_id": s.connection_id, "server_version": self.server_version},
-                "broadcast": {"user_id": user["id"]} })
+        q = parse_qs(ws.url.query)
+        cid, seq = (q.get("connection_id") or [""])[0], (q.get("sequence_number") or [""])[0]
+        dead = self.ws_dead.pop(cid, None)
+        if dead is not None and dead.user_id == user["id"] and seq.isdigit():
+            s, self.ws_resumes = dead, self.ws_resumes + 1
+            s.q, s.resumable = asyncio.Queue(), False
+            s.q.put_nowait({"event": "hello", "data": {"connection_id": cid, "server_version": self.server_version},
+                            "broadcast": {"user_id": user["id"]} })
+            for ev in s.history:
+                if ev["seq"] >= int(seq):
+                    s.q.put_nowait(ev)
+        else:
+            s = _WsSession(user["id"], "conn-%d" % next(self._ws_ids))
+            s.push({"event": "hello", "data": {"connection_id": s.connection_id,
+                                               "server_version": self.server_version},
+                    "broadcast": {"user_id": user["id"]} })
         self.ws_sessions.append(s)
 
         async def writer():
@@ -328,6 +391,8 @@ class FakeMattermost:
                 t.cancel()
             await asyncio.gather(*tasks, return_exceptions=True)
             self.ws_sessions.remove(s)
+            if s.resumable:
+                self.ws_dead[s.connection_id] = s
             with contextlib.suppress(Exception):
                 await ws.close()
 
@@ -352,13 +417,24 @@ class _WsSession:
         self.user_id, self.connection_id = user_id, connection_id
         self.q = asyncio.Queue()
         self.seq, self.last = 0, None
+        self.history = []          # every event sent (replayed from sequence_number on resume)
+        self.resumable = False
 
     def push(self, event):
         self.last = {**event, "seq": self.seq}
         self.seq += 1
+        self.history.append(self.last)
         self.q.put_nowait(self.last)
 
 
+def _page(request, items):
+    q = request.query_params
+    if "per_page" not in q:
+        return items
+    page, per_page = int(q.get("page", 0)), int(q["per_page"])
+    return items[page * per_page:(page + 1) * per_page]
+
+
 def _tok(headers):
     a = headers.get("authorization", "")
     return a[7:] if a.startswith("Bearer ") else None
"""Listener reconnect, resume and REST catch-up (slice lb5, plan Phase 5 PR-3/PR-4; ADR-0007; architecture
'catch-up channel discovery'). Fake Mattermost on a free port with a real-time post clock."""
import asyncio
import logging
import time

import pytest

from app.listener import Listener
from app.mattermost import Client, MMError
from app.state import State
from app.store import BotConfig
from drivers.fake_mattermost import FakeMattermost

FAST = dict(backoff_s=0.05, max_backoff_s=0.2, ping_s=0.2, idle_s=2.0)


@pytest.fixture
def world():
    m = FakeMattermost(clock=time.time)
    bot = m.add_user("eddie", bot=True)
    rob = m.add_user("rob")
    town = m.add_channel("main", "town-square", ["eddie", "rob"])
    dm = m.direct_channel(bot["id"], rob["id"])["id"]
    return m, {"bot": bot, "rob": rob, "town": town, "dm": dm}


@pytest.fixture
async def served(world):
    m, w = world
    async with m.serve() as base:
        yield m, w, base


async def until(pred, timeout=5.0):
    for _ in range(int(timeout / 0.02)):
        if pred():
            return
        await asyncio.sleep(0.02)
    raise AssertionError("condition not met in %.1fs" % timeout)


class Run:
    """A Listener.run() task on its own state.db, cancelled at teardown."""

    def __init__(self, served, path, client_cls=Client, **kw):
        self.m, self.w, base = served
        cfg = BotConfig(token=self.w["bot"]["token"], wake_url="https://wake.example/hook", wake_secret="s" * 40)
        self.state = State(str(path))
        self.lis = Listener(cfg, self.state, lambda tok: client_cls(tok, base_url=base), base_url=base,
                            **{**FAST, **kw})
        self.task = None

    async def start(self):
        self.task = asyncio.create_task(self.lis.run())
        await until(lambda: self.lis.status == "ok")
        return self

    async def stop(self):
        self.task.cancel()
        await asyncio.gather(self.task, return_exceptions=True)

    def posts_calls(self, cid):
        return [c for c in self.m.calls if c[1] == "/api/v4/channels/%s/posts" % cid]

    def post(self, cid, msg, user="rob", **kw):
        return self.m.add_post(cid, self.m.user_by_name(user)["id"], msg, **kw)

    async def outage(self, during, resumable=False):
        """Drop the socket, refuse reconnects while `during()` runs, then let the listener back in."""
        cid = self.lis.connection_id
        self.m.ws_refuse = True
        self.m.ws_drop(resumable=resumable)
        await until(lambda: self.lis.status != "ok")
        out = during()
        self.m.ws_refuse = False
        await until(lambda: self.lis.status == "ok" and (resumable or self.lis.connection_id != cid))
        return out


@pytest.fixture
async def run(served, tmp_path):
    r = await Run(served, tmp_path / "state.db").start()
    yield r
    await r.stop()


def ids(state):
    return [w.post_id for w in state.wakes()]


async def test_same_connection_id_resumes_without_catchup(run):
    m, w = run.m, run.w
    a = run.post(w["town"], "live one")
    await until(lambda: run.state.wake(a["id"]))
    cid = run.lis.connection_id
    b = await run.outage(lambda: run.post(w["town"], "while dropped"), resumable=True)
    await until(lambda: run.state.wake(b["id"]))
    assert m.ws_resumes == 1 and run.lis.connection_id == cid
    assert ("WS", "/api/v4/websocket", w["bot"]["token"]) in m.calls
    assert run.posts_calls(w["town"]) == []              # resumed: no REST catch-up
    assert ids(run.state) == [a["id"], b["id"]]


async def test_new_connection_id_runs_catchup_and_resets_seq(run, caplog):
    w = run.w
    a = run.post(w["town"], "live one")
    await until(lambda: run.state.wake(a["id"]))
    assert run.lis.last_seq == 1
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        b, c = await run.outage(lambda: (run.post(w["town"], "missed in town"), run.post(w["dm"], "missed dm")))
        await until(lambda: run.state.wake(b["id"]) and run.state.wake(c["id"]))
        assert run.lis.last_seq == 0                         # new connection: expected seq reset (hello is 0)
        d = run.post(w["town"], "live again")
        await until(lambda: run.state.wake(d["id"]))
    assert run.lis.last_seq == 1 and "ws_seq_gap" not in caplog.text
    assert '"event": "ws_reconnect"' in caplog.text and '"event": "catchup"' in caplog.text
    assert ids(run.state) == [a["id"], b["id"], c["id"], d["id"]]
    assert run.state.get_cursor(w["town"]) == (d["create_at"], d["id"])


async def test_seq_gap_on_resume_triggers_catchup(run, caplog):
    m, w = run.m, run.w
    a = run.post(w["town"], "live one")
    await until(lambda: run.state.wake(a["id"]))

    def lose_one():
        lost = run.post(w["town"], "lost by the server")
        dead = next(iter(m.ws_dead.values()))
        dead.history = [e for e in dead.history if lost["id"] not in str(e)]   # never replayed: a seq gap
        return lost, run.post(w["town"], "replayed")
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        lost, replayed = await run.outage(lose_one, resumable=True)
        await until(lambda: run.state.wake(lost["id"]) and run.state.wake(replayed["id"]))
    assert m.ws_resumes == 1 and "ws_seq_gap" in caplog.text and run.posts_calls(w["town"])
    assert ids(run.state) == [a["id"], lost["id"], replayed["id"]]


async def test_outage_longer_than_window_skips_old_posts(served, tmp_path, caplog):
    now = [time.time()]
    r = await Run(served, tmp_path / "state.db", clock=lambda: now[0], catchup_minutes=15).start()
    w = r.w
    t0 = int(now[0] * 1000)

    def during():
        old = r.post(w["town"], "too old", create_at=t0 + 1000)
        now[0] += 20 * 60
        return old, r.post(w["town"], "recent", create_at=int(now[0] * 1000) - 1000)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        old, recent = await r.outage(during)
        await until(lambda: r.state.wake(recent["id"]))
    await r.stop()
    assert r.state.wake(old["id"]) is None
    assert '"event": "catchup_skipped"' in caplog.text and '"n": 1' in caplog.text


async def test_catchup_paginates_450_posts_each_enqueued_once(run):
    w = run.w
    posts = await run.outage(lambda: [run.post(w["town"], "bulk %d" % i) for i in range(450)])
    await until(lambda: len(run.state.wakes()) == 450)
    assert len(run.posts_calls(w["town"])) == 3                      # 200 + 200 + 50
    assert ids(run.state) == [p["id"] for p in posts]               # ascending (create_at, post_id)


async def test_catchup_pages_by_post_id_past_the_since_cap(run):
    """Mattermost ignores page/per_page with `since` and caps it (fake: since_cap): catch-up must page by id."""
    w = run.w
    run.m.since_cap = 300
    posts = await run.outage(lambda: [run.post(w["town"], "bulk %d" % i) for i in range(700)])
    await until(lambda: len(run.state.wakes()) == 700)
    assert ids(run.state) == [p["id"] for p in posts]
    assert run.state.get_cursor(w["town"]) == (posts[-1]["create_at"], posts[-1]["id"])
    assert not any("since" in q for _, q in run.m.posts_queries)


async def test_catchup_with_old_cursor_fetches_only_back_to_it(run):
    w = run.w
    a = run.post(w["town"], "live one")
    await until(lambda: run.state.wake(a["id"]))
    n0 = len(run.posts_calls(w["town"]))
    posts = await run.outage(lambda: [run.post(w["town"], "bulk %d" % i) for i in range(30)])
    await until(lambda: len(run.state.wakes()) == 31)
    assert len(run.posts_calls(w["town"])) - n0 == 1                 # 30 newer posts: one page reaches the cursor
    assert ids(run.state) == [a["id"]] + [p["id"] for p in posts]


async def test_failed_enqueue_does_not_advance_seq(run, monkeypatch):
    """last_seq moves only after enqueue_and_advance commits: a reconnect then asks to replay the event."""
    w = run.w
    a = run.post(w["town"], "live one")
    await until(lambda: run.state.wake(a["id"]))
    real, seen = run.state.enqueue_and_advance, []

    def flaky(*args):
        if not seen:
            seen.append(run.lis.last_seq)
            raise RuntimeError("disk hiccup")
        return real(*args)
    monkeypatch.setattr(run.state, "enqueue_and_advance", flaky)
    before, alive = run.lis.last_seq, run.lis._alive_at
    run.post(w["town"], "fails once")
    await until(lambda: seen and run.task.done())
    assert seen == [before] and run.lis.last_seq == before
    assert run.lis._alive_at == alive                 # nor the in-memory catch-up start (review-3)


async def test_alive_not_persisted_until_catchup_completes(served, tmp_path, monkeypatch):
    """A restart mid catch-up must still start cursor-less channels at the catch-up's own start."""
    import app.listener as listener_mod
    monkeypatch.setattr(listener_mod, "ALIVE_EVERY_S", 0)
    r = await Run(served, tmp_path / "state.db").start()
    w = r.w
    a = r.post(w["town"], "live one")
    await until(lambda: r.state.wake(a["id"]))
    await asyncio.sleep(0.05)
    alive0 = r.state.get_meta("last_event_at")
    assert alive0 and r.state.get_cursor(w["dm"]) is None
    real, at_fail = r.lis._since, []

    async def flaky(client, cid, since_ms):
        if cid == w["dm"] and not at_fail:
            at_fail.append(r.state.get_meta("last_event_at"))
            raise MMError("mattermost_unavailable", 503)
        return await real(client, cid, since_ms)
    monkeypatch.setattr(r.lis, "_since", flaky)
    p = await r.outage(lambda: r.post(w["dm"], "dm while down"))
    await until(lambda: r.state.wake(p["id"]))
    await r.stop()
    assert at_fail == [alive0]                                      # hello did not overwrite it mid catch-up
    assert int(r.state.get_meta("last_event_at")) > int(alive0)     # written once catch-up completed


async def test_equal_create_at_straddling_a_page_boundary_both_enqueued_once(served, tmp_path):
    r = await Run(served, tmp_path / "state.db", per_page=2).start()
    w = r.w
    ts = int(time.time() * 1000) + 5000

    def during():
        return [r.post(w["town"], "same ts %d" % i, create_at=ts) for i in range(3)] + \
            [r.post(w["town"], "later", create_at=ts + 1)]
    posts = await r.outage(during)
    await until(lambda: len(r.state.wakes()) == 4)
    await asyncio.sleep(0.2)
    await r.stop()
    assert sorted(ids(r.state)) == sorted(p["id"] for p in posts)
    assert len(r.posts_calls(w["town"])) >= 2


async def test_dm_created_during_outage_is_discovered_and_caught_up(run):
    m, w = run.m, run.w
    ann = m.add_user("ann")

    def during():
        c = m.direct_channel(w["bot"]["id"], ann["id"])
        return run.post(c["id"], "first dm from ann", user="ann")
    p = await run.outage(during)
    await until(lambda: run.state.wake(p["id"]))
    assert run.state.wake(p["id"]).payload["channel"]["type"] == "D"


async def test_two_teams_and_channel_joined_during_outage_are_caught_up(served, tmp_path):
    m, w, _ = served
    ops = m.add_channel("lab2", "ops", ["eddie", "rob"])
    r = await Run(served, tmp_path / "state.db").start()

    def during():
        new = m.add_channel("lab3", "fresh", ["eddie", "rob"])     # bot added on a third team meanwhile
        return r.post(ops, "disk at 90%"), r.post(new, "welcome eddie")
    a, b = await r.outage(during)
    await until(lambda: r.state.wake(a["id"]) and r.state.wake(b["id"]))
    await r.stop()
    assert [x.payload["channel"]["team"] for x in r.state.wakes()] == ["lab2", "lab3"]


async def test_membership_events_refresh_and_user_removed_drops_cursor(run):
    m, w = run.m, run.w
    p = run.post(w["town"], "set a cursor")
    await until(lambda: run.state.wake(p["id"]))
    before = sum(c[1] == "/api/v4/users/me/teams" for c in m.calls)
    m.ws_event(w["bot"]["id"], "added_to_team", {"team_id": "t-lab2", "user_id": w["bot"]["id"]})
    await until(lambda: sum(c[1] == "/api/v4/users/me/teams" for c in m.calls) > before)
    m.channels[w["town"]]["members"].discard(w["bot"]["id"])
    m.ws_event(w["bot"]["id"], "user_removed", {"channel_id": w["town"], "remover_id": w["rob"]["id"]})
    await until(lambda: run.state.get_cursor(w["town"]) is None)
    assert w["town"] not in run.lis.members


class _FlakyClient(Client):
    """Fails the first catch-up GET of the second page (`before=`; crash between pages)."""
    failed = False

    async def get(self, path, **params):
        if path.endswith("/posts") and params.get("before") and not _FlakyClient.failed:
            _FlakyClient.failed = True
            raise MMError("mattermost_unavailable", 503)
        return await super().get(path, **params)


async def test_crash_between_pages_recovers_with_no_loss_or_duplicate(served, tmp_path):
    _FlakyClient.failed = False
    r = await Run(served, tmp_path / "state.db", client_cls=_FlakyClient).start()
    posts = await r.outage(lambda: [r.post(r.w["town"], "bulk %d" % i) for i in range(250)])
    await until(lambda: len(r.state.wakes()) == 250)
    await asyncio.sleep(0.2)
    await r.stop()
    assert _FlakyClient.failed and ids(r.state) == [p["id"] for p in posts]


async def test_crash_mid_enqueue_resumes_from_last_committed_cursor(run, monkeypatch):
    w = run.w
    real, n, cursor_at_crash = run.state.enqueue_and_advance, [0], []

    def flaky(*a):
        n[0] += 1
        if n[0] == 101:
            cursor_at_crash.append(run.state.get_cursor(w["town"]))
            raise RuntimeError("disk hiccup")
        return real(*a)
    monkeypatch.setattr(run.state, "enqueue_and_advance", flaky)

    async def supervised():                  # stands in for app.live.supervise: restart the crashed task
        while True:
            try:
                await run.lis.run()
            except RuntimeError:
                await asyncio.sleep(0.05)
    await run.stop()
    run.task = asyncio.create_task(supervised())
    await until(lambda: run.lis.status == "ok")
    posts = await run.outage(lambda: [run.post(w["town"], "bulk %d" % i) for i in range(150)])
    await until(lambda: len(run.state.wakes()) == 150)
    assert cursor_at_crash == [(posts[99]["create_at"], posts[99]["id"])]   # 100 committed before the crash
    assert n[0] > 150 and ids(run.state) == [p["id"] for p in posts]


async def test_unauthorized_token_degrades_then_retries(served, tmp_path, caplog):
    m, w, _ = served
    good = w["bot"]["token"]
    w["bot"]["token"] = "revoked-token-value"
    r = Run(served, tmp_path / "state.db", auth_retry_s=0.3)
    r.lis._cfg = lambda: BotConfig(token=good, wake_url="https://wake.example/hook", wake_secret="s" * 40)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        r.task = asyncio.create_task(r.lis.run())
        await until(lambda: r.lis.status == "degraded")
        w["bot"]["token"] = good                         # token fixed in Mattermost: next retry succeeds
        await until(lambda: r.lis.status == "ok")
    await r.stop()
    assert "mm_unauthorized" in caplog.text and good not in caplog.text


async def test_second_listener_cannot_take_the_lease(served, tmp_path, caplog):
    m = served[0]
    a = await Run(served, tmp_path / "state.db").start()
    b = Run(served, tmp_path / "state.db", lease_retry_s=0.1)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        b.task = asyncio.create_task(b.lis.run())
        await until(lambda: "listener_lease_held" in caplog.text)
    assert b.lis.status == "off"
    assert sum(c[0] == "WS" for c in m.calls) == 1
    await b.stop()
    await a.stop()


def test_reconnect_backoff_doubles_with_jitter_and_caps(tmp_path):
    lis = Listener(BotConfig("t" * 26, "https://x.example/h", "s" * 40), State(str(tmp_path / "s.db")),
                   lambda t: None, rand=lambda: 1.0)
    assert [lis._backoff(n) for n in range(1, 9)] == [1, 2, 4, 8, 16, 32, 60, 60]
    lis.rand = lambda: 0.0
    assert lis._backoff(3) == 2.0                       # jitter: between half and full delay

exec
/bin/bash -lc "git diff 3ed94b4 -- tests/acceptance/drivers/live.py tests/acceptance/drivers/wake_receiver.py; cat .claude/skills/eng-verify/SKILL.md | head -70; nl -ba app/listener.py | sed -n '360,435p'; ls .venv/bin/python*" in /mnt/d/rob/projects/mmbridge
 succeeded in 36ms:
diff --git a/tests/acceptance/drivers/live.py b/tests/acceptance/drivers/live.py
index fad2654..1dc4627 100644
--- a/tests/acceptance/drivers/live.py
+++ b/tests/acceptance/drivers/live.py
@@ -1,13 +1,21 @@
 """Live-bots protocol driver (layer 3, ADR-0010). Drivers are not locked; edit freely.
 
-lb4: in-process mode. A background event loop runs the fake Mattermost (REST + websocket, served on a free
-localhost port, MM-shaped channel ids), the real Listener and Dispatcher, and an HMAC-verifying wake receiver
-(drivers/wake_receiver.py, reached through an in-process httpx transport at https://receiver.test/wake).
-The bot is configured with the real admin CLI (`app.admin.main`, as `python -m app.admin` would run it) on a
-temp /data with a fresh MMB_STORE_KEY; the printed wake secret is handed to the receiver. Backoff is scaled
-by WAKE_BACKOFF_SCALE so retry specs run in seconds.
-lb4b: no channel list in set-bot; the fake only sends `posted` to channel members, so membership is the filter.
-lb5 adds container mode (real image) and drop/restore connection.
+A background event loop serves the fake Mattermost (REST + websocket, MM-shaped channel ids, real-time post
+clock) and the HMAC-verifying wake receiver (drivers/wake_receiver.py) on free 127.0.0.1 ports. The bot is set up
+with the real admin CLI (token on stdin, wake URL); the printed wake secret is handed to the receiver.
+Backoff is scaled by WAKE_BACKOFF_SCALE so retry specs run in seconds; LIVE_ALLOW_HTTP_WAKE=true lets the wake
+URL be the plain-HTTP local receiver (tests only).
+
+SUT mode (env LIVE_MODE):
+- `container` (default, lb5, ADR-0010 layer 4): the real image (env LIVE_IMAGE, default mmbridge:lb5; build it
+  first with `docker build -t mmbridge:lb5 .`) on `--network host` with a fresh named volume at /data, a fresh
+  MMB_STORE_KEY and LIVE_BOTS_ENABLED=true. `python -m app.admin set-bot` runs in a one-off container on the same
+  volume before the server starts (as an operator would before enabling the flag); `admin failed` runs through
+  `docker exec`; `/health` tells when the listener is connected; `docker logs` is the log capture for the token
+  scan.
+- `inprocess` (lb4): app.admin.main and app.live.LiveRuntime in this process; logs captured from the loggers.
+drop_connection: the fake closes the websocket (no resume: a new connection id) and refuses REST + websocket
+until restore_connection, so posts made meanwhile are reachable only by the listener's REST catch-up.
 """
 import asyncio
 import hashlib
@@ -19,6 +27,8 @@ import os
 import re
 import secrets
 import shutil
+import socket
+import subprocess
 import tempfile
 import threading
 import time
@@ -26,20 +36,18 @@ import time
 import httpx
 from cryptography.fernet import Fernet
 
-from app import admin, store
+from app import admin
 from app import logging as mlog
-from app.listener import Listener
-from app.mattermost import Client
-from app.state import State
-from app.wake import Dispatcher
+from app.live import LiveRuntime
 from drivers.fake_mattermost import FakeMattermost
 from drivers.wake_receiver import WakeReceiver
 
-WAKE_URL = "https://receiver.test/wake"
 TEAM = "rmlab"
 WAKE_WITHIN_S = 10.0       # design metric: wake within 10 s
 SETTLE_S = 0.3
+START_S = 30.0             # container start + listener connect
 MARKER_USER = "zz-marker"
+LOGGERS = ("mmbridge", "mmbridge.ws", "httpx", "websockets")
 
 
 class _Capture(logging.Handler):
@@ -52,29 +60,131 @@ class _Capture(logging.Handler):
         self.lines.append(self.format(record))
 
 
+def _free_port() -> int:
+    with socket.socket() as s:
+        s.bind(("127.0.0.1", 0))
+        return s.getsockname()[1]
+
+
+class _InProcess:
+    """app.admin.main + app.live.LiveRuntime on the driver's event loop."""
+
+    def __init__(self, drv, env):
+        self.drv, self.env, self.runtime = drv, env, None
+        self._saved = {k: os.environ.get(k) for k in env}
+        os.environ.update(env)
+        self._log = _Capture()
+        for name in LOGGERS:
+            logging.getLogger(name).addHandler(self._log)
+
+    def admin(self, argv, stdin=""):
+        out = io.StringIO()
+        rc = admin.main(list(argv), stdin=io.StringIO(stdin), stdout=out, transport=self.drv.mm.transport())
+        return rc, out.getvalue()
+
+    def start(self):
+        self.runtime = LiveRuntime(env=dict(os.environ), base_url=self.drv.base, poll_s=0.05)
+        self.drv._run(self.runtime.start())
+
+    def listener(self):
+        return self.runtime.listener_status() if self.runtime else "off"
+
+    def logs(self):
+        return "\n".join(self._log.lines)
+
+    def close(self):
+        try:
+            if self.runtime:
+                self.drv._run(self.runtime.stop())
+        finally:
+            for name in LOGGERS:
+                logging.getLogger(name).removeHandler(self._log)
+            for k, v in self._saved.items():
+                os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
+
+
+class _Container:
+    """The real image (ADR-0010): one-off admin containers + the server container on a fresh /data volume."""
+
+    def __init__(self, drv, env):
+        self.drv, self.env = drv, env
+        self.image = os.environ.get("LIVE_IMAGE", "mmbridge:lb5")
+        self.name = "mmb-live-" + secrets.token_hex(4)
+        self.volume = self.name + "-data"
+        self.port = _free_port()
+        self.started = False
+        if self._docker("image", "inspect", self.image).returncode != 0:
+            raise AssertionError("image %s not found: run `docker build -t %s .` first" % (self.image, self.image))
+        self._docker("volume", "create", self.volume, check=True)
+
+    def _docker(self, *args, stdin="", check=False, timeout=60):
+        r = subprocess.run(["docker", *args], input=stdin, capture_output=True, text=True, timeout=timeout)
+        if check and r.returncode != 0:
+            raise AssertionError("docker %s failed: %s" % (args[0], r.stderr.strip()))
+        return r
+
+    def _env_args(self):
+        return [a for k, v in self.env.items() for a in ("-e", "%s=%s" % (k, v))]
+
+    def admin(self, argv, stdin=""):
+        if self.started:
+            r = self._docker("exec", "-i", self.name, "python", "-m", "app.admin", *argv, stdin=stdin)
+        else:
+            r = self._docker("run", "--rm", "-i", "--network", "host", "-v", self.volume + ":/data",
+                             *self._env_args(), self.image, "python", "-m", "app.admin", *argv, stdin=stdin)
+        return r.returncode, r.stdout + r.stderr
+
+    def start(self):
+        # Same image and entrypoint as production; only the port differs (host network: avoid clashes on 8080).
+        self._docker("run", "-d", "--name", self.name, "--network", "host", "-v", self.volume + ":/data",
+                     *self._env_args(), "-e", "LIVE_BOTS_ENABLED=true", self.image,
+                     "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(self.port), "--proxy-headers",
+                     check=True)
+        self.started = True
+
+    def listener(self):
+        try:
+            return httpx.get("http://127.0.0.1:%d/health" % self.port, timeout=2).json()["listener"]
+        except (httpx.HTTPError, ValueError, KeyError):
+            return "starting"
+
+    def logs(self):
+        if not self.started:
+            return ""
+        r = self._docker("logs", self.name)
+        return r.stdout + r.stderr
+
+    def close(self):
+        if self.started:
+            if os.environ.get("LIVE_SHOW_LOGS"):
+                print(self.logs())
+            self._docker("rm", "-f", self.name)
+        self._docker("volume", "rm", "-f", self.volume)
+
+
 class LiveDriver:
     def __init__(self):
-        self._tmp = tempfile.mkdtemp(prefix="mmb-live-")
-        env = {"MMB_DATA_DIR": self._tmp, "MMB_STORE_KEY": Fernet.generate_key().decode(),
-               "WAKE_BACKOFF_SCALE": "0.05", "WAKE_MAX_ATTEMPTS": "5"}
-        self._env_saved = {k: os.environ.get(k) for k in env}
-        os.environ.update(env)
-        self.mm = FakeMattermost(mm_ids=True)
+        self.mm = FakeMattermost(mm_ids=True, clock=time.time)
         self.rx = WakeReceiver()
         self.outputs = []              # admin CLI stdout
         self.posts = {}                # message -> post id (latest)
         self.teams = {}                # channel name -> team (given_channel)
         self._last_post = None
-        self._tasks = []
-        self.state = None
-        self._log = _Capture()
-        for name in ("mmbridge", "mmbridge.ws", "httpx", "websockets"):
-            logging.getLogger(name).addHandler(self._log)
         self._loop = asyncio.new_event_loop()
         self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
         self._thread.start()
-        self._serving = self.mm.serve()
-        self.base = self._run(self._serving.__aenter__())
+        self._serving = [self.mm.serve(), self.rx.serve()]
+        self.base, self.wake_url = (self._run(cm.__aenter__()) for cm in self._serving)
+        env = {"MMB_STORE_KEY": Fernet.generate_key().decode(), "MATTERMOST_URL": self.base,
+               "WAKE_BACKOFF_SCALE": "0.05", "WAKE_MAX_ATTEMPTS": "5", "LIVE_ALLOW_HTTP_WAKE": "true"}
+        mode = os.environ.get("LIVE_MODE", "container")
+        assert mode in ("container", "inprocess"), "LIVE_MODE must be container or inprocess"
+        self._tmp = None
+        if mode == "inprocess":
+            self._tmp = tempfile.mkdtemp(prefix="mmb-live-")
+            self.sut = _InProcess(self, {**env, "MMB_DATA_DIR": self._tmp, "LIVE_BOTS_ENABLED": "true"})
+        else:
+            self.sut = _Container(self, env)
 
     def _run(self, coro, timeout=20):
         return asyncio.run_coroutine_threadsafe(coro, self._loop).result(timeout)
@@ -101,34 +211,18 @@ class LiveDriver:
         return self.mm.channel_by_name(channel, self.teams.get(channel, TEAM))
 
     def _admin(self, *argv, stdin=""):
-        out = io.StringIO()
-        rc = admin.main(list(argv), stdin=io.StringIO(stdin), stdout=out, transport=self.mm.transport())
-        self.outputs.append(out.getvalue())
-        return rc, out.getvalue()
+        rc, out = self.sut.admin(argv, stdin)
+        self.outputs.append(out)
+        return rc, out
 
     def given_live_bot(self, name):
         u = self._user(name)
         u["is_bot"], u["token"] = True, "tok-%s-%s" % (name, secrets.token_hex(12))
-        rc, out = self._admin("set-bot", "--token-stdin", "--wake-url", WAKE_URL, stdin=u["token"] + "\n")
+        rc, out = self._admin("set-bot", "--token-stdin", "--wake-url", self.wake_url, stdin=u["token"] + "\n")
         assert rc == 0, "admin set-bot failed: %s" % out.strip()
         self.rx.secret = re.search(r"wake secret \(shown once[^)]*\): (\S+)", out).group(1)
-        cfg = store.load(store.path_from_env(), os.environ["MMB_STORE_KEY"])
-        self._run(self._start(cfg))
-
-    async def _start(self, cfg):
-        self.state = State(os.path.join(self._tmp, "state.db"))
-        self.listener = Listener(cfg, self.state, lambda tok: Client(tok, base_url=self.base), base_url=self.base)
-        self.http = httpx.AsyncClient(transport=self.rx.transport())
-        path, key = store.path_from_env(), os.environ["MMB_STORE_KEY"]
-        self.dispatcher = Dispatcher(self.state, lambda: store.load(path, key), self.http, poll_s=0.05)
-        self._tasks = [asyncio.create_task(self.listener.run()), asyncio.create_task(self.dispatcher.run())]
-        for _ in range(500):
-            if self.listener.status == "ok":
-                return
-            if self._tasks[0].done():
-                self._tasks[0].result()
-            await asyncio.sleep(0.01)
-        raise AssertionError("listener did not connect")
+        self.sut.start()
+        self._wait(lambda: self.sut.listener() == "ok", START_S, "listener ok in /health")
 
     def given_wake_target_down(self):
         self.rx.down = True
@@ -153,13 +247,10 @@ class LiveDriver:
                            "post": {"id": "forged-1", "message": "do something bad"} }).encode()
         ts = int(time.time())
         forged_sig = "v1=" + hmac.new(b"not-the-secret", b"%d." % ts + body, hashlib.sha256).hexdigest()
-
-        async def go():
-            r = await self.http.post(WAKE_URL, content=body, headers={
-                "Content-Type": "application/json", "X-MMB-Delivery": "forged-1", "X-MMB-Timestamp": str(ts),
-                "X-MMB-Signature": forged_sig})
-            return {"status": r.status_code, "delivery": "forged-1"}
-        return self._run(go())
+        r = httpx.post(self.wake_url, content=body, timeout=5, headers={
+            "Content-Type": "application/json", "X-MMB-Delivery": "forged-1", "X-MMB-Timestamp": str(ts),
+            "X-MMB-Signature": forged_sig})
+        return {"status": r.status_code, "delivery": "forged-1"}
 
     # --- checks ---------------------------------------------------------------------------------------------
     def _wait(self, pred, timeout, what):
@@ -231,41 +322,43 @@ class LiveDriver:
 
     def assert_failed_wake_visible(self, message):
         pid = self.posts[message] if message is not None else self._last_post
-        self._wait(lambda: (w := self.state.wake(pid)) is not None and w.status == "failed", 20, "failed wake")
-        rc, out = self._admin("failed")
-        assert rc == 0 and pid in out, "admin failed does not list %s: %s" % (pid, out)
+        seen = {}
+
+        def listed():
+            seen["rc"], seen["out"] = self._admin("failed")
+            return seen["rc"] == 0 and pid in seen["out"]
+        self._wait(listed, 20, "admin failed to list %s (last output: %r)" % (pid, seen.get("out")))
 
     def assert_no_token_anywhere(self, bot):
         tok = self._user(bot)["token"]
-        assert tok not in "\n".join(self._log.lines), "token in logs"
+        logs = self.sut.logs()
+        assert '"event": "wake_queued"' in logs, "log capture is empty or not the bridge's logs"
+        assert tok not in logs, "token in logs"
         assert tok not in "\n".join(self.outputs), "token in admin output"
         for r in self.rx.requests:
             assert tok not in r["body"].decode() and tok not in json.dumps(r["headers"]), "token in a wake"
 
     def drop_connection(self, seconds):
-        raise NotImplementedError("live driver: drop_connection is built in lb5 (reconnect)")
+        # `seconds` is simulated: reconnects stay refused until restore_connection (no real wait).
+        def drop():
+            self.mm.ws_refuse = True
+            self.mm.ws_drop(resumable=False)
+        self._call(drop)
+        self._wait(lambda: self.sut.listener() not in ("ok", "starting"), 5, "listener to notice the drop")
 
     def restore_connection(self):
-        raise NotImplementedError("live driver: restore_connection is built in lb5 (reconnect)")
+        self._call(setattr, self.mm, "ws_refuse", False)
 
     def close(self):
-        async def stop():
-            for t in self._tasks:
-                t.cancel()
-            await asyncio.gather(*self._tasks, return_exceptions=True)
-            if self._tasks:
-                await self.http.aclose()
-            await self._serving.__aexit__(None, None, None)
         try:
-            self._run(stop())
+            self.sut.close()
         finally:
-            self._loop.call_soon_threadsafe(self._loop.stop)
-            self._thread.join(5)
-            self._loop.close()
-            if self.state:
-                self.state.close()
-            for name in ("mmbridge", "mmbridge.ws", "httpx", "websockets"):
-                logging.getLogger(name).removeHandler(self._log)
-            for k, v in self._env_saved.items():
-                os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
-            shutil.rmtree(self._tmp, ignore_errors=True)
+            try:
+                for cm in reversed(self._serving):
+                    self._run(cm.__aexit__(None, None, None))
+            finally:
+                self._loop.call_soon_threadsafe(self._loop.stop)
+                self._thread.join(5)
+                self._loop.close()
+                if self._tmp:
+                    shutil.rmtree(self._tmp, ignore_errors=True)
diff --git a/tests/acceptance/drivers/wake_receiver.py b/tests/acceptance/drivers/wake_receiver.py
index e618393..b6b3310 100644
--- a/tests/acceptance/drivers/wake_receiver.py
+++ b/tests/acceptance/drivers/wake_receiver.py
@@ -3,8 +3,11 @@
 POST /wake: records every request (headers, raw body, status), verifies the signature with app.wake.verify
 (401 when invalid), drops repeats of X-MMB-Delivery (idempotency key) and answers 204. Controls: `down`
 (503 to everything), `hang` (asyncio.Event the handler waits on, to cancel a dispatcher mid-POST).
-`transport()` routes an httpx.AsyncClient to it in-process.
+`transport()` routes an httpx.AsyncClient to it in-process; `serve()` (lb5) serves it on 127.0.0.1:<free port>
+for a dispatcher in another process (the container).
 """
+import asyncio
+import contextlib
 import json
 import time
 
@@ -46,3 +49,21 @@ class WakeReceiver:
 
     def transport(self) -> httpx.AsyncBaseTransport:
         return httpx.ASGITransport(app=self.app)
+
+    @contextlib.asynccontextmanager
+    async def serve(self):
+        """Yields the wake URL http://127.0.0.1:<port>/wake."""
+        import uvicorn
+        server = uvicorn.Server(uvicorn.Config(self.app, host="127.0.0.1", port=0, log_level="warning",
+                                               lifespan="off"))
+        task = asyncio.create_task(server.serve())
+        while not server.started:
+            if task.done():
+                task.result()
+            await asyncio.sleep(0.01)
+        port = server.servers[0].sockets[0].getsockname()[1]
+        try:
+            yield "http://127.0.0.1:%d/wake" % port
+        finally:
+            server.should_exit = True
+            await task
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
   360	        if not self._catchup_pending:
   361	            self._catchup_pending, self._catchup_from = True, alive_at
   362	        alive_at = self._catchup_from
   363	        await self._refresh_members(client)
   364	        floor = int(self.clock() * 1000) - self.window_ms
   365	        n_posts = n_skipped = 0
   366	        for cid, ch in list(self.members.items()):
   367	            cur = await asyncio.to_thread(self.state.get_cursor, cid)
   368	            if cur is None:
   369	                if alive_at is None:
   370	                    continue                  # first start ever: no backfill of history
   371	                cur = (alive_at, "")
   372	            try:                              # skipped posts are counted at most one window further back
   373	                posts = await self._since(client, cid, max(cur[0], floor - self.window_ms))
   374	            except MMError as e:
   375	                if e.code == "not_found" or e.status == 403:
   376	                    _log("channel_unavailable", channel_id=cid, code=e.code)
   377	                    self.members.pop(cid, None)
   378	                    continue
   379	                raise
   380	            ctype = ch.get("type") or (await self._get(client, self._channels, cid, "/channels/" + cid) or {}).get("type")
   381	            for p in sorted(posts, key=lambda p: (p.get("create_at", 0), p.get("id", ""))):
   382	                at = p.get("create_at")
   383	                if not isinstance(at, int) or at < cur[0] or p.get("delete_at"):
   384	                    continue                  # equal create_at is re-offered: the ledger dedupes (PR-3)
   385	                if at < floor:
   386	                    n_skipped += 1
   387	                    await asyncio.to_thread(self.state.set_cursor, cid, at, p["id"])
   388	                    continue
   389	                ev = {"event": "posted", "data": {"channel_type": ctype, "channel_name": ch.get("name"),
   390	                                                  "channel_display_name": ch.get("display_name"),
   391	                                                  "team_id": ch.get("team_id"), "post": p} }
   392	                intent = decide(ev, self.bot_user_id)
   393	                if intent:
   394	                    n_posts += await self._enqueue(intent, client)
   395	                else:
   396	                    await asyncio.to_thread(self.state.set_cursor, cid, at, p["id"])
   397	        self._catchup_pending = False
   398	        _log("catchup", reason=reason, channels=len(self.members), posts=n_posts, skipped=n_skipped)
   399	        if n_skipped:
   400	            _log("catchup_skipped", n=n_skipped, window_minutes=self.window_ms // 60_000)
   401	
   402	    async def _since(self, client, cid: str, since_ms: int) -> list:
   403	        """Every post with create_at >= since_ms. Mattermost ignores page/per_page when `since` is given (and caps
   404	        the result), so this pages by post id instead: the newest page, then `before=<oldest id seen>` until a
   405	        page reaches back past since_ms or runs out. MAX_PAGES (x per_page posts in one channel inside the
   406	        catch-up window) is the only bound; reaching it is logged (`catchup_truncated`)."""
   407	        posts: dict = {}
   408	        before = ""
   409	        for _ in range(MAX_PAGES):
   410	            q = {"page": 0, "per_page": self.per_page}
   411	            if before:
   412	                q["before"] = before
   413	            r = await client.get("/channels/%s/posts" % cid, **q)
   414	            batch = [r["posts"][i] for i in r.get("order", []) if i in r.get("posts", {})]
   415	            new = [p for p in batch if p["id"] not in posts]
   416	            posts.update((p["id"], p) for p in new)
   417	            if len(batch) < self.per_page or not new:
   418	                return list(posts.values())
   419	            oldest = batch[-1]                # Mattermost order is newest first
   420	            if oldest.get("create_at", 0) < since_ms:
   421	                return list(posts.values())
   422	            before = oldest["id"]
   423	        _log("catchup_truncated", channel_id=cid, pages=MAX_PAGES)
   424	        return list(posts.values())
   425	
   426	    async def _get(self, client, cache: dict, key: str, path: str) -> dict | None:
   427	        """Cached REST lookup; None (not cached) on Mattermost errors so the event hints are used instead."""
   428	        if key not in cache:
   429	            try:
   430	                cache[key] = await client.get(path)
   431	            except MMError as e:
   432	                _log("lookup_failed", path=path.split("/")[1], code=e.code)
   433	                return None
   434	        return cache[key]
   435	
.venv/bin/python
.venv/bin/python3
.venv/bin/python3.12

exec
/bin/bash -lc '.venv/bin/pytest tests/unit -q' in /mnt/d/rob/projects/mmbridge
exec
/bin/bash -lc 'python3 .eng/bin/eng-check .' in /mnt/d/rob/projects/mmbridge
 succeeded in 1745ms:
WARN  .eng/runners.toml: no on_complete hook configured ([hooks] empty or missing) - bots must stay attached to eng-run until exit; fire-and-forget needs a non-empty on_complete / <role>_on_complete (PROCESS.md section 10, LESSONS L-006)
WARN  PROJECT_STATE.md: ## Latest artifacts has 27 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 25 rows / 4448 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 121 artifact(s) checked

2026-10-28T18:10:26.862160Z ERROR codex_core::session: failed to record rollout items: thread 01a183b3-d2ed-7c73-a5dd-baef0dcba573 not found
codex
Catch-up can permanently miss direct messages for a bot without team membership because channel discovery depends on enumerating teams.

Review comment:

- [P2] Discover direct channels independently of team membership — /mnt/d/rob/projects/mmbridge/app/listener.py:328-331
  When the bot belongs to no teams, `/users/me/teams` returns an empty list, so this loop discovers no direct channels. A DM created during an outage also has neither a stored cursor nor an entry in `_seen`, meaning catch-up silently misses its messages even within the configured window. Direct messages do not require team membership; enumerate the bot's direct channels independently of the team loop so this supported case can recover.
Catch-up can permanently miss direct messages for a bot without team membership because channel discovery depends on enumerating teams.

Review comment:

- [P2] Discover direct channels independently of team membership — /mnt/d/rob/projects/mmbridge/app/listener.py:328-331
  When the bot belongs to no teams, `/users/me/teams` returns an empty list, so this loop discovers no direct channels. A DM created during an outage also has neither a stored cursor nor an entry in `_seen`, meaning catch-up silently misses its messages even within the configured window. Direct messages do not require team membership; enumerate the bot's direct channels independently of the team loop so this supported case can recover.
```
