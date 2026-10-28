---
id: DESIG-20261028-grok-webhook-multibot
type: design
phase: discover
status: in-review        # input (pre-draft from an earlier phase) | draft | in-review | approved | superseded
owner_agent: grok-bot
date: 2026-10-28
links: [docs/design/2026-10-26-live-bots.md]
# implementer is a PROJECT_STATE working agreement; never name it here
---
# Design: Grok Bot webhook wake and multi-bot (increment B)

## Problem
- v0.3.0 Live bots ships signed wakes (HMAC-SHA256 over timestamp + body, delivery id, 300 s window; ADR-0008) to a generic per-bot wake URL. Today that URL points at a temporary HMAC receiver run by Ulrik, not at a Grok Bot. A wake therefore never reaches a bot that can act on it.
- Rob (operator) has to watch the temp receiver's logs by hand to confirm a wake arrived. There is no true end-to-end check: nobody has seen a Mattermost post cause a Grok Bot to answer in Mattermost.
- The bridge serves exactly one registered bot (multi-bot REQ-A6 deferred in the A scope REDUCE). A retro elsewhere is blocked waiting on 2+ bots being reachable through mmbridge.
- Evidence: TODOS P1 "Grok Bot webhook wake contract (mmbridge -> Grok Bot), not Ulrik temp HMAC receiver" (Rob 2026-10-28); TODOS REQ-A6 multi-bot deferral; lb5 CP-S notes (live check via receiver logs).

## Users and success metric
- Primary user: Rob, talking to his Grok Bots in his self-hosted Mattermost. Secondary: Ulrik (operator, no longer needs to run a temp receiver).
- Primary metric: one bot round-trip - a Mattermost post (channel or DM) wakes one configured Grok Bot through mmbridge and that bot's reply appears in the same channel/DM (thread when the wake named one), observed without reading any receiver log.
- Minor metric: 2+ bots registered on mmbridge, each successfully woken by posts that concern it.

## Narrowest wedge
Slice 1: adapt the existing mmbridge HMAC wake so it is delivered into the Grok Bot inbound webhook for one configured bot; that bot gets a real wake (not the temp receiver). Reply is not required by slice 1 alone. The same increment (one version, multiple slices; Rob option C "prudent") then adds: slice 2 round-trip reply in channel/DM; slice 3 multi-bot registry and routing.

## Requirements (acceptance criteria)
- [ ] REQ-B1: WHEN a qualifying post (as defined by REQ-A1/A2) concerns a bot whose wake target is a Grok Bot inbound webhook THE SYSTEM SHALL deliver the wake in the form that Grok Bot webhook accepts, so the Grok Bot is woken with channel, sender, message text, post id and thread root id when set.
- [ ] REQ-B2: THE SYSTEM SHALL authenticate every wake to the Grok Bot webhook in the way that webhook requires, and a wake that is forged, altered or replayed SHALL NOT wake the bot; no bot token or wake secret SHALL appear in logs, tool output or wake content.
- [ ] REQ-B3: WHEN delivery to the Grok Bot webhook fails THE SYSTEM SHALL keep the existing bounded retry with backoff and record the failure for the operator, delivering each post at most once to the bot.
- [ ] REQ-B4: WHEN the operator configures or changes a bot's wake target (Grok Bot webhook or generic signed webhook) THE SYSTEM SHALL apply it without a redeploy, and the generic signed webhook SHALL keep working for bots that use it.
- [ ] REQ-B5: WHEN a woken Grok Bot replies THE SYSTEM SHALL let that reply be posted as the same bot in the channel or DM that woke it (in the named thread when the wake carried a thread root), and the reply SHALL NOT wake the bot again.
- [ ] REQ-B6: THE SYSTEM SHALL keep a registry of two or more bots, each with its own Mattermost token and wake target, and SHALL route each qualifying post only to the bot(s) it concerns (membership/DM rules of REQ-A1/A2 per bot).
- [ ] REQ-B7: WHEN the post author is any registered bot THE SYSTEM SHALL NOT wake any registered bot from it (bot-to-bot out of this increment), and a bot's own posts never wake itself.
- [ ] REQ-B8: WHEN one registered bot's token is invalid or its wake target is down THE SYSTEM SHALL keep listening and waking for every other registered bot, and SHALL show the operator which bot is failing.

