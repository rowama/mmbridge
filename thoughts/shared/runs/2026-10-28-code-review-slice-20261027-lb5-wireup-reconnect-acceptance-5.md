---
id: RUN-2026-10-28-code-review-slice-20261027-lb5-wireup-reconnect-acceptance-5
type: run-log
phase: verify
status: ok
owner_agent: eng-run
date: 2026-10-28
links: [thoughts/shared/plans/2026-10-27-live-bots.md, thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md, thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-5.md]
role: code-review
runner: codex
tool: codex
slice: SLICE-20261027-lb5-wireup-reconnect-acceptance
plan: thoughts/shared/plans/2026-10-27-live-bots.md
base: 3ed94b4
exit_code: 0
pid: 626982
eng_run_pid: 626981
started: 2026-10-28T13:14:09
prompt_template: code-review.md v2
---
# eng-run code-review slice-20261027-lb5-wireup-reconnect-acceptance

## Summary
- role: code-review; runner: codex (codex); exit code: 0; started 2026-10-28 13:14:09
- review file: thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-5.md - No findings.

## Command
````
codex review --base 3ed94b4
````

## Prompt
````
You are the independent code reviewer for this repository (eng-process kit v2.5.9). You did not write this code. Do not edit any file.

Follow the cross-model review step of eng-verify (.claude/skills/eng-verify/SKILL.md) and .eng/PROCESS.md section 10.

Review the changes of slice SLICE-20261027-lb5-wireup-reconnect-acceptance (diff 3ed94b4...HEAD; slice card: thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md; plan: thoughts/shared/plans/2026-10-27-live-bots.md) for correctness against the slice's acceptance criteria, missing or weak tests, security (auth, tenancy, secrets, injection), error handling, and maintainability.

Executable specs (v2.5): run `python .eng/bin/eng-spec status .`. Any change to locked specs or the DSL public interface is a [high] finding unless Rob re-approved it (new CP-C speclock row). For every changed DSL assertion step (assert_/then_/expect_/check_/verify_) name the step (e.g. `assert_order_placed`) in a finding and say whether the check got weaker. Driver changes are fine unless they hide failures (swallowed errors, retries that mask bugs, sleeps).

Output: a numbered list of findings, each as
  N. [severity] file:line - finding - suggested fix
with severity one of critical | high | medium | low. If you find nothing, write exactly "No findings."
Your final message is saved by eng-run to thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-5.md (a review-findings artifact). Findings are advisory; Rob decides.
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
session id: 01a183b8-3501-7de2-b320-81b2c612c428
--------
user
changes against '3ed94b4'
exec
/bin/bash -lc 'cat PROJECT_STATE.md; cat AGENTS.md; git status --short; git diff --stat 3ed94b421d7367292510790ff6f73598eee94237' in /mnt/d/rob/projects/mmbridge
 succeeded in 876ms:
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
?? thoughts/shared/runs/2026-10-28-code-review-slice-20261027-lb5-wireup-reconnect-acceptance-4.md
?? thoughts/shared/runs/2026-10-28-code-review-slice-20261027-lb5-wireup-reconnect-acceptance-5.running.md
?? thoughts/shared/runs/2026-10-28-code-review-slice-20261027-lb5-wireup-reconnect-acceptance.md
?? thoughts/shared/runs/2026-10-28-implement-slice-20261027-lb5-wireup-reconnect-acceptance.md
?? thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-2.md
?? thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-3.md
?? thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-4.md
?? thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review.md
 AGENTS.md                                          |   7 +-
 CHANGELOG.md                                       |   4 +
 OWNER-GUIDE.md                                     |   2 +
 PROJECT_STATE.md                                   |   8 +-
 README.md                                          |  21 ++
 app/listener.py                                    | 387 ++++++++++++++++++---
 app/live.py                                        | 176 ++++++++++
 app/main.py                                        |  15 +-
 app/state.py                                       |  33 +-
 tests/acceptance/drivers/fake_mattermost.py        | 123 ++++++-
 tests/acceptance/drivers/live.py                   | 253 +++++++++-----
 tests/acceptance/drivers/wake_receiver.py          |  23 +-
 tests/unit/test_app.py                             |   2 +-
 tests/unit/test_listener.py                        |  15 +-
 tests/unit/test_main_live.py                       | 297 ++++++++++++++++
 tests/unit/test_reconnect.py                       | 386 ++++++++++++++++++++
 ...-28_12-50-17_lb5-implemented-awaiting-review.md |  63 ++++
 thoughts/shared/plans/2026-10-27-live-bots.md      |   6 +-
 .../2026-10-27-lb5-wireup-reconnect-acceptance.md  |  43 ++-
 19 files changed, 1680 insertions(+), 184 deletions(-)

exec
/bin/bash -lc "cat thoughts/shared/handoffs/2026-10-28_12-50-17_lb5-implemented-awaiting-review.md; cat .eng/PROCESS.md; find app tests -name 'AGENTS*'; python3 .eng/bin/eng-check .; git diff 3ed94b421d7367292510790ff6f73598eee94237 -- app" in /mnt/d/rob/projects/mmbridge
 succeeded in 1925ms:
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

WARN  .eng/runners.toml: no on_complete hook configured ([hooks] empty or missing) - bots must stay attached to eng-run until exit; fire-and-forget needs a non-empty on_complete / <role>_on_complete (PROCESS.md section 10, LESSONS L-006)
WARN  PROJECT_STATE.md: ## Latest artifacts has 27 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 25 rows / 4448 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 123 artifact(s) checked
diff --git a/app/listener.py b/app/listener.py
index 19eed23..7281d92 100644
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
@@ -49,85 +65,372 @@ def _iso(ms: int) -> str:
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
+        try:                                  # D channels need no team: a team-less bot is found only here
+            for c in await client.get("/users/%s/channels" % self.bot_user_id):
+                if isinstance(c, dict) and c.get("type") == "D":
+                    found.setdefault(c["id"], c)
+        except MMError as e:
+            if e.code != "not_found":
+                raise
+            _log("direct_channels_unavailable", code=e.code)   # older server: team lists still carry D
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
/bin/bash -lc 'cat app/listener.py' in /mnt/d/rob/projects/mmbridge
 succeeded in 0ms:
"""Mattermost websocket listener for the ONE live bot (ADR-0007).

run(): GET /users/me -> WS /api/v4/websocket with `Authorization: Bearer` -> hello{connection_id} -> for each
`posted` event, live_filter.decide -> wake payload (ADR-0008 schema, no token; channel/team/sender lookups
cached) -> state.enqueue_and_advance (dedupe gate + forward-only cursor, PR-3). Tracks seq; sends the
Mattermost `ping` action every PING_S and treats IDLE_S without any frame as dead. Never joins channels or posts.

lb5: run() reconnects forever (backoff 1->60 s with jitter) and asks to resume with
`?connection_id&sequence_number`. Same connection_id in hello = resumed (missed events are replayed). A new id,
or a seq gap, runs REST catch-up: membership across all teams (+ D channels, channels with a cursor, channels
seen on the socket), then per channel `GET /channels/{id}/posts` paged back by post id (`before=`; never
`since`, which Mattermost does not page), ascending (create_at, post_id),
each post through decide() and enqueue_and_advance (the ledger dedupes). Channels without a cursor start at meta
`last_event_at` (last alive); posts older than LIVE_CATCHUP_MINUTES are skipped (`catchup_skipped`). 401 ->
`degraded`, retry every 5 min or on a config change. One listener per state.db (meta lease `listener_owner`).
"""
import asyncio
import itertools
import json
import logging
import os
import random
import time
from datetime import datetime, timezone

