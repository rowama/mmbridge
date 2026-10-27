---
id: SLICE-20261027-lb1-bot-store-admin-cli
type: slice
phase: implement
status: done             # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-27
links: [thoughts/shared/plans/2026-10-27-live-bots.md]
plan: thoughts/shared/plans/2026-10-27-live-bots.md
plan_phase: 1
review: required (security: stored token, ADR-0006) - thoughts/shared/verification/2026-10-27-slice-20261027-lb1-bot-store-admin-cli-review.md
reqs: [REQ-A7]
specs: none - no listener yet; REQ-A7 token-secrecy for store/CLI proven by unit tests, end-to-end spec test_bot_token_never_appears_in_logs_output_or_wakes turns green in slice 5
---
# Slice 1: Encrypted bot store + admin CLI

Plan: [thoughts/shared/plans/2026-10-27-live-bots.md](../plans/2026-10-27-live-bots.md) Phase 1. Architecture: docs/architecture/2026-10-26-live-bots.md. **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
Operator can `python -m app.admin set-bot/show` inside the container; config sits Fernet-encrypted at /data/bots.enc and the token never appears in output or logs.

## Acceptance criteria
- [x] `app/store.py`: `BotConfig` dataclass (token, wake_url, wake_secret, channels:list[str] ids, version=1); `load(path, key) -> BotConfig`, `save(path, key, cfg)` atomic (tmp+rename, mode 0600); `StoreError(code)` codes `store_key_missing`, `store_unreadable`; `__repr__` masks token+secret
- [x] `app/admin.py` (`python -m app.admin`): `set-bot --token-stdin --wake-url URL --channels team/chan,...` resolves names to ids via existing `app/mattermost.Client` (`/users/me`, channel by name, `members/me`) and refuses non-member channels (never joins); generates 32-byte wake secret printed once unless `--wake-secret-stdin`; `show` masks token to last 4, never prints secret; `wake_url` must be https (http only if `LIVE_ALLOW_HTTP_WAKE=true`, for tests)
- [x] Logs `store_updated` with field names only; `app/logging.py` redact filter extended to the stored token/secret
- [x] `requirements.txt`: pin `cryptography`; Dockerfile creates /data owned by uid 10001
- [x] No listener, no state DB, no HTTP surface change; `/health` unchanged
- [x] (PR-7) `admin rotate-key` via MultiFernet (ADR-0006); `MMB_STORE_KEY` accepts `new,old`; tests per plan Phase 1
- [x] (PR-6) Config validation on load/set-bot: version==1, required fields, https wake_url, channel id format, wake secret >= 32 chars; tests per plan Phase 1
- [x] Plan Phase 1 Automated Verification all exit 0; existing MCP suite (`.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`) still green

## Tasks
- [x] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red) - n/a, see specs:
- [x] Write failing unit tests (tests/unit/) for the behaviours above
- [x] Implement
- [x] Run Phase 1 automated verification (plan), including this slice's specs (now green)
- [x] Do not edit locked files: tests/acceptance/specs/**, DSL public interface (CP-C speclock)

## Size check
~180 lines + tests (actual: store 163 + admin 137 + logging +16; tests 330)

## Progress log
<!-- date - agent - what changed (file:line) -->
- 2026-10-27 - claude-code - red first: tests/unit/test_store.py + test_admin.py failed at collection (no app.store/app.admin).
- 2026-10-27 - claude-code - app/store.py (new, BotConfig/validate/load/save/rotate, MultiFernet, atomic 0600 via mkstemp+fsync+os.replace); app/admin.py (new, set-bot/show/rotate-key; reuses app/service._member_channel so never joins); app/logging.py register_secret + literal redaction; requirements.txt cryptography==50.0.2; Dockerfile /data 700 uid 10001. Commit cf78905.
- 2026-10-27 - claude-code - verification: `pytest tests/unit -q` 114 passed (exit 0; 43 new); `pytest tests/acceptance -q` 16 passed 9 skipped (exit 0); `eng-check .` OK exit 0; `eng-spec status .` matches lock; `docker build -t mmbridge:lb1 .` exit 0. Container smoke: /data drwx------ appuser; `admin show` with no store -> `store_unreadable: file`; http wake URL refused; saved file 0600, no plaintext.

- 2026-10-27 - claude-code - Codex slice review (`eng-run code-review`, diff 691f4ac...cf78905): no findings; review file set `addressed`. Slice -> review; awaiting planner eng-verify + CP-S manual check.

## Blockers / deviations from plan
- Minor (detail-level, no plan conflict): `StoreError` has a third code `store_invalid` for save-time validation (load-time failures stay `store_unreadable: <reason>`); `StoreError.detail` carries the field/reason. Supplied wake secret comes in via `--wake-secret-stdin` (second stdin line) as in the card/architecture, not a `--wake-secret` argv flag (plan PR-6 wording), so it never lands in shell history. `rotate-key` defaults: `--new-key-env MMB_STORE_KEY_NEW`, `--old-key-env MMB_STORE_KEY`.
- Heads-up for lb4/lb5: PR-6 requires 26-char channel ids, but `FakeMattermost.add_channel` makes ids like `c-rmlab-dev`; test_admin re-ids channels locally. The live driver (admin CLI setup against the fake) will need 26-char ids in the fake.
