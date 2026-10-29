---
id: RESEA-20261028-grok-webhook-multibot-current-code
type: research
phase: research
status: in-review
owner_agent: grok-bot
date: 2026-10-28
links: [docs/design/2026-10-28-grok-webhook-multibot.md]
git_commit: 4ab1e72
branch: main
---
# Research: mmbridge code today, for increment B (Grok Bot webhook wake + multi-bot)
<!-- Codebase research: what the code IS, file:line, no recommendations. -->

## Research questions
From the approved scope (HOLD, REQ-B1..B8) and the locked Grok Bot wake contract (POST per-routine URL, `Authorization: Bearer <routine key>`, any JSON body, 200 = run started):
1. (B1, B2) How does `app/wake.py` build, authenticate and send a wake today (URL, headers, body, signature, replay window)?
2. (B3) What retry, backoff, at-most-once and failure-recording behaviour does the dispatcher/state have?
3. (B4) How does `python -m app.admin set-bot` collect and validate the wake target, and how does a change reach the running process without a redeploy?
4. (B4, B6) What is the shape of the encrypted bot store (`app/store.py`): how many bots, which fields, validation, secret redaction?
5. (B6, B7) How does the live filter (`app/live_filter.py`) decide that a post wakes a bot, and where is "the bot" identity taken from?
6. (B6, B8) How many listeners/dispatchers/identities does the runtime hold, and how are per-bot failures surfaced?
7. (B5) How does a bot post a reply today (MCP tools, token, threads)?
8. (tests) What test scaffolding covers these modules?