import websockets
from websockets.exceptions import ConnectionClosed, InvalidHandshake, InvalidStatus

from app import logging as mlog
from app.live_filter import WakeIntent, decide
from app.mattermost import MATTERMOST_URL, MMError
from app.wake import token_fp

PING_S = 30
IDLE_S = 60
BACKOFF_S, MAX_BACKOFF_S = 1.0, 60.0
AUTH_RETRY_S = 300
LEASE_TTL_S = 60
PER_PAGE = 200
MAX_PAGES = 50
ALIVE_EVERY_S = 5

# websockets logs handshake headers (incl. Authorization) and frames at DEBUG: own logger, redacted, INFO.
_ws_log = logging.getLogger("mmbridge.ws")
_ws_log.setLevel(logging.INFO)
_ws_log.addFilter(mlog.RedactFilter())


def ws_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    return ("wss://" + base[8:] if base.startswith("https://") else "ws://" + base.removeprefix("http://")) \
        + "/api/v4/websocket"


def connect(url: str, headers: dict):
    """Default ws_connect: protocol-level keepalive off (the listener pings at application level)."""
    return websockets.connect(url, additional_headers=headers, ping_interval=None, open_timeout=10, logger=_ws_log)


def _log(event: str, **fields) -> None:
    mlog.log.info(json.dumps({"event": event, **fields}))


