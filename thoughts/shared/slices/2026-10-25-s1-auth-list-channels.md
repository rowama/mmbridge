---
id: SLICE-20261025-s1-auth-list-channels
type: slice
phase: implement
status: todo
owner_agent: Eddie
date: 2026-10-25
links: [thoughts/shared/plans/2026-10-25-mmbridge-mcp.md]
plan: thoughts/shared/plans/2026-10-25-mmbridge-mcp.md
plan_phase: 1
review: required (security slice: auth/credential) - thoughts/shared/verification/<date>-s1-review.md
reqs: [REQ-1, REQ-2]
specs: [tests/acceptance/specs/test_mmbridge.py::test_caller_without_credential_is_refused, tests/acceptance/specs/test_mmbridge.py::test_lists_only_joined_channels]
---
# Slice: Auth + echo removal + list_channels

**SECURITY SLICE** (credential handling): cross-model review required.

## Outcome (user-visible, demoable)
Rob connects a real Mattermost bot to Grok Bot via `https://chats.rmlab.cloud/mcp` with `Authorization: Bearer <token>` and it lists its channels; no-token calls get 401; the echo leak is gone.

## Acceptance criteria
- [ ] Echo route removed; unknown paths 404; `/health` unchanged
- [ ] `/mcp` without/malformed Bearer → HTTP 401 `{"error":"unauthorized"}`, zero Mattermost calls
- [ ] MM 401 → tool error `unauthorized`; connect/timeout/5xx → `mattermost_unavailable`; token never in results or logs
- [ ] `list_channels` returns O/P channels the bot is a member of across its teams `{team,name,display_name,type}`
- [ ] JSON log line per tool call (ADR-0005) with redaction filter
- [ ] Token config only in the Grok Bot MCP connection; nothing token-related added to Coolify env, Dockerfile, or repo
- [ ] AGENTS.md Commands filled (install/test/run)

## Tasks
- [ ] Implement fake Mattermost + McpDriver for auth/list_channels; run the two specs (red)
- [ ] Failing unit tests: auth, echo 404, error mapping, redaction
- [ ] Implement app/auth.py, app/errors.py, app/logging.py, app/mattermost.py, app/service.py (list_channels), app/mcp.py, app/main.py; add mcp + httpx to requirements.txt (pinned)
- [ ] Run Phase 1 automated verification (specs green)

## Size check
~200 lines prod + tests/harness; harness is one-off. Split harness into its own commit.

## Progress log

## Blockers / deviations from plan
none
