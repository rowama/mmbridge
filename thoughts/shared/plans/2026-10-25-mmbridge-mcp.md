---
id: PLAN-20261025-mmbridge-mcp
type: plan
phase: plan
status: approved            # input (pre-draft from an earlier phase) | draft | in-review | approved | in-progress | done | superseded
owner_agent: Eddie
date: 2026-10-25
links: [docs/design/2026-10-25-mmbridge-mcp.md, docs/architecture/2026-10-25-mmbridge-mcp.md]
plan_review: thoughts/shared/verification/2026-10-25-mmbridge-mcp-plan-review.md
---
# Plan: mmbridge MCP

## Overview
Turn the skeleton into the MCP bridge from the [design](../../../docs/design/2026-10-25-mmbridge-mcp.md) (REQ-1..8) per the approved [architecture](../../../docs/architecture/2026-10-25-mmbridge-mcp.md) and ADR-0001..0005. Three vertical slices; slice 1 is the shortest path to Rob connecting a real Mattermost bot from Grok Bot.

## Current State Analysis
From [research](../research/2026-10-25-mmbridge-current-code.md), verified against code:
- `app/main.py:12-14` `/health` returns `{"ok": true}`.
- `app/main.py:17-26` catch-all echo returns all request headers, including `Authorization` (token leak). Must go in the first deploy.
- `app/mattermost.py` and `app/mcp.py` are placeholders; `bot_token_for` stub conflicts with ADR-0001 and is removed.
- `requirements.txt`: fastapi, uvicorn only. No tests exist.

## Desired End State
`https://chats.rmlab.cloud/mcp` serves 5 MCP tools (Streamable HTTP, stateless). Each Grok Bot's MCP connection carries `Authorization: Bearer <its Mattermost bot token>`; the token lives only in the Grok Bot MCP connection, never in Coolify env or the repo. All 16 executable specs green; unknown paths 404; tokens never logged or echoed.

### Key Discoveries
- Echo leak at `app/main.py:25` (`"headers": dict(request.headers)`).
- Mattermost reachable only on the private stack network as `http://mattermost:8065` (`app/mattermost.py:11`).

## What We're NOT Doing
- @mention wakes / websocket events, auto-join, multi-bot routing, threads, reactions, files (TODOS.md, CP-A scope hold).
- Storing any token server-side (ADR-0001); no database; no admin token.
- Shared/distributed rate limiting (single container; ADR-0004).

## Implementation Approach
Call path: `POST /mcp` → `auth.require_bearer` (ASGI middleware on `/mcp`; 401 `{"error":"unauthorized"}` before any MM call; token into a `contextvars.ContextVar`) → `ratelimit.check(sha256(token), ip)` → MCP tool (`mcp` SDK `FastMCP`, `stateless_http=True`, `json_response=True`) → `service.*` → `mattermost.Client(token)`.

Key signatures:
```python
# app/mattermost.py
class MMError(Exception): code: str; status: int | None
class Client:
    def __init__(self, token: str, base_url: str = MATTERMOST_URL, transport: httpx.AsyncBaseTransport | None = None)
    async def get(self, path: str, **params) -> dict | list   # maps connect/timeout/5xx -> mattermost_unavailable, 401 -> unauthorized, 404 -> not_found, other 4xx -> mattermost_error
    async def post(self, path: str, json: dict) -> dict       # never retried
# app/validate.py (shared by post_channel/read_channel/dm_send/dm_read)
def identifier(kind: str, value: str) -> str   # team/channel/username: ^[a-z0-9][a-z0-9._-]{0,63}$ else invalid_argument; never interpolated unvalidated; path segments additionally URL-encoded
def message(value: str) -> str                 # 1..16383 chars after strip, else invalid_argument
def limit(value: int | None) -> int            # None -> 20; int 1..100 else invalid_argument (bools rejected)
# app/service.py
async def list_channels(c: Client) -> dict
async def post_channel(c, team, channel, message) -> dict
async def read_channel(c, team, channel, limit=20) -> dict
async def dm_send(c, username, message) -> dict
async def dm_read(c, username, limit=20) -> dict
# app/errors.py
def tool_error(code: str, message: str, **extra) -> CallToolResult  # isError=True, JSON {"code","message",...}
```
File tree diff:
```
app/main.py          M  remove echo; mount /mcp; 404 default
app/auth.py          A
app/ratelimit.py     A  (slice 1: call + anon buckets; slice 2: write bucket)
app/validate.py      A  (slice 2: shared validators for channel + DM tools; slice 3 reuses)
app/mcp.py           M  FastMCP server + tools
app/service.py       A
app/mattermost.py    M  httpx client; drop bot_token_for
app/errors.py        A
app/logging.py       A  JSON + redaction filter
requirements.txt     M  + mcp, httpx; requirements-dev.txt A (pytest, respx/none, pytest-asyncio)
tests/unit/          A
tests/acceptance/drivers/mcp.py, fake_mattermost.py  M/A
```
Fake Mattermost: an in-process ASGI app implementing only the `/api/v4` endpoints used, recording calls; injected via `httpx.ASGITransport` (env `MATTERMOST_URL` stays real in prod). The driver calls `/mcp` through `httpx.ASGITransport` on `app.main:app` with the `mcp` client SDK's Streamable HTTP client or raw JSON-RPC.