## Summary
v0.3.0 is built around exactly ONE bot end to end. The store holds one `bot` object (`token`, `wake_url`, `wake_secret`); the runtime builds one ConfigHolder, one Listener (one websocket on that bot's token) and one Dispatcher. The dispatcher POSTs the JSON payload with three custom headers (`X-MMB-Delivery`, `X-MMB-Timestamp`, `X-MMB-Signature` = HMAC-SHA256 v1); no `Authorization` header is sent to the wake target. The wake queue (`wakes` table) is keyed by `post_id` alone, and `meta` holds single-valued keys (`bot_identity`, `listener_owner`, `dispatcher_owner`, `last_event_at`). The live filter drops only the bot's own posts, system posts and group DMs; it has no notion of other registered bots. Replies go through the v1 MCP tools with the caller's Bearer token; `post_channel`/`dm_send` take no thread root.

## Detailed findings

### 1. Wake construction and authentication (`app/wake.py`)
- Contract documented in the module docstring: raw JSON body + `X-MMB-Delivery`, `X-MMB-Timestamp`, `X-MMB-Signature v1=<hex HMAC-SHA256(secret, ts + "." + body)>` (`app/wake.py:3-6`).
- Signing: `_mac` HMAC-SHA256 over `ts + b"." + body` (`app/wake.py:42-43`); `sign` prefixes `v1=` (`app/wake.py:46-47`).
- Receiver-side `verify` (used by tests / the temp receiver): lower-cases headers, requires `v1=`, rejects `|now - ts| > 300` (`WINDOW_S`, `app/wake.py:30`, `:50-61`), constant-time compare, and requires `X-MMB-Delivery` to equal the signed body's `delivery_id` (`app/wake.py:63-70`). Replay protection lives entirely in this receiver-side function plus the timestamp window; mmbridge itself does not verify anything on the outbound path.
- Send: `_send` serialises `{**payload, "attempt": attempts}` compactly (`app/wake.py:131`), sets headers `Content-Type`, `X-MMB-Delivery` (= post id), `X-MMB-Timestamp`, `X-MMB-Signature` (`app/wake.py:132-134`) and POSTs to `cfg.wake_url` with a 5 s overall deadline (`TIMEOUT_S`, `app/wake.py:31`, `:135-137`). No `Authorization` header is set anywhere in the dispatcher.
- Payload body is built by the listener, not the dispatcher (`app/listener.py:447-462`): `version`, `kind: "post"`, `delivery_id`, `attempt`, `bot {user_id, username}`, `channel {id, name, display_name, type, team}`, `sender {user_id, username}`, `post {id, message, create_at (ISO), root_id}`. These already cover the fields REQ-B1 names (channel, sender, text, post id, thread root id).
- Config is read at send time through a callable (`app/wake.py:80-82`, `:110`), so URL/secret rotation applies to already-queued wakes (docstring `app/wake.py:9-10`).
- Logging: only event name, post id, attempt, error class, latency (`app/wake.py:73-74`, `:149-161`); docstring states token/secret/signature/message text are never logged (`app/wake.py:16`).

### 2. Retry, backoff, at-most-once, failure recording (B3)
- Status classification: 2xx -> `mark_delivered`; `None` (timeout/connect/http_error/other exception), 408, 429, >=500 -> `mark_retry` with `next_delay(attempts)`; any other status (incl. 401/403/404) and `invalid_url` -> `mark_failed` (`app/wake.py:138-161`).
- Delivery loop: `tick` heartbeats a single `dispatcher_owner` lease, `recover_stale`, prunes every 6 h, then claims up to 4 due wakes and sends concurrently (`app/wake.py:96-123`; `CONCURRENCY`, `PRUNE_EVERY_S`, `app/wake.py:32-33`).
- Identity gate: nothing is claimed until meta `bot_identity` = `"<token_fp>:<bot_user_id>"` matches the current config's token fingerprint (`app/wake.py:111-119`; `token_fp` `app/wake.py:37-39`). A wake whose payload `bot.user_id` differs from that id fails `bot_rotated` (`app/wake.py:127-130`).
- Ledger: `wakes.post_id TEXT PRIMARY KEY` (`app/state.py:25-39`); `INSERT OR IGNORE` on post_id is the single enqueue gate (`app/state.py:3-4`, `:126-131`); `enqueue_and_advance` inserts and moves the per-channel cursor in one transaction (`app/state.py:145-150`). Claim flips up to `limit` rows to `in_flight` with a 30 s lease and increments attempts (`app/state.py:202-211`; `LEASE_S` `app/state.py:20`).
- Owner leases: `claim_owner`/`release_owner` on meta keys `dispatcher_owner` | `listener_owner`, one value each (`app/state.py:181-199`).
- Operator view: `admin failed` lists post id, channel id, attempts, last_error, time; `--retry` requeues (`app/admin.py:99-113`); `admin stats` counts and latency (`app/admin.py:116-124`); `/health` exposes `listener` status and `wake_failed_24h` count only (`app/live.py:171-181`, `app/main.py:36-38`). The `wakes` rows carry no bot column (`app/state.py:25-39`).

### 3. `admin set-bot` and live reconfiguration (B4)
- CLI: `set-bot --token-stdin [--wake-secret-stdin] --wake-url URL`; `--channels` hidden and refused (`app/admin.py:29-45`, `:57-58`). There is no bot name / id argument and no list/remove subcommand (`app/admin.py:31-44`).
- Flow: token = stdin line 1; secret = stdin line 2 if `--wake-secret-stdin`, else `secrets.token_urlsafe(32)` (`app/admin.py:59-64`); secret length >= 32 (`app/admin.py:65-66`, `MIN_SECRET` `app/store.py:20`); `https_ok(wake_url)` (`app/admin.py:67-68`); `MMB_STORE_KEY` required (`app/admin.py:69-71`); token checked against Mattermost `/users/me` for the username (`app/admin.py:48-53`, `:72`); a new `BotConfig` REPLACES the stored one (`app/admin.py:73-79`); logs changed field names only (`app/admin.py:80-81`); prints the generated secret once (`app/admin.py:82-84`).
- `show` prints version, last 4 of token, wake_url, "secret set (hidden)" (`app/admin.py:87-90`).
- Live reload: `ConfigHolder` stats `bots.enc` (mtime, size, inode) every `RELOAD_S = 30` s (`app/live.py:26`, `:50-55`, `:78-81`); on change it `store.load`s, keeps the old config on `StoreError` (`store_reload_failed`), compares `FIELDS = token, wake_url, wake_secret` and notifies subscribers with `(old, new)` (`app/live.py:57-76`). The Listener subscribes and reconnects only when the token changed (`app/listener.py:113-122`); the Dispatcher reads url/secret per send (`app/wake.py:110`). So a wake-target change applies without redeploy today, within ~30 s.

### 4. Bot store shape (`app/store.py`)
- File `/data/bots.enc` (`MMB_DATA_DIR`), Fernet ciphertext of `{"version": 1, "bot": {...}}`, mode 0600, atomic write (`app/store.py:1-8`, `:23-24`, `:129-143`). Key from `MMB_STORE_KEY`, comma list via MultiFernet for rotation (`app/store.py:78-85`, `:162-166`).
- `BotConfig(token, wake_url, wake_secret, version=1)`; repr masks token and hides secret (`app/store.py:39-50`).
- `validate`: version must be 1; all three fields required non-empty; `wake_url` must pass `https_ok`; secret >= 32 chars (`app/store.py:53-63`). `https_ok` parses with `httpx.URL`, needs https, or http when `LIVE_ALLOW_HTTP_WAKE=true` (`app/store.py:66-75`).
- Decode reads the single `doc["bot"]` object (`app/store.py:88-106`); `save` writes exactly one `bot` (`app/store.py:150-159`). There is no wake-target "kind" field and no per-bot name/key; legacy `channels` is ignored and dropped (`app/store.py:7`).
- Secrets: loaded/saved token and wake secret are registered with the log redact filter (`app/store.py:124-126`); the filter replaces registered literals (len >= 8) and Bearer/Authorization patterns in every log record (`app/logging.py:9-33`).

### 5. Live filter and bot identity (B6, B7)
- Module docstring: wake on DMs (`D`) and on every non-system post in O/P channels the bot is a member of; membership is the channel filter (`app/live_filter.py:1-8`).
- `decide(event, bot_user_id)` (`app/live_filter.py:41-74`): only `posted` events (`:45-46`); validates `id`, `channel_id`, `user_id`, `create_at`, `message`, `channel_type` (`:55-69`); returns `None` when `post.user_id == bot_user_id`, when `post.type` is set (system post) or when the channel is a group DM `G` (`:70-71`); otherwise a `WakeIntent` with post/channel/user ids, message, create_at, root_id and hints (`:72-74`; dataclass `:15-24`).
- `bot_user_id` is a single value: the Listener's own `/users/me` result (`app/listener.py:179-189`), passed at `app/listener.py:271` and `:403`. No list of other bot ids is consulted, and Mattermost's `is_bot`/`props.from_bot` fields are not read.
- Membership tracking is per Listener: `members` / `_seen` dicts (`app/listener.py:94-95`), refreshed by `_refresh_members` / `_refresh_soft` / `_membership_event` (`app/listener.py:329-367`); catch-up iterates the bot's member channels (`app/listener.py:369-411`).

### 6. Runtime cardinality and failure surfacing (B6, B8)
- `LiveRuntime.start`: gated by `LIVE_BOTS_ENABLED=true` (`app/live.py:131-133`); loads one config (`:135-140`), opens one `State` on `state.db` (`:141-145`), builds one ConfigHolder, one Listener, one Dispatcher and starts three tasks (`:146-157`). Listener and Dispatcher each run under `supervise` (crash -> `task_crashed`, backoff 1->60 s) (`app/live.py:89-110`).
- Listener single-instance lease `listener_owner` (`app/listener.py:172-174`); meta `bot_identity`, `bot_user_id`, `last_event_at`, `ws_connection_id` are single rows (`app/listener.py:176-189`, `:254`).
- 401 on `/users/me` or websocket -> `Unauthorized` -> status `degraded`, log `mm_unauthorized`, retry after `auth_retry_s` (`app/listener.py:144-148`, `:179-183`, `:197-199`). Health reports one `listener` word (`off|connecting|ok|degraded`) (`app/listener.py:92`, `app/live.py:171-181`); there is no per-bot status.

### 7. Reply path today (B5)
- MCP endpoint `/mcp` requires `Authorization: Bearer <Mattermost bot token>`; the token is set in a ContextVar per request (`app/auth.py:26-45`), and each tool call uses a fresh `Client` with that token (`app/mcp.py:47-84`, `app/mattermost.py:20-32`).
- Tools: `list_channels`, `post_channel(team, channel, message)`, `read_channel`, `dm_send(username, message)`, `dm_read` (`app/mcp.py:86-110`). Service functions `post_channel` (`app/service.py:59`) and `dm_send` (`app/service.py:90`) take no `root_id`; no `root_id` appears in `app/service.py`. The wake payload carries channel id/name, team name and sender username (`app/listener.py:453-461`), which are the inputs these tools take.
- Own-reply suppression: a post by the bot's own user id never produces a WakeIntent (`app/live_filter.py:70`).

### 8. Tests
- Unit: `tests/unit/test_wake.py`, `test_admin.py`, `test_store.py`, `test_live_filter.py` (74 test functions across these four), plus `test_listener.py`, `test_state.py`, `test_main_live.py`, `test_reconnect.py`.
- Acceptance: `tests/acceptance/specs/test_live_bots.py` with drivers `fake_mattermost.py`, `live.py`, `wake_receiver.py` (`tests/acceptance/drivers/`).

## Open questions (for architecture, not answered by the code)
- Exact Grok Bot webhook response codes other than 200 (401/404/429 behaviour) are not documented in the repo; the dispatcher's mapping is at `app/wake.py:149-161`.
