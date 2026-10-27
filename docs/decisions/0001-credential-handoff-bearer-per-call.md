---
id: ADR-0001
type: adr
phase: architecture
status: accepted         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: Eddie
date: 2026-10-25
links: [docs/design/2026-10-25-mmbridge-mcp.md, docs/architecture/2026-10-25-mmbridge-mcp.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0001: Credential handoff: per-call bearer Mattermost bot token, never stored

## Status
proposed

## Context
REQ-1 requires the bridge to act only as the calling bot's identity and refuse missing/invalid credentials; the design forbids a shared all-powerful credential. Grok Bot MCP connections can send a static custom header per connection. The current skeleton echoes all request headers including `Authorization` (`app/main.py:25`), which would leak tokens.

## Decision
We will require every MCP request to carry `Authorization: Bearer <mattermost-bot-token>`, configured per Grok Bot MCP connection. The bridge will hold the token only in request scope and never persist it; only a SHA-256 hash is kept in memory (rate-limit key, ADR-0004, and a 60 s `users/me` identity cache). Each call is validated via Mattermost `GET /api/v4/users/me` (cache miss). Missing/malformed header returns HTTP 401 before any Mattermost call; Mattermost 401 returns an `unauthorized` error. We will remove the catch-all echo route (unknown paths return 404) so no header is ever reflected.

## Consequences
Positive: no secret storage in the bridge; identity isolation is inherited from Mattermost; adding a bot needs no bridge deploy. Negative: token travels on every call (TLS terminates at Coolify proxy; private hop to container is plain HTTP inside the stack network); one extra `users/me` call per cache miss. Neutral: token rotation happens in Grok Bot connector config.

## Prediction (scored in a later eng-retro)
- Expected outcome: Two bots on the same bridge post under their own names; unauthenticated calls get 401 with zero Mattermost calls; no response or log contains a token (asserted by tests).
- Check date: after slice 1 ships
- What would prove it wrong: Grok Bot cannot send a per-connection Authorization header, or a token string appears in any response/log.
- Score: right (retro 2026-10-26-v0.2.0: live Grok Bot header reaches bridge; 401 w/o auth; no token in logs)
