---
id: ADR-0002
type: adr
phase: architecture
status: accepted         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: Eddie
date: 2026-10-25
links: [docs/design/2026-10-25-mmbridge-mcp.md, docs/architecture/2026-10-25-mmbridge-mcp.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0002: Mattermost access via async HTTP client to MATTERMOST_URL /api/v4

## Status
proposed

## Context
Mattermost runs in the same Coolify stack, reachable privately at `http://mattermost:8065` (`app/mattermost.py:12`, `coolify-service.snippet.yaml:13`). Options: official Go/JS drivers (wrong language), community `mattermostdriver` (sync, stale), or thin direct HTTP.

## Decision
We will use a thin `httpx.AsyncClient` wrapper over `MATTERMOST_URL` (default `http://mattermost:8065`) + `/api/v4`, passing the caller's bearer token (bot access token / PAT) per request with no client-level credential. Timeout 10 s; no automatic retries on writes; one retry on idempotent GETs for connect errors only. Endpoints: `users/me`, `users/me/teams`, `users/me/teams/{team_id}/channels`, `teams/name/{team}/channels/name/{channel}`, `channels/{id}/members/me`, `channels/{id}/posts`, `posts`, `users/username/{username}`, `channels/direct`, `users/ids`.

## Consequences
Positive: one small dependency, async, easy to stub with `respx`. Negative: we own a handful of endpoint shapes. Neutral: traffic stays on the private network.

## Prediction (scored in a later eng-retro)
- Expected outcome: Client module stays small (~200 lines) and all REQ-2..6 calls are covered by stubbed tests.
- Check date: after slice 2 ships
- What would prove it wrong: We end up reimplementing large parts of a driver (pagination, websockets) in v1.
- Score: unscored
