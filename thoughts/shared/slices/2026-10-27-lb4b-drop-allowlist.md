---
id: SLICE-20261027-lb4b-drop-allowlist
type: slice
phase: implement
status: todo             # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md, thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md
plan_phase: 1
review: required (security: membership becomes the disclosure boundary) - thoughts/shared/verification/2026-10-27-lb4b-review.md
reqs: [REQ-A1, REQ-A2, REQ-A3, REQ-A7, REQ-A8]
specs: [tests/acceptance/specs/test_live_bots.py::test_mention_in_member_channel_wakes_bot_once, tests/acceptance/specs/test_live_bots.py::test_post_without_mention_in_member_channel_also_wakes_bot, tests/acceptance/specs/test_live_bots.py::test_channel_wide_mention_wakes_bot_once, tests/acceptance/specs/test_live_bots.py::test_reply_in_thread_bot_posted_in_wakes_bot_once, tests/acceptance/specs/test_live_bots.py::test_post_in_private_member_channel_wakes_bot_once, tests/acceptance/specs/test_live_bots.py::test_post_in_channel_bot_is_not_member_of_does_not_wake, tests/acceptance/specs/test_live_bots.py::test_dm_to_bot_wakes_bot_once, tests/acceptance/specs/test_live_bots.py::test_bots_own_post_never_wakes_itself, tests/acceptance/specs/test_live_bots.py::test_forged_wake_is_rejected, tests/acceptance/specs/test_live_bots.py::test_failed_wake_is_retried_then_visible_to_operator]
---
# Slice 4b: Drop the channel allow-list (re-lock specs)

Plan: [delta](../plans/2026-10-27-live-bots-delta-no-allowlist.md) Phase 1. Sequence: after lb4 CP-S, before lb5. **Security-relevant: gets the cross-model review.**
**Precondition:** CP-C for the delta logged by Rob with the new speclock hash. Until then this card stays todo.

## Outcome (user-visible, demoable)
`set-bot` takes token + wake URL only; in-process, the bot wakes once on any post (plain, @channel/@here/@all, thread reply naming the thread) in public or private channels it is a member of and on DMs; non-member channels never wake and are never joined.

## Acceptance criteria
- [ ] Re-lock: copy thoughts/shared/plans/drafts/2026-10-27-lb4b-test_live_bots.py.draft -> tests/acceptance/specs/test_live_bots.py and 2026-10-27-lb4b-dsl.py.draft -> tests/acceptance/dsl.py; `python3 .eng/bin/eng-spec lock .` prints exactly the hash Rob approved at CP-C (candidate sha256:ea6a99cbd5601d05); any difference -> stop, no commit
- [ ] app/store.py: no channels in BotConfig/validate; legacy `channels` key loads and is ignored (unit test)
- [ ] app/admin.py: no `--channels`; passing it -> `invalid_argument: channels no longer used`; show/set-bot output without channels
- [ ] app/live_filter.py: `decide(event, bot_user_id)`; O/P wake, D wake, own/system/G drop (unit tests incl. @channel, thread reply with root_id, non-member never reaches)
- [ ] tests/acceptance/drivers/live.py: given_channel(team, channel, members, private), reply in thread, membership check; no --channels; no join calls
- [ ] Wake payload carries root_id for thread replies

## Tasks
- [ ] Apply the re-lock (above) and confirm the specs: node ids fail for the right reason (red)
- [ ] Write failing unit tests, implement, go green
- [ ] Automated: `.venv/bin/pytest tests/unit -q` exit 0; `.venv/bin/pytest -q --channel live <specs: node ids>` exit 0; `.venv/bin/pytest tests/acceptance -q` (MCP regression) exit 0; `python3 .eng/bin/eng-spec status .` matches the new lock; `python3 .eng/bin/eng-check .` exit 0
- [ ] Manual (in-process demo, CP-S): with the fake MM, a plain post, an @channel post and a thread reply in a member channel each wake once (reply names the thread); a DM wakes; a post in a non-member private channel does not wake. Container suite + deployed demo stay in lb5.

## Size check
~150 lines + tests

## Progress log
<!-- date - agent - what changed (file:line) -->

## Blockers / deviations from plan
- Blocked on CP-C (Rob approves the delta and speclock hash).
- Drop/reconnect specs (test_post_during_connection_drop_..., test_post_during_drop_in_channel_on_another_team_...) and the token spec run in lb5.
