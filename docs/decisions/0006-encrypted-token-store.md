---
id: ADR-0006
type: adr
phase: architecture
status: accepted         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-26
links: [docs/design/2026-10-26-live-bots.md, docs/architecture/2026-10-26-live-bots.md, docs/decisions/0001-credential-handoff-bearer-per-call.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0006: Encrypted token store (partially supersedes ADR-0001)

## Status
proposed

## Context
Design Q7 (Rob 2026-10-26): the Live bots listener must hold the bot's Mattermost token continuously, outside any MCP call, and changing the bot must not need a redeploy. ADR-0001 says tokens are never stored. That remains true for the MCP tool path; it cannot hold for the listener.

## Decision
We will store the one bot's config (token, wake URL, wake secret, chosen channel ids) in `/data/bots.enc`, a Fernet ciphertext (AES-128-CBC + HMAC-SHA256, `cryptography` package, new pinned dep) on the persistent volume, mode 0600. The key comes from env `MMB_STORE_KEY` (Coolify secret), never written to disk. Written only by the admin CLI (`python -m app.admin`) inside the container; no HTTP admin endpoint. Decrypted config is held in memory only; the token is never logged, returned, or placed in wake payloads. Key rotation: `admin rotate-key` re-encrypts (MultiFernet). This supersedes ADR-0001 only for the listener; the MCP path stays per-call bearer, never stored. On acceptance ADR-0001 gets a note "partially superseded by ADR-0006 (listener)".

## Consequences
Positive: no redeploy to change the bot; volume/backups leak only ciphertext. Negative: a long-lived secret now exists in the bridge; key+volume compromise exposes the token; operator needs container shell. Neutral: one bot in v1; format has `version` and a `bot` object so A6 can widen it to a list.

## Prediction (scored in a later eng-retro)
- Expected outcome: token never appears in logs, /health, tool output or wake payloads (tested); token rotation via CLI takes effect within 60 s without redeploy.
- Check date: after the Live bots v1 ship
- What would prove it wrong: a token string found in any log/output; Rob needs a redeploy to change the bot; key management proves too awkward in Coolify.
- Score: unclear (retro v0.3.0, 2026-10-28): no-token-in-output covered by tests; 60 s CLI rotation not exercised live, only in tests
