---
id: SLICE-20261027-lb4-signed-wake-dispatcher
type: slice
phase: implement
status: todo             # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
plan_phase: 4
review: required (security: wake authentication REQ-A7, ADR-0008) - thoughts/shared/verification/2026-10-27-lb4-review.md
reqs: [REQ-A1, REQ-A2, REQ-A3, REQ-A7, REQ-A8]
specs: [tests/acceptance/specs/test_live_bots.py::test_mention_in_chosen_channel_wakes_bot_once, tests/acceptance/specs/test_live_bots.py::test_post_without_mention_in_chosen_channel_also_wakes_bot, tests/acceptance/specs/test_live_bots.py::test_post_in_member_channel_not_chosen_does_not_wake, tests/acceptance/specs/test_live_bots.py::test_dm_to_bot_wakes_bot_once, tests/acceptance/specs/test_live_bots.py::test_bots_own_post_never_wakes_itself, tests/acceptance/specs/test_live_bots.py::test_forged_wake_is_rejected, tests/acceptance/specs/test_live_bots.py::test_failed_wake_is_retried_then_visible_to_operator]
---
# Slice 4: Signed wake dispatcher (HMAC, retries, fake receiver)

Plan: [thoughts/shared/plans/2026-10-27-live-bots.md](../plans/2026-10-27-live-bots.md) Phase 4. Architecture: docs/architecture/2026-10-26-live-bots.md. **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
Queued wakes reach a receiver as signed HTTPS POSTs (HMAC-SHA256 over ts.body); failures retry with backoff then show in `admin failed`; the live driver (in-process listener + dispatcher + fake MM + HMAC-verifying receiver) turns A1/A2/A3/A7-forged/A8 specs green.

## Acceptance criteria
- [ ] `app/wake.py`: `sign(secret, ts, body) -> 'v1=<hex>'`; `verify(secret, headers, body, now, window=300) -> bool` (constant-time; used by test receiver and documented for receivers); `Dispatcher(state, cfg, http)` loop: claim_due -> POST with `X-MMB-Delivery/Timestamp/Signature`, 5 s timeout, concurrency 4; 2xx delivered; 408/429/5xx/timeout/connect retry; other 4xx failed; log `wake_failed`; payload has no token
- [ ] `tests/acceptance/drivers/live.py` + wake receiver: in-process mode (listener + dispatcher tasks against fake MM + receiver); admin CLI invoked as subprocess/function
- [ ] Test-only fast backoff via env (`WAKE_BACKOFF_SCALE`) so A8 spec runs in seconds
- [ ] Plan Phase 4 Automated Verification all exit 0; existing MCP suite (`.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`) still green

## Tasks
- [ ] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red) (`.venv/bin/pytest tests/acceptance --channel live -q -k <names>`)
- [ ] Write failing unit tests (tests/unit/) for the behaviours above
- [ ] Implement
- [ ] Run Phase 4 automated verification (plan), including this slice's specs (now green)
- [ ] Do not edit locked files: tests/acceptance/specs/**, DSL public interface (CP-C speclock)

## Size check
~200 lines + driver

## Progress log
<!-- date - agent - what changed (file:line) -->

## Blockers / deviations from plan
none
