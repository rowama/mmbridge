---
id: SLICE-20261027-lb4-signed-wake-dispatcher
type: slice
phase: implement
status: review              # todo | in-progress | blocked | review | done
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
- [x] `app/wake.py`: `sign(secret, ts, body) -> 'v1=<hex>'`; `verify(secret, headers, body, now, window=300) -> bool` (constant-time; used by test receiver and documented for receivers); `Dispatcher(state, cfg, http)` loop: claim_due -> POST with `X-MMB-Delivery/Timestamp/Signature`, 5 s timeout, concurrency 4; 2xx delivered; 408/429/5xx/timeout/connect retry; other 4xx failed; log `wake_failed`; payload has no token
- [x] `tests/acceptance/drivers/live.py` + wake receiver: in-process mode (listener + dispatcher tasks against fake MM + receiver); admin CLI invoked as subprocess/function
- [x] Test-only fast backoff via env (`WAKE_BACKOFF_SCALE`) so A8 spec runs in seconds
- [x] (PR-1) Dispatcher: atomic claim with instance id, `recover_stale` at start + each loop, owner heartbeat; crash-mid-POST and two-dispatcher tests
- [x] (PR-2) Sign/POST with current config at send time; bot-id rotation fails old wakes `bot_rotated`; rotation tests
- [x] (PR-5) Bridge-generated signature tests (independent recompute, ts skew, byte-identical body) + tamper/skew/unknown-version/missing-header rejection
- [x] (PR-8) Runtime prune scheduling (start + every 6 h) with fake-clock test
- [x] (PR-12) Phase 4 acceptance run uses explicit node ids (see plan), expects exactly 7 passed
- [x] Plan Phase 4 Automated Verification all exit 0; existing MCP suite (`.venv/bin/pytest tests/unit -q && .venv/bin/pytest tests/acceptance -q`) still green

