---
id: PLAN-20261027-live-bots-delta-no-allowlist
type: plan
phase: plan
status: draft
owner_agent: grok-bot
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md, docs/design/2026-10-26-live-bots.md, docs/architecture/2026-10-26-live-bots.md, tests/acceptance/specs/test_live_bots.py]
---
# Plan delta (draft, needs CP-C): drop the channel allow-list (Live bots v1)

Source: Rob decision 2026-10-27 (via Eddie). Amends [the approved plan](2026-10-27-live-bots.md); not yet approved, specs NOT re-locked.

## Overview
Remove the per-bot channel allow-list; channel wakes come from Mattermost membership plus a wake rule.

## Desired End State
One bot, configured with token + wake URL + secret only, wakes on DMs and on @mentions in any channel it is a member of; specs re-locked at CP-C.

## What We're NOT Doing
Ignore-list, auto-join (REQ-A5), multi-bot (REQ-A6), thread-follow wakes.

## Decision
- No per-bot channel allow-list, no `--channels` CLI step.
- Bot wakes on (1) every DM to the bot (unchanged, REQ-A2) and (2) channel posts (O/P) in channels the bot is a Mattermost member of WHERE a wake rule fires.
- Optional ignore-list: out of scope (later, only if blast radius becomes real).

## Open questions for Rob (answer with CP-C)
- OQ-D1 Channel wake rule: proposed = **@mention of the bot only** (`@eddie`, via `data.mentions` containing the bot user id; regex `@<username>\b` fallback). Alternative = every post in any member channel (old Q3 "all activity", now unbounded since there is no list). Rob's wording "(@mention etc.)" read as mention-only.
- OQ-D2 `@channel` / `@here` / `@all`: proposed = do NOT wake (blast radius).
- OQ-D3 Thread replies in a thread the bot posted in, without @mention: proposed = do NOT wake in v1 (thread behaviour stays deferred).

## Requirement / doc changes (CP-A-level text, ride along with CP-C)
- docs/design/2026-10-26-live-bots.md: REQ-A1 -> "WHEN a new post by someone else in a channel the bot is a member of @mentions the bot THE SYSTEM SHALL deliver one wake"; RESOLVED Q3 note superseded; metric "chosen channel" -> "member channel @mention".
- docs/architecture/2026-10-26-live-bots.md: store schema drops `channels`; CLI line drops `--channels`; filter rules (line ~64): O/P wake only if mentioned; catch-up iterates the bot's member channels (`GET /users/me/teams/{team}/channels`) + DM channels, not a chosen list.
- ADR-0006 text: config = token, wake URL, wake secret (no channel ids). ADR-0007 unchanged in substance.
- Plan: Phase 1 PR-6 (`channels` validation) removed; Phase 3 `decide(event, bot_user_id, chosen)` -> `decide(event, bot_user_id, bot_username)`; Phase 5 PR-2 "channel set change" and PR-3 catch-up list -> member channels; deploy step `set-bot ... --channels main/town-square` -> no `--channels`.

## Code touch points
| Area | File | Change |
|---|---|---|
| store | app/store.py | `BotConfig.channels` removed (or optional, default `[]`, ignored); `validate` drops the channels rule; `load` tolerates a legacy `channels` key (ignored) so existing `/data/bots.enc` keeps loading; `version` stays 1 |
| admin | app/admin.py | drop `--channels`, `_channel_specs`, member-channel resolution (`_member_channel` import); `show`/`set-bot` output without channels; passing `--channels` -> clear `invalid_argument: channels no longer used` |
| filter | app/live_filter.py | O/P: wake only if bot mentioned (mentions list or `@username` word match); drop `chosen` arg; D unchanged; own/system/G drops unchanged |
| listener | app/listener.py | pass bot username (from users/me) instead of chosen set |
| catch-up (lb5) | app/listener.py / lb5 | iterate member + DM channels; still only enqueue posts that pass `decide` |
| unit tests | tests/unit/test_store.py:105-106, test_admin.py, test_live_filter.py, test_listener.py | channels cases removed; new filter cases: mention wakes, no-mention drops, @channel drops, mention of another user drops |
| DSL | tests/acceptance/dsl.py:147 | `given_live_bot(name, channels=())` -> `given_live_bot(name)` (DSL interface change -> re-lock) |
| driver | tests/acceptance/drivers/live.py | admin setup without `--channels`; fake MM `posted` event carries `mentions` |
| specs (locked) | tests/acceptance/specs/test_live_bots.py | see below |
| lock | tests/acceptance/spec-lock.json | regenerate via eng-spec after CP-C (new sha) |

## Locked spec changes (need CP-C re-lock)
- `test_mention_in_chosen_channel_wakes_bot_once` -> `test_mention_in_member_channel_wakes_bot_once` (drop `channels=`).
- `test_post_without_mention_in_chosen_channel_also_wakes_bot` -> INVERT to `test_post_without_mention_in_member_channel_does_not_wake` (if OQ-D1 = mention-only).
- `test_post_in_member_channel_not_chosen_does_not_wake` -> DELETE (no "chosen" concept); optionally add `test_channel_wide_mention_does_not_wake` (`@channel`, OQ-D2).
- `test_bot_token_never_appears_in_logs_output_or_wakes`: post text "hello eddie" -> "@eddie hello" (else no wake under mention-only).
- All other specs: remove the `channels=` argument only.
- Plan PR-12 node-id list for lb4 updated to the new names.

## Unblocking lb4 (recommended)
Minimal change, no spec edits, no re-lock: make the store and `admin set-bot` accept an EMPTY channel list (lb4 Option A, ~10 lines in `store.validate` + admin; flip `tests/unit/test_store.py:106` `_raw(channels=[])` to accepted). The two blocked specs (`test_dm_to_bot_wakes_bot_once`, `test_forged_wake_is_rejected` use `channels=[]`) then pass -> 7/7 under the CURRENT lock. This is forward-compatible with full removal.
Then, after Rob's CP-C on this delta, do the allow-list removal as its own slice (proposed `lb4b-drop-allowlist`, before lb5) or fold into lb5; lb5 catch-up must use member channels either way.

## Phase 1: Drop allow-list (proposed slice lb4b, after lb4)
Changes per the touch-point table above.
### Success Criteria
#### Automated Verification
- [ ] `.venv/bin/pytest tests/unit -q` exit 0 incl. new mention/no-mention/@channel filter cases and legacy-`channels`-key load test
- [ ] `.venv/bin/pytest -q --channel live tests/acceptance/specs/test_live_bots.py` (re-locked specs for lb4b scope) exit 0; `python3 .eng/bin/eng-spec status .` matches the new lock; `python3 .eng/bin/eng-check .` exit 0
#### Manual Verification
- [ ] Rob: after redeploy, `set-bot` without `--channels`; `@eddie` in a member channel wakes once; a plain post there does not; a DM wakes.
