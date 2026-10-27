---
id: SLICE-20261027-lb1-bot-store-admin-cli
type: slice
phase: implement
status: todo             # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
plan_phase: 1
review: required (security: stored token, ADR-0006) - thoughts/shared/verification/2026-10-27-lb1-review.md
reqs: [REQ-A7]
specs: none - no listener yet; REQ-A7 token-secrecy for store/CLI proven by unit tests, end-to-end spec test_bot_token_never_appears_in_logs_output_or_wakes turns green in slice 5
---
# Slice 1: Encrypted bot store + admin CLI

Plan: [thoughts/shared/plans/2026-10-27-live-bots.md](../plans/2026-10-27-live-bots.md) Phase 1. Architecture: docs/architecture/2026-10-26-live-bots.md. **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
Operator can `python -m app.admin set-bot/show` inside the container; config sits Fernet-encrypted at /data/bots.enc and the token never appears in output or logs.

## Acceptance criteria
- [ ] `app/store.py`: `BotConfig` dataclass (token, wake_url, wake_secret, channels:list[str] ids, version=1); `load(path, key) -> BotConfig`, `save(path, key, cfg)` atomic (tmp+rename, mode 0600); `StoreError(code)` codes `store_key_missing`, `store_unreadable`; `__repr__` masks token+secret
- [ ] `app/admin.py` (`python -m app.admin`): `set-bot --token-stdin --wake-url URL --channels team/chan,...` resolves names to ids via existing `app/mattermost.Client` (`/users/me`, channel by name, `members/me`) and refuses non-member channels (never joins); generates 32-byte wake secret printed once unless `--wake-secret-stdin`; `show` masks token to last 4, never prints secret; `wake_url` must be https (http only if `LIVE_ALLOW_HTTP_WAKE=true`, for tests)
- [ ] Logs `store_updated` with field names only; `app/logging.py` redact filter extended to the stored token/secret
- [ ] `requirements.txt`: pin `cryptography`; Dockerfile creates /data owned by uid 10001
- [ ] No listener, no state DB, no HTTP surface change; `/health` unchanged
- [ ] Plan Phase 1 Automated Verification all exit 0; existing MCP suite (`.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`) still green

## Tasks
- [ ] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red) - n/a, see specs:
- [ ] Write failing unit tests (tests/unit/) for the behaviours above
- [ ] Implement
- [ ] Run Phase 1 automated verification (plan), including this slice's specs (now green)
- [ ] Do not edit locked files: tests/acceptance/specs/**, DSL public interface (CP-C speclock)

## Size check
~180 lines + tests

## Progress log
<!-- date - agent - what changed (file:line) -->

## Blockers / deviations from plan
none
