# Changelog
All notable changes to this project. Format: Keep a Changelog style; newest first.

## [Unreleased]
<!-- id: CHANG-20261030-b-s2-round-trip-reply | owner_agent: claude-code | date: 2026-10-30 -->
### Added
- Grok Bots answer where they were woken: the wake carries reply hints (version 2: reply tool, team/channel or DM username, thread root_id, issued_at) and post_channel / dm_send take an optional root_id to answer inside a thread; a root_id from another channel or DM, or one the bot cannot see, is refused as invalid_root and nothing is posted. The relay raises a tripwire (log relay_tripwire, optional Mattermost alert via RELAY_ALERT_URL/TOKEN/CHANNEL) on repeated bad signatures, rate-limit hits, routine 401/403 and double forwards, and /health shows double_forward_24h.

<!-- id: CHANG-20261029-b-s1-wake-relay | owner_agent: claude-code | date: 2026-10-29 -->
### Added
- Wake relay (relay/, own image and Coolify app): verifies mmbridge's signed wakes (signature, 5-minute window, per-bot secret) and starts each bot's Grok Bot routine with its Bearer routine key; forged, altered, stale and repeated wakes never start a routine, each bot is rate-limited (30/min, burst 10), and a routine or relay outage is retried by mmbridge then shown as one failed wake. Point a bot at it with `set-bot --wake-url https://<relay>/wake/<name>`; no mmbridge redeploy.


## [0.3.0] - 2026-10-28
<!-- id: CHANG-20261028-ship-0.3.0 | owner_agent: grok-bot | date: 2026-10-28 -->
Live bots (increment A, slices lb1-lb5): with LIVE_BOTS_ENABLED=true the bridge listens to Mattermost as the configured bot and sends one signed wake to its wake URL for every post by someone else in its member channels and DMs, with retries, reconnect and catch-up. Operator CLI `python -m app.admin` manages the encrypted bot store and the wake queue. Known gap: a live Mattermost-restart resume check was deferred (TODOS).
<!-- id: CHANG-20261028-lb5-wireup-reconnect | owner_agent: unassigned | date: 2026-10-28 -->
### Added
- Live bots go live with LIVE_BOTS_ENABLED=true: the listener and wake dispatcher start with the bridge, /health reports listener (disabled|off|connecting|ok|degraded) and wake_failed_24h, dropped Mattermost connections reconnect and catch up missed posts (all member channels on all teams and DMs, 15 min window) with exactly one wake per post, and store edits (token, wake URL, secret) apply without a redeploy. Catch-up pages by post id (Mattermost ignores paging with `since`), finds DMs for a bot in no team, and a token rotated mid-connect reconnects.

<!-- id: CHANG-20261027-lb4b-drop-allowlist | owner_agent: unassigned | date: 2026-10-27 -->
### Changed
- Live bots: no channel allow-list. `python -m app.admin set-bot` takes only the token and wake URL (`--channels` is refused as no longer used; existing /data/bots.enc files with channel ids still load), and the bot wakes on every post by someone else in public or private channels it is a Mattermost member of, plus DMs; thread replies carry root_id. The bridge never joins channels.

<!-- id: CHANG-20261027-lb2-state-db | owner_agent: unassigned | date: 2026-10-27 -->
### Added
- Live bots: durable wake ledger and queue in /data/state.db (one wake per post, retries with 2-32 s backoff, crash-safe claims); `python -m app.admin failed [--retry POST_ID]` and `stats` for operators.

<!-- id: CHANG-20261027-lb1-bot-store | owner_agent: unassigned | date: 2026-10-27 -->
### Added
- Operator CLI `python -m app.admin set-bot | show | rotate-key` stores the live bot's token, wake URL, wake secret and channel ids Fernet-encrypted at /data/bots.enc (key MMB_STORE_KEY); the token is never printed or logged. No runtime behaviour change yet.

<!-- id: CHANG-20261026-d-hardening-xff-bearer | owner_agent: unassigned | date: 2026-10-26 -->
### Security
- Forged X-Forwarded-For headers no longer bypass the anonymous rate limit (only FORWARDED_ALLOW_IPS proxies are trusted), and the Bearer scheme is matched case-insensitively.


## [0.2.0] - 2026-10-26
<!-- id: CHANG-20261026-ship-0.2.0 | owner_agent: Eddie | date: 2026-10-26 -->
First release of the Mattermost MCP bridge at https://chats.rmlab.cloud/mcp (slices 1-3).
Each Grok Bot connects with its own Mattermost bot token and gets five tools: list_channels,
post_channel, read_channel, dm_send, dm_read. Posts and DMs share a 20-per-minute limit per bot.
<!-- id: CHANG-20261026-s3-dm | owner_agent: unassigned | date: 2026-10-26 -->
### Added
- Bots can send direct messages to a Mattermost user by username and read that DM (dm_send, dm_read); a second DM reuses the same conversation, unknown usernames are refused, and DMs count against the 20 posts per minute limit.

<!-- id: CHANG-20261026-s2-post-read-channel | owner_agent: unassigned | date: 2026-10-26 -->
### Added
- Bots can post to and read channels they belong to (post_channel, read_channel); non-member channels are refused without joining, and posts are limited to 20 per minute per bot.

<!-- id: CHANG-20261026-s1-mcp-list-channels | owner_agent: unassigned | date: 2026-10-26 -->
### Added
- MCP endpoint at /mcp: Grok Bots connect with their own Mattermost bot token (Authorization: Bearer) and can list their channels; the header-echo placeholder is removed and unknown paths return 404.

