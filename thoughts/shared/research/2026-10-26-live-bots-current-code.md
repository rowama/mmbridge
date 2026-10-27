---
id: RESEA-20261026-live-bots-current-code
type: research
phase: research
status: approved
owner_agent: grok-bot
date: 2026-10-26
links: [docs/design/2026-10-26-live-bots.md]
git_commit: a5bf726
branch: main
---
# Research: mmbridge code today, for Live bots one-bot v1
<!-- Codebase research: what the code IS, file:line, no recommendations. -->

## Research questions
From the approved scope (REQ-A1, A2, A3 own-post, A4, A7, A8; hand-set channel list; encrypted token store Q7; HTTPS webhook wake Q6):
1. (A1/A2/A4) Does any long-lived process, background task, websocket or event subscription to Mattermost exist? How is the app process started and its lifecycle managed?
2. (A1/A2) How does the code talk to Mattermost today (base URL, auth, endpoints, retries, timeouts)? Which endpoints resolve channels, members, posts, DMs and usernames?
3. (A3) How does the code learn the bot's own identity (user id/username)?
4. (A1 hand-set channels) Is there any configuration for channel lists or per-bot settings?
5. (A4) Is there any persistence (DB, files, volumes) usable for dedupe/last-seen state? Any post-id dedupe?
6. (A7, Q7) How are tokens handled today: storage, hashing, redaction in logs, exposure in outputs? Any encryption or secret-key handling?
7. (A7, Q6) Is there any outbound HTTP to non-Mattermost targets, any HMAC/signature code?
8. (A8) What retry/backoff and failure-recording mechanisms exist?
9. (deploy) What does the container/Coolify config provide (process model, env, network, storage)?
10. (tests) What test scaffolding exists for Mattermost (fakes) and for async/background behaviour?

## Summary
mmbridge v0.2.0 is a stateless FastAPI app that mounts a FastMCP Streamable-HTTP server at /mcp with five tools (list_channels, post_channel, read_channel, dm_send, dm_read). Every Mattermost call uses the caller's per-request Bearer token over REST (httpx, one client per call). There is no websocket, background listener, persistence, channel configuration, outbound webhook, HMAC, encryption or token store. Token protection consists of: token held in a ContextVar per request, SHA-256 hash for cache/rate-limit keys, a repr that hides the token, and a log redaction filter for Bearer/Authorization patterns.

## Detailed findings
### Q1 Process and lifecycle
- App factory `create_app(mm_transport, limiter)` builds the MCP server and FastAPI app (app/main.py:15-35); module-level `app = create_app()` (app/main.py:38).
- The only lifespan work is running the MCP session manager (app/main.py:21-24); no other startup/shutdown tasks.
- Routes: GET /health (app/main.py:29-31) plus MCP routes (app/main.py:33); BearerAuth middleware wraps all (app/main.py:34).
- Started by a single uvicorn process, no workers flag (Dockerfile:19).
- No websocket client or event subscription anywhere in app/ (grep for "websocket"/"create_task" finds none in app/; only tests/unit/conftest.py:38 uses asyncio.create_task).

### Q2 Mattermost access
- Base URL from env MATTERMOST_URL, default http://mattermost:8065 (app/mattermost.py:10); REST prefix /api/v4 (app/mattermost.py:23).
- One httpx.AsyncClient per request, 10 s timeout, header "Authorization: Bearer <token>" (app/mattermost.py:11,30-32).
- Endpoints used: GET /users/me (app/service.py:20); /users/me/teams and /users/me/teams/{id}/channels (app/service.py:28,31); /teams/name/{t}/channels/name/{c} (app/service.py:45); /channels/{id}/members/me (app/service.py:51); POST /posts (app/service.py:61,92); GET /channels/{id}/posts with page/per_page (app/service.py:66); POST /users/ids (app/service.py:69); GET /users/username/{u} (app/service.py:82); POST /channels/direct (app/service.py:87).
- Post fields read: id, user_id, create_at, message (app/service.py:67-71); timestamps converted ms -> ISO UTC (app/service.py:38-39).
- Membership checked, never joined (app/service.py:42-56).
- Mapping of HTTP status to error codes (app/mattermost.py:51-62).

