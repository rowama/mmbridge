---
id: ADR-0003
type: adr
phase: architecture
status: proposed         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: Eddie
date: 2026-10-25
links: [docs/design/2026-10-25-mmbridge-mcp.md, docs/architecture/2026-10-25-mmbridge-mcp.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0003: MCP surface: Streamable HTTP at https://chats.rmlab.cloud/mcp with five tools

## Status
proposed

## Context
Grok Bot connects to remote MCP servers over HTTPS. The MCP spec deprecates HTTP+SSE in favour of Streamable HTTP. The official Python `mcp` SDK (FastMCP) provides a Streamable HTTP ASGI app that mounts into FastAPI.

## Decision
We will mount the official `mcp` SDK (pinned) Streamable HTTP transport at `/mcp`, stateless, JSON responses, inside the existing FastAPI app. Tools: `list_channels()`, `post_channel(team, channel, message)`, `read_channel(team, channel, limit=20, max 100)`, `dm_send(username, message)`, `dm_read(username, limit=20, max 100)`. Tool errors are results with `isError: true` and structured `{code, message}`; codes: `unauthorized`, `not_member`, `unknown_channel`, `unknown_user`, `invalid_argument`, `rate_limited`, `mattermost_unavailable`, `mattermost_error`. SSE is a fallback only if Grok Bot cannot use Streamable HTTP.

## Consequences
Positive: standard transport, no session state. Negative: SDK churn (pin it). Neutral: tool names become a public contract.

## Prediction (scored in a later eng-retro)
- Expected outcome: A Grok Bot connector lists the five tools and passes the REQ-1..8 acceptance examples end to end.
- Check date: after slice 1 ships (first live connector test)
- What would prove it wrong: Grok Bot's connector cannot handshake with Streamable HTTP and needs SSE.
- Score: unscored
