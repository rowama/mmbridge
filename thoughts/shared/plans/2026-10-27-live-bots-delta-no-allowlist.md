---
id: PLAN-20261027-live-bots-delta-no-allowlist
type: plan
phase: plan
status: approved
owner_agent: grok-bot
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md, docs/design/2026-10-26-live-bots.md, docs/architecture/2026-10-26-live-bots.md, tests/acceptance/specs/test_live_bots.py]
plan_review: thoughts/shared/verification/2026-10-27-live-bots-delta-no-allowlist-plan-review-2.md
---
# Plan delta: drop the channel allow-list (Live bots v1)

Source: Rob decision 2026-10-27 (via Eddie). Amends [the approved plan](2026-10-27-live-bots.md). Rob decided the wake rules below on 2026-10-27; CP-C is logged by Rob once the plan-review highs are fixed AND he approves the candidate speclock hash below; slice lb4b applies the re-lock.

## Overview
Remove the per-bot channel allow-list; channel wakes come from Mattermost membership plus a wake rule.

## Desired End State
One bot, configured with token + wake URL + secret only, wakes on DMs and on every post (incl. @channel/@here/@all and thread replies) in any channel it is a member of; specs re-locked in lb4b.

## What We're NOT Doing
Ignore-list (later), auto-join (REQ-A5), multi-bot (REQ-A6), mention-only filtering.

## Decision
- No per-bot channel allow-list, no `--channels` CLI step.
- Bot wakes on (1) every DM to the bot (unchanged, REQ-A2) and (2) channel posts (O/P) in channels the bot is a Mattermost member of WHERE a wake rule fires.
- Optional ignore-list: out of scope (later, only if blast radius becomes real).

## Wake rules (Rob 2026-10-27, relayed by Eddie)
- D1 Channel wake rule: **every post** (by someone else, non-system) in any channel the bot is a Mattermost member of. No mention required.
- D2 `@channel` / `@here` / `@all`: **wake** (same as any post).
- D3 Thread-follow: **wake** on threaded replies in threads the bot posted in. In v1 this is already covered by D1 (all posts in member channels wake, replies carry `root_id`); keep a spec so it stays true if an ignore-list is added later.
- DMs still wake (REQ-A2). Group DMs (G) still dropped.

## Requirement / doc changes (CP-A-level text, ride along with CP-C)
- docs/design/2026-10-26-live-bots.md: REQ-A1 -> "WHEN any new post by someone else appears in a channel the bot is a member of THE SYSTEM SHALL deliver one wake"; RESOLVED Q3 note superseded; metric "chosen channel" -> "member channel".
- docs/architecture/2026-10-26-live-bots.md: store schema drops `channels`; CLI line drops `--channels`; filter rules (line ~64): O/P wake whenever the post reaches the bot's websocket (membership is the filter); catch-up iterates the bot's member channels (`GET /users/me/teams/{team}/channels`) + DM channels, not a chosen list.
- ADR-0006 text: config = token, wake URL, wake secret (no channel ids). ADR-0007 unchanged in substance.
- Plan: Phase 1 PR-6 (`channels` validation) removed; Phase 3 `decide(event, bot_user_id, chosen)` -> `decide(event, bot_user_id)`; Phase 5 PR-2 "channel set change" and PR-3 catch-up list -> member channels; deploy step `set-bot ... --channels main/town-square` -> no `--channels`.

## Code touch points
| Area | File | Change |
|---|---|---|
| store | app/store.py | `BotConfig.channels` removed (or optional, default `[]`, ignored); `validate` drops the channels rule; `load` tolerates a legacy `channels` key (ignored) so existing `/data/bots.enc` keeps loading; `version` stays 1 |
| admin | app/admin.py | drop `--channels`, `_channel_specs`, member-channel resolution (`_member_channel` import); `show`/`set-bot` output without channels; passing `--channels` -> clear `invalid_argument: channels no longer used` |
| filter | app/live_filter.py | O/P: always wake (membership is the filter); drop `chosen` arg; D unchanged; own/system/G drops unchanged |
| listener | app/listener.py | stop passing a chosen set |
| catch-up (lb5) | app/listener.py / lb5 | iterate member + DM channels; still only enqueue posts that pass `decide` |
| unit tests | tests/unit/test_store.py:105-106, test_admin.py, test_live_filter.py, test_listener.py | channels cases removed; filter cases: any member-channel post wakes, @channel wakes, thread reply wakes with root_id |
| DSL | tests/acceptance/dsl.py:147 | `given_live_bot(name, channels=())` -> `given_live_bot(name)` (DSL interface change -> re-lock) |
| driver | tests/acceptance/drivers/live.py | admin setup without `--channels` |
| specs (locked) | tests/acceptance/specs/test_live_bots.py | see below |
| lock | tests/acceptance/spec-lock.json | regenerate via eng-spec after CP-C (new sha) |

