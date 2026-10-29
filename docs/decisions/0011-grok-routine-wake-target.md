---
id: ADR-0011
type: adr
phase: architecture
status: proposed         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-28
links: [docs/design/2026-10-28-grok-webhook-multibot.md, docs/architecture/2026-10-28-grok-webhook-multibot.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0011: Grok Bot routine wake target kind

## Status
proposed

## Context
REQ-B1/B2/B4. The Grok Bot wake contract was locked at CP-A: POST to a per-routine URL, `Authorization: Bearer <routine key>`, any JSON body, 200 = run started. ADR-0008 only sends HMAC headers and no Authorization (research Q1, app/wake.py:131-137). Alternatives in design B: relay service (rejected: another deploy), polling (rejected: latency).

## Decision
Each bot's wake target gets a `kind`: `signed` (ADR-0008, unchanged, default) or `grok`. For `grok` the dispatcher POSTs the version-2 JSON payload (architecture doc) with `Authorization: Bearer <key>` and `X-MMB-Delivery`; no HMAC. 2xx = delivered; 408/429/5xx/network = retry (2,4,8,16,32 s); other 4xx = permanent failure. Sender is a strategy chosen per row at send time from current config, so a kind switch applies to queued wakes (B4). ADR-0008 is amended, not superseded.

## Consequences
Positive: no relay, reuses queue/retry/dedupe. Negative: two wire formats to test; Bearer key is a long-lived secret (stored encrypted, redacted). Neutral: retry mapping for undocumented codes verified in the B-s1 spike.

## Prediction (scored in a later eng-retro)
- Expected outcome: a real Grok routine starts on every qualifying post in B-s1 CP-S; signed receivers keep verifying.
- Check date: after the increment B ship
- What would prove it wrong: the routine rejects or mangles our POST, or needs a different auth/format.