## Acceptance examples
- REQ-B1: Given bot "eddie" is registered with a Grok Bot webhook as wake target and is a member of Town Square, When Rob posts "what is on deck?" there, Then the Eddie Grok Bot is woken once with Town Square, Rob as sender and the text, and nobody had to read a receiver log. / Given the same, When Ulrik DMs eddie "ping", Then Eddie is woken once with Ulrik and "ping".
- REQ-B2: Given someone sends Eddie's webhook a wake not produced by mmbridge, Then Eddie is not woken. / Given a genuine wake is captured and re-sent ten minutes later, Then Eddie is not woken again. / Given any operator log after a day of wakes, Then no token or secret is visible.
- REQ-B3: Given Eddie's Grok Bot webhook is unreachable, When Rob posts in Town Square, Then delivery is retried and, if still failing, the operator sees one failed wake for that post; When the webhook recovers before retries run out, Then Eddie is woken exactly once.
- REQ-B4: Given eddie uses the generic signed webhook, When the operator switches eddie to its Grok Bot webhook, Then the next post wakes the Grok Bot with no redeploy. / Given bot "test" stays on the generic signed webhook, Then its wakes keep arriving signed as before.
- REQ-B5: Given Rob posts "@eddie status?" in Town Square, When Eddie is woken and answers "all green", Then "all green" appears in Town Square as Eddie, and Eddie is not woken by its own answer. / Given Rob replies inside an Eddie thread, Then Eddie's answer lands in that thread. / Given Rob DMs Eddie "hi", Then Eddie's answer appears in that DM.
- REQ-B6: Given bots "eddie" and "grok" are registered and only grok is a member of "dev", When Rob posts in "dev", Then grok is woken once and eddie is not. / Given both are in Town Square, When Rob posts there, Then each is woken once. / Given Rob DMs grok, Then only grok is woken.
- REQ-B7: Given eddie and grok are in Town Square, When eddie posts "@grok hi", Then neither bot is woken.
- REQ-B8: Given grok's token is revoked, When Rob posts in Town Square, Then eddie is still woken once and the operator sees grok marked failing.

## Constraints and assumptions
- Builds on v0.3.0 Live bots (listener, encrypted token store, state.db wake queue, signed dispatcher; ADR-0006..0010). Single container on Coolify.
- Order fixed by Rob 2026-10-28: Grok Bot webhook first, then multi-bot, same version, multi-slice (option C).
- Assumption: the reply path (REQ-B5) can reuse the existing v1 MCP post tools with the bot's own token; architecture confirms.
- [NEEDS CLARIFICATION: What does the Grok Bot inbound webhook accept for a wake - its endpoint per bot, how it authenticates callers (shared secret / HMAC header / bearer token / signed URL), and the expected body shape? Rob to provide the Grok Bot webhook settings or docs for one bot (e.g. Eddie). This drives REQ-B1/B2.]

## Out of scope
- Web admin UI; bot-to-bot wakes and loop caps (REQ-A3 bot-to-bot part); channel ignore-list. Auto-accept invites (REQ-A5 suite) stays in TODOS.

## Alternatives considered
| Option | Pros | Cons |
|---|---|---|
| Adapter in mmbridge dispatcher: per-bot wake target kind (generic signed / Grok Bot webhook) | one place, reuses queue/retry/dedupe, no extra service | must match Grok Bot webhook contract exactly; two formats to maintain |
| Small relay service that verifies mmbridge HMAC and forwards to Grok Bot | mmbridge unchanged | another deploy to run (the temp-receiver pain again), extra hop and secret |
| Grok Bot routine polls dm_read/read_channel | no webhook contract needed | latency minutes, cost, misses round-trip metric; the reason Live bots was built |

## Scope decision (filled by eng-scope-review)
Baseline: the Requirements list above as approved at CP-A (REQ ids).
Mode (relative to that baseline): <expand | selective | hold | reduce>
- In:
- Out (also recorded in TODOS.md):

## Architecture (filled by eng-architecture-review)
<to be filled after CP-A>

## Open questions
- Q1 (Rob): Grok Bot inbound webhook contract - see NEEDS CLARIFICATION above.
