---
id: VERIFY-20261029-b-s1-relay-grok-wake-one-bot
type: verification
phase: verify
status: pass             # draft | pass | fail
owner_agent: grok-bot
date: 2026-10-29
links: [thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md, thoughts/shared/verification/2026-10-29-slice-20261028-b-s1-relay-grok-wake-one-bot-review-2.md]
plan: thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md
git_commit: abf873a
---
# Verification: B-s1 wake relay + Grok Bot wake for one bot (plan Phase 1)

Verifier: grok-bot (planner). The implementer was claude-code (cd07811, abf873a). grok-bot wrote no code in this slice. eng-run was not run with `--allow-self-review`.

## Implementation status
- [x] Phase 1: relay + Grok wake for one bot: complete (cd07811). There were no review fixes.

## Automated verification (re-executed at abf873a, 2026-10-29 on Merkle WSL)
I extracted the plan Phase 1 block verbatim from the plan and ran it: `docker build` of both `:bs1` images, then `run_all` 3x, then eng-check and eng-spec status.

| Command | Exit | Run 1 | Run 2 | Run 3 |
|---|---|---|---|---|
| `docker build -t mmbridge:bs1 . && docker build -t mmbridge-relay:bs1 relay` | 0 | | | |
| `.venv/bin/pytest tests/unit -q` | 0 | 322 passed | 322 passed | 322 passed |
| `.venv/bin/pytest tests/acceptance -q --channel mcp` | 0 | 16 passed, 36 skipped | same | same |
| `LIVE_MODE=inprocess ... --channel live test_live_bots.py $B1` | 0 | 26 passed (64.5s) | 26 passed | 26 passed |
| `LIVE_MODE=container ... --channel live test_live_bots.py $B1` | 0 | 26 passed (153.1s) | 26 passed | 26 passed |
| `python3 .eng/bin/eng-check .` | 0 | OK, 0 errors, 3 old warnings | | |
| `python3 .eng/bin/eng-spec status .` | 0 | lock approval ok (2026-10-29); specs and DSL interface match the lock | | |
| `.venv/bin/pytest tests -q` (DoD collection) | 0 | 338 passed, 36 skipped (= unit 322 + mcp 16 + 36 channel skips; nothing silently left out) | | |

`git diff bc73656 HEAD -- app tests/acceptance/specs tests/acceptance/dsl.py` is empty: no runtime change, no locked spec change, no DSL change.

