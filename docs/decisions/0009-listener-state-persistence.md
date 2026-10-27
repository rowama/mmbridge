---
id: ADR-0009
type: adr
phase: architecture
status: proposed         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-26
links: [docs/design/2026-10-26-live-bots.md, docs/architecture/2026-10-26-live-bots.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0009: Listener state in SQLite on a persistent volume

## Status
proposed

## Context
REQ-A4 needs at-most-once delivery and catch-up across reconnects and restarts; REQ-A8 needs a durable failure record. Today all state is in memory and no volume exists (research Q5, OQ2).

## Decision
We will keep `/data/state.db` (stdlib `sqlite3`, WAL, via `asyncio.to_thread`) with tables `wakes` (post_id PK = dedupe ledger + delivery queue), `cursors` (per-channel last create_at) and `meta` (connection_id, seq, single-listener lease). `INSERT OR IGNORE` on post_id is the only enqueue gate for both socket and catch-up. Terminal rows pruned after 7 days. A Coolify persistent volume at `/data` writable by uid 10001 is a required deploy prerequisite; without it the listener refuses to start (MCP unaffected). Rejected: Postgres/Redis (extra service), in-memory (loses dedupe on restart).

## Consequences
Positive: zero new services; durable dedupe and queue. Negative: needs a volume; single writer means one replica. Neutral: residual duplicate if the process dies between receiver 2xx and marking delivered - mitigated by the `X-MMB-Delivery` idempotency key.

## Prediction (scored in a later eng-retro)
- Expected outcome: 0 duplicate wakes from the bridge over 7 days including at least one restart.
- Check date: 7 days after v1 is enabled
- What would prove it wrong: SQLite lock errors under load, or duplicate wakes logged after restarts.
- Score: unscored
