---
id: ADR-0014
type: adr
phase: architecture
status: proposed         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-28
links: [docs/design/2026-10-28-grok-webhook-multibot.md, docs/architecture/2026-10-28-grok-webhook-multibot.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0014: Per-bot listeners, shared dispatcher and state.db v2

## Status
proposed

## Context
REQ-B6/B7/B8. Runtime builds one Listener/Dispatcher (app/live.py:146-157); wakes keyed by post_id only (app/state.py:25-39); filter knows one bot id (app/live_filter.py:70); health has one status word.

## Decision
One Listener task per bot (own websocket on its token, own membership, own catch-up), each under `supervise`, started/stopped by a BotSupervisor on store reload. One shared Dispatcher with per-bot in-flight cap 2. state.db schema v2: wakes and cursors keyed by (bot, ...), per-bot meta keys, `claimed_at`; migrated in one transaction with backup. Filter drops posts authored by any registered bot user id. Per-bot status map exposed via `admin status`; /health shows only counts.

## Consequences
Positive: failure isolation per bot (B8), exact once-per-bot dedupe, simple reuse of the proven Listener. Negative: N websockets (fine for a handful of bots); migration risk. Neutral: a non-registered integration bot can still wake bots (same as today).

## Prediction (scored in a later eng-retro)
- Expected outcome: two bots woken correctly with one revoked token not affecting the other, in specs and CP-S.
- Check date: after the increment B ship
- What would prove it wrong: websocket count or per-bot state causes resource or ordering bugs, or migration fails in production.