## Tasks
- [x] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red) (`.venv/bin/pytest -q --channel live <node ids from specs:>`)
- [x] Write failing unit tests (tests/unit/) for the behaviours above
- [x] Implement
- [x] Run Phase 4 automated verification (plan), including this slice's specs (now green)
- [x] Do not edit locked files: tests/acceptance/specs/**, DSL public interface (CP-C speclock)

## Size check
~200 lines + driver

## Progress log
<!-- date - agent - what changed (file:line) -->
- 2026-10-27 - claude-code - Red first: all 7 `specs:` failed with `NotImplementedError: live driver step 'given_channel' not built yet` (stub driver, the right reason). `tests/unit/test_wake.py` failed at collection (no `app.wake`).
- 2026-10-27 - claude-code - `app/wake.py:37` `sign`, `:41` `verify` (lower-cased headers, `v1=` only, int ts, |skew| <= 300, `hmac.compare_digest`; the MAC is computed over the raw timestamp header bytes). `:59` `Dispatcher(state, cfg, http, max_attempts, clock, poll_s, concurrency)`: `cfg` is a BotConfig or a zero-arg provider that is read at every send (PR-2). `:77` `tick()`: `claim_owner` heartbeat (standby while another owner is fresh) -> `recover_stale` -> prune(7) at start and every 6 h -> `claim_due(now, 4)` -> concurrent `_send`. `:97` `_send`: rotated bot -> `failed bot_rotated`; body = payload with `attempt` = claim attempt (signed bytes = sent bytes); 5 s timeout; 2xx delivered (`wake_delivered` latency_ms), 408/429/5xx/timeout/connect -> `mark_retry` with `state.next_delay` (logs `wake_retry`, or `wake_failed` once max attempts is reached), other 4xx -> failed. Logs carry post_id/attempt/error only.
- 2026-10-27 - claude-code - `app/listener.py:70` stores meta `bot_user_id` after users/me (the dispatcher's rotation check).
- 2026-10-27 - claude-code - `tests/acceptance/drivers/wake_receiver.py` (new): HMAC-verifying receiver (401 invalid, 503 when `down`, `hang` event, dedupes on X-MMB-Delivery). `tests/acceptance/drivers/live.py`: in-process mode (background loop: served fake MM + Listener + Dispatcher; receiver via ASGI transport at https://receiver.test/wake; real `app.admin.main set-bot`/`failed` on a temp /data with a fresh key; the printed secret goes to the receiver; `WAKE_BACKOFF_SCALE=0.05`; `assert_not_woken` uses a marker-DM barrier; signatures are re-verified independently with hashlib). `drop/restore_connection` are left for lb5. `fake_mattermost.py`: `FakeMattermost(mm_ids=True)` gives 26-char channel ids (lb1 heads-up).
- 2026-10-27 - claude-code - Tests: `tests/unit/test_wake.py` 40 (known vector; verify reject table; signature recomputed from the captured request; 5 s timeout; 2xx; retry classes with 2/4/8/16/32 then failed + one `wake_failed`; 4xx permanent; receiver 401 -> failed; attempt signed; concurrency 4; no token/secret/message in payload, headers or logs; crash mid-POST -> exactly once after restart; two dispatchers no double-send; standby takeover; run() recovers stale; prune at start and at +6 h; url/secret rotated after enqueue -> new values; bot rotated -> `bot_rotated`), + listener meta assertion. Mutation check: dropping the own-post / not-chosen filter rules makes the A1-not-chosen and A3 specs fail.
- 2026-10-27 - claude-code - Verification (commit 446047a): `.venv/bin/pytest tests/unit -q` exit 0 (216 passed); `.venv/bin/pytest tests/acceptance -q` exit 0 (16 passed, 9 skipped); `python3 .eng/bin/eng-spec status .` exit 0 (matches lock); PR-12 spec run exit 1: **5 passed, 2 failed** (`test_dm_to_bot_wakes_bot_once`, `test_forged_wake_is_rejected`), both because of the blocker below. Also ran (not in this slice) `test_bot_token_never_appears_in_logs_output_or_wakes`: passed.
- 2026-10-27 - claude-code - Codex slice-diff review NOT run: `codex` CLI is not installed on this machine (`which codex` is empty). Required for this slice (security): the planner should run `python3 .eng/bin/eng-run code-review SLICE-20261027-lb4-signed-wake-dispatcher` where Codex is available.
- 2026-10-27 - grok-bot - Unblocked per plan delta `thoughts/shared/plans/2026-10-27-live-bots-delta-no-allowlist.md` ("Unblocking lb4"): `app/store.py` validate accepts `channels: []` (ids still 26 chars); `app/admin.py` `set-bot --channels` optional (omitted = DM-only bot, explicit `""` still refused); `tests/unit/test_store.py` `channels=[]` case moved from rejected to accepted (`test_empty_channel_list_is_a_dm_only_bot`); `tests/unit/test_admin.py` `test_set_bot_without_channels_is_dm_only`; driver `tests/acceptance/drivers/live.py` omits `--channels` for an empty list. No locked file touched. Unit 217 passed; PR-12 run 7 passed.

- 2026-10-27 - grok-bot - Codex review fixes (verification FAIL 8b7be94): P1 `app/wake.py` `token_fp()`; listener stores meta `bot_token_fp` next to `bot_user_id`; `Dispatcher.tick` claims nothing until meta id is set AND fp matches the current config token (logs `dispatcher_waiting_identity`), so a stale id from a previous token/run never approves old wakes and missing meta no longer skips the check. P2 each POST wrapped in `asyncio.wait_for(..., TIMEOUT_S)` -> retryable `timeout`. Tests: `test_no_identity_sends_nothing`, `test_restart_after_token_swap_waits_then_fails_old_wakes`, `test_drip_response_hits_overall_deadline`, listener fp assertion. Unit 220 passed.

## Blockers / deviations from plan
- RESOLVED 2026-10-27 (see progress log): the DM-only bot issue below.
- **Issue in Phase 4: spec tests/acceptance/specs/test_live_bots.py::test_dm_to_bot_wakes_bot_once and ::test_forged_wake_is_rejected - both call `given_live_bot("eddie", channels=[])` (a DM-only bot), but lb1's store validation (PR-6, `app/store.py:66-68`, locked in by `tests/unit/test_store.py:107` "channels=[] rejected") and `admin set-bot --channels` (required, `app/admin.py:52-62`) refuse an empty channel list.** The driver goes through the real admin CLI (DSL docstring "via the admin CLI"), which answers `error: invalid_argument: channels must be team/channel,... (got '')`. I did not improvise: no store/admin change, no driver workaround (such as registering a dummy channel). Decision needed (Rob/planner). Suggested minimal resolution: allow an empty `channels` list (a DM-only bot is valid per REQ-A2): `store.validate` accepts `[]` (each id still 26 chars), `set-bot --channels ""` (or optional) stores `[]`, and `test_store.py:107` flips to "empty list accepted". That is about 10 lines plus tests. The dispatcher and receiver behind both specs are built, and the forged-wake path is unit-tested (`test_verify_rejects`, `test_receiver_rejecting_signature_is_permanent_failure`).
- Deviation (PR-2, design detail): no `cfg_gen` column. The bot identity of a wake is the `bot.user_id` already in its payload, and the dispatcher compares it with meta `bot_user_id` (written by the listener after users/me). url/secret are read from the config provider at send time, so they need no generation, and no schema migration is needed. Behaviour matches the plan's tests.
- Deviation (small): a second dispatcher whose owner heartbeat is fresh does not exit. It stands by (`tick()` returns 0, logs `dispatcher_standby`) and takes over after the heartbeat expires (60 s). The plan says "refuses to start"; standby is a superset and still never sends.
- Codex review not run (codex CLI unavailable here); see the progress log.
- 2026-10-27: code-review 2 P2 (unsigned X-MMB-Delivery replay) fixed: verify() requires X-MMB-Delivery == signed body delivery_id; 4 new verify reject cases.
- 2026-10-27: code-review 3 P2 (split read of bot_user_id / bot_token_fp) fixed: listener writes one meta row bot_identity = "<token_fp>:<bot_user_id>"; dispatcher reads only that; test_identity_is_one_snapshot_not_split_keys.
- 2026-10-27: code-review 4 P2 (malformed wake_url raised InvalidURL out of tick) fixed: store.https_ok parses with httpx.URL; dispatcher fails that wake permanently as invalid_url and keeps running.
- 2026-10-27: code-review 5 P2 (httpx.DecodingError escaped tick) fixed: other httpx.HTTPError -> retry http_error; any other exception -> retry error_<Class>; send errors can no longer stop the dispatcher.