## Draft specs, DSL and candidate lock (F1, F5, F6)
Full drafts (not yet in the locked paths): thoughts/shared/plans/drafts/2026-10-27-lb4b-test_live_bots.py.draft and thoughts/shared/plans/drafts/2026-10-27-lb4b-dsl.py.draft. 13 spec functions / 15 cases: mention + no-mention in member channel; @channel/@here/@all (parametrized); reply in a thread the bot posted in (asserts the wake names the thread, DSL `reply_in_thread`, `assert_woken_once(thread=)`); private member channel wakes; non-member private channel never wakes and is never joined (`assert_not_member`); DM; own post; connection drop; NEW drop + post in a channel on another team; forged; token; failed. DSL: `given_live_bot(name)` (no channels), `given_member_channel(..., private=False)`.
Candidate lock (eng-spec lock on the drafts, kit 2.5.6, deterministic): 2 spec files, 44 DSL symbols, 19 assertion steps -> CP-C row `| 2026-10-27 | CP-C | thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md | approved speclock sha256:ea6a99cbd5601d05 |` (pending Rob; full sha256 ea6a99cbd5601d05fe7d0d77ba2c3ebfc0b9b414c55af0cfb8e680f45b69d1ad). System-message and group-DM exclusions stay covered by unit tests (test_live_filter.py).

## Locked spec changes (re-lock in lb4b under this CP-C)
- `test_mention_in_chosen_channel_wakes_bot_once` -> `test_mention_in_member_channel_wakes_bot_once` (drop `channels=`).
- `test_post_without_mention_in_chosen_channel_also_wakes_bot` -> `test_post_without_mention_in_member_channel_also_wakes_bot` (drop `channels=`).
- `test_post_in_member_channel_not_chosen_does_not_wake` -> DELETE (no "chosen" concept).
- ADD `test_channel_wide_mention_wakes_bot_once` (`@channel`) and `test_reply_in_thread_bot_posted_in_wakes_bot_once` (root_id in wake).
- All other specs: remove the `channels=` argument only.
- Plan PR-12 node-id list updated to the new names.

## Unblocking lb4 (recommended)
Minimal change, no spec edits, no re-lock: make the store and `admin set-bot` accept an EMPTY channel list (lb4 Option A, ~10 lines in `store.validate` + admin; flip `tests/unit/test_store.py:106` `_raw(channels=[])` to accepted). The two blocked specs (`test_dm_to_bot_wakes_bot_once`, `test_forged_wake_is_rejected` use `channels=[]`) then pass -> 7/7 under the CURRENT lock. This is forward-compatible with full removal.
Done (lb4 verify PASS at 219a9a1). Sequence decided: allow-list removal is its own slice thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md, after lb4 CP-S and CP-C, before lb5; lb5 catch-up uses member channels on all teams (architecture 'catch-up channel discovery').

## Phase 1: Drop allow-list (slice lb4b: thoughts/shared/slices/2026-10-27-lb4b-drop-allowlist.md)
Changes per the touch-point table above.
### Success Criteria
#### Automated Verification
- [ ] `.venv/bin/pytest tests/unit -q` exit 0 incl. member-channel/@channel/thread-reply filter cases and legacy-`channels`-key load test
- [ ] `.venv/bin/pytest -q --channel live <the 10 node ids listed in the lb4b card Tasks; 12 passed>` (in-process; drop/reconnect + token specs stay in lb5) exit 0; `python3 .eng/bin/eng-spec status .` matches the new lock; `python3 .eng/bin/eng-check .` exit 0
#### Manual Verification
- [ ] Rob (in-process demo at lb4b CP-S; deployed demo in lb5): `set-bot` without `--channels`; a plain post and an `@channel` post in a member channel each wake once; a thread reply wakes with root_id; a DM wakes.

## Plan-review findings carried into lb4b
Codex plan review (8 findings, advisory; `thoughts/shared/verification/2026-10-27-live-bots-delta-no-allowlist-plan-review.md`). Rob has decided the wake rules above; these must be resolved in the lb4b card before it starts, and the re-locked spec hash gets its own Rob approval:
- F1 draft revised specs + DSL, re-lock, Rob approves the new speclock hash.
- F2 reconcile design REQ-A1/acceptance examples, architecture, ADR-0007 (chosen-channel catch-up).
- F3 create the lb4b slice card (sequence: after lb4 CP-S, before lb5); update lb5 card spec references.
- F4 catch-up across all memberships (all teams, pagination, new channels, DMs).
- F5 negative spec: non-member private channel never wakes; keep system/own/G exclusions.
- F6 DSL steps for a reply in the bot's thread, assert wake names the thread.
- F7 lb4b uses explicit node ids + in-process demo; full container suite stays in lb5.
- F8 ask Rob to confirm live-only acceptance per ADR-0010.

Status 2026-10-27: F1 drafted (above; hash approval pending Rob), F2 done (design Amendments, architecture 'catch-up channel discovery', ADR-0007 Amendment), F3 done (lb4b card; lb5 card + plan refs), F4 done (architecture + lb5 PR-3), F5/F6 in drafts, F7 in lb4b card; F8 open for Rob. Re-review (plan-review-2, supersedes the first): the REQ-A1/examples amendment needs a new CP-A row by Rob (with the CP-C); until then eng-check reports design-changed-after-approval.

