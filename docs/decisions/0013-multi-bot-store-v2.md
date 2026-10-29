---
id: ADR-0013
type: adr
phase: architecture
status: proposed         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-28
links: [docs/design/2026-10-28-grok-webhook-multibot.md, docs/architecture/2026-10-28-grok-webhook-multibot.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0013: Multi-bot encrypted store v2 and admin CLI

## Status
proposed

## Context
REQ-B4/B6. Store holds one bot (app/store.py:88-106, :150-159); CLI has no name and replaces the bot (app/admin.py:73-79). ADR-0006 encryption stays.

## Decision
Store document version 2: `bots` map keyed by operator-chosen name; each bot has `token`, cached `user_id`, `wake` {url, secret} (always HMAC-signed per ADR-0008; Grok routines are reached through the relay, ADR-0011, so no Bearer routine key is stored in mmbridge). v1 loads as one bot named after its MM username and is rewritten as v2 on first save, keeping `bots.enc.v1.bak`. Tokens unique across bots. CLI: `set-bot --name` (create/replace one), `list`, `show NAME`, `remove-bot`, `status`, `--wake-secret-stdin`. Reload every 30 s, no redeploy.

## Consequences
Positive: one file, one key, same rotation; backward compatible. Negative: whole-file rewrite on every change (fine at <10 bots). Neutral: still no web admin (out of scope).

## Prediction (scored in a later eng-retro)
- Expected outcome: Rob registers 2+ bots and repoints a bot's wake URL with no redeploy; v0.3.0 store migrates untouched.
- Check date: after the increment B ship
- What would prove it wrong: migration loses or corrupts the v1 bot, or concurrent CLI writes clobber each other.
