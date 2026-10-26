---
id: SLICE-20261025-s1-auth-list-channels
type: slice
phase: implement
status: review
owner_agent: Eddie
date: 2026-10-25
links: [thoughts/shared/plans/2026-10-25-mmbridge-mcp.md]
plan: thoughts/shared/plans/2026-10-25-mmbridge-mcp.md
plan_phase: 1
review: required (security slice: auth/credential) - thoughts/shared/verification/<date>-s1-review.md
reqs: [REQ-1, REQ-2]
specs: [tests/acceptance/specs/test_mmbridge.py::test_invalid_credential_is_rejected_and_not_exposed, tests/acceptance/specs/test_mmbridge.py::test_each_caller_sees_only_its_own_identity, tests/acceptance/specs/test_mmbridge.py::test_caller_without_credential_is_refused, tests/acceptance/specs/test_mmbridge.py::test_lists_only_joined_channels]
---
# Slice: Auth + echo removal + list_channels

**SECURITY SLICE** (credential handling): cross-model review required.

## Outcome (user-visible, demoable)
Rob connects a real Mattermost bot to Grok Bot via `https://chats.rmlab.cloud/mcp` with `Authorization: Bearer <token>` and it lists its channels; no-token calls get 401; the echo leak is gone.

## Acceptance criteria
- [x] Echo route removed; unknown paths 404; `/health` unchanged
- [x] `/mcp` without/malformed Bearer → HTTP 401 `{"error":"unauthorized"}`, zero Mattermost calls
- [x] Invalid (well-formed) token: MM 401 → tool error `unauthorized`, token not in result or logs
- [x] Caller isolation: alternating + concurrent calls from two tokens with disjoint memberships see only their own identity/channels; every outbound MM call carries the caller's own token; ContextVar reset after each request; identity cache keyed by token hash
- [x] Rate limits (ADR-0004) from the first deploy: 60 calls/min per token hash, 30/min anon per IP → `rate_limited`/429 + `retry_after_s`, no MM call
- [x] Client retry policy (ADR-0002): writes never retried; GET retried once on connection error only; call-count tests for connect error/timeout/5xx/4xx
- [x] MM 401 → tool error `unauthorized`; connect/timeout/5xx → `mattermost_unavailable`; token never in results or logs
- [x] `list_channels` returns O/P channels the bot is a member of across its teams `{team,name,display_name,type}`
- [x] JSON log line per tool call (ADR-0005) with redaction filter
- [x] Token config only in the Grok Bot MCP connection; nothing token-related added to Coolify env, Dockerfile, or repo
- [x] AGENTS.md Commands filled (install/test/run)

## Tasks
- [x] Implement fake Mattermost + McpDriver for auth/list_channels; run the two specs (red)
- [x] Failing unit tests: auth, invalid token, caller isolation/ContextVar/cache, echo 404, error mapping, retry call counts, call + anon rate limits, redaction
- [x] Implement app/auth.py, app/errors.py, app/logging.py, app/mattermost.py, app/ratelimit.py (call + anon buckets), app/service.py (list_channels), app/mcp.py, app/main.py; add mcp + httpx to requirements.txt (pinned)
- [x] Run Phase 1 automated verification (specs green)

## Size check
~200 lines prod + tests/harness; harness is one-off. Split harness into its own commit.

## Progress log
- 2026-10-26 (Eddie executor on box, Rob asked to start now): abc010a harness + red tests (ImportError create_app). Impl commit follows.
- `pip install -r requirements.txt -r requirements-dev.txt` exit 0 (mcp pinned 1.30.0: mcp 2.x renamed FastMCP->MCPServer; plan names FastMCP).
- `pytest tests/unit -q` exit 0: 26 passed.
- Slice specs: invalid_credential, caller_without_credential, lists_only_joined_channels PASS; each_caller_sees_only_its_own_identity passes all list/isolation steps, fails at line 44 `assert_post_visible` (post_channel arrives slice 2, as plan states). Plan's `-k "refused or ..."` also matches 3 slice-2 specs (non_member/read_non_member/unknown_channel) which fail red as expected.
- `docker build .`: NOT RUN (no docker on box). Substitute: uvicorn app.main:app -> /health {"ok":true}, /foo 404, POST /mcp no auth 401; official mcp client (streamablehttp_client) initialize + tools/list = [list_channels], call -> mattermost_unavailable; token absent from logs; JSON call line emitted.
- `eng-check .` exit 0.
- Cross-model review (required, security slice): NOT RUN - codex CLI not on box. Must run on Rob's PC before CP-S: `codex review --base 277b923 > thoughts/shared/verification/2026-10-26-s1-review.md`.

## Blockers / deviations from plan
plan review 2026-10-25: findings 2, 3, 9 folded into this slice.
- Deviation: call bucket capacity = per-minute limit (60), not ADR-0004's burst 10, to satisfy the plan's "61st call limited" test. Flag for Rob/eng-verify.
- Deviation: mcp pinned <2 (1.30.0) so FastMCP per plan exists.
- Review item for codex: anon-per-IP bucket uses scope client, which uvicorn sets from X-Forwarded-For with `--forwarded-allow-ips *` (Dockerfile) - leftmost XFF is client-spoofable, so the anon limit can be dodged. Fix candidate: trust only Coolify's Traefik IP.
- Driver: tolerates SDK-level non-JSON error text (unknown tool).
