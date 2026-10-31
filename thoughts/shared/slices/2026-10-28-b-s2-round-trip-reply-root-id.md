---
id: SLICE-20261028-b-s2-round-trip-reply-root-id
type: slice
phase: implement
status: done             # todo | in-progress | blocked | review | done
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
- [x] `app/service.py` + `app/mcp.py`: optional `root_id` on post_channel/dm_send (26-char id validated); before POST the root is fetched (`GET /posts/{root_id}` with the bot token) and must belong to the target channel / DM channel, else `invalid_root` and no post is created; MM 400/403/404 on root -> `invalid_root`; existing MCP specs unchanged
- [x] `app/listener.py` payload `version: 2` + `issued_at` + `reply{tool, team, channel|username, root_id}` per architecture contract (thread -> root_id, top-level/DM -> null)
- [x] relay `Tripwire` (bad_sig > 5 / 10 min, rate limit hit, upstream 401/403, **count drift**: forwards > distinct delivery ids in 24 h, i.e. an accepted-risk double wake happened) -> `relay_tripwire{reason}` log + optional MM alert; `/health` adds `double_forward_24h`. >= 3 in 24 h is the signal to revisit option C (Rob 2026-10-28)
- [x] (n/a: spike observed verbatim body, no fallback) If the B-s1 spike chose the OQ-B2 fallback: relay adds the readable `text` reply-hint field built only from the verified body
- [x] fake routine replies via the real MCP bridge using reply hints; DSL given_routine_answers / replay_last_wake / assert_replied
- [x] Unit tests per plan Phase 2 (root_id, invalid_root, **valid root_id from a foreign channel on post_channel and from an inaccessible/other DM on dm_send -> invalid_root, fake MM shows no new post**, payload v2 cases, tripwire incl. count drift with fake clock)
- [x] Routine instruction text documented (relay/README.md or OWNER-GUIDE); CHANGELOG
- [x] B-s2 specs green; B-s1, A live and MCP specs still green

## Tasks
- [x] eng-resume; read plan Phase 2 (Changes Required is the detailed checklist), architecture contracts, ADRs above
- [x] Run this slice's executable specs and confirm they fail for the right reason (red): `LIVE_MODE=inprocess .venv/bin/pytest -q --channel live $B2` (`B2` = this card's `specs:` list, defined in plan Phase 2 Automated Verification). Specs of later slices are NOT selected and stay red.
- [x] Write failing unit tests (tests/unit/) for the behaviours above
- [x] Implement (drivers/DSL bodies may change; spec files and DSL public interface are locked - do not edit them, raise a back-up instead)
- [x] Run plan Phase 2 Automated Verification block verbatim (explicit `LIVE_IMAGE`/`RELAY_IMAGE` = `:bs2`, in-process AND container, full selection 3x per DoD concurrency rule); all exit 0; paste outputs in the handoff
- [x] Do not stage Rob's uncommitted AGENTS.md, OWNER-GUIDE.md, receiver.py or untracked thoughts/shared files
- [x] Commit; eng-handoff ("implemented, awaiting review/verify")

## Manual verification (Rob, at CP-S)
See plan Phase 2 Manual Verification.

## Progress log
<!-- date - agent - what changed (file:line) -->
- 2026-10-30 - claude-code - red first: the 3 `$B2` specs (`LIVE_MODE=inprocess --channel live`) -> 3 failed `AttributeError: 'LiveDriver' object has no attribute 'given_routine_answers'`. Unit tests written before code (tests/unit/test_root_id.py new; test_listener.py payload v2; test_relay.py tripwire) -> 46 failed, then green.
- 2026-10-30 - claude-code - code: app/validate.py `post_id`; app/service.py `_root`/`check_root`, `post_channel(..., root_id=None)`, `dm_send(..., *, me, root_id=None)` (root fetched with the bot token before any write; MM 400/403/404 or other channel -> `invalid_root`); app/mcp.py `root_id` arg (schema + description) on post_channel/dm_send; app/listener.py `_payload` version 2 + `issued_at` + `reply`; relay/relay.py `Tripwire`, `forwards` table in Seen (count drift), optional RELAY_ALERT_* Mattermost alert, /health `double_forward_24h`. Harness: fake_mattermost GET /posts/{id}, root_id on POST /posts, 26-char post ids with mm_ids; fake_routine acts as the bot via the real MCP bridge; live.py `given_routine_answers`, `assert_replied` (driver only), in-process MCP app; LIVE_IMAGE/RELAY_IMAGE defaults -> :bs2. Docs: relay/README.md (routine instruction text, tripwire table, alert env), coolify snippet, CHANGELOG. No spec or DSL edit.
- 2026-10-30 - claude-code - plan Phase 2 Automated Verification block run (WSL), exit 0 all 3 runs: unit 389 passed; mcp 16 passed/36 skipped; live inprocess A+B1+B2 29 passed (~71 s); live container A+B1+B2 29 passed (~189 s). eng-check OK (3 pre-existing warnings); eng-spec status: specs and DSL interface match the lock.
- 2026-10-30 - claude-code - Codex slice review (`eng-run code-review ... --base d5dc1ae`): 2 P2 findings, both fixed: root_id that is itself a reply -> invalid_root (app/service.py `_same_channel`); relay bad-signature window kept in 10 s buckets (bounded under a forged flood). Review file thoughts/shared/verification/2026-10-30-slice-20261028-b-s2-round-trip-reply-root-id-review.md `addressed`. Phase 2 block re-run after the fixes, exit 0 all 3 runs: unit 392; mcp 16p/36s; live inprocess 29; live container 29; eng-check OK; eng-spec lock clean.

## Blockers / deviations from plan
- DM reply hints always carry `root_id: null` (architecture contract "DMs `null`"), so a reply inside a DM thread is answered at DM top level; `dm_send` still accepts `root_id`. Planner: confirm, or change the contract to pass post.root_id for DMs too.
- `dm_send` fetches the root before opening the DM, so an unknown/inaccessible root creates neither a post nor a DM conversation; a root in another conversation the bot can see is checked after the (reused or opened) DM lookup.
- `issued_at` is stamped when the wake is queued (listener clock), not per retry attempt.
- Tripwire `bad_sig` counts bad signatures and stale timestamps (both HMAC failures, architecture wording); alerts are throttled to one per reason per 10 min; drift alert only from 3 per 24 h. Drift counting: a forward row is written before the upstream call and deleted when the routine definitely did not start (non-2xx answer or connect error), so ambiguous timeouts and a crash after 2xx count; `double_forward_24h` = rows - distinct deliveries in 24 h.
- MCP results of post_channel/dm_send include `root_id` only when one was given (existing result shapes unchanged).
- OWNER-GUIDE.md not edited (Rob's uncommitted edits); routine instruction text is in relay/README.md "Grok routine setup".
