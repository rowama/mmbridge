---
id: SLICE-20261028-b-s3-multi-bot-registry-routing
type: slice
phase: implement
status: review           # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-28
links: [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, docs/architecture/2026-10-28-grok-webhook-multibot.md]
plan: thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md
plan_phase: 3
review: required (security: encrypted store v2 migration, per-bot isolation, token uniqueness) - thoughts/shared/verification/2026-10-28-slice-20261028-b-s3-multi-bot-registry-routing-review.md
reqs: [REQ-B4, REQ-B6, REQ-B7, REQ-B8]
specs: [tests/acceptance/specs/test_grok_multibot.py::test_bot_on_generic_signed_webhook_keeps_receiving_signed_wakes, tests/acceptance/specs/test_grok_multibot.py::test_post_in_channel_only_one_bot_is_in_wakes_only_that_bot, tests/acceptance/specs/test_grok_multibot.py::test_post_in_shared_channel_wakes_each_bot_once, tests/acceptance/specs/test_grok_multibot.py::test_dm_to_one_bot_wakes_only_that_bot, tests/acceptance/specs/test_grok_multibot.py::test_post_by_a_registered_bot_wakes_no_bot, tests/acceptance/specs/test_grok_multibot.py::test_revoked_token_of_one_bot_leaves_other_bots_working_and_marks_it_failing, tests/acceptance/specs/test_grok_multibot.py::test_one_bot_routine_down_leaves_other_bot_waking_and_shows_its_failed_wake]
---
# Slice B-s3: multi-bot registry and routing

Plan: [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md](../plans/2026-10-28-grok-webhook-multibot.md) Phase 3. Architecture: docs/architecture/2026-10-28-grok-webhook-multibot.md; ADRs 0011, 0013..0016 (0012 rejected - no claim_wake). **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
Two or more bots (e.g. eddie, grok, test) registered on one mmbridge, each with its own token and wake target; each post wakes only the bots it concerns, once each; posts by any registered bot wake nobody; a revoked token or dead target for one bot leaves the others working and shows that bot failing in admin status and /health counts. Existing one-bot v1 store and state.db migrate in place with .v1.bak backups.