def _iso(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Unauthorized(Exception):
    """users/me or the websocket handshake refused the bot token."""


class LeaseHeld(Exception):
    """Another listener holds the state.db lease."""


class Listener:
    def __init__(self, cfg, state, client_factory, ws_connect=connect, clock=time.time,
                 base_url: str = MATTERMOST_URL, ping_s: float = PING_S, idle_s: float = IDLE_S,
                 backoff_s: float = BACKOFF_S, max_backoff_s: float = MAX_BACKOFF_S,
                 auth_retry_s: float = AUTH_RETRY_S, lease_retry_s: float = LEASE_TTL_S / 2,
                 catchup_minutes: float | None = None, refresh_s: float | None = None, per_page: int = PER_PAGE,
                 rand=random.random):
        """cfg: BotConfig or a zero-arg callable returning the current one (ConfigHolder.get, PR-2)."""
        self._cfg = cfg if callable(cfg) else (lambda: cfg)
        self.state, self.client_factory, self.ws_connect = state, client_factory, ws_connect
        self.clock, self.base_url, self.ping_s, self.idle_s = clock, base_url, ping_s, idle_s
        self.backoff_s, self.max_backoff_s, self.rand = backoff_s, max_backoff_s, rand
        self.auth_retry_s, self.lease_retry_s, self.per_page = auth_retry_s, lease_retry_s, per_page
        self.window_ms = int(60_000 * (catchup_minutes if catchup_minutes is not None
                                       else float(os.getenv("LIVE_CATCHUP_MINUTES", "15"))))
        self.refresh_s = refresh_s if refresh_s is not None else float(os.getenv("LIVE_MEMBERSHIP_REFRESH_S", "300"))
        self.status = "off"                   # off | connecting | ok | degraded (401)
        self.bot_user_id = self.connection_id = self.last_seq = None
        self.members: dict = {}               # channel id -> channel (O/P/D), catch-up set
        self._seen: dict = {}                 # channel id -> type, seen on the socket since start
        self._bot: dict = {}
        self._channels: dict = {}
        self._teams: dict = {}
        self._users: dict = {}
        self._alive_at = None                 # ms, last frame received (meta last_event_at)
        self._alive_written = 0.0
        self._refreshed_at = 0.0
        self._catchup_pending = False
        self._catchup_from = None
        self._resume_id = None
        self._ws = None
        self._wake = asyncio.Event()

    @property
    def cfg(self):
        return self._cfg()

    def config_changed(self, old, new) -> None:
        """ConfigHolder subscriber: a new token reconnects at once (no resume across tokens, fresh lookups)."""
        if new.token == old.token:
            return
        mlog.register_secret(new.token)
        self.connection_id = None
        self._channels, self._teams, self._users = {}, {}, {}
        self._wake.set()
        if self._ws is not None:
            asyncio.ensure_future(self._ws.close())

    def _backoff(self, attempt: int) -> float:
        d = min(self.max_backoff_s, self.backoff_s * 2 ** (max(attempt, 1) - 1))
        return d * (0.5 + 0.5 * self.rand())

    async def _pause(self, seconds: float) -> None:
        """Sleep, cut short by a config change."""
        self._wake.clear()
        try:
            await asyncio.wait_for(self._wake.wait(), seconds)
        except TimeoutError:
            pass

    async def run(self) -> None:
        """Reconnect forever (cancel to stop)."""
        attempt = 0
        try:
            while True:
                try:
                    ok = await self.connect_once()
                    attempt = 0 if ok else attempt + 1
                except Unauthorized:
                    self.status = "degraded"
                    mlog.log.warning(json.dumps({"event": "mm_unauthorized", "retry_s": self.auth_retry_s}))
                    await self._pause(self.auth_retry_s)
                    continue
                except LeaseHeld:
                    _log("listener_lease_held", instance=self.state.instance_id)
                    await self._pause(self.lease_retry_s)
                    continue
                except (OSError, TimeoutError, MMError, InvalidHandshake, ConnectionClosed) as e:
                    attempt += 1
                    _log("ws_connect_failed", error=getattr(e, "code", None) or type(e).__name__)
                delay = self._backoff(attempt)
                self.status = "connecting"
                _log("ws_reconnect", attempt=attempt, delay=round(delay, 2))
                await self._pause(delay)
        finally:
            self.status = "off"
            await asyncio.to_thread(self.state.release_owner, "listener_owner")

    async def connect_once(self) -> bool:
        """One connection; True if it reached hello (then dropped/idled). Raises Unauthorized / LeaseHeld."""
        cfg = self.cfg
        mlog.register_secret(cfg.token)
        client = self.client_factory(cfg.token)
        self.status = "connecting"
        reached = False
        try:
            if not await asyncio.to_thread(self.state.claim_owner, self.clock(), LEASE_TTL_S, "listener_owner"):
                self.status = "off"
                raise LeaseHeld()
            if self._alive_at is None:
                v = await asyncio.to_thread(self.state.get_meta, "last_event_at")
                self._alive_at = int(v) if v else None
            try:
                me = await client.get("/users/me")
            except MMError as e:
                if e.code == "unauthorized":
                    raise Unauthorized() from None
                raise
            if me["id"] != self.bot_user_id:
                self.connection_id, self.members, self._seen = None, {}, {}
            self.bot_user_id, self._bot = me["id"], {"user_id": me["id"], "username": me["username"]}
            await asyncio.to_thread(self.state.set_meta, "bot_user_id", me["id"])   # dispatcher: bot_rotated
            await asyncio.to_thread(self.state.set_meta, "bot_identity",              # id + token as one row
                                    token_fp(cfg.token) + ":" + me["id"])
            url = ws_url(self.base_url)
            self._resume_id = self.connection_id
            if self.connection_id and self.last_seq is not None:
                url += "?connection_id=%s&sequence_number=%d" % (self.connection_id, self.last_seq + 1)
            try:
                conn = self.ws_connect(url, {"Authorization": "Bearer " + cfg.token})
                ws = await conn.__aenter__()
            except InvalidStatus as e:
                if e.response.status_code in (401, 403):
                    raise Unauthorized() from None
                raise
            self._ws = ws
            try:
                pinger = asyncio.create_task(self._ping(ws))
                try:
                    reached = await self._read(ws, client)
                finally:
                    pinger.cancel()
            finally:
                self._ws = None
                await conn.__aexit__(None, None, None)
        finally:
            if self.status != "degraded":
                self.status = "off"
        return reached

    async def _read(self, ws, client) -> bool:
        reached = False
        while True:
            try:
                raw = await asyncio.wait_for(ws.recv(), self.idle_s)
            except TimeoutError:
                _log("ws_idle", seconds=self.idle_s)
                return reached
            except ConnectionClosed:
                _log("ws_closed", connection_id=self.connection_id)
                return reached
            prev_alive = self._alive_at
            self._alive_at = int(self.clock() * 1000)   # persisted only once the frame is handled
            try:
                if await self._frame(raw, client, prev_alive):
                    reached = True
            except BaseException:
                self._alive_at = prev_alive   # not handled: a later catch-up must still start before this frame
                raise
            await self._mark_alive()

    async def _frame(self, raw, client, prev_alive: int | None) -> bool:
        """Handle one frame; True when it was a hello (connection established). Raises leave last_seq and
        meta last_event_at untouched, so a reconnect resumes/catches up from before this frame."""
        try:
            ev = json.loads(raw)
        except ValueError:
            mlog.log.warning(json.dumps({"event": "event_invalid", "reason": "json"}))
            return False
        if not isinstance(ev, dict) or "event" not in ev:
            return False                      # ping replies ({"status","seq_reply"}) and other non-events
        if ev["event"] == "hello":
            cid = (ev.get("data") or {}).get("connection_id")
            resumed = bool(cid) and cid == self._resume_id
            self.connection_id = cid
            await asyncio.to_thread(self.state.set_meta, "ws_connection_id", cid or "")
            if not resumed:
                self.last_seq = ev.get("seq") if isinstance(ev.get("seq"), int) else 0
            _log("ws_connected", connection_id=cid, resumed=resumed,
                 server_version=(ev.get("data") or {}).get("server_version"))
            if not resumed or self._catchup_pending:
                await self._catch_up(client, "new_connection" if not resumed else "pending", prev_alive)
            elif time.monotonic() - self._refreshed_at >= self.refresh_s:
                await self._refresh_soft(client)
            self.status = "ok"
            return True
        seq = ev.get("seq")
        if self._seq_gap(ev):
            await self._catch_up(client, "seq_gap", prev_alive)
        if time.monotonic() - self._refreshed_at >= self.refresh_s:
            await self._refresh_soft(client)
        await self._membership_event(ev, client)
        intent = decide(ev, self.bot_user_id)
        if intent:
            self._seen.setdefault(intent.channel_id, {"id": intent.channel_id, "type": intent.channel_type})
            await self._enqueue(intent, client)
        if isinstance(seq, int):
            self.last_seq = seq           # only after the event is committed (a raise above replays it)
        return False

    async def _enqueue(self, intent: WakeIntent, client) -> bool:
        payload = await self._payload(intent, client)
        new = await asyncio.to_thread(self.state.enqueue_and_advance, intent.post_id, intent.channel_id,
                                      payload, intent.create_at)
        _log("wake_queued", post_id=intent.post_id, channel_id=intent.channel_id, new=new)
        return new

    def _seq_gap(self, ev: dict) -> bool:
        """True on a seq gap (missed events). Does not advance last_seq (_frame does, after the commit)."""
        seq = ev.get("seq")
        if not isinstance(seq, int):
            return False
        gap = self.last_seq is not None and seq != self.last_seq + 1
        if gap:
            _log("ws_seq_gap", expected=self.last_seq + 1, got=seq)
        return gap

    async def _mark_alive(self) -> None:
        """Persist the last-alive time of a fully handled frame (never mid catch-up: a restart then still
        starts cursor-less channels at the catch-up's own start)."""
        if self._alive_at is None or self._catchup_pending:
            return
        if time.monotonic() - self._alive_written >= ALIVE_EVERY_S:
            self._alive_written = time.monotonic()
            await asyncio.to_thread(self.state.set_meta, "last_event_at", str(self._alive_at))

    async def _ping(self, ws) -> None:
        for n in itertools.count(1):
            await asyncio.sleep(self.ping_s)
            if not await asyncio.to_thread(self.state.claim_owner, self.clock(), LEASE_TTL_S, "listener_owner"):
                _log("listener_lease_lost", instance=self.state.instance_id)
                await ws.close()
                return
            try:
                await ws.send(json.dumps({"action": "ping", "seq": n}))
            except ConnectionClosed:
                return

    # --- membership + catch-up (architecture 'catch-up channel discovery') -------------------------------------
    async def _paged(self, client, path: str) -> list:
        out, ids = [], set()
        for page in range(MAX_PAGES):
            batch = await client.get(path, page=page, per_page=self.per_page)
            new = [x for x in batch if isinstance(x, dict) and x.get("id") not in ids]
            ids.update(x["id"] for x in new)
            out += new
            if len(batch) < self.per_page or not new:
                break
        return out

    async def _refresh_members(self, client) -> None:
        found = {}
        for t in await self._paged(client, "/users/me/teams"):
            for c in await self._paged(client, "/users/me/teams/%s/channels" % t["id"]):
                if c.get("type") in ("O", "P", "D"):
                    found[c["id"]] = c
        try:                                  # D channels need no team: a team-less bot is found only here
            for c in await client.get("/users/%s/channels" % self.bot_user_id):
                if isinstance(c, dict) and c.get("type") == "D":
                    found.setdefault(c["id"], c)
        except MMError as e:
            if e.code != "not_found":
                raise
            _log("direct_channels_unavailable", code=e.code)   # older server: team lists still carry D
        for cid in await asyncio.to_thread(self.state.cursor_channels):
            found.setdefault(cid, self.members.get(cid) or {"id": cid})
        for cid, c in self._seen.items():
            found.setdefault(cid, c)
        self.members, self._refreshed_at = found, time.monotonic()

    async def _refresh_soft(self, client) -> None:
        """Periodic/event refresh: a Mattermost error keeps the old set (catch-up refreshes again)."""
        try:
            await self._refresh_members(client)
        except MMError as e:
            self._refreshed_at = time.monotonic()
            _log("membership_refresh_failed", code=e.code)

    async def _membership_event(self, ev: dict, client) -> None:
        kind, data, bc = ev["event"], ev.get("data") or {}, ev.get("broadcast") or {}
        if kind in ("user_added", "added_to_team") and data.get("user_id") == self.bot_user_id:
            await self._refresh_soft(client)
        elif kind == "user_removed" and self.bot_user_id in (data.get("user_id"), bc.get("user_id")):
            cid = data.get("channel_id") or bc.get("channel_id")
            if cid:
                self.members.pop(cid, None)
                self._seen.pop(cid, None)
                await asyncio.to_thread(self.state.delete_cursor, cid)
                _log("channel_removed", channel_id=cid)

    async def _catch_up(self, client, reason: str, alive_at: int | None) -> None:
        """REST catch-up of every member channel; raises (and stays pending, keeping its start) on MM errors."""
        if not self._catchup_pending:
            self._catchup_pending, self._catchup_from = True, alive_at
        alive_at = self._catchup_from
        await self._refresh_members(client)
        floor = int(self.clock() * 1000) - self.window_ms
        n_posts = n_skipped = 0
        for cid, ch in list(self.members.items()):
            cur = await asyncio.to_thread(self.state.get_cursor, cid)
            if cur is None:
                if alive_at is None:
                    continue                  # first start ever: no backfill of history
                cur = (alive_at, "")
            try:                              # skipped posts are counted at most one window further back
                posts = await self._since(client, cid, max(cur[0], floor - self.window_ms))
            except MMError as e:
                if e.code == "not_found" or e.status == 403:
                    _log("channel_unavailable", channel_id=cid, code=e.code)
                    self.members.pop(cid, None)
                    continue
                raise
            ctype = ch.get("type") or (await self._get(client, self._channels, cid, "/channels/" + cid) or {}).get("type")
            for p in sorted(posts, key=lambda p: (p.get("create_at", 0), p.get("id", ""))):
                at = p.get("create_at")
                if not isinstance(at, int) or at < cur[0] or p.get("delete_at"):
                    continue                  # equal create_at is re-offered: the ledger dedupes (PR-3)
                if at < floor:
                    n_skipped += 1
                    await asyncio.to_thread(self.state.set_cursor, cid, at, p["id"])
                    continue
                ev = {"event": "posted", "data": {"channel_type": ctype, "channel_name": ch.get("name"),
                                                  "channel_display_name": ch.get("display_name"),
                                                  "team_id": ch.get("team_id"), "post": p} }
                intent = decide(ev, self.bot_user_id)
                if intent:
                    n_posts += await self._enqueue(intent, client)
                else:
                    await asyncio.to_thread(self.state.set_cursor, cid, at, p["id"])
        self._catchup_pending = False
        _log("catchup", reason=reason, channels=len(self.members), posts=n_posts, skipped=n_skipped)
        if n_skipped:
            _log("catchup_skipped", n=n_skipped, window_minutes=self.window_ms // 60_000)

    async def _since(self, client, cid: str, since_ms: int) -> list:
        """Every post with create_at >= since_ms. Mattermost ignores page/per_page when `since` is given (and caps
        the result), so this pages by post id instead: the newest page, then `before=<oldest id seen>` until a
        page reaches back past since_ms or runs out. MAX_PAGES (x per_page posts in one channel inside the
        catch-up window) is the only bound; reaching it is logged (`catchup_truncated`)."""
        posts: dict = {}
        before = ""
        for _ in range(MAX_PAGES):
            q = {"page": 0, "per_page": self.per_page}
            if before:
                q["before"] = before
            r = await client.get("/channels/%s/posts" % cid, **q)
            batch = [r["posts"][i] for i in r.get("order", []) if i in r.get("posts", {})]
            new = [p for p in batch if p["id"] not in posts]
            posts.update((p["id"], p) for p in new)
            if len(batch) < self.per_page or not new:
                return list(posts.values())
            oldest = batch[-1]                # Mattermost order is newest first
            if oldest.get("create_at", 0) < since_ms:
                return list(posts.values())
            before = oldest["id"]
        _log("catchup_truncated", channel_id=cid, pages=MAX_PAGES)
        return list(posts.values())

    async def _get(self, client, cache: dict, key: str, path: str) -> dict | None:
        """Cached REST lookup; None (not cached) on Mattermost errors so the event hints are used instead."""
        if key not in cache:
            try:
                cache[key] = await client.get(path)
            except MMError as e:
                _log("lookup_failed", path=path.split("/")[1], code=e.code)
                return None
        return cache[key]

    async def _payload(self, w: WakeIntent, client) -> dict:
        h = w.hints
        ch = await self._get(client, self._channels, w.channel_id, "/channels/" + w.channel_id) or {}
        team_id = ch.get("team_id", h.get("team_id")) or ""
        team = await self._get(client, self._teams, team_id, "/teams/" + team_id) if team_id else None
        user = await self._get(client, self._users, w.user_id, "/users/" + w.user_id) or {}
        return {
            "version": 1, "kind": "post", "delivery_id": w.post_id, "attempt": 1,
            "bot": dict(self._bot),
            "channel": {"id": w.channel_id, "name": ch.get("name", h.get("channel_name")),
                        "display_name": ch.get("display_name", h.get("channel_display_name")),
                        "type": w.channel_type, "team": (team or {}).get("name")},
            "sender": {"user_id": w.user_id,
                       "username": user.get("username") or (h.get("sender_name") or "").lstrip("@") or None},
            "post": {"id": w.post_id, "message": w.message, "create_at": _iso(w.create_at), "root_id": w.root_id},
        }

exec
/bin/bash -lc 'cat app/live_filter.py; cat app/mattermost.py; cat app/wake.py; cat .claude/skills/eng-code-review/SKILL.md 2>/dev/null; find .. -maxdepth 2 -name AGENTS.override.md; git diff 3ed94b421d7367292510790ff6f73598eee94237 -- tests/acceptance/drivers/live.py' in /mnt/d/rob/projects/mmbridge
 succeeded in 103ms:
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
"""Signed wake webhook (ADR-0008): sign/verify and the Dispatcher that delivers queued wakes from state.db.

POST <wake_url> with the wake payload as raw JSON body and headers X-MMB-Delivery (post id, idempotency key),
X-MMB-Timestamp (unix seconds), X-MMB-Signature `v1=<hex HMAC-SHA256(secret, ts + "." + body)>`.
Receivers: `verify(secret, headers, raw_body, now)`; constant-time, rejects |now - ts| > 300 s, an X-MMB-Delivery that is missing or differs from the signed delivery_id, unknown versions
and missing headers.

Dispatcher.tick(): heartbeat the single-owner lease (standby while another owner is fresh), recover_stale,
prune (start + every 6 h), claim_due up to 4 and POST them concurrently (5 s timeout). Config is read at
send time (url/secret rotation applies to queued wakes); wakes of a previous bot user fail `bot_rotated`.
Nothing is claimed until the listener has resolved the identity of the CURRENT token (meta bot_identity =
"<token_fp>:<bot_user_id>", one row, matches the config), so a stale id from a previous token/run never approves old wakes (review P1).
Each POST has an overall deadline of TIMEOUT_S (not only per network step), so a slow-drip receiver cannot
stall the loop and the owner heartbeat (review P2).
2xx delivered; 408/429/5xx/timeout/connect retry (state.next_delay; failed after max attempts); other 4xx
failed. Logs carry post id, attempt and error class only: never token, secret, signature or message text.
"""
import asyncio
import hashlib
import hmac
import json
import time
from collections.abc import Mapping

import httpx

from app import logging as mlog
from app.state import next_delay

WINDOW_S = 300
TIMEOUT_S = 5
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

exec
/bin/bash -lc 'ls .venv/bin/python*; find . -name AGENTS.md -o -name AGENTS.override.md; cat tests/unit/test_reconnect.py' in /mnt/d/rob/projects/mmbridge
 succeeded in 1061ms:
.venv/bin/python
.venv/bin/python3
.venv/bin/python3.12
./.eng/templates/AGENTS.md
./AGENTS.md
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


async def test_teamless_bot_discovers_dm_created_during_outage(world, tmp_path):
    """A bot in no team still has D channels: catch-up discovers them via GET /users/{id}/channels."""
    m, w = world
    m.channels[w["town"]]["members"].discard(w["bot"]["id"])
    ann = m.add_user("ann")
    async with m.serve() as base:
        r = await Run((m, w, base), tmp_path / "state.db").start()

        def during():
            c = m.direct_channel(w["bot"]["id"], ann["id"])
            return r.post(c["id"], "dm to a team-less bot", user="ann")
        p = await r.outage(during)
        await until(lambda: r.state.wake(p["id"]))
        await r.stop()
    assert r.state.wake(p["id"]).payload["channel"]["type"] == "D"


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
/bin/bash -lc '.venv/bin/pytest tests/unit -q' in /mnt/d/rob/projects/mmbridge
exec
/bin/bash -lc "git diff 3ed94b421d7367292510790ff6f73598eee94237 > /tmp/mmbridge-review.diff; sed -n '1,100p' /tmp/mmbridge-review.diff; cat tests/unit/test_main_live.py; python3 .eng/bin/eng-check ." in /mnt/d/rob/projects/mmbridge
 succeeded in 2255ms:
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
index 40c9701..9e0e39e 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -2,6 +2,10 @@
 All notable changes to this project. Format: Keep a Changelog style; newest first.
 
 ## [Unreleased]
+<!-- id: CHANG-20261028-lb5-wireup-reconnect | owner_agent: unassigned | date: 2026-10-28 -->
+### Added
+- Live bots go live with LIVE_BOTS_ENABLED=true: the listener and wake dispatcher start with the bridge, /health reports listener (disabled|off|connecting|ok|degraded) and wake_failed_24h, dropped Mattermost connections reconnect and catch up missed posts (all member channels on all teams and DMs, 15 min window) with exactly one wake per post, and store edits (token, wake URL, secret) apply without a redeploy.
+
 <!-- id: CHANG-20261027-lb4b-drop-allowlist | owner_agent: unassigned | date: 2026-10-27 -->
 ### Changed
 - Live bots: no channel allow-list. `python -m app.admin set-bot` takes only the token and wake URL (`--channels` is refused as no longer used; existing /data/bots.enc files with channel ids still load), and the bot wakes on every post by someone else in public or private channels it is a Mattermost member of, plus DMs; thread replies carry root_id. The bridge never joins channels.
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
 
diff --git a/PROJECT_STATE.md b/PROJECT_STATE.md
index 257bc9a..35a11a8 100644
--- a/PROJECT_STATE.md
+++ b/PROJECT_STATE.md
@@ -3,7 +3,7 @@ id: STATE
 type: project-state
 phase: implement
 status: active
-owner_agent: grok-bot
+owner_agent: claude-code
 date: 2026-10-28
 links: []
 triage: large             # unset | small | medium | large
@@ -31,10 +31,10 @@ implement (increment A Live bots, Large) - PROCESS.md section 3.
 A public HTTPS MCP bridge (Python, deployed on Coolify at chats.rmlab.cloud) that lets Grok Bots read and post in Rob's self-hosted Mattermost, each bot using its own Mattermost bot token.
 
 ## Active slice
-[SLICE-20261027-lb5-wireup-reconnect-acceptance](thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md) (in-progress: eng-run implement on Merkle). Previous: lb4b [done](thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md)
+[SLICE-20261027-lb5-wireup-reconnect-acceptance](thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md) (review: implemented b5926c6, all Phase 5 automated checks exit 0 incl. container live suite). Previous: lb4b [done](thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md)
 
 ## Next action
-lb4b done (CP-S 2026-10-28; live Mattermost->receiver e2e and wake posts deferred until lb5 wires listener/dispatcher into main). lb5 implement running (eng-run, claude-code); then Codex review + planner eng-verify, then CP-S lb5 (live e2e demo). Deploy prerequisites before enabling: Coolify volume /data (uid 10001), env MMB_STORE_KEY, replicas 1.
+lb4b done (CP-S 2026-10-28; live Mattermost->receiver e2e and wake posts deferred until lb5 wires listener/dispatcher into main). lb5 implemented (b5926c6, status review). Next: advisory Codex slice review (codex CLI missing on the implementer shell; run `eng-run code-review` where available), planner eng-verify (incl. PR-11 eng-spec trace), OWNER-GUIDE pointer, then CP-S lb5 (live e2e demo, Mattermost restart mid-demo). Deploy prerequisites before enabling: Coolify volume /data (uid 10001), env MMB_STORE_KEY, replicas 1.
 
 ## Blockers
 - none
@@ -63,7 +63,7 @@ none
 - Architecture: [docs/architecture/2026-10-25-mmbridge-mcp.md](docs/architecture/2026-10-25-mmbridge-mcp.md)
 - ADRs 0001-0010 (all accepted): [docs/decisions/](docs/decisions/)
 - Verification lb4b (PASS): [thoughts/shared/verification/2026-10-27-lb4b-drop-allowlist.md](thoughts/shared/verification/2026-10-27-lb4b-drop-allowlist.md)
-- Latest handoff: [thoughts/shared/handoffs/2026-10-27_22-25-35_lb4b-implemented-awaiting-verify.md](thoughts/shared/handoffs/2026-10-27_22-25-35_lb4b-implemented-awaiting-verify.md)
+- Latest handoff: [thoughts/shared/handoffs/2026-10-28_12-50-17_lb5-implemented-awaiting-review.md](thoughts/shared/handoffs/2026-10-28_12-50-17_lb5-implemented-awaiting-review.md)
 - Review lb4b (addressed, no findings): [thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review.md](thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review.md)
 - Review lb3 (addressed, no findings): [thoughts/shared/verification/2026-10-27-slice-20261027-lb3-listener-filters-review.md](thoughts/shared/verification/2026-10-27-slice-20261027-lb3-listener-filters-review.md)
 - Changelog: [CHANGELOG.md](CHANGELOG.md)
diff --git a/README.md b/README.md
index 47a36d3..0087c18 100644
--- a/README.md
+++ b/README.md
@@ -53,6 +53,27 @@ own Mattermost bot token per call.
 ## Process
 This repo uses the eng-process kit; start at [PROJECT_STATE.md](PROJECT_STATE.md).
 
+## Live bots (deploy)
+Off by default: with `LIVE_BOTS_ENABLED` unset the bridge is the MCP bridge only and `/health` says
+`"listener": "disabled"`. To turn it on (Coolify):
+1. Persistent volume mounted at `/data` (writable by uid 10001; the image's `/data` already is). Replicas stay 1.
+2. Env secret `MMB_STORE_KEY`: generate one with
"""Live wiring (slice lb5, plan Phase 5): lifespan gating on LIVE_BOTS_ENABLED + store + state, /health listener
and wake_failed_24h (PR-10), supervisor restarts (PR-4), startup delivery of pending wakes, coordinated store
reload (PR-2). The app runs its real lifespan; Mattermost is the fake on a free port, the receiver in-process."""
import asyncio
import contextlib
import json
import logging
import os
import time

import httpx
import pytest
from cryptography.fernet import Fernet

from conftest import call
from app import store
from app.listener import Listener
from app.live import ConfigHolder, LiveRuntime
from app.main import create_app
from app.state import State
from app.store import BotConfig
from app.wake import Dispatcher
from drivers.fake_mattermost import FakeMattermost
from drivers.wake_receiver import WakeReceiver

SECRET = "s" * 40
URL = "https://receiver.test/wake"


@pytest.fixture
def world():
    m = FakeMattermost(clock=time.time)
    m.add_user("eddie", bot=True)
    m.add_user("eddie2", bot=True)
    m.add_user("rob")
    town = m.add_channel("main", "town-square", ["eddie", "eddie2", "rob"])
    return m, town


@pytest.fixture
async def served(world):
    m, town = world
    async with m.serve() as base:
        yield m, town, base


@pytest.fixture
def key():
    return Fernet.generate_key().decode()


def tok(m, name):
    return m.user_by_name(name)["token"]


def save(tmp_path, key, token, secret=SECRET):
    store.save(str(tmp_path / "bots.enc"), key, BotConfig(token, URL, secret))


def runtime(tmp_path, key, base, rx=None, flag="true", **kw):
    env = {"MMB_STORE_KEY": key, "MMB_DATA_DIR": str(tmp_path)}
    if flag:
        env["LIVE_BOTS_ENABLED"] = flag
    http = httpx.AsyncClient(transport=(rx or WakeReceiver(SECRET)).transport())
    return LiveRuntime(env=env, base_url=base, http=http, restart_base_s=kw.pop("restart_base_s", 0.3),
                       reload_s=0.05, poll_s=0.02,
                       listener_kw=dict(backoff_s=0.05, max_backoff_s=0.2, ping_s=0.2), **kw)


@contextlib.asynccontextmanager
async def running(live, m):
    app = create_app(mm_transport=m.transport(), live=live)
    started, stop = asyncio.Event(), asyncio.Event()

    async def hold():
        async with app.router.lifespan_context(app):
            started.set()
            await stop.wait()
    task = asyncio.create_task(hold())
    await asyncio.wait_for(started.wait(), 5)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testserver") as c:
        try:
            yield c
        finally:
            stop.set()
            await task


async def health(c):
    r = await c.get("/health")
    assert r.status_code == 200
    return r.json()


async def until(pred, timeout=5.0):
    for _ in range(int(timeout / 0.02)):
        got = pred()
        if asyncio.iscoroutine(got):
            got = await got
        if got:
            return
        await asyncio.sleep(0.02)
    raise AssertionError("condition not met in %.1fs" % timeout)


async def listener_is(c, status):
    return await until(lambda: _status(c, status))


async def _status(c, status):
    return (await health(c))["listener"] == status


async def mcp_works(c, m):
    r = await call(c, token=tok(m, "eddie"))
    assert r.status_code == 200 and "town-square" in r.text


async def test_flag_off_reports_disabled_and_starts_nothing(served, tmp_path, key):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    async with running(runtime(tmp_path, key, base, flag=None), m) as c:
        assert await health(c) == {"ok": True, "listener": "disabled", "wake_failed_24h": 0}
        await mcp_works(c, m)
    assert not any(x[0] == "WS" for x in m.calls) and not (tmp_path / "state.db").exists()


async def test_bad_store_key_reports_off_and_mcp_still_works(served, tmp_path, key, caplog):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    wrong = Fernet.generate_key().decode()
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with running(runtime(tmp_path, wrong, base), m) as c:
            assert await health(c) == {"ok": True, "listener": "off", "wake_failed_24h": 0}
            await mcp_works(c, m)
    assert '"event": "store_unreadable"' in caplog.text and wrong not in caplog.text and key not in caplog.text
    assert not any(x[0] == "WS" for x in m.calls)


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory permissions")
async def test_readonly_data_dir_reports_off(served, tmp_path, key, caplog):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    tmp_path.chmod(0o500)
    try:
        with caplog.at_level(logging.INFO, logger="mmbridge"):
            async with running(runtime(tmp_path, key, base), m) as c:
                assert (await health(c))["listener"] == "off"
                await mcp_works(c, m)
    finally:
        tmp_path.chmod(0o700)
    assert '"event": "state_unwritable"' in caplog.text


async def test_health_connecting_before_hello_then_ok(served, tmp_path, key):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    m.ws_refuse = True
    async with running(runtime(tmp_path, key, base), m) as c:
        await listener_is(c, "connecting")
        m.ws_refuse = False
        await listener_is(c, "ok")
        h = await health(c)
    assert set(h) == {"ok", "listener", "wake_failed_24h"} and tok(m, "eddie") not in json.dumps(h)


async def test_wake_failed_24h_counts_failed_rows_of_the_last_24h_only(served, tmp_path, key):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    t = [time.time() - 2 * 86400]
    s = State(str(tmp_path / "state.db"), clock=lambda: t[0])
    for pid, at, mark in (("old", time.time() - 2 * 86400, "failed"), ("recent", time.time() - 3600, "failed"),
                          ("ok", time.time() - 60, "delivered")):
        t[0] = at
        s.enqueue(pid, town, {"bot": {"user_id": "u-eddie"} })
        s.claim_due(int(at))
        s.mark_failed(pid, "http_410") if mark == "failed" else s.mark_delivered(pid)
    s.close()
    async with running(runtime(tmp_path, key, base), m) as c:
        assert (await health(c))["wake_failed_24h"] == 1


def _crash_once(monkeypatch, cls):
    real, calls = cls.run, []

    async def flaky(self):
        calls.append(1)
        if len(calls) == 1:
            raise RuntimeError("boom")
        return await real(self)
    monkeypatch.setattr(cls, "run", flaky)
    return calls


async def test_crashed_listener_is_restarted_health_degraded_then_ok(served, tmp_path, key, monkeypatch, caplog):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    calls = _crash_once(monkeypatch, Listener)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with running(runtime(tmp_path, key, base, restart_base_s=0.5), m) as c:
            await listener_is(c, "degraded")
            await mcp_works(c, m)                      # MCP keeps serving while the listener restarts
            await listener_is(c, "ok")
    assert len(calls) == 2 and '"event": "task_crashed"' in caplog.text and '"task": "listener"' in caplog.text


async def test_crashed_dispatcher_is_restarted_and_delivers(served, tmp_path, key, monkeypatch):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    calls = _crash_once(monkeypatch, Dispatcher)
    rx = WakeReceiver(SECRET)
    async with running(runtime(tmp_path, key, base, rx=rx), m) as c:
        await listener_is(c, "degraded")
        await listener_is(c, "ok")
        p = m.add_post(town, "u-rob", "after the restart")
        await until(lambda: p["id"] in rx.accepted)
    assert len(calls) == 2


async def test_startup_delivers_pending_and_stale_in_flight_wakes_exactly_once(served, tmp_path, key):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    old = time.time() - 120
    s = State(str(tmp_path / "state.db"), instance_id="crashed-run", clock=lambda: old)
    payload = lambda pid: {"version": 1, "delivery_id": pid, "bot": {"user_id": "u-eddie"}, "post": {"id": pid} }
    s.enqueue("stale", town, payload("stale"))
    assert [w.post_id for w in s.claim_due(int(old))] == ["stale"]       # lease long expired
    s.enqueue("queued", town, payload("queued"))
    s.close()
    rx = WakeReceiver(SECRET)
    async with running(runtime(tmp_path, key, base, rx=rx), m) as c:
        await until(lambda: {"stale", "queued"} <= set(rx.accepted))
        await asyncio.sleep(0.3)
    assert [r["status"] for r in rx.attempts("stale")] == [204]
    assert [r["status"] for r in rx.attempts("queued")] == [204]


async def test_store_token_change_reconnects_listener_with_new_bearer(served, tmp_path, key, caplog):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    rx = WakeReceiver(SECRET)
    live = runtime(tmp_path, key, base, rx=rx)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with running(live, m) as c:
            await listener_is(c, "ok")
            save(tmp_path, key, tok(m, "eddie2"))
            await until(lambda: ("WS", "/api/v4/websocket", tok(m, "eddie2")) in m.calls)
            await until(lambda: live.listener.status == "ok" and live.listener.bot_user_id == "u-eddie2")
            p = m.add_post(town, "u-rob", "hello new bot")
            await until(lambda: p["id"] in rx.accepted)
    assert rx.accepted[p["id"]]["bot"]["username"] == "eddie2"
    assert '"event": "store_updated"' in caplog.text and '"token"' in caplog.text
    assert tok(m, "eddie2") not in caplog.text and tok(m, "eddie") not in caplog.text


async def test_wake_secret_rotation_applies_to_the_next_send(served, tmp_path, key):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    rx = WakeReceiver(SECRET)
    live = runtime(tmp_path, key, base, rx=rx)
    async with running(live, m) as c:
        await listener_is(c, "ok")
        new = "n" * 40
        save(tmp_path, key, tok(m, "eddie"), secret=new)
        await until(lambda: live.holder.get().wake_secret == new)
        rx.secret = new
        p = m.add_post(town, "u-rob", "signed with the new secret")
        await until(lambda: p["id"] in rx.accepted)
    assert [r["status"] for r in rx.attempts(p["id"])] == [204]


async def test_invalid_store_edit_keeps_old_config(served, tmp_path, key, caplog):
    m, town, base = served
    save(tmp_path, key, tok(m, "eddie"))
    rx = WakeReceiver(SECRET)
    live = runtime(tmp_path, key, base, rx=rx)
    with caplog.at_level(logging.INFO, logger="mmbridge"):
        async with running(live, m) as c:
            await listener_is(c, "ok")
            (tmp_path / "bots.enc").write_bytes(b"not a fernet token")
            await until(lambda: "store_reload_failed" in caplog.text)
            assert live.holder.get().token == tok(m, "eddie")
            p = m.add_post(town, "u-rob", "still served")
            await until(lambda: p["id"] in rx.accepted)


def test_config_holder_only_notifies_on_a_real_change(tmp_path, key):
    save(tmp_path, key, "t" * 26)
    path = str(tmp_path / "bots.enc")
    h = ConfigHolder(path, key, store.load(path, key))
    seen = []
    h.subscribe(lambda old, new: seen.append((old.token, new.token)))
    assert h.check() is False
    save(tmp_path, key, "t" * 26)                         # rewritten, same values: no notification
    assert h.check() is False and seen == []
    save(tmp_path, key, "u" * 26)
    assert h.check() is True and seen == [("t" * 26, "u" * 26)] and h.generation == 1
WARN  .eng/runners.toml: no on_complete hook configured ([hooks] empty or missing) - bots must stay attached to eng-run until exit; fire-and-forget needs a non-empty on_complete / <role>_on_complete (PROCESS.md section 10, LESSONS L-006)
WARN  PROJECT_STATE.md: ## Latest artifacts has 27 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 25 rows / 4448 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 123 artifact(s) checked

exec
/bin/bash -lc "nl -ba app/listener.py | sed -n '110,130p;160,205p'; nl -ba app/live.py | sed -n '90,106p'; .venv/bin/python - <<'PY'
from app.listener import Listener
from app.store import BotConfig
l=Listener(BotConfig('a','https://x','s'),None,None)
try: print(l._backoff(1025))
except Exception as e: print(type(e).__name__, str(e))
PY" in /mnt/d/rob/projects/mmbridge
 succeeded in 563ms:
   110	    def cfg(self):
   111	        return self._cfg()
   112	
   113	    def config_changed(self, old, new) -> None:
   114	        """ConfigHolder subscriber: a new token reconnects at once (no resume across tokens, fresh lookups)."""
   115	        if new.token == old.token:
   116	            return
   117	        mlog.register_secret(new.token)
   118	        self.connection_id = None
   119	        self._channels, self._teams, self._users = {}, {}, {}
   120	        self._wake.set()
   121	        if self._ws is not None:
   122	            asyncio.ensure_future(self._ws.close())
   123	
   124	    def _backoff(self, attempt: int) -> float:
   125	        d = min(self.max_backoff_s, self.backoff_s * 2 ** (max(attempt, 1) - 1))
   126	        return d * (0.5 + 0.5 * self.rand())
   127	
   128	    async def _pause(self, seconds: float) -> None:
   129	        """Sleep, cut short by a config change."""
   130	        self._wake.clear()
   160	        finally:
   161	            self.status = "off"
   162	            await asyncio.to_thread(self.state.release_owner, "listener_owner")
   163	
   164	    async def connect_once(self) -> bool:
   165	        """One connection; True if it reached hello (then dropped/idled). Raises Unauthorized / LeaseHeld."""
   166	        cfg = self.cfg
   167	        mlog.register_secret(cfg.token)
   168	        client = self.client_factory(cfg.token)
   169	        self.status = "connecting"
   170	        reached = False
   171	        try:
   172	            if not await asyncio.to_thread(self.state.claim_owner, self.clock(), LEASE_TTL_S, "listener_owner"):
   173	                self.status = "off"
   174	                raise LeaseHeld()
   175	            if self._alive_at is None:
   176	                v = await asyncio.to_thread(self.state.get_meta, "last_event_at")
   177	                self._alive_at = int(v) if v else None
   178	            try:
   179	                me = await client.get("/users/me")
   180	            except MMError as e:
   181	                if e.code == "unauthorized":
   182	                    raise Unauthorized() from None
   183	                raise
   184	            if me["id"] != self.bot_user_id:
   185	                self.connection_id, self.members, self._seen = None, {}, {}
   186	            self.bot_user_id, self._bot = me["id"], {"user_id": me["id"], "username": me["username"]}
   187	            await asyncio.to_thread(self.state.set_meta, "bot_user_id", me["id"])   # dispatcher: bot_rotated
   188	            await asyncio.to_thread(self.state.set_meta, "bot_identity",              # id + token as one row
   189	                                    token_fp(cfg.token) + ":" + me["id"])
   190	            url = ws_url(self.base_url)
   191	            self._resume_id = self.connection_id
   192	            if self.connection_id and self.last_seq is not None:
   193	                url += "?connection_id=%s&sequence_number=%d" % (self.connection_id, self.last_seq + 1)
   194	            try:
   195	                conn = self.ws_connect(url, {"Authorization": "Bearer " + cfg.token})
   196	                ws = await conn.__aenter__()
   197	            except InvalidStatus as e:
   198	                if e.response.status_code in (401, 403):
   199	                    raise Unauthorized() from None
   200	                raise
   201	            self._ws = ws
   202	            try:
   203	                pinger = asyncio.create_task(self._ping(ws))
   204	                try:
   205	                    reached = await self._read(ws, client)
    90	        started = time.monotonic()
    91	        try:
    92	            await factory()
    93	            err = "returned"
    94	        except asyncio.CancelledError:
    95	            raise
    96	        except Exception as e:                      # type only: messages may carry request details
    97	            err = type(e).__name__
    98	        attempt = 1 if time.monotonic() - started > max_s else attempt + 1
    99	        delay = min(max_s, base_s * 2 ** (attempt - 1))
   100	        crashed.add(name)
   101	        _log("task_crashed", "error", task=name, error=err, attempt=attempt, restart_in_s=delay)
   102	        try:
   103	            await asyncio.sleep(delay)
   104	        finally:
   105	            crashed.discard(name)
   106	
OverflowError int too large to convert to float

exec
/bin/bash -lc 'python3 .eng/bin/eng-check .' in /mnt/d/rob/projects/mmbridge
 succeeded in 1582ms:
WARN  .eng/runners.toml: no on_complete hook configured ([hooks] empty or missing) - bots must stay attached to eng-run until exit; fire-and-forget needs a non-empty on_complete / <role>_on_complete (PROCESS.md section 10, LESSONS L-006)
WARN  PROJECT_STATE.md: ## Latest artifacts has 27 in-play links (> 12) - keep only the current increment + standing links; move older ones under ## Prior increments (PROCESS.md section 8)
WARN  PROJECT_STATE.md: ## Approval log is 25 rows / 4448 bytes (> 40 rows or > 3072 bytes) - reopen the Approval-log archive design (CHANGELOG 2.5.8); no archive exists yet
eng-check: OK - 0 error(s), 3 warning(s), 123 artifact(s) checked

2026-10-28T18:15:44.356601Z ERROR codex_core::session: failed to record rollout items: thread 01a183b8-39a2-78e1-8263-5dc8442be6d1 not found
codex
Token rotation can strand a connection on stale credentials, and sustained failures can terminate the recovery supervisor. Both undermine the runtime's promised automatic recovery.

Full review comments:

- [P2] Detect token changes during connection establishment — /mnt/d/rob/projects/mmbridge/app/listener.py:195-201
  If the store reloads while `connect_once()` is awaiting REST or the websocket handshake, `config_changed()` sees `_ws is None` and cannot close the connection. The handshake then completes using the captured old token, and the healthy socket can remain connected indefinitely. Meanwhile, the dispatcher reads the new configuration and refuses delivery because `bot_identity` still matches the old token. Recheck the current token after establishing the socket and reconnect if it changed.

- [P2] Bound the exponent before computing restart delays — /mnt/d/rob/projects/mmbridge/app/live.py:98-99
  When a task repeatedly crashes quickly, approximately 1,025 failures cause `base_s * 2 ** (attempt - 1)` to raise `OverflowError` before `min()` can cap the delay. The supervisor then exits permanently, stopping listener recovery or wake delivery even after the underlying fault clears. Cap the exponent or attempt counter before exponentiation; the listener's `_backoff()` uses the same unsafe calculation.
Token rotation can strand a connection on stale credentials, and sustained failures can terminate the recovery supervisor. Both undermine the runtime's promised automatic recovery.

Full review comments:

- [P2] Detect token changes during connection establishment — /mnt/d/rob/projects/mmbridge/app/listener.py:195-201
  If the store reloads while `connect_once()` is awaiting REST or the websocket handshake, `config_changed()` sees `_ws is None` and cannot close the connection. The handshake then completes using the captured old token, and the healthy socket can remain connected indefinitely. Meanwhile, the dispatcher reads the new configuration and refuses delivery because `bot_identity` still matches the old token. Recheck the current token after establishing the socket and reconnect if it changed.

- [P2] Bound the exponent before computing restart delays — /mnt/d/rob/projects/mmbridge/app/live.py:98-99
  When a task repeatedly crashes quickly, approximately 1,025 failures cause `base_s * 2 ** (attempt - 1)` to raise `OverflowError` before `min()` can cap the delay. The supervisor then exits permanently, stopping listener recovery or wake delivery even after the underlying fault clears. Cap the exponent or attempt counter before exponentiation; the listener's `_backoff()` uses the same unsafe calculation.
````
