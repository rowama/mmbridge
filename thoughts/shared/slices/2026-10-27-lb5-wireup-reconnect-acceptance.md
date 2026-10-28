---
id: SLICE-20261027-lb5-wireup-reconnect-acceptance
type: slice
phase: implement
status: review           # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-28
links: [thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
plan_phase: 5
review: required (security + deploy: lifespan, reconnect, token secrecy end to end) - thoughts/shared/verification/2026-10-27-lb5-review.md
reqs: [REQ-A1, REQ-A2, REQ-A3, REQ-A4, REQ-A7, REQ-A8]
specs: [tests/acceptance/specs/test_live_bots.py::test_post_during_connection_drop_wakes_exactly_once_after_reconnect, tests/acceptance/specs/test_live_bots.py::test_post_during_drop_in_channel_on_another_team_wakes_once_after_reconnect, tests/acceptance/specs/test_live_bots.py::test_bot_token_never_appears_in_logs_output_or_wakes]
---
# Slice 5: Wire-up + LIVE_BOTS_ENABLED + reconnect; acceptance green

Plan: [thoughts/shared/plans/2026-10-27-live-bots.md](../plans/2026-10-27-live-bots.md) Phase 5. Architecture: docs/architecture/2026-10-26-live-bots.md. **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
In the real container, `LIVE_BOTS_ENABLED=true` starts listener + dispatcher from FastAPI lifespan, `/health` reports listener state, drops reconnect with resume or REST catch-up (15 min window) with exactly-once wakes; full live acceptance suite (re-locked lb4b specs) green against the container.

## Acceptance criteria
- [x] `app/main.py`: lifespan starts listener+dispatcher tasks only if flag true and store+state readable; `/health` adds `listener: disabled|off|connecting|ok|degraded` and `wake_failed_24h` (no secrets); MCP path unchanged
- [x] `app/listener.py`: reconnect backoff 1->60 s jitter, `?connection_id&sequence_number`, new id -> REST catch-up `GET /channels/{id}/posts?since=` for all member channels (all teams, paged) + DM channels within `LIVE_CATCHUP_MINUTES` (default 15), seq reset to 0; 401 -> retry every 5 min; store mtime re-read every 30 s; single-listener lease in meta
- [x] `tests/acceptance/drivers/live.py`: container mode (docker image, temp /data, fakes on host network) per ADR-0010; scenario log capture for token scan
- [ ] README/OWNER-GUIDE: deploy prerequisites + receiver HMAC verification snippet; CHANGELOG Unreleased (README + CHANGELOG done; OWNER-GUIDE pending, see deviations)
- [x] (PR-2) `ConfigHolder` coordinated reload for listener+dispatcher; invalid edit keeps old config; token/url/secret rotation tests (no channel list after lb4b)
- [x] (PR-3) Catch-up pagination, `(create_at, post_id)` ordering for equal timestamps, membership discovery across all teams (`/users/me/teams` + `/users/me/teams/{team}/channels`, paged) incl. DMs, refresh every `LIVE_MEMBERSHIP_REFRESH_S` and on `user_added`/`added_to_team`/`user_removed`, first-seen-channel cursor = meta `last_event_at` bounded by window, atomic cursor; tests: crash-between-pages recovery, two teams, membership change, post during an outage in a channel joined during the outage (F4; architecture 'catch-up channel discovery')
- [x] (PR-4) Seq-gap on resume triggers catch-up; supervisor restarts crashed listener/dispatcher (MCP stays up, health degraded); startup delivers pending wakes exactly once
- [x] (PR-10) `/health` `listener: disabled|off|connecting|ok|degraded` + `wake_failed_24h` per architecture (replaces `on`)
- [ ] (PR-11) Verification report includes `eng-spec status .` and `eng-spec trace .` output
- [x] Plan Phase 5 Automated Verification all exit 0; existing MCP suite (`.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`) still green

## Tasks
- [x] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red) (`.venv/bin/pytest -q --channel live <node ids from specs:>`)
- [x] Write failing unit tests (tests/unit/) for the behaviours above
- [x] Implement
- [x] Run Phase 5 automated verification (plan), including this slice's specs (now green)
- [x] Do not edit locked files: tests/acceptance/specs/**, DSL public interface (CP-C speclock)

## Size check
~200 lines + driver/docs

## Progress log
<!-- date - agent - what changed (file:line) -->
- 2026-10-28 - claude-code - red first: the 3 specs (`--channel live`, in-process) -> 2 failed `NotImplementedError: drop_connection is built in lb5`, token spec passed in-process (its lb5 part is container mode). New unit tests run against the pre-lb5 listener/state: 7 failed + 7 errors (red), then green.
- 2026-10-28 - claude-code - code in b5926c6: app/live.py (new: ConfigHolder, supervise, LiveRuntime), app/main.py (lifespan start/stop, /health fields), app/listener.py (run() reconnect loop, connect_once(), resume, _catch_up/_since/_refresh_members/_membership_event, Unauthorized/LeaseHeld, config_changed), app/state.py (claim_owner(key), release_owner, delete_cursor, cursor_channels, failed_count). Tests: tests/unit/test_reconnect.py (14), tests/unit/test_main_live.py (12); test_listener.py uses connect_once() for single-connection tests; test_app.py health expects the new fields. Driver: drivers/live.py container mode (default, LIVE_IMAGE=mmbridge:lb5, --network host, named volume, admin via one-off `docker run` then `docker exec`, `docker logs` for the token scan) + `LIVE_MODE=inprocess`; drop/restore. Fake MM: real-time clock option, `since`, paging, D/G in team channel lists, `ws_refuse`, resumable dead queue; receiver `serve()`.
- 2026-10-28 - claude-code - verification at b5926c6: `.venv/bin/pytest tests/unit -q` 260 passed (exit 0); `docker build -t mmbridge:lb5 .` exit 0; `.venv/bin/pytest tests/acceptance --channel live -q` (container) 15 passed / 16 skipped (exit 0, ~58 s); `LIVE_MODE=inprocess` same 15 passed; `.venv/bin/pytest tests/acceptance -q` 16 passed / 15 skipped (exit 0); `eng-spec status .` matches lock (exit 0); `eng-check .` OK, 3 pre-existing warnings (exit 0).
- 2026-10-28 - claude-code - slice-diff Codex review NOT run: `codex` CLI is not installed in the implementer's WSL shell (`eng-run code-review` exit 1). Security-relevant slice: planner/Rob to run `python3 .eng/bin/eng-run code-review SLICE-20261027-lb5-wireup-reconnect-acceptance` where Codex is available.

## Blockers / deviations from plan
- Runtime wiring lives in a new module `app/live.py` (plan named only app/main.py); main.py just calls it.
- OWNER-GUIDE.md not edited: it has uncommitted edits by someone else in the working tree; deploy prerequisites went to README.md "Live bots (deploy)" (receiver HMAC snippet was already there from lb4). Planner to add an OWNER-GUIDE pointer.
- Container mode overrides only the uvicorn port (`--host 127.0.0.1 --port <free>`, host network) so tests never clash on 8080; same image and entrypoint otherwise. The wake URL is the plain-HTTP local receiver (LIVE_ALLOW_HTTP_WAKE=true, tests only).
- Catch-up re-offers posts with create_at equal to the cursor (not strictly after the (create_at, post_id) tuple): Mattermost ids are random, so tuple order among equal timestamps is arbitrary; the ledger dedupes (PR-3 backstop). Fetch looks back at most one extra window, so `catchup_skipped` counts posts up to 2x the window old.
- Known limit: a bot in no team finds DM channels only via existing cursors or the socket, so a brand-new DM made during an outage is missed for a teamless bot (team bots get DMs from the team channel lists).
- PR-11 (`eng-spec trace` in the verification report) is planner work: trace currently lists REQ-A1..A8 as "(not in an approved design)" (design amendment approval tracking), not a spec gap.
- Fake drift: the fake sends hello without seq on resume; the listener also treats a first non-hello event after a resume request as resumed. Check against real Mattermost at CP-S (restart Mattermost mid-demo).
- Depends on lb4b (allow-list removal + re-locked specs, CP-C). The cross-team drop spec id above exists only after lb4b applies the re-lock (draft: thoughts/shared/plans/drafts/2026-10-27-lb4b-test_live_bots.py.draft).
