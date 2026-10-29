---
id: SLICE-20261028-b-s1-relay-grok-wake-one-bot
type: slice
phase: implement
status: todo             # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-28
links: [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, docs/architecture/2026-10-28-grok-webhook-multibot.md]
plan: thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md
plan_phase: 1
review: required (security: HMAC verify at relay, replay dedupe, rate limit, Bearer routine key handling, redaction) - thoughts/shared/verification/2026-10-28-slice-20261028-b-s1-relay-grok-wake-one-bot-review.md
reqs: [REQ-B1, REQ-B2, REQ-B3, REQ-B4]
specs: [tests/acceptance/specs/test_grok_multibot.py::test_post_in_member_channel_starts_grok_routine_once, tests/acceptance/specs/test_grok_multibot.py::test_dm_to_bot_starts_grok_routine_once, tests/acceptance/specs/test_grok_multibot.py::test_wake_not_produced_by_mmbridge_does_not_start_routine, tests/acceptance/specs/test_grok_multibot.py::test_altered_wake_does_not_start_routine, tests/acceptance/specs/test_grok_multibot.py::test_wake_replayed_ten_minutes_later_does_not_start_routine_again, tests/acceptance/specs/test_grok_multibot.py::test_wake_replayed_within_window_does_not_start_routine_again, tests/acceptance/specs/test_grok_multibot.py::test_no_token_secret_or_routine_key_in_logs_output_or_wakes, tests/acceptance/specs/test_grok_multibot.py::test_routine_recovering_before_retries_run_out_is_started_exactly_once, tests/acceptance/specs/test_grok_multibot.py::test_routine_down_for_good_shows_one_failed_wake, tests/acceptance/specs/test_grok_multibot.py::test_relay_down_then_up_starts_routine_exactly_once, tests/acceptance/specs/test_grok_multibot.py::test_switching_bot_from_signed_webhook_to_grok_applies_without_redeploy]
---
# Slice B-s1: wake relay + Grok Bot wake for one bot

Plan: [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md](../plans/2026-10-28-grok-webhook-multibot.md) Phase 1. Architecture: docs/architecture/2026-10-28-grok-webhook-multibot.md; ADRs 0011, 0013..0016 (0012 rejected - no claim_wake). **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
A Mattermost post in a member channel or a DM to eddie starts the Eddie Grok routine exactly once through the new HMAC->Bearer wake relay (relay/ in this repo, own image + Coolify app); forged, tampered, stale and replayed (within-window) wakes never start a routine; the relay rate-limits per bot (dedupe + rate limit moved here from B-s2, plan review #1); routine/relay outages retry then show one failed wake; switching eddie's wake URL to the relay applies without redeploy. mmbridge runtime code is unchanged (relay + harness + docs). OQ-B1/B2 answered by a spike against a real routine.

## Acceptance criteria
- [ ] **Spike first** `relay/spike_routine.py` (key via stdin/env only): Rob runs against a real routine; record status codes for valid key / wrong key / bad URL and whether the bot sees the JSON body verbatim (OQ-B1/B2) in the handoff + an Observed note in ADR-0011; apply plan fallback if different
- [ ] `relay/relay.py`: `load_bots(env)` (RELAY_BOT_<NAME>_HMAC_SECRET|ROUTINE_URL|ROUTINE_KEY; fail fast on missing field, secret < 32, non-https); `POST /wake/{bot}` 404 unknown / 401 bad_sig|stale (300 s window, constant time) / forward body byte-for-byte with Bearer + X-MMB-Delivery, 5 s timeout; `map_upstream`: 2xx->200, 408/429/5xx/timeout/connect->503, other 4xx->424 {upstream}; `GET /health` counts only; JSON logs with redaction of every secret/key
- [ ] relay `Seen` dedupe (sqlite /data/relay.db, `X-MMB-Delivery`/`delivery_id` PK; record **only after upstream 2xx** - accepted risk A, Rob 2026-10-28, see plan "Delivery guarantee"; duplicate -> 200 {status: duplicate}, not forwarded; prune 24 h) + in-flight guard (two concurrent identical deliveries forward once) + `RateLimit` per bot (30/min burst 10, env) -> 429
- [ ] Replay/dedupe unit tests green BEFORE the B-s1 live demo: replay within window -> not forwarded; concurrent duplicate -> one forward; 503 then retry -> forwarded once; rate limit with fake clock; ambiguous outcomes characterised (upstream 2xx but response lost/timeout -> retry forwards again, logs `relay_delivery_ambiguous`; crash injected between upstream 2xx and `Seen.add` -> retry forwards again) - these document the accepted double-wake, they do not hide it
- [ ] relay `verify` is a copy of `app.wake.verify`; unit test signs with `app.wake.sign` and verifies with the relay (drift guard); relay image imports nothing from `app/`
- [ ] `relay/Dockerfile` (non-root 10001, /data), `relay/requirements.txt` pinned; `coolify-service.snippet.yaml` relay app; `relay/README.md` setup + key rotation runbook
- [ ] `tests/unit/test_relay.py` per plan Phase 1 (env parsing, verify cases, mapping table, byte-identical forward, Bearer set, no key/secret in logs or responses, 404)
- [ ] Harness: `drivers/fake_routine.py` (checks Bearer, records bodies, down/up), `drivers/relay.py` (in-process, or container image from env `RELAY_IMAGE`, default `mmbridge-relay:bs1`), `drivers/live.py` register_bot/switch_wake_target/forge/tamper/replay/relay_down/up + B-s1 assertions
- [ ] README + CHANGELOG Unreleased; OWNER-GUIDE only after Rob commits his pending edits (else text in relay/README.md, noted in handoff)
- [ ] B-s1 specs (11, incl. replay-within-window) green; A live + MCP specs still green; B-s2/B-s3 specs not selected

## Tasks
- [ ] eng-resume; read plan Phase 1 (Changes Required is the detailed checklist), architecture contracts, ADRs above
- [ ] Run this slice's executable specs and confirm they fail for the right reason (red): `LIVE_MODE=inprocess .venv/bin/pytest -q --channel live $B1` (`B1` = this card's `specs:` list, defined in plan Phase 1 Automated Verification). Specs of later slices are NOT selected and stay red.
- [ ] Write failing unit tests (tests/unit/) for the behaviours above
- [ ] Implement (drivers/DSL bodies may change; spec files and DSL public interface are locked - do not edit them, raise a back-up instead)
- [ ] Run plan Phase 1 Automated Verification block verbatim (explicit `LIVE_IMAGE`/`RELAY_IMAGE` = `:bs1`, in-process AND container, full selection 3x per DoD concurrency rule); all exit 0; paste outputs in the handoff
- [ ] Do not stage Rob's uncommitted AGENTS.md, OWNER-GUIDE.md, receiver.py or untracked thoughts/shared files
- [ ] Commit; eng-handoff ("implemented, awaiting review/verify")

## Manual verification (Rob, at CP-S)
See plan Phase 1 Manual Verification.
