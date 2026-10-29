---
id: ADR-0012
type: adr
phase: architecture
status: proposed         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-28
links: [docs/design/2026-10-28-grok-webhook-multibot.md, docs/architecture/2026-10-28-grok-webhook-multibot.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0012: Wake authenticity and replay defence via claim_wake

## Status
proposed

## Context
REQ-B2: forged, altered or replayed wakes must not wake the bot. The Grok routine only checks a static Bearer key; it cannot verify HMAC or timestamps, so mmbridge-side protection is needed (design B constraints).

## Decision
Add MCP tool `claim_wake(delivery_id)`, authenticated by the calling bot's MM token. It succeeds once per delivered wake row owned by that token, within `WAKE_CLAIM_TTL_S` (900 s), sets `claimed_at`, and returns the trusted context (channel, sender, post, reply hints) from state.db. The wake body and routine prompt instruct the bot to call it first and act only on `ok`, using the returned context. Unknown/foreign/claimed/expired -> no action.

## Consequences
Positive: forgery (unknown id), tampering (trusted context) and replay (already_claimed/expired) defeated even if the routine key leaks. Negative: relies on the Grok Bot following its routine instructions (accepted risk, verified at CP-S); one extra MCP call per wake. Neutral: gives round-trip latency metric (delivered->claimed).

## Prediction (scored in a later eng-retro)
- Expected outcome: every real wake is claimed once; replayed and forged wakes in specs and CP-S get no reply.
- Check date: after the increment B ship
- What would prove it wrong: Grok Bots routinely skip the claim step, or claim latency breaks the round-trip metric.
