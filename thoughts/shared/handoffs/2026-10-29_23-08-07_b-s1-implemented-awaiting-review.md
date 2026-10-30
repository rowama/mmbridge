---
id: HANDO-20261029-b-s1-implemented-awaiting-review
type: handoff
phase: implement
status: complete
owner_agent: claude-code
date: 2026-10-29T23:08:07-05:00
links: [thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md, thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md]
git_commit: cd07811
branch: main
next_skill: eng-verify
---
# Handoff: B-s1 implemented, awaiting review/verify

## Task(s)
- SLICE-20261028-b-s1-relay-grok-wake-one-bot (plan B Phase 1): **implemented, status `review`**. Code commit cd07811 (not pushed). All 11 `$B1` specs + A live + MCP specs green, in-process and container, 3 runs.
- Not done (needs Rob or the planner): OQ-B1/B2 spike run, Codex slice review, OWNER-GUIDE text, CP-S manual checks.

## Critical References
- thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md (Progress log + Blockers/deviations)
- relay/relay.py, relay/README.md
- tests/acceptance/drivers/relay.py (how the relay is run and tapped in the harness)

## Recent changes
- relay/relay.py:1 - new relay app (`create_app` factory; `load_bots`, `verify` copy, `map_upstream`, `Seen`, `RateLimit`, `_Relay.wake/_deliver/_forward`).
- relay/Dockerfile, relay/requirements.txt, relay/.dockerignore, relay/spike_routine.py, relay/README.md - new.
- tests/unit/test_relay.py:1 - 55 unit tests (plan Phase 1 list incl. replay/dedupe and ambiguous outcomes).
- tests/acceptance/drivers/fake_routine.py, drivers/relay.py, drivers/_serve.py - new; drivers/live.py - B-s1 steps (`register_bot` ... `assert_no_secret_anywhere`), generic `_barrier`, `assert_wake_retried` for relay paths, WAKE_BACKOFF_SCALE 0.25, in-process reload_s 0.1, LIVE_IMAGE default mmbridge:bs1.
- README.md "Grok Bot routines (wake relay)"; CHANGELOG.md Unreleased (Added); coolify-service.snippet.yaml relay service + volume.
- No change to app/, tests/acceptance/specs/, or tests/acceptance/dsl.py (no DSL assertion body edits).

## Verification (plan Phase 1 block, run verbatim, exit 0)
```
run 1: unit 322 passed | mcp 16 passed, 36 skipped | live inprocess A+B1 26 passed (65.9s) | live container A+B1 26 passed (169.3s)
run 2: unit 322 passed | mcp 16 passed, 36 skipped | live inprocess 26 passed (64.4s) | live container 26 passed (167.8s)
run 3: unit 322 passed | mcp 16 passed, 36 skipped | live inprocess 26 passed (65.3s) | live container 26 passed (167.6s)
eng-check: OK - 0 error(s), 3 warning(s), 149 artifact(s) checked
eng-spec status: lock approval: ok (2026-10-29); specs and DSL interface match the lock
```
Red first: the 11 specs failed with `AttributeError: 'LiveDriver' object has no attribute 'register_bot'`.

## Learnings
- mmbridge's store reload is a fixed 30 s (app/live.py RELOAD_S, no env), so the container switch spec waits for the bridge's own `store_updated ... generation` log line; in-process passes `reload_s=0.1`.
- The routine only sees the forwarded body (no signature headers), so tamper/replay need the genuinely captured signed request: the harness puts a recording tap between mmbridge and the relay. `relay_down` stops tap + relay (connection refused at mmbridge).
- Relay retries in container mode need time: WAKE_BACKOFF_SCALE 0.25 gives ~7.5 s before a wake fails (was ~1.5 s).
- `codex` is not installed in the implementer's WSL shell, even with `bash -lc`.

## Artifacts
- relay/relay.py, relay/Dockerfile, relay/requirements.txt, relay/.dockerignore, relay/spike_routine.py, relay/README.md
- tests/unit/test_relay.py
- tests/acceptance/drivers/fake_routine.py, tests/acceptance/drivers/relay.py, tests/acceptance/drivers/_serve.py, tests/acceptance/drivers/live.py
- README.md, CHANGELOG.md, coolify-service.snippet.yaml
- thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md (status review, progress log, deviations)
- thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md (Phase 1 automated checkbox ticked)
- Images built locally: mmbridge:bs1, mmbridge-relay:bs1

## Approvals
- None requested or granted this session. Next stop: CP-S for B-s1 (after verify), with the plan Phase 1 manual checks and the Before -> After line, e.g. "Before: a post wakes Eddie's signed receiver. After: a post in Town Square or a DM to eddie starts the Eddie Grok routine once, via the relay."

## Action Items & Next Steps
1. Planner: run the advisory Codex slice review where Codex is available: `python3 .eng/bin/eng-run code-review SLICE-20261028-b-s1-relay-grok-wake-one-bot` (base bc73656). Security-relevant (HMAC verify, dedupe, rate limit, Bearer key, redaction).
2. Planner: eng-verify for B-s1 (re-run the Phase 1 block).
3. Rob before CP-S: run `python3 relay/spike_routine.py https://<eddie-routine-url>` (key at the prompt) and note the 3 codes + whether the bot saw the JSON marker verbatim; planner records them in ADR-0011 as an "Observed" note (and applies the OQ-B1/B2 fallback if they differ).
4. Rob at CP-S: deploy the relay on Coolify per relay/README.md "Setup on Coolify"; plan Phase 1 Manual Verification.
5. OWNER-GUIDE "Grok routine setup": after Rob commits his pending OWNER-GUIDE.md edits (text is in relay/README.md).
6. Push cd07811 only per push_permission (standing: after eng-verify PASS).

## Other Notes
- Container-mode `replay_last_wake(600)` is refused as a duplicate, not as stale (no clock hook in the relay image on purpose); in-process it is refused as stale. Stale is unit-tested.
- Rob's uncommitted AGENTS.md, OWNER-GUIDE.md, receiver.py and untracked thoughts/shared files were not staged.
