---
id: SLICE-20261027-lb3-listener-filters
type: slice
phase: implement
status: todo             # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
plan_phase: 3
review: required (long-lived network component, ADR-0007) - thoughts/shared/verification/2026-10-27-lb3-review.md
reqs: [REQ-A1, REQ-A2, REQ-A3]
specs: none - wakes are only observable at a receiver after slice 4; this slice proves filter + listener->state.db with unit tests and an integration test against the fake MM websocket (specs for A1/A2/A3 turn green in slice 4)
---
# Slice 3: Listener + filters (fake MM websocket)

Plan: [thoughts/shared/plans/2026-10-27-live-bots.md](../plans/2026-10-27-live-bots.md) Phase 3. Architecture: docs/architecture/2026-10-26-live-bots.md. **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
Against a fake Mattermost websocket, the listener authenticates, tracks seq, and puts exactly the qualifying posts (chosen channels + DMs, not own/system/group posts) into the wake queue.

## Acceptance criteria
- [ ] `app/live_filter.py`: pure `decide(event: dict, bot_user_id: str, chosen: set[str]) -> WakeIntent | None` (rules from architecture Filter rules; malformed -> None + `event_invalid`)
- [ ] `app/listener.py`: `Listener(cfg, state, client_factory, ws_connect)`; `run()` = GET /users/me -> WS connect `Authorization: Bearer` -> hello(connection_id) -> on `posted` decide -> build payload (channel/sender lookups cached) -> `state.enqueue` + cursor; seq tracking, ping 30 s/idle 60 s; no reconnect/catch-up yet (slice 5)
- [ ] Spike (OQ1): confirm hello/seq/posted shape against Rob's Mattermost version; record result in progress log
- [ ] `tests/acceptance/drivers/fake_mattermost.py`: websocket endpoint (hello, seq, posted, drop) - reusable by the live driver
- [ ] `requirements.txt`: pin `websockets` explicitly (ADR-0007)
- [ ] Plan Phase 3 Automated Verification all exit 0; existing MCP suite (`.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`) still green

## Tasks
- [ ] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red) - n/a, see specs:
- [ ] Write failing unit tests (tests/unit/) for the behaviours above
- [ ] Implement
- [ ] Run Phase 3 automated verification (plan), including this slice's specs (now green)
- [ ] Do not edit locked files: tests/acceptance/specs/**, DSL public interface (CP-C speclock)

## Size check
~200 lines + tests (split filter/listener if larger)

## Progress log
<!-- date - agent - what changed (file:line) -->

## Blockers / deviations from plan
none
