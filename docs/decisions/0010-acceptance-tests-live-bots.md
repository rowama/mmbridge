---
id: ADR-0010
type: adr
phase: architecture
status: accepted         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-26
links: [docs/design/2026-10-26-live-bots.md, docs/architecture/2026-10-26-live-bots.md]
superseded_by: none
revisit: none            # for deferred: the trigger or date to revisit
---
# ADR-0010: Acceptance tests for Live bots (four-layer model)

## Status
proposed

## Context
Large work (PROCESS 13). REQ-A1/A2/A3/A4/A7/A8 are event-driven: the observable outcome is a wake at a receiver, not an MCP response. The existing suite has an api/MCP driver and a REST-only fake Mattermost (research Q10). No UI in this increment.

## Decision
We will write acceptance tests as executable specifications in four layers (Dave Farley):
1. Specs in `tests/acceptance/specs/test_live_bots.py`, domain language only, tagged `@pytest.mark.req("REQ-An")`.
2. The shared DSL (`tests/acceptance/dsl.py`) gains steps such as `post_in(channel, text, as_user)`, `dm(bot, text, as_user)`, `drop_connection(seconds)`, `wake_target_down()`, `assert_woken_once(...)`, `assert_not_woken(...)`, `assert_failed_wake_visible()`, `assert_no_token_anywhere()`.
3. Protocol drivers: `mattermost` = fake Mattermost extended with a websocket endpoint (hello, seq, posted, drop/resume) plus existing REST; `wake` = local receiver capturing requests and verifying HMAC; existing `api` (MCP) driver for regression. No Playwright channel: no UI in this increment (n.a.).
4. SUT deployed like production: the real container image started outside the tests with a temp `/data` volume, `MMB_STORE_KEY`, `LIVE_BOTS_ENABLED=true`, `MATTERMOST_URL` and `wake_url` pointing at the fakes (external systems stubbed at the boundary); bot configured via the real admin CLI.
Specs and the DSL public interface are locked at CP-C. DSL assertion-step changes must be covered by code review. Drivers are freely editable.

## Consequences
- Positive: specs read as REQ-A examples; real reconnect/dedupe exercised against the fake WS.
- Negative: the fake WS must track Mattermost's real seq/resume semantics (fake drift risk; mitigated by a live check at CP-S).
- Neutral: changing a spec after CP-C needs Rob's re-approval.

## Prediction (scored in a later eng-retro)
- Expected outcome: no shipped REQ-A without a passing spec; live CP-S checks agree with the fake.
- Check date: after the Live bots v1 ship
- What would prove it wrong: live behaviour differs from the fake WS in a way specs did not catch, or specs rewritten in most slices.
- Score: unclear (retro v0.3.0, 2026-10-28): specs pass, but live MM-restart resume unchecked and lb5 reviews found fake drift (team-less D-channel discovery, 9bdff90)
