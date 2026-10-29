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
review: required (security: replay dedupe, rate limit, tripwire; MCP tool surface change) - thoughts/shared/verification/2026-10-28-slice-20261028-b-s2-round-trip-reply-root-id-review.md
reqs: [REQ-B2, REQ-B5]
specs: [tests/acceptance/specs/test_grok_multibot.py::test_wake_replayed_within_window_does_not_start_routine_again, tests/acceptance/specs/test_grok_multibot.py::test_bot_answer_appears_in_channel_and_does_not_wake_it_again, tests/acceptance/specs/test_grok_multibot.py::test_bot_answer_to_thread_reply_lands_in_that_thread, tests/acceptance/specs/test_grok_multibot.py::test_bot_answer_to_dm_appears_in_that_dm]
---
# Slice B-s2: round-trip reply, root_id, relay replay + rate-limit hardening

Plan: [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md](../plans/2026-10-28-grok-webhook-multibot.md) Phase 2. Architecture: docs/architecture/2026-10-28-grok-webhook-multibot.md; ADRs 0011, 0013..0016 (0012 rejected - no claim_wake). **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
Rob posts "@eddie status?" in Town Square, Eddie's answer appears there as Eddie and does not wake Eddie again; a thread reply gets its answer in the thread; a DM gets its answer in the DM. A captured wake re-sent within the window is a relay duplicate (no second run); relay rate-limits per bot and raises a tripwire on bad signatures / upstream 401-403.

## Acceptance criteria
- [ ] `app/service.py` + `app/mcp.py`: optional `root_id` on post_channel/dm_send (26-char id validated), passed to POST /posts; MM 400/404 on root -> `invalid_root`; existing MCP specs unchanged
- [ ] `app/listener.py` payload `version: 2` + `issued_at` + `reply{tool, team, channel|username, root_id}` per architecture contract (thread -> root_id, top-level/DM -> null)
- [ ] relay `Seen` (sqlite /data/relay.db; record only after upstream 2xx; duplicate -> 200 {status: duplicate}, not forwarded; concurrent identical delivery forwards once; prune 24 h)
- [ ] relay `RateLimit` (30/min burst 10 per bot, env) -> 429; `Tripwire` (bad_sig > 5 / 10 min, rate limit hit, upstream 401/403) -> `relay_tripwire` log + optional MM alert
- [ ] If the B-s1 spike chose the OQ-B2 fallback: relay adds the readable `text` reply-hint field built only from the verified body
- [ ] fake routine replies via the real MCP bridge using reply hints; DSL given_routine_answers / replay_last_wake / assert_replied
- [ ] Unit tests per plan Phase 2 (root_id, invalid_root, payload v2 cases, dedupe incl. lost-response retry and 503-then-retry, prune, rate limit, tripwire with fake clock)
- [ ] Routine instruction text documented (relay/README.md or OWNER-GUIDE); CHANGELOG
- [ ] B-s2 specs green; B-s1, A live and MCP specs still green

## Tasks
- [ ] eng-resume; read plan Phase 2 (Changes Required is the detailed checklist), architecture contracts, ADRs above
- [ ] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red): `.venv/bin/pytest -q --channel live <node ids from specs:>`
- [ ] Write failing unit tests (tests/unit/) for the behaviours above
- [ ] Implement (drivers/DSL bodies may change; spec files and DSL public interface are locked - do not edit them, raise a back-up instead)
- [ ] Run plan Phase 2 Automated Verification; all exit 0; in-process AND `LIVE_MODE=container`
- [ ] Do not stage Rob's uncommitted AGENTS.md, OWNER-GUIDE.md, receiver.py or untracked thoughts/shared files
- [ ] Commit; eng-handoff ("implemented, awaiting review/verify")

## Manual verification (Rob, at CP-S)
See plan Phase 2 Manual Verification.
