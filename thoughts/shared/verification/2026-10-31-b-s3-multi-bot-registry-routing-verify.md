---
id: VERIFY-20261031-b-s3-multi-bot-registry-routing
type: verification
phase: verify
status: pass
owner_agent: grok-bot
date: 2026-10-31
links: [thoughts/shared/slices/2026-10-28-b-s3-multi-bot-registry-routing.md, thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, thoughts/shared/verification/2026-10-31-slice-20261028-b-s3-multi-bot-registry-routing-review.md, thoughts/shared/handoffs/2026-10-31_01-41-16_b-s3-implemented-awaiting-verify.md]
verdict: PASS
---
# Verification: B-s3 multi-bot registry and routing

Verifier: grok-bot (planner; implementer was claude-code). Base `e2f6091` (B-s2 CP-S), tip under test `48d049e` (code: cfe29e2 + aa7ce74; 48d049e is docs only). Machine: Merkle, WSL, `:bs3` images rebuilt by the block.

## Re-executed evidence
Command: plan Phase 3 Automated Verification block, lines 203-216 of the plan, copied verbatim into `/tmp/bs3v/block.sh` and run with `bash /tmp/bs3v/block.sh` (includes `docker build -t mmbridge:bs3 .`, `docker build -t mmbridge-relay:bs3 relay`, explicit `LIVE_IMAGE`/`RELAY_IMAGE`, 3x `run_all`, then eng-check / eng-spec status / eng-spec trace). Process exit code **0**, no `RUN n FAILED` line. Total ~30 min (2026-10-31, about 12:00-12:30 CT).

| Run | unit | acceptance --channel mcp | live inprocess | live container |
|---|---|---|---|---|
| 1 | 459 passed (exit 0) | 16 passed, 36 skipped (exit 0) | 36 passed, 16 skipped, 97.7 s (exit 0) | 36 passed, 16 skipped, 440.4 s (exit 0) |
| 2 | 459 passed (exit 0) | 16 passed, 36 skipped (exit 0) | 36 passed, 16 skipped, 98.0 s (exit 0) | 36 passed, 16 skipped, 439.2 s (exit 0) |
| 3 | 459 passed (exit 0) | 16 passed, 36 skipped (exit 0) | 36 passed, 16 skipped, 96.9 s (exit 0) | 36 passed, 16 skipped, 438.4 s (exit 0) |

Skips are channel selection only (36 live specs skipped on the mcp channel, 16 mcp specs skipped on the live channel; 16 + 36 = 52 specs, all run on their channel). Matches the implementer's handoff counts exactly. DoD concurrency rule (full suite 3x) met.

- `.eng/bin/eng-check .` (session start and inside the block): OK, 0 errors, 3 pre-existing warnings (runners.toml on_complete hook; Latest artifacts > 12 links; Approval log size).
- `eng-spec status .`: `lock approval: ok (2026-10-29)`; `specs and DSL interface match the lock`.

