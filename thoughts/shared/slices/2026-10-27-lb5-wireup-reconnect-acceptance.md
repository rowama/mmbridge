---
id: SLICE-20261027-lb5-wireup-reconnect-acceptance
type: slice
phase: implement
status: todo             # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
plan_phase: 5
review: required (security + deploy: lifespan, reconnect, token secrecy end to end) - thoughts/shared/verification/2026-10-27-lb5-review.md
reqs: [REQ-A1, REQ-A2, REQ-A3, REQ-A4, REQ-A7, REQ-A8]
specs: [tests/acceptance/specs/test_live_bots.py::test_post_during_connection_drop_wakes_exactly_once_after_reconnect, tests/acceptance/specs/test_live_bots.py::test_bot_token_never_appears_in_logs_output_or_wakes]
---
# Slice 5: Wire-up + LIVE_BOTS_ENABLED + reconnect; acceptance green

Plan: [thoughts/shared/plans/2026-10-27-live-bots.md](../plans/2026-10-27-live-bots.md) Phase 5. Architecture: docs/architecture/2026-10-26-live-bots.md. **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
In the real container, `LIVE_BOTS_ENABLED=true` starts listener + dispatcher from FastAPI lifespan, `/health` reports listener state, drops reconnect with resume or REST catch-up (15 min window) with exactly-once wakes; full live acceptance suite green against the container.

## Acceptance criteria
- [ ] `app/main.py`: lifespan starts listener+dispatcher tasks only if flag true and store+state readable; `/health` adds `listener: on|off|disabled|degraded` (no secrets); MCP path unchanged
- [ ] `app/listener.py`: reconnect backoff 1->60 s jitter, `?connection_id&sequence_number`, new id -> REST catch-up `GET /channels/{id}/posts?since=` for chosen+DM channels within `LIVE_CATCHUP_MINUTES` (default 15), seq reset to 0; 401 -> retry every 5 min; store mtime re-read every 30 s; single-listener lease in meta
- [ ] `tests/acceptance/drivers/live.py`: container mode (docker image, temp /data, fakes on host network) per ADR-0010; scenario log capture for token scan
- [ ] README/OWNER-GUIDE: deploy prerequisites + receiver HMAC verification snippet; CHANGELOG Unreleased
- [ ] Plan Phase 5 Automated Verification all exit 0; existing MCP suite (`.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`) still green

## Tasks
- [ ] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red) (`.venv/bin/pytest tests/acceptance --channel live -q -k <names>`)
- [ ] Write failing unit tests (tests/unit/) for the behaviours above
- [ ] Implement
- [ ] Run Phase 5 automated verification (plan), including this slice's specs (now green)
- [ ] Do not edit locked files: tests/acceptance/specs/**, DSL public interface (CP-C speclock)

## Size check
~200 lines + driver/docs

## Progress log
<!-- date - agent - what changed (file:line) -->

## Blockers / deviations from plan
none
