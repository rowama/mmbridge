---
id: HANDO-20261031-b-s3-implemented-awaiting-verify
type: handoff
phase: implement
status: complete
owner_agent: claude-code
date: 2026-10-31T01:41:16-05:00
links: [thoughts/shared/slices/2026-10-28-b-s3-multi-bot-registry-routing.md, thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, thoughts/shared/verification/2026-10-31-slice-20261028-b-s3-multi-bot-registry-routing-review.md]
git_commit: aa7ce74
branch: main
next_skill: eng-verify
---
# Handoff: B-s3 implemented, awaiting verify

## Task(s)
- SLICE-20261028-b-s3-multi-bot-registry-routing (plan B Phase 3, incl. friendlier `bin/set-bot`): **implemented, status `review`**. Commits cfe29e2 (slice) + aa7ce74 (Codex review fix), on main, **not pushed** (push only after eng-verify PASS, push_permission standing).
- Codex slice review done (advisory, security): 1 P2, fixed; review file `addressed`.
- Not done: eng-verify (planner), CP-S live demo (Rob), OWNER-GUIDE multi-bot text (Rob's uncommitted OWNER-GUIDE edits; text is in README.md "Several bots" and relay/README.md "Adding a second bot").

## Critical References
- thoughts/shared/slices/2026-10-28-b-s3-multi-bot-registry-routing.md (Progress log + Blockers/deviations: read before verifying)
- thoughts/shared/verification/2026-10-31-slice-20261028-b-s3-multi-bot-registry-routing-review.md
- README.md "Several bots (v0.4.0)" (owner commands, upgrade + rollback)

## Recent changes
- app/store.py: `BotEntry`, `Store` v2, `NAME_RE`, `validate` (unique token / user id), v1 decode -> `migrated_from=1`, `save` keeps `bots.enc.v1.bak`, `rename_v1`, `legacy_owner`, `locked` (store lock), `rotate` re-encrypts the backup.
- app/state.py: schema v2 (`wakes` PK (bot, post_id), `cursors` PK (bot, channel_id)), `meta_key`, `_v1_rename/_v1_create/_v1_copy/_v1_meta` + `State._migrate` (backup 0600 first, one transaction, `live_migration_failed`), bot-first methods, `due_bots`, `fail_pending`, `last_wake`, `failed_for_post`, `BotState` view.
- app/live_filter.py:42 `decide(event, bot_user_id, registered_ids=frozenset())`.
- app/listener.py: per-bot `name`, `self._log` adds `bot`, `registered` callable, `last_error`, payload `delivery_id` `<bot>:<post_id>` and `bot.name`.
- app/wake.py: shared `Dispatcher` (`_pass` round robin, per-bot cap 2 / total 4, background sends, `bot_removed`, per-bot `_identity`, `_crashed` -> `wake_send_crashed`); `tick()` = pass + drain.
- app/live.py: `store_diff`, `ConfigHolder` on Store, `BotSupervisor` (reconcile, status, `report` -> meta `bot:<name>:status`), `LiveRuntime._load/_migrate_store/_commit_migration` (locked re-read), `live_runtime_off` on migration failure, /health `bots_total`/`bots_failing`.
- app/admin.py: `set-bot --name`, `list`, `show [NAME]`, `remove-bot`, `status`, `failed --bot / --retry BOT:POST_ID`, `stats --bot`; refuses to overwrite an unreadable store.
- app/setbot.py + bin/set-bot (new); Dockerfile copies bin; .gitattributes keeps bin/* LF.
- Harness (drivers only): fake_mattermost `revoke_token`; live.py `--name`, wait for added bot (`ADD_BOT_S`), `_post_of` delivery parsing, `revoke_token`, `assert_bot_failing`, `assert_failed_wake_visible_for_bot`, `health()`; image defaults `:bs3`. **No edit** to tests/acceptance/specs/ or tests/acceptance/dsl.py.
- Docs: README.md, relay/README.md, coolify-service.snippet.yaml (RELAY_BOT_GROK_* example), CHANGELOG.md Unreleased.

## Verification (plan Phase 3 block verbatim, WSL, after the review fix, `:bs3` images)
```
== RUN 1  unit 459 passed | mcp 16 passed, 36 skipped | live inprocess 36 passed (96 s) | live container 36 passed (446 s)
== RUN 2  unit 459 passed | mcp 16 passed, 36 skipped | live inprocess 36 passed | live container 36 passed
== RUN 3  unit 459 passed | mcp 16 passed, 36 skipped | live inprocess 36 passed | live container 36 passed
eng-check: OK - 0 error(s), 3 warning(s) (pre-existing) | eng-spec status: lock approval ok, specs and DSL interface match the lock
eng-spec trace: REQ-B1..B8 each mapped to tests/acceptance/specs/test_grok_multibot.py ("(not in an approved design)" label for A/B REQs: tool quirk, see Other Notes)
BLOCK EXIT 0
```
(Same block also exit 0 x3 before the review fix: unit 458.) Red first: the 7 `$B3` specs failed (second set-bot replaced the first bot: `bot_rotated`, wake/marker timeouts).

## Learnings
- eng-run code-review findings parser again wrote "No findings." while Codex listed a P2: always read the raw output (logged in process-feedback.md).
- Container mode: a bot added to a running bridge is live only after the 30 s store reload; the driver waits on /health `bots_total` + `listener ok` (adds ~30 s per second bot per spec; container run ~7.5 min).
- Per-bot in-flight cap also limits a single bot to 2 concurrent wakes (plan decision); two existing tests adjusted (counts/loops, not assertions).

## Artifacts
- thoughts/shared/slices/2026-10-28-b-s3-multi-bot-registry-routing.md (status review)
- thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md (Phase 3 automated checkbox ticked)
- thoughts/shared/verification/2026-10-31-slice-20261028-b-s3-multi-bot-registry-routing-review.md (addressed)
- thoughts/shared/runs/2026-10-31-code-review-slice-20261028-b-s3-multi-bot-registry-routing.md
- app/setbot.py, bin/set-bot, .gitattributes; CHANGELOG.md; README.md; relay/README.md; coolify-service.snippet.yaml; thoughts/shared/process-feedback.md

## Approvals
- None granted this session. Next: CP-S for B-s3 after eng-verify (planner adds it to pending_approvals).
- Planner decisions (slice Blockers): bots_failing also counts a bot whose last wake failed for good; v1 bot named `bot` permanently if Mattermost is unreachable at first boot; per-bot cap 2 applies to a lone bot too.

## Action Items & Next Steps
1. Planner: eng-verify for B-s3 (base e2f6091); after PASS push main (standing).
2. Planner: CP-S ask to Rob per plan Phase 3 Manual Verification. Before -> After: "Before: one mmbridge serves only Eddie; a second set-bot replaces him. After: Rob runs `bin/set-bot grok`, adds the printed RELAY_BOT_GROK_HMAC_SECRET line (+ routine URL/key) to the relay env, and a post in `dev` (grok only) wakes only Grok, Town Square wakes Eddie and Grok once each, Eddie's posts wake nobody, and revoking Grok's token leaves Eddie answering while `admin status` shows grok degraded." Deploy new mmbridge image first; check `/data/bots.enc.v1.bak` and `/data/state.db.v1.bak` exist and eddie still answers.
3. Planner: fold README "Several bots" into OWNER-GUIDE once Rob's uncommitted edits are in (TODOS P2 OWNER-GUIDE pointer).
4. Then eng-ship v0.4.0.

## Other Notes
- Rob's uncommitted AGENTS.md, OWNER-GUIDE.md, receiver.py and untracked thoughts/shared files were not staged.
- `eng-spec trace` labels REQ-A*/REQ-B* "(not in an approved design)" although designs A and B are approved (likely the tool's design-doc REQ parsing); pass/fail column is a template placeholder. Planner to check before pasting into the verify report.
