---
id: SLICE-20261027-lb3-listener-filters
type: slice
phase: implement
status: review               # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
plan_phase: 3
review: required (long-lived network component, ADR-0007) - thoughts/shared/verification/2026-10-27-slice-20261027-lb3-listener-filters-review.md (Codex: no findings; addressed)
reqs: [REQ-A1, REQ-A2, REQ-A3]
specs: none - wakes are only observable at a receiver after slice 4; this slice proves filter + listener->state.db with unit tests and an integration test against the fake MM websocket (specs for A1/A2/A3 turn green in slice 4)
---
# Slice 3: Listener + filters (fake MM websocket)

Plan: [thoughts/shared/plans/2026-10-27-live-bots.md](../plans/2026-10-27-live-bots.md) Phase 3. Architecture: docs/architecture/2026-10-26-live-bots.md. **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
Against a fake Mattermost websocket, the listener authenticates, tracks seq, and puts exactly the qualifying posts (chosen channels + DMs, not own/system/group posts) into the wake queue.

## Acceptance criteria
- [x] `app/live_filter.py`: pure `decide(event: dict, bot_user_id: str, chosen: set[str]) -> WakeIntent | None` (rules from architecture Filter rules; malformed -> None + `event_invalid`)
- [x] `app/listener.py`: `Listener(cfg, state, client_factory, ws_connect)`; `run()` = GET /users/me -> WS connect `Authorization: Bearer` -> hello(connection_id) -> on `posted` decide -> build payload (channel/sender lookups cached) -> `state.enqueue` + cursor; seq tracking, ping 30 s/idle 60 s; no reconnect/catch-up yet (slice 5)
- [ ] Spike (OQ1): confirm hello/seq/posted shape against Rob's Mattermost version; record result in progress log
- [x] `tests/acceptance/drivers/fake_mattermost.py`: websocket endpoint (hello, seq, posted, drop) - reusable by the live driver
- [x] `requirements.txt`: pin `websockets` explicitly (ADR-0007)
- [x] (PR-3) Listener persists via `state.enqueue_and_advance`
- [x] Plan Phase 3 Automated Verification all exit 0; existing MCP suite (`.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`) still green

## Tasks
- [x] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red) - n/a, see specs:
- [x] Write failing unit tests (tests/unit/) for the behaviours above
- [x] Implement
- [x] Run Phase 3 automated verification (plan), including this slice's specs (now green)
- [x] Do not edit locked files: tests/acceptance/specs/**, DSL public interface (CP-C speclock)

## Size check
~200 lines + tests (split filter/listener if larger)

## Progress log
<!-- date - agent - what changed (file:line) -->
- 2026-10-27 - claude-code - Red first: test_live_filter.py / test_listener.py failed on ModuleNotFoundError (app.live_filter, app.listener) before code existed.
- 2026-10-27 - claude-code - `app/live_filter.py:40` `decide()` + `WakeIntent` (frozen; carries event `hints` for lookup fallbacks). Malformed -> None + `event_invalid` (reason only, never message text); non-`posted` events ignored silently. Commit 8174ba2.
- 2026-10-27 - claude-code - `app/listener.py`: `ws_url` :32, `connect` :38 (websockets, protocol keepalive off, own redacted `mmbridge.ws` logger :27), `Listener.run` :63 (users/me -> WS Bearer -> read loop), `_read` :79 (hello -> `meta.ws_connection_id`, status ok; `posted` -> decide -> payload -> `state.enqueue_and_advance` via to_thread), `_track_seq` :111 (`ws_seq_gap` logged; catch-up is slice 5), `_ping` :119 (Mattermost `ping` action every 30 s; any frame resets the 60 s idle timer; idle -> `ws_idle`, run returns), `_payload` :137 (ADR-0008 schema, `attempt: 1` placeholder for lb4; channel/team/user lookups cached, event hints on MMError). One connection per `run()`; MMError/handshake errors propagate (reconnect/401 policy is slice 5). Commit c170d0d.
- 2026-10-27 - claude-code - `tests/acceptance/drivers/fake_mattermost.py`: GET channels/{id}, teams/{id}, users/{id}; `/api/v4/websocket` (Bearer, hello{connection_id, server_version}, per-connection seq, `posted` broadcast to members incl. author, ping action -> `{status, seq_reply}`), controls `ws_send_raw`, `ws_resend_last`, `ws_skip_seq`, `ws_drop`, `ws_answer_pings`; `serve()` runs it on a free 127.0.0.1 port (uvicorn) so tests use the real `websockets` client - reusable by the live driver. `add_post(..., type, root_id)`.
- 2026-10-27 - claude-code - Security finding during TDD: `websockets` logs handshake request headers (incl. `Authorization: Bearer <token>`) at DEBUG. Fixed with a dedicated `mmbridge.ws` logger (RedactFilter, INFO) passed to `websockets.connect`; test runs with that logger at DEBUG too, and a mutation check (filter removed) makes it fail.
- 2026-10-27 - claude-code - OQ1 spike: `python -m app.ws_spike` (`app/ws_spike.py`; token on stdin, prints hello / ping-reply / posted / post key->type shapes, no token, no message text); tested against the fake. **Not run against Rob's Mattermost** (no token/network in this session) -> this is the Phase 3 manual check: in the Coolify container terminal `echo "$TOKEN" | python -m app.ws_spike`, then post in a channel the bot is in. Contract the fake/listener assume: hello `{event:"hello", seq:0, data:{connection_id, server_version}}`; posted `{event:"posted", seq, data:{channel_type, channel_name, channel_display_name, sender_name, team_id, post:<JSON string>}, broadcast:{channel_id}}`; ping reply `{status:"OK", seq_reply}`.
- 2026-10-27 - claude-code - `requirements.txt`: `websockets==17.3` (version already resolved via uvicorn[standard]).
- 2026-10-27 - claude-code - Automated verification: `.venv/bin/pytest tests/unit -q` exit 0 (176 passed, 3 consecutive runs), `.venv/bin/pytest tests/acceptance -q` exit 0 (16 passed, 9 skipped), `python3 .eng/bin/eng-check .` exit 0, `python3 .eng/bin/eng-spec status .` matches lock; extra: `docker build -t mmbridge:lb3 .` exit 0 and `import websockets, app.listener, app.ws_spike` inside the image OK.

## Blockers / deviations from plan
- `Listener.__init__` has extra keyword args beyond the plan signature: `base_url` (default `MATTERMOST_URL`; ws URL derived from it), `ping_s`, `idle_s` (tests). `ws_connect` defaults to `app.listener.connect`.
- Ping/idle uses the Mattermost application-level `ping` action (reply is a frame, so it resets the idle timer) instead of protocol pings; to confirm in the OQ1 spike output (`ping reply shape`).
- Size: ~300 app lines (filter 75, listener 152, spike 71) + fake 150 + tests; split into two commits (filter / listener) rather than two slices.
- No CHANGELOG entry: nothing user-visible yet (listener not wired until lb5; spike is a dev check).
- No locked spec or DSL file touched.
