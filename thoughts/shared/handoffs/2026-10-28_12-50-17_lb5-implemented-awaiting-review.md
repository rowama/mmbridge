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
