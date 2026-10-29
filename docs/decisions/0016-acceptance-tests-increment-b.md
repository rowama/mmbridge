---
id: ADR-0016
type: adr
phase: architecture
status: proposed         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-28
links: [docs/design/2026-10-28-grok-webhook-multibot.md, docs/architecture/2026-10-28-grok-webhook-multibot.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0016: Acceptance tests for increment B (four-layer model)

## Status
proposed

## Context
Large work (PROCESS 13). ADR-0010 suite covers A; B adds a Grok routine target, round-trip replies and multiple bots. No UI.

## Decision
Specs in `tests/acceptance/specs/test_grok_multibot.py` tagged REQ-B1..B8, domain language. DSL gains `register_bot(name, kind)`, `grok_routine_down/up`, `assert_routine_started_once(bot, ...)`, `replay_last_wake`, `forge_wake`, `assert_replied(bot, where, text, thread)`, `revoke_token(bot)`, `assert_bot_failing(bot)`. Drivers: fake Grok routine (checks Bearer, records bodies, acts as the bot: calls claim_wake and replies via the real MCP bridge), fake Mattermost extended to multiple bot users, existing wake/MCP drivers. SUT = real container image with temp /data, fakes at the boundary, bots set via the real CLI. No Playwright (no UI). Specs + DSL interface locked at CP-C.

## Consequences
Positive: round-trip exercised end to end without a real Grok. Negative: fake routine drift from real Grok (mitigated by CP-S live run). Neutral: A specs remain as regression.

## Prediction (scored in a later eng-retro)
- Expected outcome: no shipped REQ-B without a passing spec; CP-S live run agrees with fakes.
- Check date: after the increment B ship
- What would prove it wrong: live Grok behaviour differs from the fake routine in a way specs missed.
