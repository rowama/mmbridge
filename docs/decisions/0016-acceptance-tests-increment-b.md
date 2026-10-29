---
id: ADR-0016
type: adr
phase: architecture
status: accepted         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
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
Large work (PROCESS 13). ADR-0010 suite covers A; B adds a Grok routine target reached via the HMAC->Bearer relay (ADR-0011), round-trip replies and multiple bots. No UI.

## Decision
Specs in `tests/acceptance/specs/test_grok_multibot.py` tagged REQ-B1..B8, domain language. DSL gains `register_bot(name, kind)`, `grok_routine_down/up`, `assert_routine_started_once(bot, ...)`, `relay_down/up`, `replay_last_wake`, `forge_wake`, `tamper_wake`, `assert_relay_rejected(reason)`, `assert_replied(bot, where, text, thread)`, `revoke_token(bot)`, `assert_bot_failing(bot)`. Drivers: real relay container in front of a fake Grok routine (fake checks Bearer, records bodies, acts as the bot and replies via the real MCP bridge; no claim_wake), fake Mattermost extended to multiple bot users, existing wake/MCP drivers. SUT = real mmbridge container image with temp /data plus the real relay image, fakes at the boundary, bots set via the real CLI. No Playwright (no UI). Specs + DSL interface locked at CP-C.

## Consequences
Positive: round-trip exercised end to end without a real Grok. Negative: two images in the harness; fake routine drift from real Grok (mitigated by CP-S live run). Neutral: A specs remain as regression.

## Prediction (scored in a later eng-retro)
- Expected outcome: no shipped REQ-B without a passing spec; CP-S live run agrees with fakes.
- Check date: after the increment B ship
- What would prove it wrong: live Grok behaviour differs from the fake routine in a way specs missed.
