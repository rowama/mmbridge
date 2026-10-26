# TODOS
<!-- Deferred work and scope cuts. Format: - **<title>** (filed YYYY-MM-DD, from <artifact>) — <why deferred>. **Effort:** S/M/L. **Priority:** P1–P3. -->
- **@mention-only responding and channel/DM activity wake-ups** (filed 2026-10-25, from [design scope](docs/design/2026-10-25-mmbridge-mcp.md#scope-decision-filled-by-eng-scope-review)) — needs event/websocket path and a wake callback into Grok Bot; outside v1 wedge. **Effort:** L. **Priority:** P2.
- **Auto-join channels / handle invites** (filed 2026-10-25, from [design scope](docs/design/2026-10-25-mmbridge-mcp.md#scope-decision-filled-by-eng-scope-review)) — Rob adds bots to channels manually in v1; REQ-7 forbids implicit join. **Effort:** S. **Priority:** P3.
- **Multi-bot routing/registry** (filed 2026-10-25, from [design scope](docs/design/2026-10-25-mmbridge-mcp.md#scope-decision-filled-by-eng-scope-review)) — v1 uses per-connection credential; no registry needed. **Effort:** M. **Priority:** P3.
- **Thread replies, reactions, file attachments** (filed 2026-10-25, from [design scope](docs/design/2026-10-25-mmbridge-mcp.md#scope-decision-filled-by-eng-scope-review)) — Slack-parity extras, not needed for success metric. **Effort:** M. **Priority:** P2.
- **Scope acceptance conftest hook to tests/acceptance** (filed 2026-10-26, from [s1 verify](thoughts/shared/verification/2026-10-26-s1-verify.md)) — `pytest` from repo root skips all unit tests ("not a mcp-channel spec"). **Effort:** S. **Priority:** P1.
- **Trust only the Coolify proxy for X-Forwarded-For** (filed 2026-10-26, from [s1 verify](thoughts/shared/verification/2026-10-26-s1-verify.md)) — `--forwarded-allow-ips *` lets clients spoof IP and dodge the anon rate limit. **Effort:** S. **Priority:** P1 (pending codex review).
- **Reconcile ADR-0004 burst (10) vs implemented capacity (60)** (filed 2026-10-26, from [s1 verify](thoughts/shared/verification/2026-10-26-s1-verify.md)) — Rob to accept deviation or amend ADR. **Effort:** S. **Priority:** P2.
- **Add a linter (ruff) to the gate** (filed 2026-10-26, from [s1 verify](thoughts/shared/verification/2026-10-26-s1-verify.md)) — no lint step exists for DoD. **Effort:** S. **Priority:** P3.
- **Plan for mcp 2.x (FastMCP→MCPServer)** (filed 2026-10-26, from [s1 verify](thoughts/shared/verification/2026-10-26-s1-verify.md)) — pinned 1.30.0. **Effort:** S. **Priority:** P3.

## Follow-ups
- [ ] P2: Case-insensitive Bearer scheme match in auth.py (F2 accepted-risk 2026-10-26)
