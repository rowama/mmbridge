---
id: VERIF-20261027-lb3-listener-filters
type: verification
phase: verify
status: pass
owner_agent: eddie
date: 2026-10-27
links: [thoughts/shared/slices/2026-10-27-lb3-listener-filters.md, thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
git_commit: 0022a89
---
# Verification: SLICE-20261027-lb3-listener-filters

## Implementation status
- [x] Phase 3: Listener + filters (fake MM websocket) - complete (slice status review; commits 8174ba2, c170d0d, 0022a89)

## Automated verification (re-executed in this session on Merkle WSL; paste exit codes)
| Command | Exit | Notes |
|---|---|---|
| .venv/bin/pytest tests/unit -q (x3) | 0 | 176 passed, 14 warnings each run (~11.5s); stable |
| .venv/bin/pytest tests/unit/test_listener.py tests/unit/test_live_filter.py -q | 0 | 38 passed (real localhost websocket via fake MM; Codex sandbox could not run these) |
| .venv/bin/pytest tests/acceptance -q | 0 | 16 passed, 9 skipped (live specs, lb5) |
| python3 .eng/bin/eng-check . | 0 | 0 errors, 0 warnings, 83 artifacts |
| python3 .eng/bin/eng-spec status . | 0 | lock approval ok; specs and DSL interface match the lock |

## Executable specs (v2.5)
| REQ | design doc | specs | result |
|---|---|---|---|
| live-bot REQs (per card) | docs/design/2026-10-26-live-bots.md | tests/acceptance/specs/test_live_bots.py | n/a this slice - listener not wired; e2e green in lb5 |

Spec lock: clean (speclock sha256:3108f1fe6a93cfae). No locked spec or DSL step edited.

## Code review findings
Diff 8bd8d68...0022a89: app/live_filter.py (decide), app/listener.py (ws -> state.enqueue_and_advance, seq gaps, 30s ping / 60s idle, lookup cache), app/ws_spike.py, fake_mattermost websocket driver, websockets==17.3 pin, 38 new unit tests.
- Token redaction: websockets client gets dedicated logger `mmbridge.ws` with RedactFilter (app/listener.py:26-40); parametrized test at DEBUG (test_listener.py:125-128) asserts no token. Pass.
- Wake payload carries no token; malformed events logged as event_invalid without message text.
- Skips/timeouts: no new pytest skip/xfail. Test helper `until(pred, timeout=5.0)` and short asyncio.sleep polls are bounded waits, not weakened assertions; one `asyncio.sleep(1.0)` in a seq-gap test. Acceptable.
- Deviations (recorded on card, accepted): Listener extra kwargs base_url/ping_s/idle_s; app-level `ping` action for idle detection (to be confirmed by spike); ~300 lines vs ~200 est; no CHANGELOG (not user-visible until lb5).
- Note (low): 14 pytest warnings in unit runs - not triaged; follow-up only.

## Cross-model review (advisory)
- Findings file: thoughts/shared/verification/2026-10-27-slice-20261027-lb3-listener-filters-review.md
- Reviewer: codex (codex review --base 8bd8d68); 0 findings. Caveat: sandbox could not open local ports, so websocket tests were re-run here instead (pass).

## Manual verification required (for Rob)
- [ ] After redeploy, in the Coolify container terminal: `echo "$TOKEN" | python -m app.ws_spike`, then post in a channel the bot is in. Spike against real Mattermost prints hello + one `posted` event shape matching the contract (token redacted), and the ping reply shape `{status:"OK", seq_reply}` confirms the server answers the listener's `ping` action.

## Definition of Done
- Automated verification re-run: **pass**
- Cross-model review present: **pass** (0 findings; port caveat covered by local re-run)
- Spec lock unchanged: **pass**
- Token never logged (incl. websockets DEBUG): **pass**
- Manual spike vs real Mattermost: **pending CP-S**

## Verdict
**PASS** (automated). Open for Rob **CP-S** manual spike above before lb4.