## Executable specs
| REQ | specs | result |
|---|---|---|
| REQ-B1..B4 | the 11 `$B1` specs in tests/acceptance/specs/test_grok_multibot.py | pass (live, inprocess + container, 3x) |
| REQ-A1..A4, A7, A8 | tests/acceptance/specs/test_live_bots.py | pass (live, inprocess + container, 3x) |
| REQ-1..8 | tests/acceptance/specs/test_mmbridge.py | pass (mcp, 3x) |
| REQ-B5..B8 | later slices (B-s2/B-s3) | not selected by design (plan review #3) |

`eng-spec trace .` again prints "(not in an approved design)" for REQ-A*/B*. This is the known tooling issue filed in TODOS (P3), not a spec gap.

## Diff review (bc73656...abf873a, ~1570 lines)
- The diff matches plan Phase 1. relay/relay.py has `load_bots` fail-fast, `verify` (`hmac.compare_digest`, a copy of app.wake.verify with a drift-guard unit test), byte-for-byte forward with Bearer, `map_upstream`, `Seen` recorded only after upstream 2xx, an in-flight guard, a per-bot `RateLimit`, a logger-level redact filter, and `/health` with counts only.
- Accepted risk A (double wake on an ambiguous outcome) is characterised by tests and logged as `relay_delivery_ambiguous`. It is not hidden.
- Deviations, all recorded in the slice and accepted here:
  1. **Container-mode stale replay:** `replay_last_wake(600)` is rejected as a *duplicate*, not as *stale*, because the relay image has no clock hook. The stale path is covered in-process and by the unit test `test_bad_wakes_401_and_upstream_not_called[stale]`. Accepted: the user-visible outcome (no second run) holds in both modes.
  2. **Harness timing:** `WAKE_BACKOFF_SCALE` 0.05 -> 0.25 in drivers/live.py, so a failing wake now takes ~7.5s to fail instead of ~1.5s. This is a test-harness *timeout lengthening* so the relay container can restart. Assertions are not weakened, and production backoff is unchanged. Named here per DoD.
  3. The routine setup text is in relay/README.md, not OWNER-GUIDE.md, because Rob's OWNER-GUIDE edits are uncommitted. This is the plan's own fallback. It is tracked in TODOS.
  4. Relay extras: in-flight rows are cleared at start (single replica), taken over after 60s, and a delivery held elsewhere gets 503 `in_flight`. The RateLimit is monotonic.
- Weakened tests or suppressions: none, apart from the harness backoff lengthening named above. No skips were added.
- No sleeps on threads in the tests: the rate limit and prune tests use a fake clock.

## Cross-model review (advisory)
- Reviewer: codex (gpt-6.1-sol, `codex review`, Codex CLI 0.166.0), run by grok-bot. The implementer was claude-code, so this is not a self-review.
- Run 1: `python3 .eng/bin/eng-run code-review SLICE-20261028-b-s1-relay-grok-wake-one-bot` (no `--base`). This reviewed only Rob's uncommitted working-tree docs, not the slice. **Invalid, superseded.** File: `...-review.md`.
- Run 2 (counts): `python3 .eng/bin/eng-run code-review SLICE-20261028-b-s1-relay-grok-wake-one-bot --base bc73656`. Codex read the relay, tests and harness, and re-ran `pytest tests/unit/test_relay.py` (55 passed) and eng-check. Result: **0 findings** (P1 0, P2 0, P3 0). Because of the known parser bug (TODOS P1), I checked the raw run log by hand: there are no `[P#]` tags. Codex's own caveat: it did not verify the live Coolify/Grok path (that is CP-S).
- Unresolved high findings: none.

## DoD
| Item | Result |
|---|---|
| Plan success criteria: automated | pass (re-run above) |
| Plan success criteria: manual (Rob) | pending at CP-S (spike, Coolify deploy, captured-wake replay) |
| New behavior has tests | pass (55 relay unit tests, 11 B-s1 specs) |
| Nothing weakened without approval | pass. One harness backoff lengthening is named above (assertions unchanged); flagged for Rob at CP-S |
| Build / tests pass | pass. No lint step exists (TODOS P3 ruff) |
| Executable specs | pass for the B-s1 selection; lock clean |
| Error paths, no silent failures | pass (401/404/424/429/503 mapping, failed wake visible, ambiguous outcome logged) |
| Docs updated | pass with deviation: README, relay/README.md and the Coolify snippet are updated; OWNER-GUIDE is deferred (Rob's uncommitted edits, TODOS) |
| CHANGELOG Unreleased | pass |
| ADRs / TODOS | pass. The ADR-0011 "Observed" note is pending the spike run |
| Verification report PASS | this file |
| PROJECT_STATE + handoff | done in this session |
| `pytest tests` collection | pass (338 + 36 skipped) |
| Injected clock for time/rate tests | pass |
| Suite 3x (concurrency) | pass (3/3) |
| Before -> After line for CP-S | Before: a Mattermost post wakes Eddie's signed HMAC receiver. After: a post in Town Square or a DM to eddie starts the Eddie Grok Bot routine once, via the relay |
| Live path runnable at CP-S | yes once Rob deploys the relay (steps below) |

## Verdict
**PASS** (automated + review). The manual items move to CP-S for Rob. There is no unresolved high finding.

## Manual verification for CP-S (L-009 filtered)
Runnable now:
1. Spike. `ready:` relay/spike_routine.py is in the repo and needs only Rob's routine URL + key. Command: `python3 relay/spike_routine.py https://<eddie-routine-url>` (paste the key at the prompt). Record the 3 status codes (valid key / wrong key / bad URL) and whether Eddie saw the JSON marker verbatim.
2. Coolify relay deploy. `ready:` the Dockerfile builds (verified), and the snippet and runbook are in relay/README.md "Setup on Coolify" steps 1-5. Steps: new app (build context `relay`, port 8080, volume `/data`, own domain); set the `RELAY_BOT_EDDIE_HMAC_SECRET|ROUTINE_URL|ROUTINE_KEY` secrets; deploy; `curl https://<relay>/health` should show `"ok": true, "bots": 1`; in the mmbridge container terminal run `python -m app.admin set-bot --token-stdin --wake-secret-stdin --wake-url https://<relay>/wake/eddie`; post in Town Square and DM eddie, and the Eddie routine should run each time; `curl -X POST https://<relay>/wake/eddie -d '{}'` should return 401 with no run.
3. Re-POST a captured signed wake within 5 min. Expect `duplicate` and no new run. `ready:` after step 2. Capturing needs the signed request headers (`X-MMB-*`). This is optional for Rob; Ulrik can do it.

Blocked / deferred:
- Reply in channel/thread/DM. `blocked: needs root_id + reply hints → unblocks in B-s2`.
- Multiple bots. `blocked: registry → unblocks in B-s3`.