## Diff review (e2f6091...HEAD, 35 files, +8801/-498 incl. ~6.5k lines of review/run logs)
- Matches plan Phase 3 Changes Required item by item: store v2 + v1 migration + `.v1.bak` + rotate (app/store.py), admin multi-bot commands (app/admin.py), state schema v2 + one-transaction migration + `live_migration_failed` (app/state.py), `decide(..., registered_ids)` (app/live_filter.py), `BotSupervisor` reconcile + per-bot status (app/live.py), shared dispatcher with per-bot cap 2 / `delivery_id <bot>:<post_id>` / `bot_removed` (app/wake.py), /health `bots_total` / `bots_failing` (app/live.py + app/main.py), harness drivers, docs, CHANGELOG Unreleased. Plus the owner-requested `bin/set-bot` wrapper (app/setbot.py, bin/set-bot, Dockerfile, .gitattributes).
- **Locked specs / DSL untouched:** `git diff --stat e2f6091...HEAD -- tests/acceptance/specs tests/acceptance/dsl.py` is empty. Only drivers changed.
- Deviations (all listed in the slice Blockers, accepted by planner below): diff size well over the 100-200 line guideline; per-bot cap 2 also applies to a lone bot; dispatcher sends run as background tasks; v1 bot named after its MM username at first boot, `bot` permanently if MM unreachable; `bots_failing` also counts a bot whose last wake failed for good; `admin status` reads a 10 s meta heartbeat; per-bot `store_updated` log fields; set-bot refuses to overwrite an undecryptable store (safer); OWNER-GUIDE not edited (Rob's uncommitted edits; text in README "Several bots" + relay/README).
- **Test changes named (weakening check):** `test_concurrency_4` renamed `test_concurrency_4_total_2_per_bot` and asserts per-bot <= 2 (stricter, follows the plan's cap); `test_two_dispatchers` loop 4 -> 6 ticks (assertions unchanged); all other unit edits are the `wake(post)` -> `wake(BOT, post)` API change with the same assertions. No skip, xfail, timeout raise, noqa or suppression added.
- **Sleep-based waits (DoD item, flagged):** new tests add short `asyncio.sleep` calls: in tests/unit/test_main_live.py three 0.1-0.2 s grace sleeps before *negative* assertions (after a polled barrier), and in tests/unit/test_wake.py `test_dead_target_of_one_bot_never_blocks_the_other` a polling loop with a 100x0.01 s deadline (allowed form) followed by `asyncio.sleep(0.05)` before a positive assertion (timing wait). Same pattern already exists at base (16 sleeps across 5 unit files) and is tracked in TODOS P2 "Flaky timing-race unit tests"; 3/3 runs passed. Not treated as FAIL; folded into that TODO (see Follow-ups). Planner call, named here so Rob can overrule.
- Security: tokens/secrets registered for redaction for all bots (spec `test_no_token_secret_or_routine_key_in_logs_output_or_wakes` green on both live modes); backups 0600; store edits serialized by a shared lock (Codex P2 fix); set-bot never echoes the token.

## Executable specs
`python3 .eng/bin/eng-spec trace .` (from the block run):

| REQ | design doc | specs | result |
|---|---|---|---|
| REQ-1..REQ-8 | docs/design/2026-10-25-mmbridge-mcp.md | tests/acceptance/specs/test_mmbridge.py | pass (mcp channel, 16 passed x3) |
| REQ-7 | docs/design/2026-10-26-live-bots.md | tests/acceptance/specs/test_mmbridge.py | pass |
| REQ-A1, A2, A3, A4, A7, A8 | (tool label: "not in an approved design") | tests/acceptance/specs/test_live_bots.py | pass (live inprocess + container x3) |
| REQ-B1..REQ-B8 | (tool label: "not in an approved design") | tests/acceptance/specs/test_grok_multibot.py | pass (live inprocess + container x3) |

The "(not in an approved design)" label is the known eng-spec quirk: PROJECT_STATE Approval log has CP-A approved for docs/design/2026-10-26-live-bots.md (2026-10-26) and docs/design/2026-10-28-grok-webhook-multibot.md (2026-10-28, REQ-B1..B8). Every REQ-B1..B8 maps to >= 1 spec and all pass. REQ-A5/A5b/A5c/A6 were scoped out (A REDUCE), A6 delivered as B3/B8. `eng-spec status`: clean (above). Logged as process feedback, not a FAIL.

## Cross-model review
- Reviewer: Codex (v0.166.0), command `codex review --base e2f6091` via `eng-run code-review` (run by the implementer's runner, reviewer is not the implementer; no `--allow-self-review`). File: thoughts/shared/verification/2026-10-31-slice-20261028-b-s3-multi-bot-registry-routing-review.md, status `addressed`.
- Counts: 0 P0/P1 (high), 1 P2, 0 P3.
- P2 #1 (boot v1 store migration could overwrite a concurrent set-bot): **fixed** in aa7ce74 (`store.locked` shared by admin and runtime, re-read under lock, keep an existing v2 file; regression test `test_boot_migration_never_overwrites_a_concurrent_set_bot`, in the 459 passing). Confirmed by diff read.
- eng-run findings parser again wrote "No findings." while raw output had the P2; table filled by hand (logged in process-feedback.md). No unresolved high finding.

## Definition of Done
| Item | Result |
|---|---|
| Plan success criteria: automated re-run exit 0 | pass (3x, above) |
| Plan success criteria: manual (Rob) | pending at CP-S (that is this checkpoint) |
| New behavior has tests; bug fix has regression test | pass (unit + 7 `$B3` specs red first; P2 regression test) |
| No weakened/skipped/suppressed checks | pass (renamed/adjusted tests named above, assertions unchanged or stricter) |
| Build, lint/typecheck, full suite | pass (both images build; full unit + acceptance all channels; project has no separate lint step) |
| Executable specs: trace, all channels, lock clean | pass |
| Error paths handled, no silent failures | pass (`live_migration_failed` -> live off + MCP up, `bot_removed`, `wake_send_crashed`, per-bot degraded status) |
| Docs updated | pass (README "Several bots", relay/README, coolify snippet); OWNER-GUIDE deferred (Rob's uncommitted edits, TODOS P2) |
| CHANGELOG Unreleased | pass |
| ADRs / TODOS | pass (ADR-0013/0014 cover the store/state design; follow-ups in TODOS) |
| Verification report PASS | pass (this file) |
| PROJECT_STATE + handoff | pass (this session) |
| `pytest tests` zero silent collection skips | pass (skips are channel selection; counts add to 52) |
| Injected/frozen clocks | pass (dispatcher tests use `clk`) |
| No sleep-based waits; full suite 3x for concurrency | pass with flag (3x done; residual short sleeps follow existing pattern, tracked TODOS P2) |
| CP-S ask has Before -> After | pass (in handoff / PROJECT_STATE) |
| Live path thin demo runnable at CP-S | pass (runnable-now steps only) |

## Planner decisions (slice Blockers)
1. `bots_failing` also counts a bot whose most recent wake failed for good (clears on its next delivered wake): **confirmed** (operator sees a dead routine, not just a dead socket; matches B8).
2. v1 bot named after its MM username at first boot, `bot` permanently if MM unreachable then: **confirmed** (plan fallback); low risk on Coolify since MM is up; rename = `remove-bot` + `set-bot --name`. Noted for CP-S: check the name `admin list` shows is `eddie`.
3. Per-bot in-flight cap 2 applies to a lone bot too: **confirmed** (fairness rule is simple and per row; wakes are small; total stays 4).

## Verdict
**PASS.** All automated criteria re-executed and green 3x; specs/DSL lock clean; Codex P2 fixed, no unresolved high finding. Manual verification goes to Rob at CP-S.

## Follow-ups (TODOS.md)
- Flaky timing-race unit tests (P2, existing): add the B-s3 grace sleeps in tests/unit/test_main_live.py and tests/unit/test_wake.py (`asyncio.sleep(0.05)` before a positive assertion) to the deterministic-rewrite list.
- OWNER-GUIDE multi-bot pointer (P2, existing).
