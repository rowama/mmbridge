---
id: HANDO-20261026-architecture-proposed-cp-b-pending
type: handoff
phase: architecture
status: complete
owner_agent: grok-bot
date: 2026-10-26T23:57:56-05:00
links: [docs/architecture/2026-10-26-live-bots.md, thoughts/shared/verification/2026-10-26-live-bots-arch-review.md]
git_commit: b8c32e3
branch: main
next_skill: eng-plan
---
# Handoff: Architecture proposed, CP-B pending

## Task(s)
- CP-R logged (research accepted) - done.
- eng-architecture-review for A Live bots one-bot v1 - done, status in-review; ADR-0006..0010 proposed. Awaiting Rob CP-B.
- Cross-model review (advisory): stub written; awaiting Rob running Codex.

## Critical References
- PROJECT_STATE.md
- docs/architecture/2026-10-26-live-bots.md
- docs/decisions/0006..0010
- thoughts/shared/verification/2026-10-26-live-bots-arch-review.md

## Recent changes
- docs/architecture/2026-10-26-live-bots.md - new (components, contracts incl. wake HTTP + WS, schemas, sequence, failure table, flags/rollback, observability, STRIDE, OQ1-4, deploy prerequisites)
- docs/decisions/0006-encrypted-token-store.md
- docs/decisions/0007-mattermost-websocket-listener.md
- docs/decisions/0008-signed-wake-webhook.md
- docs/decisions/0009-listener-state-persistence.md
- docs/decisions/0010-acceptance-tests-live-bots.md - new, proposed
- docs/design/2026-10-26-live-bots.md - Architecture section links the doc
- thoughts/shared/verification/2026-10-26-live-bots-arch-review.md - stub awaiting Codex
- PROJECT_STATE.md - CP-R log row, phase architecture, CP-B pending

## Learnings
- `uvicorn[standard]` brings `websockets` only transitively; ADR-0007 pins it.
- `codex exec -o` overwrites the findings file; restore front matter + table after the run.

## Open items
- Deploy prerequisites (Rob, Coolify): persistent volume at /data writable by uid 10001; env secret MMB_STORE_KEY; replicas 1; LIVE_BOTS_ENABLED only after admin set-bot.
- For Rob at CP-B: residual risk that message text sits in state.db up to 7 days; residual duplicate on crash after receiver 2xx (idempotency key mitigates); Grok Bot may not verify HMAC (OQ3, deferred).
- Next: on CP-B accept, mark ADRs accepted, architecture approved, one Approval log row naming all files, note on ADR-0001 "partially superseded by ADR-0006"; then eng-plan.

## Artifacts
- docs/architecture/2026-10-26-live-bots.md
- docs/decisions/0006-encrypted-token-store.md
- docs/decisions/0007-mattermost-websocket-listener.md
- docs/decisions/0008-signed-wake-webhook.md
- docs/decisions/0009-listener-state-persistence.md
- docs/decisions/0010-acceptance-tests-live-bots.md
- thoughts/shared/verification/2026-10-26-live-bots-arch-review.md
- thoughts/shared/handoffs/2026-10-26_23-57-56_architecture-proposed-cp-b-pending.md
