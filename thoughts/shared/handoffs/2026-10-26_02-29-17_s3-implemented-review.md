---
id: HANDO-20261026-s3-implemented-review
type: handoff
phase: implement
status: complete
owner_agent: claude-code
date: 2026-10-26T02:29:17-05:00
links: [thoughts/shared/slices/2026-10-25-s3-dm.md, thoughts/shared/plans/2026-10-25-mmbridge-mcp.md]
git_commit: c6f2427
branch: main
next_skill: eng-verify
---
# Handoff: Slice 3 (DM) implemented; status review

## Task(s)
- Plan Phase 3 / SLICE-20261025-s3-dm: **completed (implementer)**, slice `status: review`. All Phase 3 automated checks ticked in the plan. Manual verification (real bot DMs Rob) pending for CP-S.

## Critical References
- thoughts/shared/slices/2026-10-25-s3-dm.md (Progress log has the exit codes)
- app/service.py:79 (DM path), app/mcp.py:101 (DM tools)

## Recent changes
- app/service.py:65 `_read_posts` extracted from read_channel (shared with dm_read); :79 `_direct_channel` (`users/username/{u}` 404 -> `unknown_user`, then `POST /channels/direct [me, u]`); :90 `dm_send` -> `{post_id, channel_id, create_at}`; :96 `dm_read` -> `{username, posts}` (posts shape identical to read_channel).
- app/mcp.py:47 `run(..., with_me=True)` passes the cached identity as `me=` (no extra `users/me` call); :101 `dm_send` (write bucket), :106 `dm_read`; `Username` schema arg.
- app/main.py:15 `create_app(mm_transport=None, limiter=None)` (test injection; prod unchanged).
- tests/acceptance/drivers/fake_mattermost.py:38-39, :194, :203 users/username + idempotent direct channel (creation recorded in `changes`); teamless direct channels skipped in teams/by-name lookups.
- tests/acceptance/drivers/mcp.py:65 `given_dm_post`, `given_no_user`; :129 `dm_posts`, `dm_channel_count`.
- tests/acceptance/conftest.py:20 channel filter scoped to tests/acceptance (it was skipping all unit tests under `pytest tests`).
- tests/unit/conftest.py:21 `limiter` fixture: frozen-clock RateLimiter for the unit `bridge`.
- tests/unit/test_dm.py (new, 19 tests). CHANGELOG.md Unreleased entry.

## Learnings
- `pytest tests -q` (Phase 3 command) previously reported only the 16 specs: the acceptance conftest's `pytest_collection_modifyitems` marked every non-`channels` item skipped, including tests/unit. Fixed (conftest is not locked).
- Once the unit tests ran in the same process as the acceptance specs, slice-1 `test_call_rate_limit_no_mm_call` failed every time: the bucket used the real clock, and 60 calls took 1.2-1.4 s on WSL /mnt/d, so a token refilled. Fixed with a frozen clock via the `limiter` fixture; assertions unchanged.
- No locked spec, DSL public interface or DSL assertion step body was changed. `eng-spec status`: no drift.

## Artifacts
- app/service.py, app/mcp.py, app/main.py
- tests/unit/test_dm.py, tests/unit/conftest.py
- tests/acceptance/conftest.py, tests/acceptance/drivers/fake_mattermost.py, tests/acceptance/drivers/mcp.py
- CHANGELOG.md
- thoughts/shared/slices/2026-10-25-s3-dm.md, thoughts/shared/plans/2026-10-25-mmbridge-mcp.md, PROJECT_STATE.md
- this handoff

## Approvals
- None granted this session. Planner to request after eng-verify: `CP-S: thoughts/shared/slices/2026-10-25-s3-dm.md - manual verification` (plan Phase 3 Manual Verification: DM rob "hello" + second DM same conversation; Rob replies "ping", bot reads it; DM "nobody" -> unknown user).
- Push of local commits still needs Rob's OK (`push_permission: ask`). Nothing pushed.

## Action Items & Next Steps
1. Planner: eng-verify for SLICE-20261025-s3-dm (re-run `pytest tests -q`, `eng-spec status .`, `eng-check .`).
2. Optional advisory Codex review of the slice diff (card says skipped; the slice-1 test harness changes in tests/unit/conftest.py and tests/acceptance/conftest.py are worth a look).
3. Rob: redeploy, then the Phase 3 manual checks -> CP-S. Phase 3 is the last plan phase, so after CP-S comes eng-ship.

## Other Notes
- `dm_read` for a user the bot has never DM'd opens the direct channel (Mattermost's `POST /channels/direct` creates it). This matches the architecture's DM flow but it is a side effect of a read; nothing in the design forbids it. Flagging for Rob.
- `dm_read` returns `{username, posts}` rather than `{team, channel, posts}`. The architecture says "same shape as read_channel", which I took to mean the posts list. Not a spec concern.
- `.eng/runners.toml` local modification (bypassPermissions for claude) and the earlier failed run log `thoughts/shared/runs/2026-10-26-implement-slice-20261025-s3-dm.md` (exit 129) were present before this session. Left uncommitted.
