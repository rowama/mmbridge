---
id: DESIG-20261025-mmbridge-mcp
type: design
phase: discover
status: in-review        # input (pre-draft from an earlier phase) | draft | in-review | approved | superseded
owner_agent: Eddie
date: 2026-10-25
links: [PROJECT_STATE.md]
# implementer is a PROJECT_STATE working agreement; never name it here
---
# Design: mmbridge MCP (Grok Bot <-> Mattermost)

## Problem
Rob's Grok Bots cannot read or post in Mattermost at all. Rob will not pay for Slack groups, so he installed a self-hosted Mattermost, then found Grok Bot has no way to use it. Today there is no workaround: any bot-to-team conversation in Mattermost simply does not happen. Grok Bot already has working Slack communication, so the gap is specific to Mattermost.

## Users and success metric
- Primary user: Rob, through his Grok Bots (each bot acting under its own Mattermost bot identity).
- Success metric: a Grok Bot, connected to the bridge with one Mattermost bot identity, can post a message into a channel it belongs to and into a DM with Rob, and can read back recent messages from both, with the posts visible to Rob in Mattermost under the bot's name. Target: working end to end within the first slice, no manual relay by Rob.
- Long-term goal (not v1): Slack parity where Mattermost allows - per-bot identities, DM, read/write posts, joining/invite handling, listening but responding only to @mention, waking on channel/DM activity.

## Narrowest wedge
One Grok Bot, one Mattermost bot identity: list the channels it belongs to, read recent posts from a channel or DM, post into a channel, and send/read a DM with a named Mattermost user. Nothing proactive: the bot acts only when it calls the bridge.

## Requirements (acceptance criteria)
- [ ] REQ-1: WHEN a Grok Bot connects to the bridge presenting its Mattermost bot credential THE SYSTEM SHALL act in Mattermost only as that bot identity, and SHALL refuse connections with a missing or invalid credential.
- [ ] REQ-2: WHEN the bot asks for its channels THE SYSTEM SHALL return the channels (name and team) that the bot identity is already a member of.
- [ ] REQ-3: WHEN the bot posts a message to a channel it belongs to THE SYSTEM SHALL create the post in that channel under the bot's identity and return a reference to the new post.
- [ ] REQ-4: WHEN the bot asks to read a channel it belongs to THE SYSTEM SHALL return the most recent posts (author, time, text), newest-limited to a requested count with a sensible default and maximum.
- [ ] REQ-5: WHEN the bot sends a DM to a Mattermost user by username THE SYSTEM SHALL deliver it in the direct conversation between the bot and that user, opening the conversation if it does not yet exist.
- [ ] REQ-6: WHEN the bot asks to read its DM with a Mattermost user THE SYSTEM SHALL return the most recent posts of that direct conversation in the same shape as REQ-4.
- [ ] REQ-7: WHEN the bot targets a channel it is not a member of, an unknown channel, or an unknown user THE SYSTEM SHALL return a clear error explaining why and SHALL NOT join the channel or post anywhere.
- [ ] REQ-8: WHEN Mattermost is unreachable or rejects a request THE SYSTEM SHALL return a clear error to the bot without exposing the bot's credential.

## Acceptance examples
- REQ-1 / example 1: GIVEN bot "eddie" has a valid credential WHEN it connects and posts THEN the post appears in Mattermost authored by "eddie".
- REQ-1 / example 2: GIVEN a caller with no credential WHEN it tries to list channels THEN it is refused and nothing is read from Mattermost.
- REQ-2 / example 1: GIVEN "eddie" is a member of "town-square" and "dev" in team "rmlab" WHEN it asks for its channels THEN it gets "town-square" and "dev" with team "rmlab", and not channels it has not joined.
- REQ-3 / example 1: GIVEN "eddie" is in "dev" WHEN it posts "build is green" to "dev" THEN Rob sees "build is green" from "eddie" in "dev".
- REQ-4 / example 1: GIVEN "dev" has 30 posts WHEN "eddie" reads "dev" asking for 5 THEN it gets the 5 newest posts with author, time and text.
- REQ-4 / example 2: GIVEN "dev" has 30 posts WHEN "eddie" reads "dev" without a count THEN it gets the default number of newest posts.
- REQ-5 / example 1: GIVEN "eddie" has never messaged "rob" WHEN it sends "hello" to "rob" THEN a direct conversation opens and Rob sees "hello" from "eddie".
- REQ-5 / example 2: GIVEN an existing DM between "eddie" and "rob" WHEN it sends "again" THEN it lands in that same conversation.
- REQ-6 / example 1: GIVEN Rob wrote "ping" to "eddie" in their DM WHEN "eddie" reads its DM with "rob" THEN "ping" from "rob" is among the returned posts.
- REQ-7 / example 1: GIVEN "eddie" is not in "finance" WHEN it posts to "finance" THEN it is told it is not a member, it does not join, and nothing is posted.
- REQ-7 / example 2: GIVEN no user "nobody" exists WHEN "eddie" sends a DM to "nobody" THEN it is told the user is unknown.
- REQ-8 / example 1: GIVEN Mattermost is down WHEN "eddie" posts THEN it is told Mattermost is unavailable and the message does not contain its credential.

## Constraints and assumptions
- Bridge is already reachable over public HTTPS on Coolify; Mattermost runs in the same stack and is reachable privately by the bridge.
- Bot accounts and bot access tokens are enabled in Mattermost; Rob creates each bot identity and adds it to channels himself in v1.
- Each Grok Bot supplies its own bot credential; the bridge holds no shared all-powerful credential.
- Side venture: speed over polish; slicing toward Slack parity is our call.

## Alternatives considered
| Option | Pros | Cons |
|---|---|---|
| A. Remote MCP bridge, per-bot credential passed by each Grok Bot (chosen) | Native tools for Grok Bot; per-bot identities from day one; fits existing Coolify deploy | Must build and host a small service |
| B. Mattermost incoming/outgoing webhooks only | No new service logic; built in | Write-only incoming; no reading or DMs; no per-bot identity |
| C. Pay for Slack groups / use Slack | Already works with Grok Bot | Rob explicitly rejected the cost; abandons installed Mattermost |

## Scope decision (filled by eng-scope-review)
Baseline: the Requirements list above as approved at CP-A (REQ ids).
Mode (relative to that baseline): <expand | selective | hold | reduce>
- In:
- Out (also recorded in TODOS.md): @mention-only responding and channel/DM activity wake-ups; auto-joining channels or answering invites; multi-bot routing/registry. (Proposed for later increments.)

## Architecture (filled by eng-architecture-review)
<not yet>

## Open questions
- For CP-B (architecture): exact credential handoff from Grok Bot to the bridge (header vs. per-bot connector config) and rate limiting.
