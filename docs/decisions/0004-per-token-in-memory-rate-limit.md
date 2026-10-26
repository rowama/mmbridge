---
id: ADR-0004
type: adr
phase: architecture
status: accepted         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: Eddie
date: 2026-10-25
links: [docs/design/2026-10-25-mmbridge-mcp.md, docs/architecture/2026-10-25-mmbridge-mcp.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0004: Rate limiting: per-token in-memory token bucket (v1); Redis deferred

## Status
proposed

## Context
The bridge is public; a runaway bot loop could flood Mattermost. One container instance in v1; no shared store in the stack.

## Decision
We will apply an in-memory token bucket keyed by SHA-256(token): 60 tool calls/min (burst 10) and 20 writes/min (`post_channel` + `dm_send`) per token. Exceeded calls return `rate_limited` with `retry_after_s`. Requests without a valid-looking bearer are limited to 30/min per client IP. Limits are env-configurable (`RL_CALLS_PER_MIN`, `RL_WRITES_PER_MIN`, `RL_ANON_PER_MIN`). Redis-backed limiting is deferred (revisit: a second replica or multi-host deploy).

## Consequences
Positive: zero infra. Negative: limits reset on restart and are per replica. Neutral: Mattermost's own rate limit remains a backstop.

## Prediction (scored in a later eng-retro)
- Expected outcome: No legitimate bot use hits the limit; a loop is throttled within a minute.
- Check date: 2 weeks after first live use
- What would prove it wrong: Normal bot use regularly gets rate_limited, or we run more than one replica.
- Score: unscored
