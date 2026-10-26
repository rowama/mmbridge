---
id: SLICE-20261025-s2-post-read-channel
type: slice
phase: implement
status: todo
owner_agent: Eddie
date: 2026-10-25
links: [thoughts/shared/plans/2026-10-25-mmbridge-mcp.md]
plan: thoughts/shared/plans/2026-10-25-mmbridge-mcp.md
plan_phase: 2
review: required (write path + rate limiting) - thoughts/shared/verification/<date>-s2-review.md
reqs: [REQ-1, REQ-3, REQ-4, REQ-7, REQ-8]
specs: [tests/acceptance/specs/test_mmbridge.py::test_posts_appear_as_the_connecting_bot, tests/acceptance/specs/test_mmbridge.py::test_post_to_member_channel, tests/acceptance/specs/test_mmbridge.py::test_read_requested_count, tests/acceptance/specs/test_mmbridge.py::test_read_default_count, tests/acceptance/specs/test_mmbridge.py::test_non_member_channel_is_refused_without_join, tests/acceptance/specs/test_mmbridge.py::test_mattermost_down_is_clear_and_leaks_nothing]
---
# Slice: Post and read channel (+ rate limits)

## Outcome (user-visible, demoable)
The bot posts to and reads channels it belongs to; non-member channels are refused without joining; calls are rate limited.

## Acceptance criteria
- [ ] `post_channel(team, channel, message)` → `{post_id, channel, team, create_at}`; membership checked before any write; no join ever
- [ ] `read_channel(team, channel, limit=20)` 1..100, newest first, `{id, author, create_at ISO-8601 UTC, message}`
- [ ] Errors: `not_member`, `unknown_channel`, `invalid_argument`, `mattermost_unavailable` (no token)
- [ ] Rate limits per ADR-0004 with `rate_limited` + `retry_after_s`

## Tasks
- [ ] Extend fake MM/driver; run this slice's specs (red)
- [ ] Failing unit tests: validation, rate limiter, not_member makes no POST
- [ ] Implement service/tools/ratelimit
- [ ] Run Phase 2 automated verification

## Size check
~150-200 lines.

## Progress log

## Blockers / deviations from plan
none
