---
id: VERIFY-20261028-lb5-wireup-reconnect-acceptance
type: verification
phase: verify
status: pass             # draft | pass | fail
owner_agent: grok-bot
date: 2026-10-28
links: [thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md, thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-6.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
git_commit: 8f987e7
---
# Verification: lb5 wire-up, reconnect, acceptance (plan Phase 5)

Verifier: grok-bot (planner). **Note:** grok-bot also wrote the review fix commits 54ae627, 0a50e87, 9bdff90, 8f987e7 (b5926c6 is claude-code's). The independent check on those commits is the Codex slice review (rounds 2-6, all on `--base 3ed94b4`, review 6 clean). eng-run was never run with `--allow-self-review`.

## Implementation status
- [x] Phase 5: Wire-up + LIVE_BOTS_ENABLED + reconnect: complete (b5926c6 + review fixes 54ae627, 0a50e87, 9bdff90, 8f987e7)

## Automated verification (re-executed at 8f987e7, 2026-10-28 on Merkle WSL)
| Command | Exit | Notes |
|---|---|---|
| `.venv/bin/pytest tests/unit -q` | 0 | 267 passed |
| `.venv/bin/pytest tests/acceptance -q` | 0 | 16 passed, 15 skipped (live specs skip on the default channel by design) |
| `docker build -t mmbridge:lb5 .` | 0 | |
| `.venv/bin/pytest tests/acceptance --channel live -q` (container mode) | 0 | 15 passed, 16 skipped (MCP specs on the live channel) |
| `LIVE_MODE=inprocess .venv/bin/pytest tests/acceptance --channel live -q` | 0 | 15 passed, 16 skipped |
| `.venv/bin/pytest tests -q` | 0 | 283 passed, 15 skipped; `--collect-only` 298 = 283+15, so no tests silently left out |
| `python3 .eng/bin/eng-spec status .` | 0 | lock approval ok (2026-10-27); specs and DSL interface match the lock |
| `python3 .eng/bin/eng-check .` | 0 | OK, 3 old warnings (no on_complete hook, Latest artifacts count, Approval log size) |
| Red/green for each fix | n/a | Each new regression test failed before its fix and passed after (logged in the slice progress log) |

## Executable specs
| REQ | design doc | specs | result |
|---|---|---|---|
| REQ-A1 | docs/design/2026-10-26-live-bots.md (approved, amended 2026-10-27) | tests/acceptance/specs/test_live_bots.py | pass (live, container + inprocess) |
| REQ-A2 | same | tests/acceptance/specs/test_live_bots.py | pass |
| REQ-A3 | same | tests/acceptance/specs/test_live_bots.py | pass |
| REQ-A4 | same | tests/acceptance/specs/test_live_bots.py | pass (both drop specs) |
| REQ-A7 | same | tests/acceptance/specs/test_live_bots.py | pass (token scan over container logs) |
| REQ-A8 | same | tests/acceptance/specs/test_live_bots.py | pass |
| REQ-1..8, REQ-7 (v1) | docs/design/2026-10-25-mmbridge-mcp.md | tests/acceptance/specs/test_mmbridge.py | pass (default channel, 16) |

`eng-spec trace .` prints "(not in an approved design)" for REQ-A1..A8. The REQs are in the approved design `docs/design/2026-10-26-live-bots.md` (lines 36-41). The trace tool just doesn't pick up the amended doc's approval, so this is a tooling issue, not a gap in the specs. It is the same note lb5's implementer recorded and is filed in TODOS. Spec lock: clean. Locked specs and the DSL interface are unchanged since 3ed94b4.

## Code review findings (diff 3ed94b4...8f987e7)
- Matches plan Phase 5. Deviations are recorded in the slice: the new app/live.py; deploy docs in README instead of OWNER-GUIDE; container mode overrides only the port; catch-up re-offers posts with equal create_at and the ledger dedupes them; the hello-without-seq fake drift, to check at CP-S.
- **Teamless-bot DM limit is now closed** (9bdff90, `GET /users/{id}/channels`).
- Catch-up now pages by post id with `before`, because Mattermost ignores paging when `since` is set and caps the result. When it hits MAX_PAGES it logs `catchup_truncated`, which is not silent.
- Seq and alive state now advance only after the commit.
- Recovery stays pending until catch-up completes.
- A token rotated mid-connect forces a reconnect.
- Backoff and restart exponents are capped.
- Weakened tests, timeouts, skips, or suppressions: none. One new `skipif(geteuid()==0)` is on a unit test for a directory-permission error path, because root ignores permissions. It is legitimate, not a weakening. The fake gained Mattermost-faithful `since` capping, `before`/`after` anchors, the `/users/{id}/channels` route and multiple access tokens per user. These make it stricter, not looser.
- Security: the token never appears in container logs (REQ-A7 spec); `/health` exposes no secrets.

## Cross-model review (advisory)
- Reviewer: codex (gpt-6.1-sol, `codex review`), via `python3 .eng/bin/eng-run code-review SLICE-20261027-lb5-wireup-reconnect-acceptance --base 3ed94b4`.
- **Kit bug:** eng-run's parser wrote "No findings." for every round even when Codex reported [P1]/[P2]. I read the raw output by hand each round and added the rows.

| Round | Diff | Findings | Resolution |
|---|---|---|---|
| review (1) | main...b7c2ae9 | none (base was local main, so the diff was empty) | superseded by rounds 2-6 |
| review-2 | 3ed94b4...b7c2ae9 | 1 P1, 2 P2 | all fixed in 54ae627 |
| review-3 | 3ed94b4...54ae627 | 1 P2 | fixed in 0a50e87 |
| review-4 | 3ed94b4...0a50e87 | 1 P2 | fixed in 9bdff90 |
| review-5 | 3ed94b4...9bdff90 | 2 P2 | fixed in 8f987e7 |
| review-6 | 3ed94b4...8f987e7 | **none** (its raw log quotes review-5's findings only because it read that file) | clean |

- Findings file: thoughts/shared/verification/2026-10-28-slice-20261027-lb5-wireup-reconnect-acceptance-review-6.md. No unresolved high findings.

## Manual verification required (for Rob), CP-S
See the CP-S Action for Rob in PROJECT_STATE / handoff. The steps are runnable after main (8f987e7+docs) is deployed.

## Definition of Done
- Plan success criteria: automated **pass**. Manual (Coolify demo, Mattermost restart mid-demo): pending Rob at CP-S.
- Tests for new behaviour / regression tests that failed first: **pass**
- Nothing weakened: **pass**
- Build + full suite: **pass**. Lint: n.a. (no linter; TODOS P3)
- Executable specs: **pass** (trace label caveat above)
- Error paths, no silent failures: **pass** (`catchup_truncated`, `direct_channels_unavailable`, `token_changed_during_connect`, `store_reload_failed` are logged)
- Docs: **pass with deferral**. README deploy section and CHANGELOG are done. The OWNER-GUIDE pointer is deferred because OWNER-GUIDE.md has Rob's uncommitted edits and must not be touched now (TODOS).
- CHANGELOG Unreleased: **pass**
- ADRs/deferrals: **pass** (TODOS updated)
- Verification report: this file, PASS
- PROJECT_STATE + handoff: **pass** (this session)
- `pytest tests` collection count matches: **pass** (298)
- Injected clock: **pass** for the new review-fix tests (no wall-clock waits added; they use the fake's clock / polling helpers). Pre-existing lb5 tests not re-audited for this item.

## Verdict
**PASS** (automated). CP-S manual demo is pending with Rob. Follow-ups are in TODOS: an OWNER-GUIDE pointer to the README live-bots deploy section, the eng-run findings-parser bug, and the eng-spec trace approved-amendment label.
