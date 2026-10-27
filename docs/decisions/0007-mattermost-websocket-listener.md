---
id: ADR-0007
type: adr
phase: architecture
status: accepted         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-26
links: [docs/design/2026-10-26-live-bots.md, docs/architecture/2026-10-26-live-bots.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0007: Mattermost websocket listener inside the bridge process

## Status
proposed

## Context
REQ-A1/A2/A4 need real-time post events. Research: no background task or WS client exists; single uvicorn process (Dockerfile:19); `websockets` arrives only transitively via `uvicorn[standard]` (OQ4). Mattermost exposes `/api/v4/websocket` with header auth, `hello{connection_id}`, per-event `seq`, and resume via `connection_id` + `sequence_number` query params (OQ1).

## Decision
We will run one asyncio listener task from the FastAPI lifespan, gated by `LIVE_BOTS_ENABLED`, using the `websockets` library pinned explicitly in requirements.txt. Auth with `Authorization: Bearer` on the handshake. Track `seq`; on reconnect pass `connection_id` and next sequence; if the hello brings a new connection_id (or a seq gap) run a REST catch-up of chosen + DM channels since the stored cursor, bounded by `LIVE_CATCHUP_MINUTES` (default 15). Ping every 30 s, treat 60 s silence as dead; backoff 1 s doubling to 60 s with jitter. Exactly one listener per deployment (replicas=1 plus SQLite lease, ADR-0009). Rejected: separate worker container (two deploys, shared volume); MM outgoing webhooks (no DMs); polling (latency).

## Consequences
Positive: one deploy, real-time, reuses existing MM REST client. Negative: bridge becomes stateful; listener bugs share the process with MCP tools (mitigated: task exceptions caught and restarted, flag to disable). Neutral: Mattermost version-specific behaviour verified in the first slice.

## Prediction (scored in a later eng-retro)
- Expected outcome: >=95% of wakes within 10 s over 7 days; a 30 s connection drop yields exactly one wake per gap post.
- Check date: 7 days after v1 is enabled
- What would prove it wrong: reconnect loops, missed posts after MM restarts, or MCP tool latency regressions caused by the listener.
- Score: unscored
