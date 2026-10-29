---
id: ADR-0015
type: adr
phase: architecture
status: accepted         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-28
links: [docs/design/2026-10-28-grok-webhook-multibot.md, docs/architecture/2026-10-28-grok-webhook-multibot.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0015: Thread replies via optional root_id

## Status
proposed

## Context
REQ-B5: reply as the same bot in the waking channel/DM, in the named thread when the wake carried a root. Tools take no root_id today (app/service.py:59, :90); bots already reply with their own token through /mcp (research Q7).

## Decision
Add optional `root_id` to `post_channel` and `dm_send`, passed to Mattermost `POST /posts`; validate id format; map MM 400/404 to `invalid_root`. The wake carries `reply` hints (tool, team, channel or username, root_id). No new reply-by-delivery tool. Self-wake already prevented by the filter.

## Consequences
Positive: additive, backward compatible MCP change. Negative: bot must pick the right tool (hints make it explicit). Neutral: top-level posts are answered top-level.

## Prediction (scored in a later eng-retro)
- Expected outcome: Eddie's replies land in the right channel, DM and thread at CP-S.
- Check date: after the increment B ship
- What would prove it wrong: bots misroute replies often enough that a reply-to-wake tool is needed.
