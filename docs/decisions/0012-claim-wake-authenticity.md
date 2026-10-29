---
id: ADR-0012
type: adr
phase: architecture
status: rejected         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-28
links: [docs/design/2026-10-28-grok-webhook-multibot.md, docs/architecture/2026-10-28-grok-webhook-multibot.md]
superseded_by: ADR-0011 (HMAC->Bearer wake relay)
revisit: only if a future wake path reaches Grok Bot without HMAC verification in front of it
---
# ADR-0012: Wake authenticity and replay defence via claim_wake

## Status
rejected (2026-10-28, Rob decision). Kept for the record.

## Context
REQ-B2: forged, altered or replayed wakes must not wake the bot. The earlier ADR-0011 draft sent wakes straight from mmbridge to the Grok routine with a static Bearer key, which cannot verify HMAC or timestamps; `claim_wake` was proposed to recover authenticity on the mmbridge side.

## Original proposal (not adopted)
MCP tool `claim_wake(delivery_id)`, authenticated by the calling bot's MM token; succeeds once per delivered row within 900 s, sets `claimed_at`, returns trusted context; the routine prompt tells the bot to act only on `ok`.

## Decision
Rejected for increment B. Authenticity is enforced before the routine is woken: mmbridge keeps HMAC-signed wakes (ADR-0008) and the relay (ADR-0011) verifies signature, timestamp window and delivery-id dedupe, then holds the Bearer key. No `claim_wake` tool, no `claimed_at` column, no claim instruction in the wake body.

## Consequences
Positive: no extra MCP call per wake; no reliance on the Grok Bot obeying a claim instruction; smaller MCP surface and schema. Negative: if the routine Bearer key leaks from the relay, nothing on the mmbridge side stops a direct forged wake (accepted in ADR-0011). Neutral: round-trip latency metric delivered->claimed is dropped; use delivered->reply post time at CP-S instead.

## Prediction (scored in a later eng-retro)
- Expected outcome: no forged or replayed wake reaches a routine in specs or CP-S without claim_wake.
- Check date: after the increment B ship
- What would prove it wrong: a forged/replayed wake produces a bot reply, showing a mmbridge-side check is still needed.
