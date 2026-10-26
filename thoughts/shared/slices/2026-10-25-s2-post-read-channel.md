---
id: SLICE-20261025-s2-post-read-channel
type: slice
phase: implement
status: done
owner_agent: claude-code
date: 2026-10-25
links: [thoughts/shared/plans/2026-10-25-mmbridge-mcp.md]
plan: thoughts/shared/plans/2026-10-25-mmbridge-mcp.md
plan_phase: 2
review: required (write path + rate limiting) - thoughts/shared/verification/2026-10-26-slice-20261025-s2-post-read-channel-review.md
reqs: [REQ-1, REQ-3, REQ-4, REQ-7, REQ-8]
specs: [tests/acceptance/specs/test_mmbridge.py::test_read_of_non_member_channel_is_refused, tests/acceptance/specs/test_mmbridge.py::test_unknown_channel_is_refused, tests/acceptance/specs/test_mmbridge.py::test_posts_appear_as_the_connecting_bot, tests/acceptance/specs/test_mmbridge.py::test_post_to_member_channel, tests/acceptance/specs/test_mmbridge.py::test_read_requested_count, tests/acceptance/specs/test_mmbridge.py::test_read_default_count, tests/acceptance/specs/test_mmbridge.py::test_non_member_channel_is_refused_without_join, tests/acceptance/specs/test_mmbridge.py::test_mattermost_down_is_clear_and_leaks_nothing]
---
# Slice: Post and read channel (+ write rate limit)

## Outcome (user-visible, demoable)
The bot posts to and reads channels it belongs to; non-member channels are refused without joining; writes are rate limited.

## Acceptance criteria
- [x] `post_channel(team, channel, message)` → `{post_id, channel, team, create_at}`; membership checked before any write; no join ever
- [x] `read_channel` checks membership first (REQ-7): non-member → `not_member`, no posts fetched, no join
- [x] Unknown channel → `unknown_channel` for post and read, nothing posted or joined
- [x] Shared validators (`app/validate.py`) for team/channel/message/limit; unsafe identifier segments rejected (and URL-encoded); invalid input → `invalid_argument` with zero MM calls
- [x] `read_channel(team, channel, limit=20)` 1..100, newest first, `{id, author, create_at ISO-8601 UTC, message}`
- [x] Errors: `not_member`, `unknown_channel`, `invalid_argument`, `mattermost_unavailable` (no token)
- [x] Write bucket (20/min per token hash, ADR-0004) added to the slice-1 limiter; `rate_limited` + `retry_after_s`

## Tasks
- [x] Extend fake MM/driver; run this slice's specs (red)
- [x] Failing unit tests: shared validators (boundaries + malformed identifiers), write bucket, not_member (post and read) makes no POST / no posts GET, unknown_channel
- [x] Implement service/tools/ratelimit
- [x] Run Phase 2 automated verification

## Size check
~150-200 lines.

## Progress log
- 2026-10-26 (claude-code): session stopped before starting. The permission mode refused every command (eng-check, eng-status, pytest), so the specs couldn't be confirmed red and nothing could be verified. No code changed. See thoughts/shared/handoffs/2026-10-26_09-00-00_s2-blocked-no-exec.md.

- 2026-10-26 (claude-code, re-run): venv built with Python 3.12 via uv (requirements pins don't resolve on the box's Python 3.14; see TODOS). Fake MM + driver extended; slice specs red for the right reason ("Unknown tool: post_channel"/"read_channel"). Unit tests red (no app/validate). Implemented app/validate.py, write bucket (RL_WRITES_PER_MIN=20), service.post_channel/read_channel (by-name lookup -> members/me -> POST /posts | channel posts + POST /users/ids), MCP tools with Any-typed args + explicit JSON schema so validators (not pydantic coercion) produce invalid_argument. Results: `pytest tests/unit -q` exit 0 (49 passed); `pytest tests/acceptance -q -k "not dm"` exit 0 (12 passed); `pytest tests/acceptance -q` 12 passed / 4 failed (the 4 DM specs, slice 3); `eng-check` exit 0; `eng-spec status` ok, specs + DSL match lock; `docker build` exit 0, container /health {"ok":true}, /foo 404. Code commit 8334f40. Codex review (advisory): no findings. Specs, DSL untouched. Status -> review.

## Blockers / deviations from plan
- 2026-10-26: resolved. The earlier run couldn't execute commands; the re-run (bypassPermissions in .eng/runners.toml) could.
- none from plan (plan review 2026-10-25: findings 1, 7, 8 folded in; call/anon rate limits moved to slice 1)


## Approvals
- CP-S approved by Rob 2026-10-26 (America/Chicago): live post/read/not_member confirmed.