### Q3 Bot identity
- IdentityCache: GET /users/me, cached 60 s keyed by token hash, keeps id and username, cleared above 10000 entries (app/service.py:9-24).
- Used per tool call; username is logged as "bot" (app/mcp.py:65-66).

### Q4 Configuration
- Env settings present: MATTERMOST_URL (app/mattermost.py:10), RL_CALLS_PER_MIN / RL_WRITES_PER_MIN / RL_ANON_PER_MIN (app/ratelimit.py:31-33), FORWARDED_ALLOW_IPS (Dockerfile:16).
- No channel list, bot registry, wake URL or secret setting exists. coolify-service.snippet.yaml:16 has a comment that per-bot tokens would be added later as Coolify secrets.

### Q5 Persistence and dedupe
- All state is in-process memory: identity cache dict (app/service.py:14) and rate-limit buckets (app/ratelimit.py:35-37).
- No DB, file writes, or volume in Dockerfile (Dockerfile:1-19) or compose snippet (coolify-service.snippet.yaml:3-25). No post-id dedupe code.
- Container runs as non-root uid 10001 with home dir (Dockerfile:11-12).

### Q6 Token handling
- ADR-0001 decision: token per call, never persisted, only SHA-256 hash kept (docs/decisions/0001-credential-handoff-bearer-per-call.md:19).
- Bearer regex, case-insensitive scheme, token 8-512 chars (app/auth.py:14); token placed in ContextVar and reset in finally (app/auth.py:12,41-45).
- token_hash = sha256 hex (app/auth.py:17-18); logs record first 8 hex chars (app/mcp.py:52).
- Client.__repr__ omits token (app/mattermost.py:27-28).
- RedactFilter rewrites "Bearer <x>" and "authorization: <x>" in messages and exception text (app/logging.py:7-25), applied to loggers and handler (app/logging.py:36-41).
- Tool errors use fixed messages, not MM bodies (app/errors.py:1, app/mcp.py:22-27,73-76).
- No encryption library in requirements (requirements.txt:1-4); no key management code.

### Q7 Outbound non-Mattermost HTTP / signatures
- None. The only outbound HTTP is the Mattermost Client (app/mattermost.py:30-32). No hmac usage in app/.

### Q8 Retry / failure recording
- GET retried exactly once on ConnectError; POST never retried (app/mattermost.py:4,34-49).
- Failures recorded only as one structured JSON log line per tool call with outcome, mm_status, latency_ms (app/mcp.py:52,70-84; app/logging.py:45-46). No backoff, queue or dead-letter record.

### Q9 Deploy
- python:3.12-slim, uvicorn on 0.0.0.0:8080 with --proxy-headers, HEALTHCHECK on /health (Dockerfile:1,17-19).
- Compose: built from GitHub main, restart unless-stopped, same stack network as mattermost, expose 8080, domain chats.rmlab.cloud (coolify-service.snippet.yaml:5-7,10,14-15,17,24-25).
- Dependencies: fastapi, uvicorn[standard], mcp, httpx (requirements.txt:1-4).

### Q10 Tests
- Fake Mattermost served via an httpx transport (tests/acceptance/drivers/fake_mattermost.py:89-104) with users, teams, channels, posts, DMs (fake_mattermost.py:43-85) and REST handlers (fake_mattermost.py:105-215). No websocket emulation.
- pytest-asyncio available (requirements-dev.txt:2).

## Open questions (not answerable from this codebase)
- OQ1: Shape of Mattermost websocket events (posted, auth challenge, seq, reconnect/missed-event behaviour) for a bot token - external; belongs in market-research or architecture, not in this repo.
- OQ2: Whether Coolify provides a persistent volume for this service (snippet defines none; coolify-service.snippet.yaml:3-25) - operator fact for Rob.
- OQ3: Grok Bot side of the webhook wake (receiving URL, how it verifies a signature) - outside this repo.
- OQ4: Whether the transitive deps of uvicorn[standard] (requirements.txt:2) include a websocket client library usable here - not pinned in repo.