## Phase 1: Auth + echo removal + list_channels (real-bot connect)
Slice card: [thoughts/shared/slices/2026-10-25-s1-auth-list-channels.md](../slices/2026-10-25-s1-auth-list-channels.md) — **security slice: cross-model review required.**

### Changes Required
#### 1. Remove echo, mount MCP
**File**: `app/main.py` — delete catch-all; keep `/health`; mount MCP app at `/mcp`; unknown paths 404.
#### 2. Auth
**File**: `app/auth.py` — Bearer extraction, 401 without MM call, ContextVar token (set per request, reset in `finally`); never log the header. A well-formed but invalid token reaches MM, which returns 401 → tool error `unauthorized` (no token in result/logs). Identity cache (`users/me`, 60 s) is keyed by sha256(token) only; never shared across tokens.
**Isolation tests (unit/integration):** alternating and concurrent (`asyncio.gather`) calls from two tokens with disjoint memberships each get only their own identity and channels; the fake records the outbound `Authorization` per call and every MM call carries the caller's own token; the ContextVar is unset after each request (incl. on error); cache entries for token A are never returned for token B.
#### 3. Mattermost client + error mapping
**Files**: `app/mattermost.py`, `app/errors.py` — httpx, 10 s timeout, error codes per architecture table.
**Retry policy (ADR-0002, explicit):** `post()` (all writes) is **never** retried automatically. `get()` retries **exactly once**, only on a connection error (`httpx.ConnectError`); no retry on timeout, HTTP 4xx or 5xx. No generic retry transport/middleware may be added. Unit tests assert upstream call counts against the fake: write + connect error → 1 call; GET + connect error → 2 calls (then `mattermost_unavailable` if both fail, success if the retry succeeds); GET + timeout → 1; GET + 500 → 1; GET + 401/404 → 1.
#### 3b. Rate limiting (moved from slice 2, finding 3)
**File**: `app/ratelimit.py` — ADR-0004 buckets in slice 1: 60 calls/min per token hash, 30/min anonymous per client IP (401s count against the anon bucket); `rate_limited` + `retry_after_s`; 429 for anon. The 20 writes/min bucket is added in slice 2 with the first write tool. Tests: 61st call in a minute → `rate_limited`, retry_after_s > 0, no MM call; 31st anon request → 429; buckets independent per token.
#### 4. list_channels tool
**Files**: `app/mcp.py`, `app/service.py` — `users/me` (60 s cache by token hash), `users/me/teams`, `users/me/teams/{id}/channels`; return O/P channels only.
#### 5. Logging
**File**: `app/logging.py` — JSON line per call (ADR-0005), redaction filter.
#### 6. Test harness
`requirements-dev.txt`, `tests/unit/`, fake Mattermost + `McpDriver` (auth + list_channels), `pytest.ini`/conftest path setup. Update AGENTS.md Commands.

