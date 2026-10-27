---
id: HANDO-20261027-lb3-implemented-awaiting-verify
type: handoff
phase: implement
status: complete
owner_agent: claude-code
date: 2026-10-27T02:25:15-05:00
links: [thoughts/shared/plans/2026-10-27-live-bots.md, thoughts/shared/slices/2026-10-27-lb3-listener-filters.md]
git_commit: c170d0d
branch: main
next_skill: eng-verify
---
# Handoff: lb3 implemented, awaiting verify
<!-- Session handoff (agent to agent, one session). A standing orientation for a new implementer is a project brief: .eng/bin/eng-new brief. -->

## Task(s)
- SLICE-20261027-lb3-listener-filters (plan Phase 3): **completed, status review**. Test-first; all Phase 3 automated verification exit 0. The manual check (OQ1 spike against Rob's real Mattermost) is still pending.

## Critical References
- thoughts/shared/slices/2026-10-27-lb3-listener-filters.md (progress log with file:line, deviations, the contract the fake assumes)
- thoughts/shared/plans/2026-10-27-live-bots.md Phase 3
- docs/decisions/0007-mattermost-websocket-listener.md

## Recent changes
- app/live_filter.py:40 `decide()`; `WakeIntent` dataclass with `hints` (event channel/sender names for lookup fallbacks)
- app/listener.py:27 redacted `mmbridge.ws` logger, :32 `ws_url`, :38 `connect`, :63 `Listener.run`, :79 `_read` (hello -> meta `ws_connection_id`; posted -> decide -> payload -> `enqueue_and_advance`), :111 `_track_seq` (`ws_seq_gap`), :119 `_ping` (MM `ping` action), :127 `_get` cached lookups, :137 `_payload` (ADR-0008 schema, `attempt: 1`)
- app/ws_spike.py: `python -m app.ws_spike` (token on stdin) prints hello/ping-reply/posted key->type shapes
- tests/acceptance/drivers/fake_mattermost.py: websocket endpoint + controls (`ws_send_raw`, `ws_resend_last`, `ws_skip_seq`, `ws_drop`, `ws_answer_pings`), GET channels/teams/users by id, `serve()` (uvicorn on a free port), `add_post(type, root_id)` broadcasts `posted`
- requirements.txt: `websockets==17.3`
- tests/unit/test_live_filter.py (25), tests/unit/test_listener.py (13); commits 8174ba2, c170d0d

## Learnings
- **`websockets` logs handshake request headers, including `Authorization: Bearer <token>`, at DEBUG.** Fixed by passing `logger=` (redacted, INFO) to `websockets.connect`. Any future websockets/httpx client must use a redacted logger the same way. Covered by `test_token_absent_from_logs_and_state[ws-debug]`; a mutation check showed this test fails when the filter is removed.
- Codex's sandbox cannot bind localhost ports, so it cannot run the uvicorn-backed listener tests. Verifiers must run them locally.
- Ping/idle uses Mattermost's application-level `{"action":"ping"}`, not protocol pings. Its `{status, seq_reply}` reply is a real frame, so it resets the idle timer. The OQ1 spike should confirm that real MM replies this way.
- `Listener.run()` handles exactly one connection. MMError from users/me and handshake errors propagate on purpose: the reconnect and 401 policy belong to lb5.
- Fake channel ids (`c-main-...`) are not 26-char ids, so tests build `BotConfig` directly; `store.validate` is not involved here.

## Artifacts
- app/live_filter.py, app/listener.py, app/ws_spike.py, requirements.txt
- tests/unit/test_live_filter.py, tests/unit/test_listener.py, tests/acceptance/drivers/fake_mattermost.py
- thoughts/shared/slices/2026-10-27-lb3-listener-filters.md (status review, progress log, deviations)
- thoughts/shared/plans/2026-10-27-live-bots.md (Phase 3 automated boxes ticked)
- thoughts/shared/verification/2026-10-27-slice-20261027-lb3-listener-filters-review.md (Codex: no findings; addressed, partial-validation note)
- thoughts/shared/runs/2026-10-27-code-review-slice-20261027-lb3-listener-filters.md

## Approvals
- Pending (planner to request): `CP-S: thoughts/shared/slices/2026-10-27-lb3-listener-filters.md - manual verification`. Manual step: in the Coolify container terminal run `echo "$TOKEN" | python -m app.ws_spike`, then post in a channel the bot is in. Check that the printed hello/posted/ping-reply shapes match the contract in the slice progress log. Note that the image must be redeployed first, because ws_spike is new.
- None granted this session.

## Action Items & Next Steps
1. Planner: run eng-verify on lb3. Re-run the Phase 3 automated checks locally (not in a socket-restricted sandbox) and review the deviations in the slice card.
2. Request CP-S from Rob with the spike step. Record the spike output in the slice progress log. Do not start lb4 before CP-S.
3. Not pushed (push_permission standing applies only after eng-verify PASS).

## Other Notes
- Untracked files left as found: thoughts/shared/inbox.md (empty), thoughts/shared/inbox-local-bak-1793080755/, the eng-run `.running.md` marker.
- No CHANGELOG entry: nothing is user-visible until lb5 wires the listener.
