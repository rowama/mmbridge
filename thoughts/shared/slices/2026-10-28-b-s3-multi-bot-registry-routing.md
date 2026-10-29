---
id: SLICE-20261028-b-s3-multi-bot-registry-routing
type: slice
phase: implement
status: todo             # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-28
links: [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, docs/architecture/2026-10-28-grok-webhook-multibot.md]
plan: thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md
plan_phase: 3
review: required (security: encrypted store v2 migration, per-bot isolation, token uniqueness) - thoughts/shared/verification/2026-10-28-slice-20261028-b-s3-multi-bot-registry-routing-review.md
reqs: [REQ-B4, REQ-B6, REQ-B7, REQ-B8]
specs: [tests/acceptance/specs/test_grok_multibot.py::test_bot_on_generic_signed_webhook_keeps_receiving_signed_wakes, tests/acceptance/specs/test_grok_multibot.py::test_post_in_channel_only_one_bot_is_in_wakes_only_that_bot, tests/acceptance/specs/test_grok_multibot.py::test_post_in_shared_channel_wakes_each_bot_once, tests/acceptance/specs/test_grok_multibot.py::test_dm_to_one_bot_wakes_only_that_bot, tests/acceptance/specs/test_grok_multibot.py::test_post_by_a_registered_bot_wakes_no_bot, tests/acceptance/specs/test_grok_multibot.py::test_revoked_token_of_one_bot_leaves_other_bots_working_and_marks_it_failing]
---
# Slice B-s3: multi-bot registry and routing

Plan: [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md](../plans/2026-10-28-grok-webhook-multibot.md) Phase 3. Architecture: docs/architecture/2026-10-28-grok-webhook-multibot.md; ADRs 0011, 0013..0016 (0012 rejected - no claim_wake). **Security-relevant: gets the cross-model review.**

## Outcome (user-visible, demoable)
Two or more bots (e.g. eddie, grok, test) registered on one mmbridge, each with its own token and wake target; each post wakes only the bots it concerns, once each; posts by any registered bot wake nobody; a revoked token or dead target for one bot leaves the others working and shows that bot failing in admin status and /health counts. Existing one-bot v1 store and state.db migrate in place with .v1.bak backups.

## Acceptance criteria
- [ ] `app/store.py` v2 (ADR-0013): named bots, name regex, unique tokens, v1->v2 migrate on load, v2 on save with `bots.enc.v1.bak` 0600, redaction for all bots, rotate-key covers v2
- [ ] `app/admin.py`: set-bot --name (+ --wake-secret-stdin), list, show NAME, remove-bot (pending -> failed bot_removed), status, failed/stats --bot, --retry BOT:POST_ID; no --name on one-bot store edits that bot
- [ ] `app/state.py` schema v2 (ADR-0014) with user_version migration in one transaction after `state.db.v1.bak`; idempotent; failure -> live off, MCP up, `live_migration_failed`
- [ ] `app/live_filter.py` decide(event, bot_user_id, registered_ids) drops any registered bot author (B7)
- [ ] `app/live.py` BotSupervisor: listener per bot, reconcile on reload (add/remove/rotate, no redeploy), per-bot status; one bot 401 never affects others (B8)
- [ ] `app/wake.py` per-row config, delivery_id `<bot>:<post_id>`, per-bot in-flight cap 2; `app/main.py` /health bots_total, bots_failing
- [ ] fake MM multiple bot users + revoke; DSL register_bot for several bots, assert_bot_failing
- [ ] Unit tests per plan Phase 3 (migrations incl. crash mid-migration, admin, filter table, supervisor, dispatcher fairness, health)
- [ ] README/OWNER-GUIDE multi-bot setup + rollback; CHANGELOG
- [ ] Full suite: all A + B live specs (container), MCP specs; `eng-spec trace .` maps REQ-B1..B8

## Tasks
- [ ] eng-resume; read plan Phase 3 (Changes Required is the detailed checklist), architecture contracts, ADRs above
- [ ] Run this slice's executable specs (specs:) and confirm they fail for the right reason (red): `.venv/bin/pytest -q --channel live <node ids from specs:>`
- [ ] Write failing unit tests (tests/unit/) for the behaviours above
- [ ] Implement (drivers/DSL bodies may change; spec files and DSL public interface are locked - do not edit them, raise a back-up instead)
- [ ] Run plan Phase 3 Automated Verification; all exit 0; in-process AND `LIVE_MODE=container`
- [ ] Do not stage Rob's uncommitted AGENTS.md, OWNER-GUIDE.md, receiver.py or untracked thoughts/shared files
- [ ] Commit; eng-handoff ("implemented, awaiting review/verify")

## Manual verification (Rob, at CP-S)
See plan Phase 3 Manual Verification.