### Success Criteria
#### Automated Verification
- [x] `pip install -r requirements.txt -r requirements-dev.txt` succeeds
- [x] `pytest tests/unit -q` passes (auth 401 with zero MM calls; invalid token → `unauthorized`; caller isolation/ContextVar cleanup/cache keying; error mapping; retry call counts; call + anon rate limits; redaction; echo gone: `GET /anything` → 404 and body lacks headers)
- [ ] `pytest tests/acceptance -q -k "refused or joined_channels or invalid_credential or own_identity"` passes (REQ-1 ex2, invalid credential, caller isolation, REQ-2 ex1; the isolation spec's post step goes green in slice 2)
- [ ] `docker build .` succeeds; container `/health` returns `{"ok": true}`
- [x] `python3 .eng/bin/eng-check .` passes
#### Manual Verification (Rob — proves auth with a real bot)
- [ ] Coolify redeploy from `main`; `https://chats.rmlab.cloud/health` → `{"ok":true}`; `https://chats.rmlab.cloud/foo` → 404 (no headers echoed)
- [ ] `curl -X POST https://chats.rmlab.cloud/mcp` without Authorization → 401
- [ ] In Grok Bot, add MCP connection URL `https://chats.rmlab.cloud/mcp`, header `Authorization: Bearer <bot token>` (token only here; not in Coolify, not in repo)
- [ ] Ask the bot "list my Mattermost channels" → returns the channels the bot account was added to, team names correct
- [ ] Coolify logs show the call with bot username and token-hash prefix, no token

**Stop:** after automated checks pass, pause for Rob's manual verification before Phase 2.

---

## Phase 2: Post and read channel (+ write rate limit)
Slice card: [thoughts/shared/slices/2026-10-25-s2-post-read-channel.md](../slices/2026-10-25-s2-post-read-channel.md)

### Changes Required
#### 1. `post_channel`, `read_channel`
**Files**: `app/mcp.py`, `app/service.py`, `app/validate.py` — inputs validated by the shared validators before any MM call; by-name lookup (404 → `unknown_channel`); `channels/{id}/members/me` membership check before **both** `post_channel` and `read_channel` (REQ-7; 404/403 → `not_member`; never join); `POST /posts`; read via `channels/{id}/posts` + `POST /users/ids`, ISO-8601 UTC, newest first, limit 1..100 default 20, message 1..16383.
#### 2. Rate limiting
**File**: `app/ratelimit.py` — add the 20 writes/min per token hash bucket (ADR-0004) to the slice-1 limiter; `rate_limited` + `retry_after_s`.
#### 3. Fake MM + driver extensions for channel posts.

### Success Criteria
#### Automated Verification
- [x] `pytest tests/unit -q` passes (shared validators: boundary values 0/1/100/101, None, bool, non-int limit; empty/16383/16384-char message; identifiers with `/`, `..`, `%2F`, spaces, uppercase, 65 chars → `invalid_argument` with zero MM calls; write bucket; not_member path (post and read) issues no POST and no posts GET)
- [x] `pytest tests/acceptance -q -k "not dm"` passes (REQ-1 ex1 + isolation, REQ-3, REQ-4 x2, REQ-7 non-member post/read + unknown channel, REQ-8)
- [x] `python3 .eng/bin/eng-check .` passes
#### Manual Verification
- [x] After redeploy, bot posts "build is green" to a channel it's in; Rob sees it in Mattermost authored by the bot
- [x] Bot reads that channel with limit 5 → 5 newest posts with authors/times
- [x] Bot posts to a channel it is not in → told not a member; Rob confirms it didn't join

**Stop:** pause for Rob's manual verification before Phase 3.

---

## Phase 3: DMs
Slice card: [thoughts/shared/slices/2026-10-25-s3-dm.md](../slices/2026-10-25-s3-dm.md)

### Changes Required
#### 1. `dm_send`, `dm_read`
**Files**: `app/mcp.py`, `app/service.py` — `username`, `message`, `limit` validated with the same `app/validate.py` validators as Phase 2 before any MM call; `users/username/{u}` (404 → `unknown_user`), `POST /channels/direct [me,u]` (idempotent), post/read as Phase 2. Unit tests: DM boundary values and malformed usernames → `invalid_argument`, zero MM calls.
#### 2. Fake MM + driver: direct channels.

### Success Criteria
#### Automated Verification
- [x] `pytest tests -q` passes (all 16 acceptance specs + unit)
- [x] `python3 .eng/bin/eng-spec status .` reports no drift; `python3 .eng/bin/eng-check .` passes
#### Manual Verification
- [ ] Bot DMs Rob "hello" → Rob sees it in a DM from the bot; a second DM lands in the same conversation
- [ ] Rob replies "ping"; bot reads DM with rob → "ping" returned
- [ ] DM to "nobody" → unknown user error

## Demo script
1. Open `https://chats.rmlab.cloud/health` → `{"ok":true}`.
2. In Grok Bot, MCP connection `https://chats.rmlab.cloud/mcp` with `Authorization: Bearer <bot token>`.
3. "List my Mattermost channels" → channels the bot is in.
4. "Post 'build is green' in dev" → appears in Mattermost from the bot.
5. "DM rob 'hello'" → Rob gets the DM; reply "ping", ask the bot to read it.

## Testing Strategy
- Unit: `tests/unit/` — auth, client error mapping, validation, rate limiter, log redaction (pytest, pytest-asyncio).
- Integration: bridge app in-process over httpx ASGITransport against fake Mattermost ASGI app.
- Acceptance (executable specs): `tests/acceptance/specs/test_mmbridge.py`, 16 specs tagged REQ-1..8, channel `mcp` (the bridge's only API surface is MCP). Speclock before CP-C.
- Manual steps: per phase above, with a real Mattermost bot via Grok Bot.

## Plan review dispositions
[Plan review](../verification/2026-10-25-mmbridge-mcp-plan-review.md): findings 1, 2, 3, 6, 7, 8, 9 fixed in this plan, slice cards, specs and DSL; 4, 5, 10, 11, 12 accepted-risk (Rob 2026-10-25).

## Risks, Rollback, Migration
- Rollback: redeploy previous commit in Coolify; no data, always safe. Slice 1 ships the echo removal so the leak closes on first deploy.
- Risk: Grok Bot MCP connector must send custom `Authorization` header — verified in slice 1 manual step; if it can't, back up to architecture (ADR-0001).
- Risk: `mcp` SDK Streamable HTTP mount under FastAPI — pin version in slice 1.

## References
- Design: docs/design/2026-10-25-mmbridge-mcp.md
- Research: thoughts/shared/research/2026-10-25-mmbridge-current-code.md
- Architecture: docs/architecture/2026-10-25-mmbridge-mcp.md
- ADRs: docs/decisions/0001..0005
