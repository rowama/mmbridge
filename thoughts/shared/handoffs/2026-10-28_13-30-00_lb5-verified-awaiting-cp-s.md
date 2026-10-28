---
id: HANDO-20261028-lb5-verified-awaiting-cp-s
type: handoff
phase: verify
status: complete
owner_agent: grok-bot
date: 2026-10-28T13:30:00-05:00
links: [thoughts/shared/plans/2026-10-27-live-bots.md, thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md, thoughts/shared/verification/2026-10-28-lb5-wireup-reconnect-acceptance-verify.md]
git_commit: 8f987e7
branch: main
next_skill: eng-ship
---
# Handoff: lb5 verified PASS, awaiting CP-S

## Done this session
- Codex review fixes, all test-first:
  - 54ae627 (review-2: P1 catch-up since+paging, P2 seq, P2 alive)
  - 0a50e87 (review-3)
  - 9bdff90 (review-4)
  - 8f987e7 (review-5)
- Review-6 on --base 3ed94b4 is clean.
- eng-verify PASS at 8f987e7. Report: thoughts/shared/verification/2026-10-28-lb5-wireup-reconnect-acceptance-verify.md.
- Not touched: Rob's uncommitted AGENTS.md, OWNER-GUIDE.md, receiver.py, thoughts/shared/inbox*.

## Action for Rob: CP-S (L-009: runnable now)
`CP-S: thoughts/shared/slices/2026-10-27-lb5-wireup-reconnect-acceptance.md - manual verification`

Checked 2026-10-28 13:23 CDT: `curl https://chats.rmlab.cloud/health` returned `{"ok":true}` with no `listener` field. That means lb5 is **not deployed yet**, so step 1 comes first.

1. **Deploy main.** In Coolify, redeploy mmbridge from main (the tip is pushed). Set up:
   - persistent volume at `/data`
   - env secret `MMB_STORE_KEY`, generated with `python -c "from cryptography.fernet import Fernet;print(Fernet.generate_key().decode())"`
   - replicas 1
   - leave `LIVE_BOTS_ENABLED` unset for now

   Success: `curl https://chats.rmlab.cloud/health` shows `"listener": "disabled"`.
   ready: image builds from main (docker build exit 0); README "Live bots (deploy)" documents it.
2. **Register the bot.** In the Coolify container terminal, run `python -m app.admin set-bot --token-stdin --wake-url https://<receiver>/wake` and paste the bot token. Copy the printed wake secret into your receiver (it is shown once). In Mattermost, add the bot to Town Square.
   ready: set-bot is covered by tests; needs step 1 done.
3. **Turn it on.** Set env `LIVE_BOTS_ENABLED=true` and redeploy. Success: `/health` shows `"listener": "ok", "wake_failed_24h": 0`.
   ready: needs steps 1-2.
4. **Check wakes.** Post "eddie is great" in Town Square and DM the bot "ping". Success: the receiver shows 2 wakes with valid signatures within 10 s. A post by the bot itself gives no wake.
5. **Restart test.** Restart the Mattermost container. While it is down, post in Town Square. Success: after it is back, exactly one wake arrives for that post. This also checks for drift between the fake and real Mattermost resume (hello without seq).
6. **Failed wakes.** Stop the receiver and post again. Success: `python -m app.admin failed` lists the post after retries. Restart the receiver and run `python -m app.admin failed --retry <post_id>`: it delivers once.

To roll back, unset `LIVE_BOTS_ENABLED` and redeploy. The MCP path is unaffected.

## Next
After CP-S is approved: eng-ship. Follow-ups in TODOS:
- OWNER-GUIDE pointer (after Rob commits his edits)
- eng-run findings-parser kit bug
- eng-spec trace label