## Acceptance criteria
- [x] `app/store.py` v2 (ADR-0013): named bots, name regex, unique tokens, v1->v2 migrate on load, v2 on save with `bots.enc.v1.bak` 0600, redaction for all bots, rotate-key covers v2
- [x] `app/admin.py`: set-bot --name (+ --wake-secret-stdin), list, show NAME, remove-bot (pending -> failed bot_removed), status, failed/stats --bot, --retry BOT:POST_ID; no --name on one-bot store edits that bot
- [x] `app/state.py` schema v2 (ADR-0014) with user_version migration in one transaction after `state.db.v1.bak`; idempotent; failure -> live off, MCP up, `live_migration_failed`
- [x] `app/live_filter.py` decide(event, bot_user_id, registered_ids) drops any registered bot author (B7)
- [x] `app/live.py` BotSupervisor: listener per bot, reconcile on reload (add/remove/rotate, no redeploy), per-bot status; one bot 401 never affects others (B8)
- [x] `app/wake.py` per-row config, delivery_id `<bot>:<post_id>`, per-bot in-flight cap 2; `app/main.py` /health bots_total, bots_failing
- [x] fake MM multiple bot users + revoke; DSL register_bot for several bots, assert_bot_failing, assert_failed_wake_visible_for_bot (two-bot outage spec: grok routine down, eddie still woken once, grok's failed wake visible via `failed --bot grok`)
- [x] Unit tests per plan Phase 3 (migrations incl. crash mid-migration, admin, filter table, supervisor, dispatcher fairness, health)
- [x] Friendlier `bin/set-bot` (Rob 2026-10-30, folded into B-s3): one owner-facing wrapper for `app.admin set-bot --name NAME` that prompts for the Mattermost bot token (shown once in Mattermost; regenerate if lost) and wake URL default `http://relay:8080/wake/NAME`, generates or accepts the HMAC-SHA256 wake secret and prints the matching `RELAY_BOT_<NAME>_HMAC_SECRET` line for Coolify; never echoes the token; Fernet store key stays a one-time Coolify env (not touched by the wrapper)
- [x] README/OWNER-GUIDE multi-bot setup + rollback; CHANGELOG (README + relay/README; OWNER-GUIDE not edited: Rob's uncommitted edits)
- [x] Full suite: all A + B live specs (in-process and container, 3x), MCP specs; `eng-spec trace .` maps REQ-B1..B8

## Tasks
- [x] eng-resume; read plan Phase 3 (Changes Required is the detailed checklist), architecture contracts, ADRs above
- [x] Run this slice's executable specs and confirm they fail for the right reason (red): `LIVE_MODE=inprocess .venv/bin/pytest -q --channel live $B3` (`B3` = this card's `specs:` list, defined in plan Phase 3 Automated Verification). Specs of later slices are NOT selected and stay red.
- [x] Write failing unit tests (tests/unit/) for the behaviours above
- [x] Implement (drivers/DSL bodies may change; spec files and DSL public interface are locked - do not edit them, raise a back-up instead)
- [x] Run plan Phase 3 Automated Verification block verbatim (explicit `LIVE_IMAGE`/`RELAY_IMAGE` = `:bs3`, in-process AND container, full selection 3x per DoD concurrency rule); all exit 0; paste outputs in the handoff
- [x] Do not stage Rob's uncommitted AGENTS.md, OWNER-GUIDE.md, receiver.py or untracked thoughts/shared files
- [x] Commit; eng-handoff ("implemented, awaiting review/verify")

## Manual verification (Rob, at CP-S)
See plan Phase 3 Manual Verification.

## Progress log
<!-- date - agent - what changed (file:line) -->
- 2026-10-31 - claude-code - red first: the 7 `$B3` specs (`LIVE_MODE=inprocess --channel live`) failed for the right reason: the one-bot store, so a second `set-bot` replaced the first bot (`wake_failed ... bot_rotated`, marker/routine waits timed out).
- 2026-10-31 - claude-code - code: app/store.py v2 (`BotEntry`, `Store`, NAME_RE, unique token/user id, v1 -> one bot + `rename_v1`, `bots.enc.v1.bak` on first save, rotate covers the backup, `legacy_owner`); app/state.py schema v2 (PK (bot, post_id) / (bot, channel_id), per-bot meta `bot:<name>:*`, lease `listener_owner:<name>`, `user_version` 2, v1 migration in one transaction after `state.db.v1.bak`, `BotState` view, `due_bots`, `fail_pending`, `last_wake`, per-bot failed/stats); app/live_filter.py `registered_ids`; app/listener.py per-bot name/logs, `delivery_id` `<bot>:<post_id>`, `last_error`; app/wake.py shared Dispatcher (per-bot in-flight 2, total 4, round robin, background sends, `bot_removed`, per-bot identity, `wake_send_crashed`); app/live.py `BotSupervisor` (reconcile add/remove/rotate, status reporter to meta), v1 store migration at boot, `live_migration_failed` -> degraded/MCP up, /health `bots_total`/`bots_failing`; app/admin.py `--name`, list, show NAME, remove-bot, status, failed/stats `--bot`, `--retry BOT:POST_ID`, store lock; app/setbot.py + bin/set-bot (Dockerfile copies bin, .gitattributes keeps LF). Harness: fake MM `revoke_token`; live driver `--name`, wait for an added bot, delivery-id parsing, `revoke_token`, `assert_bot_failing`, `assert_failed_wake_visible_for_bot`; image defaults `:bs3`. No edit to specs or tests/acceptance/dsl.py.
- 2026-10-31 - claude-code - unit tests updated to the bot-first API and extended (store v2/migration/backup/rotation, state v2/migration incl. crash mid-migration + idempotent rerun, filter table with registered ids, admin multi-bot + wrapper, supervisor add/remove/rotate, revoked bot isolation, dead-target fairness, bot_removed, health counts, boot migration): 458 passed.
- 2026-10-31 - claude-code - plan Phase 3 Automated Verification block verbatim (WSL, `:bs3` images), exit 0, all 3 runs: unit 458 passed; mcp 16 passed/36 skipped; live inprocess 36 passed (~96 s); live container 36 passed (~445 s). eng-check OK (3 pre-existing warnings); eng-spec status: lock approval ok, specs and DSL interface match the lock; eng-spec trace maps REQ-B1..B8 to test_grok_multibot.py.
- 2026-10-31 - claude-code - Codex slice review (`eng-run code-review ... --base e2f6091`): 1 P2 (boot-time v1 store migration could overwrite a concurrent set-bot), fixed: `store.locked` (moved from admin) taken by the runtime, which re-reads and keeps an already-v2 file. Review file `addressed`. Phase 3 block re-run after the fix (see next entry).

## Blockers / deviations from plan
- Diff is ~2.1k added / ~0.5k removed lines (plan Phase 3 scope in one slice), well over the 100-200 line guideline.
- Per-bot in-flight cap 2 also applies to a single bot (was 4 in flight); tests test_concurrency_4 -> `_total_2_per_bot`, test_two_dispatchers loop 4 -> 6 ticks (assertions unchanged).
- Dispatcher sends now run as background tasks (so a dead target cannot stall other bots); `tick()` still waits for its sends.
- A v1 store is renamed after its Mattermost username and saved as v2 by the runtime at first boot (and by admin commands when they meet a v1 file); if Mattermost cannot be reached then, the bot is named `bot` (plan fallback) permanently.
- /health `bots_failing` counts bots whose listener is degraded OR whose most recent wake failed for good (dead target); clears on that bot's next delivered wake.
- `admin status` reads listener state from meta `bot:<name>:status` written by the running bridge every change / 10 s; shown as `off (no report for Ns; runtime stopped?)` when older than 60 s.
- Log `store_updated` fields are now per bot (`eddie.wake_url`, `+grok`, `-test`); live log lines carry `bot`.
- `set-bot` refuses to write when bots.enc exists but does not decrypt (before: overwrote it), so other bots are never lost.
- OWNER-GUIDE.md not edited (Rob's uncommitted edits); multi-bot setup and rollback are in README.md "Several bots" and relay/README.md "Adding a second bot". Planner: fold into OWNER-GUIDE once Rob's edits are in.
- eng-spec trace prints "(not in an approved design)" for REQ-A*/B* although designs A and B are approved (tool parsing; planner to check).
