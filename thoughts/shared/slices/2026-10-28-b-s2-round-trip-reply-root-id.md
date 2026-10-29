---
id: SLICE-20261028-b-s2-round-trip-reply-root-id
type: slice
phase: implement
status: todo             # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-28
links: [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, docs/architecture/2026-10-28-grok-webhook-multibot.md]
plan: thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md
plan_phase: 2
review: required (security: tripwire, root_id authorization; MCP tool surface change) - thoughts/shared/verification/2026-10-28-slice-20261028-b-s2-round-trip-reply-root-id-review.md
reqs: [REQ-B2, REQ-B5]
specs: [tests/acceptance/specs/test_grok_multibot.py::test_bot_answer_appears_in_channel_and_does_not_wake_it_again, tests/acceptance/specs/test_grok_multibot.py::test_bot_answer_to_thread_reply_lands_in_that_thread, tests/acceptance/specs/test_grok_multibot.py::test_bot_answer_to_dm_appears_in_that_dm]
---
# Slice B-s2: round-trip reply, root_id, relay tripwire

Plan: [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md](../plans/2026-10-28-grok-webhook-multibot.md) Phase 2. Architecture: docs/architecture/2026-10-28-grok-webhook-multibot.md; ADRs 0011, 0013..0016 (0012 rejected - no claim_wake). **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
Rob posts "@eddie status?" in Town Square, Eddie's answer appears there as Eddie and does not wake Eddie again; a thread reply gets its answer in the thread; a DM gets its answer in the DM. The relay raises a tripwire on bad signatures, rate-limit hits, upstream 401/403 and double-forward count drift (dedupe + rate limit already shipped in B-s1).

## Acceptance criteria
- [ ] `app/service.py` + `app/mcp.py`: optional `root_id` on post_channel/dm_send (26-char id validated); before POST the root is fetched (`GET /posts/{root_id}` with the bot token) and must belong to the target channel / DM channel, else `invalid_root` and no post is created; MM 400/403/404 on root -> `invalid_root`; existing MCP specs unchanged
- [ ] `app/listener.py` payload `version: 2` + `issued_at` + `reply{tool, team, channel|username, root_id}` per architecture contract (thread -> root_id, top-level/DM -> null)
- [ ] relay `Tripwire` (bad_sig > 5 / 10 min, rate limit hit, upstream 401/403, **count drift**: forwards > distinct delivery ids in 24 h, i.e. an accepted-risk double wake happened) -> `relay_tripwire{reason}` log + optional MM alert; `/health` adds `double_forward_24h`. >= 3 in 24 h is the signal to revisit option C (Rob 2026-10-28)
- [ ] If the B-s1 spike chose the OQ-B2 fallback: relay adds the readable `text` reply-hint field built only from the verified body
- [ ] fake routine replies via the real MCP bridge using reply hints; DSL given_routine_answers / replay_last_wake / assert_replied
- [ ] Unit tests per plan Phase 2 (root_id, invalid_root, **valid root_id from a foreign channel on post_channel and from an inaccessible/other DM on dm_send -> invalid_root, fake MM shows no new post**, payload v2 cases, tripwire incl. count drift with fake clock)
- [ ] Routine instruction text documented (relay/README.md or OWNER-GUIDE); CHANGELOG
- [ ] B-s2 specs green; B-s1, A live and MCP specs still green

## Tasks
- [ ] eng-resume; read plan Phase 2 (Changes Required is the detailed checklist), architecture contracts, ADRs above
- [ ] Run this slice's executable specs and confirm they fail for the right reason (red): `LIVE_MODE=inprocess .venv/bin/pytest -q --channel live $B2` (`B2` = this card's `specs:` list, defined in plan Phase 2 Automated Verification). Specs of later slices are NOT selected and stay red.
- [ ] Write failing unit tests (tests/unit/) for the behaviours above
- [ ] Implement (drivers/DSL bodies may change; spec files and DSL public interface are locked - do not edit them, raise a back-up instead)
- [ ] Run plan Phase 2 Automated Verification block verbatim (explicit `LIVE_IMAGE`/`RELAY_IMAGE` = `:bs2`, in-process AND container, full selection 3x per DoD concurrency rule); all exit 0; paste outputs in the handoff
- [ ] Do not stage Rob's uncommitted AGENTS.md, OWNER-GUIDE.md, receiver.py or untracked thoughts/shared files
- [ ] Commit; eng-handoff ("implemented, awaiting review/verify")

## Manual verification (Rob, at CP-S)
See plan Phase 2 Manual Verification.
