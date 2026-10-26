---
id: ADR-0005
type: adr
phase: architecture
status: proposed         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: Eddie
date: 2026-10-25
links: [docs/design/2026-10-25-mmbridge-mcp.md, docs/architecture/2026-10-25-mmbridge-mcp.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0005: Observability: structured JSON logs without secrets; /health public

## Status
proposed

## Context
Coolify collects container stdout. Tokens must never appear in logs or responses (REQ-8). Coolify/Docker healthchecks call `/health` unauthenticated (`Dockerfile:15`).

## Decision
We will emit one JSON log line per tool call: timestamp, request id, tool, bot username/user id (from `users/me`), token hash prefix (8 hex), outcome code, Mattermost HTTP status, latency ms. We will never log headers, tokens or message bodies (lengths only). A redaction filter strips `Bearer ...` and token-like strings from log messages and exception text. `/health` stays public, unauthenticated, returns `{"ok": true}` only and does not call Mattermost (liveness only).

## Consequences
Positive: debuggable per bot without secrets. Negative: no message content in logs. Neutral: no metrics stack in v1.

## Prediction (scored in a later eng-retro)
- Expected outcome: Any failed call can be diagnosed from logs alone; grepping logs for test tokens finds nothing.
- Check date: after slice 1 ships
- What would prove it wrong: A token or message body is found in logs, or an incident cannot be diagnosed from logs.
- Score: unscored
