---
id: PLAN-20261028-grok-webhook-multibot
type: plan
phase: plan
status: draft            # input (pre-draft from an earlier phase) | draft | in-review | approved | in-progress | done | superseded
owner_agent: grok-bot
date: 2026-10-28
links: [docs/design/2026-10-28-grok-webhook-multibot.md, docs/architecture/2026-10-28-grok-webhook-multibot.md, thoughts/shared/research/2026-10-28-grok-webhook-multibot-current-code.md]
plan_review: thoughts/shared/verification/2026-10-28-grok-webhook-multibot-plan-review.md
---
# Plan: Grok Bot webhook wake, round-trip reply and multi-bot (increment B)

## Overview
Make a Mattermost post wake a real Grok Bot routine (through a thin HMAC->Bearer wake relay), let that bot answer in the same channel/DM/thread, then serve two or more bots from one mmbridge. Implements REQ-B1..B8 of [design B](../../../docs/design/2026-10-28-grok-webhook-multibot.md) per the approved [architecture B](../../../docs/architecture/2026-10-28-grok-webhook-multibot.md) and ADR-0011, 0013..0016 (ADR-0012 claim_wake rejected). Research: [current code](../research/2026-10-28-grok-webhook-multibot-current-code.md). Three vertical slices, order approved by Rob 2026-10-28 (option C "prudent", thin wedge first): **B-s1** relay + Grok wake for one bot -> **B-s2** round-trip reply + root_id + relay replay/rate-limit hardening -> **B-s3** multi-bot registry and routing. One version (v0.4.0).

## Current State Analysis
Verified against code 2026-10-28 (commit 0430daa):
- `app/wake.py:46` `sign(secret, ts, body)` and `:50` `verify(secret, headers, body, now, window=300)` already exist (ADR-0008) -> the relay reuses `verify` verbatim (strong reason for `relay/` in this repo, OQ-B3).
- `app/wake.py:77-125` `Dispatcher(state, cfg, http)`: single `cfg`; `_send(w, bot_id, cfg)`; response mapping 2xx/408/429/5xx/other-4xx already as the architecture needs -> relay's 503/424/429 map onto existing behaviour with no mmbridge change in B-s1.
- `app/listener.py:447-462` `_payload` emits `version: 1` with `bot`, `channel`, `sender`, `post{id,message,create_at,root_id}`; `delivery_id = post_id`. Already carries everything REQ-B1 needs; `reply` hints and `delivery_id = <bot>:<post_id>` are added in B-s2/B-s3.
- `app/store.py:40-166` `BotConfig` single bot, `version == 1` validated; `load/save/rotate`. Multi-bot v2 is B-s3 only (ADR-0013).
- `app/state.py:94-293` `State` keyed by `post_id` only; `claim_owner(key=...)` already parameterised (reused for per-bot listener lease in B-s3).
- `app/live_filter.py:41` `decide(event, bot_user_id)` -> gains `registered_ids` in B-s3.
- `app/live.py:35-181` `ConfigHolder` (30 s mtime reload) + `LiveRuntime` single listener + dispatcher -> `BotSupervisor` in B-s3. Reload already makes wake-URL changes apply without redeploy (B4 one-bot part works today; B-s1 proves it via the relay).
- `app/service.py:59` `post_channel(c, team, channel, message)`, `:90` `dm_send(c, username, message, *, me)`; `app/mcp.py:91,101` tool signatures; no `root_id` (B-s2, ADR-0015).
- No `relay/` directory exists; `Dockerfile` builds the bridge only; `coolify-service.snippet.yaml` describes one app.
- Acceptance: `tests/acceptance/drivers/live.py` (in-process + container mode, `LIVE_MODE`), `drivers/wake_receiver.py` (HMAC-verifying fake receiver), `drivers/fake_mattermost.py` (REST+WS, one bot). DSL `given_live_bot`, `post_in`, `dm`, `assert_woken_once`, etc. Speclock currently covers `test_live_bots.py` + `test_mmbridge.py`.

## Desired End State
With the relay deployed as its own Coolify app (env per bot `RELAY_BOT_<NAME>_HMAC_SECRET|ROUTINE_URL|ROUTINE_KEY`) and each bot registered on mmbridge with `--wake-url https://<relay>/wake/<name>`: a post in a member channel or a DM starts that bot's Grok routine exactly once within 10 s; the routine replies via `post_channel`/`dm_send` (with `root_id` for threads) as itself and is not re-woken; forged/tampered/replayed wakes never start a routine; two+ bots route independently and one failing bot never blocks the others; operator sees per-bot state in `admin status`. Verified by `.venv/bin/pytest tests/acceptance --channel live -q` (A + B specs) against the mmbridge and relay containers, unit tests, and a live CP-S demo per slice.

### Key Discoveries
- HMAC verify code is reusable as-is (`app/wake.py:50`) -> relay imports a copied/shared module; no second implementation.
- Existing dispatcher response classes already treat 503/429 as retry and 424 as permanent, so B-s1 needs zero mmbridge runtime changes: it is relay + harness + docs.
- Live reload of the store already exists, so REQ-B4 (switch target, no redeploy) is a `set-bot --wake-url` call.

## Open questions resolved in this plan
- **OQ-B1 (non-200 mapping)** - assumed mapping (architecture): upstream 2xx -> relay 200; 408/429/5xx/timeout/connect error -> 503 (mmbridge retries); 401/403/404/other 4xx -> 424 `{"upstream":<code>}` (mmbridge permanent `failed http_424`; relay tripwire on 401/403). **Verified in the B-s1 spike** (`relay/spike_routine.py` against a real Rob routine: valid key -> 200; wrong key; unknown routine URL) and recorded in the B-s1 handoff + ADR-0011 note. Fallback if the real routine returns something unexpected (e.g. 200 on a bad key, or 302): treat any non-2xx not in the retry set as permanent 424 (safe default, never re-wakes), and if a bad key returns 200 the tripwire relies on the daily count check; the deviation is recorded before CP-S.
- **OQ-B2 (body passthrough)** - assumed: the routine exposes the JSON body to the bot verbatim. **Verified in the B-s1 spike** (spike posts a body with a marker; Rob's routine instruction echoes it back to a Mattermost post or Grok chat). Fallback if not verbatim (no claim_wake, ADR-0012 stays rejected): relay additionally sends a compact human-readable `text` field first in the body (`"text": "Mattermost wake: reply with post_channel team=<t> channel=<c> root_id=<r> | from @rob: <message>"`) built only from the verified body, so reply hints survive in whatever the routine exposes; the routine instruction in OWNER-GUIDE tells the bot to parse it. Decision recorded at B-s1 CP-S; B-s2 reply depends on it.
- **OQ-B3 (relay location)** - **decided: `relay/` in this repo**, own `relay/Dockerfile`, own Coolify app (architecture default). Evidence: `app/wake.py:50` verify is shared code, one CI/test run covers both, and the acceptance harness (ADR-0016) builds both images from one checkout. Relay imports nothing else from `app/` (copy of `verify` pinned by a unit test that compares against `app.wake.sign`) so the image stays tiny and has no Mattermost/store code.
- **OQ-B4** - out of this increment (TODOS).

## What We're NOT Doing
- Web admin UI; HTTP admin endpoint.
- Bot-to-bot wakes and loop caps (REQ-A3 bot-to-bot part) - registered-bot posts are always dropped (B7).
- Channel ignore-list; auto-accept invites (REQ-A5 suite, stays in TODOS).
- `claim_wake` or any mmbridge-side Bearer routine key (ADR-0012 rejected; ADR-0011 keeps keys only in relay env).
- Relay admin CLI or relay-side bot store: relay config is Coolify env only (Rob 2026-10-28).
- Moving the relay onto the Grok Bot computer (OQ-B4).
- Group DMs, reactions, files, edits/deletes; multiple replicas of mmbridge or relay.
- Strict-v1 generic receivers (unknown payload fields are additive).

## Implementation Approach
Runtime call path (end state): `Listener(bot)` WS `posted` -> `live_filter.decide(event, bot_user_id, registered_ids)` -> `State.enqueue(bot, post_id, ...)` || shared `Dispatcher.tick` -> `claim_due` -> per-row `cfg.bots[w.bot]` -> `wake.sign` -> POST `https://relay/wake/<bot>` -> relay `verify` + window + dedupe + rate limit -> POST routine URL `Authorization: Bearer <key>` (body byte-for-byte) -> Grok routine -> MCP `post_channel(..., root_id)`/`dm_send(..., root_id)` with the bot's MM token -> Mattermost -> Listener drops (author registered).

Key signatures:
```python
# relay/relay.py (new, B-s1; FastAPI app, own image)
@dataclass(frozen=True)
class RelayBot: name: str; hmac_secret: str; routine_url: str; routine_key: str
def load_bots(env: Mapping[str, str]) -> dict[str, RelayBot]   # RELAY_BOT_<NAME>_{HMAC_SECRET,ROUTINE_URL,ROUTINE_KEY}; <NAME> upper, '-'->'_'
def verify(secret: str, headers: Mapping, body: bytes, now: int, window: int = 300) -> bool   # copy of app.wake.verify
def map_upstream(status: int | None) -> tuple[int, dict]       # None = timeout/connect error
def create_app(env=None, http: httpx.AsyncClient | None = None, clock=time.time, seen: "Seen | None" = None) -> FastAPI
#   POST /wake/{bot} -> 404 unknown bot | 401 bad_sig/stale | 200 duplicate (B-s2) | 429 rate_limited (B-s2) | forward -> map_upstream
#   GET /health -> {"ok": true, "bots": n, "forwarded_24h": n, "rejected_24h": n}
class Seen:                                                     # B-s2: sqlite /data/relay.db, (delivery_id PK, seen_at), prune 24 h
    def __init__(self, path: str); def has(self, d: str) -> bool; def add(self, d: str, now: int) -> None; def prune(self, now: int) -> int
class RateLimit:                                                # B-s2: token bucket per bot, 30/min burst 10 (env RELAY_RATE_PER_MIN, RELAY_BURST)
    def allow(self, bot: str, now: float) -> bool
class Tripwire:                                                 # B-s2: counts bad_sig/rate_limited/upstream_401_403; logs relay_tripwire; optional MM post via RELAY_ALERT_URL/TOKEN
# app/service.py + app/mcp.py (B-s2, ADR-0015)
async def post_channel(c, team, channel, message, root_id: str | None = None) -> dict   # invalid_root on MM 400/404 for root
async def dm_send(c, username, message, *, me, root_id: str | None = None) -> dict
# app/listener.py _payload (B-s2): version 2, reply{tool, team, channel|username, root_id}, issued_at
# app/store.py (B-s3, ADR-0013)
@dataclass
class BotEntry: name: str; token: str; user_id: str; wake_url: str; wake_secret: str
@dataclass
class Store: version: int; bots: dict[str, BotEntry]            # load() migrates v1 -> {"<username>": ...}; save writes v2 + bots.enc.v1.bak
# app/state.py (B-s3, ADR-0014): schema v2, every method takes bot first: enqueue(bot, post_id, ...), mark_*(bot, post_id), get_cursor(bot, ch)...
# app/live_filter.py (B-s3): decide(event, bot_user_id, registered_ids: frozenset[str])
# app/live.py (B-s3): class BotSupervisor: reconcile(store) starts/stops Listener per bot; status() -> dict[name, BotStatus]
# app/wake.py (B-s3): Dispatcher(state, holder, http, per_bot_in_flight=2) - looks up cfg per row
```
Config (env): mmbridge unchanged until B-s3 (`LIVE_BOTS_ENABLED`, `MMB_STORE_KEY`, `MMB_DATA_DIR`, ...). Relay: `RELAY_BOT_<NAME>_HMAC_SECRET` (copy of that bot's mmbridge wake secret), `RELAY_BOT_<NAME>_ROUTINE_URL`, `RELAY_BOT_<NAME>_ROUTINE_KEY`, `RELAY_DATA_DIR` (/data), `RELAY_UPSTREAM_TIMEOUT_S` (5), `RELAY_RATE_PER_MIN` (30), `RELAY_BURST` (10), `RELAY_ALLOW_HTTP_UPSTREAM` (false; tests only), optional `RELAY_ALERT_URL`/`RELAY_ALERT_TOKEN`/`RELAY_ALERT_CHANNEL`.

File-tree diff:
```
relay/relay.py      + (S1; S2 Seen/RateLimit/Tripwire)   relay/Dockerfile + (S1)   relay/requirements.txt + (S1)
relay/spike_routine.py + (S1, OQ-B1/B2 spike, not in image) relay/README.md + (S1)
tests/unit/test_relay.py + (S1, S2)
app/service.py ~ (S2 root_id)   app/mcp.py ~ (S2 root_id)   app/listener.py ~ (S2 payload v2; S3 per bot)
app/store.py ~ (S3 v2)   app/admin.py ~ (S3 --name, list, remove-bot, status, --bot)   app/state.py ~ (S3 schema v2)
app/live_filter.py ~ (S3)   app/live.py ~ (S3 BotSupervisor)   app/wake.py ~ (S3 per-row cfg, fairness)   app/main.py ~ (S3 /health counts)
tests/acceptance/specs/test_grok_multibot.py + (CP-C lock)   tests/acceptance/dsl.py ~ (new steps, CP-C lock)
tests/acceptance/drivers/relay.py + (S1: runs relay in-process or container)   drivers/fake_routine.py + (S1; S2 replies via MCP)
tests/acceptance/drivers/live.py ~ (S1 relay wiring; S3 multi-bot)   drivers/fake_mattermost.py ~ (S3 multiple bot users, revoke)
coolify-service.snippet.yaml ~ (S1 relay app)   README.md / OWNER-GUIDE.md / CHANGELOG.md ~ (each slice; OWNER-GUIDE edits only after Rob's uncommitted changes are in)
```

---

## Phase 1: B-s1 relay + Grok Bot wake for one bot
Slice card: [thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md](../slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md). **Security-relevant (auth: HMAC verify, Bearer key handling): cross-model review required.**
### Changes Required
- **Spike first (OQ-B1/B2):** `relay/spike_routine.py` - posts one JSON body with a marker to a real routine URL (key via stdin/env, never argv/log); cases valid key, wrong key, bad URL; prints status codes only. Rob runs it once; results recorded in the handoff and an "Observed" note appended to ADR-0011. Apply the OQ-B1/B2 fallback (see above) if observations differ.
- `relay/relay.py`: `load_bots(env)` (fail start if any bot lacks a field or secret < 32 chars or URL not https unless `RELAY_ALLOW_HTTP_UPSTREAM`); `POST /wake/{bot}`: unknown bot -> 404; read raw body; `verify` (constant-time, 300 s window) else 401 `{"reason":"bad_sig"|"stale"}`; forward body byte-for-byte with `Authorization: Bearer`, `Content-Type: application/json`, `X-MMB-Delivery`, timeout 5 s; `map_upstream`; JSON logs `relay_forwarded`, `relay_rejected{reason}`, `relay_upstream{code}` with a redact filter registered for every secret and key; `GET /health` counts only.
- `relay/Dockerfile` (python slim, non-root uid 10001, `/data` volume, uvicorn), `relay/requirements.txt` (fastapi, uvicorn, httpx pinned as root).
- `tests/unit/test_relay.py`: env parsing (name mapping, missing field, short secret, http url); verify accepts a body signed by `app.wake.sign` (drift guard); bad sig / tampered body / stale ts / missing headers -> 401 and upstream not called; mapping table (200, 204, 408, 429, 500, 503, timeout, connect error -> 503; 401/403/404/400 -> 424 with upstream code); body forwarded byte-identical and Bearer set; key/secret absent from captured logs and responses; unknown bot 404.
- Acceptance harness: `drivers/fake_routine.py` (HTTP server, checks `Authorization: Bearer <key>`, records bodies, 401 on wrong key, can be set down/up); `drivers/relay.py` (in-process relay app, or container `mmbridge-relay:bs1` when `LIVE_MODE=container`); `drivers/live.py` gains `register_bot(name, wake="grok"|"signed")` wiring mmbridge `set-bot --wake-url <relay>/wake/<name>` and relay env with the same secret; implements the B-s1 DSL steps.
- Ops/docs: `coolify-service.snippet.yaml` relay app; `relay/README.md` (env, Coolify setup, key rotation runbook); README section; CHANGELOG Unreleased. OWNER-GUIDE: add "Grok routine setup" only after Rob's uncommitted OWNER-GUIDE.md edits are committed by Rob (else put the text in relay/README.md and note it in the handoff).
### Success Criteria
#### Automated Verification
- [ ] `.venv/bin/pytest tests/unit -q` exit 0 incl. `tests/unit/test_relay.py`
- [ ] `docker build -t mmbridge:bs1 . && docker build -t mmbridge-relay:bs1 relay` exit 0
- [ ] `.venv/bin/pytest -q --channel live <B-s1 node ids from the slice card specs:>` exit 0 (in-process and `LIVE_MODE=container`)
- [ ] `.venv/bin/pytest tests/acceptance --channel live -q` A specs still green; `.venv/bin/pytest tests/acceptance -q` (MCP specs) green
- [ ] `python3 .eng/bin/eng-check .` exit 0; `python3 .eng/bin/eng-spec status .` matches lock
#### Manual Verification
- [ ] Rob: spike run against his real Eddie routine; observed codes for valid / wrong key / bad URL and whether the body is visible verbatim to the bot are written down (OQ-B1/B2 closed or fallback chosen).
- [ ] Rob on Coolify: relay app deployed with eddie env; `set-bot --wake-url https://<relay>/wake/eddie` (existing secret copied into `RELAY_BOT_EDDIE_HMAC_SECRET`); post in Town Square and DM eddie -> Eddie routine run starts each time (seen in Grok Bot routine history), no receiver log needed; `curl -X POST https://<relay>/wake/eddie -d '{}'` -> 401, no run.

**Stop:** CP-S for B-s1 before Phase 2.

---

## Phase 2: B-s2 round-trip reply, root_id, relay replay + rate limit hardening
Slice card: [thoughts/shared/slices/2026-10-28-b-s2-round-trip-reply-root-id.md](../slices/2026-10-28-b-s2-round-trip-reply-root-id.md). **Security-relevant (replay protection, rate limit, tripwire): cross-model review required.**
### Changes Required
- `app/service.py`, `app/mcp.py`: optional `root_id` on `post_channel`/`dm_send` (validated 26-char id via `app/validate.py`; passed on `POST /posts`); MM 400/404 attributable to root -> tool error `invalid_root`; tool schema documents it. Existing MCP specs unchanged.
- `app/listener.py` `_payload`: `version: 2`, `issued_at`, `reply{tool: post_channel|dm_send, team, channel | username, root_id}` per architecture (`root_id` = post.root_id when set, else null; DMs: `dm_send` username=sender). `delivery_id` stays `post_id` until B-s3 (then `<bot>:<post_id>`).
- `relay/relay.py`: `Seen` dedupe (sqlite `/data/relay.db`, delivery id recorded only after upstream 2xx; duplicate -> 200 `{"status":"duplicate"}` not forwarded; prune 24 h); in-flight guard so two concurrent identical deliveries forward once; `RateLimit` per bot -> 429; `Tripwire` (bad_sig > 5 in 10 min, rate limit hit, upstream 401/403) -> `relay_tripwire` log + optional MM alert post; OQ-B2 fallback `text` field if B-s1 spike required it.
- Harness: `fake_routine` acts as the bot on wake: reads `reply` hints (or fallback `text`), calls the real MCP bridge `post_channel`/`dm_send` with the bot's MM token; DSL `given_routine_answers`, `replay_last_wake`, `assert_replied`.
- Unit: `tests/unit/test_service.py`/`test_mcp.py` root_id pass-through + invalid_root + bad id format; listener payload v2 for channel top-level / thread / DM; relay dedupe (lost-response retry -> duplicate, upstream 503 then retry forwards once, concurrent duplicate), prune, rate limit, tripwire thresholds with fake clock.
- Docs: OWNER-GUIDE/relay README routine instruction text ("when woken, answer with the tool and target in `reply`"); CHANGELOG.
### Success Criteria
#### Automated Verification
- [ ] `.venv/bin/pytest tests/unit -q` exit 0 incl. new root_id, payload v2 and relay hardening tests
- [ ] B-s2 node ids from the slice card `specs:` pass with `--channel live` (in-process and container); all B-s1 and A live specs still green
- [ ] `.venv/bin/pytest tests/acceptance -q` (MCP) green; `docker build` both images exit 0
- [ ] `python3 .eng/bin/eng-check .` exit 0; `python3 .eng/bin/eng-spec status .` matches lock
#### Manual Verification
- [ ] Rob: post "@eddie status?" in Town Square -> Eddie's answer appears there as Eddie, and no second Eddie run starts; reply inside an Eddie thread -> answer lands in that thread; DM "hi" -> answer in the DM.
- [ ] Rob/Ulrik: re-POST a captured signed wake (from relay debug or a curl with the same headers) within 5 min -> `duplicate`, no new routine run.

**Stop:** CP-S for B-s2 before Phase 3.

---

## Phase 3: B-s3 multi-bot registry and routing
Slice card: [thoughts/shared/slices/2026-10-28-b-s3-multi-bot-registry-routing.md](../slices/2026-10-28-b-s3-multi-bot-registry-routing.md). **Security-relevant (token store v2 migration, per-bot isolation): cross-model review required.**
### Changes Required
- `app/store.py` v2 (ADR-0013): `Store{version: 2, bots}`; name regex `^[a-z0-9][a-z0-9-]{0,31}$`; token unique across bots; v1 loads as one bot named by MM username (fallback `bot`); first save writes v2 and keeps `bots.enc.v1.bak` 0600; all tokens/secrets registered with redaction; rotate-key covers v2.
- `app/admin.py`: `set-bot --name NAME --token-stdin --wake-url URL [--wake-secret-stdin]`; `list`, `show NAME`, `remove-bot NAME` (pending wakes -> failed `bot_removed`), `status`; `failed [--bot] [--retry BOT:POST_ID]`, `stats [--bot]`. Backward compat: `set-bot` without `--name` on a one-bot store edits that bot.
- `app/state.py` schema v2 (ADR-0014): `wakes PK(bot, post_id)`, `cursors PK(bot, channel_id)`, per-bot meta keys, listener lease `listener_owner:<name>`; migration `user_version 1->2` in one transaction after `state.db.v1.bak`; idempotent; failure -> `live_migration_failed`, live runtime off, MCP up.
- `app/live_filter.py`: `decide(event, bot_user_id, registered_ids)` drops posts by any registered bot (B7).
- `app/live.py`: `BotSupervisor` reconciles listeners on store reload (add/remove/rotate without redeploy); per-bot status `off|connecting|ok|degraded` + last error; one bot's 401 never stops another (B8).
- `app/wake.py`: shared dispatcher, per-row config lookup, `delivery_id = <bot>:<post_id>`, per-bot in-flight cap 2 (fairness), bot removed -> failed.
- `app/main.py` `/health`: add `bots_total`, `bots_failing` (counts only); `listener` = worst bot.
- Harness: fake MM with multiple bot users and `revoke_token`; DSL `register_bot` for several bots, `assert_bot_failing`.
- Unit: store v1->v2 migration + backup + rollback read, name/uniqueness validation; admin commands; state migration (crash mid-migration, idempotent rerun); filter table with registered ids; supervisor add/remove/rotate; dispatcher fairness with one dead target; health counts.
- Docs: README/OWNER-GUIDE multi-bot setup (one relay env block per bot, same name everywhere); CHANGELOG; rollback steps (restore `.v1.bak` files).
### Success Criteria
#### Automated Verification
- [ ] `.venv/bin/pytest tests/unit -q` exit 0 incl. store/state migration, admin, filter, supervisor, fairness tests
- [ ] `docker build -t mmbridge:bs3 . && docker build -t mmbridge-relay:bs3 relay` exit 0; `.venv/bin/pytest tests/acceptance --channel live -q` exit 0 (all A + B specs, container mode)
- [ ] `.venv/bin/pytest tests/acceptance -q` (MCP) green
- [ ] `python3 .eng/bin/eng-check .` exit 0; `python3 .eng/bin/eng-spec status .` matches lock; `python3 .eng/bin/eng-spec trace .` maps every REQ-B1..B8 to >= 1 spec (pasted into verification report)
#### Manual Verification
- [ ] Rob on Coolify: after deploy the existing eddie bot still works (v1 store migrated, `.v1.bak` present); register grok (`set-bot --name grok`, relay env `RELAY_BOT_GROK_*`); post in a channel only grok is in -> only Grok answers; post in Town Square -> both answer once each; eddie posts "@grok hi" -> nobody woken; revoke grok's token in Mattermost -> eddie still answers, `admin status` shows grok degraded.

**Stop:** CP-S for B-s3, then eng-ship (v0.4.0).

## Demo script
1. Coolify: deploy relay app (`relay/Dockerfile`, volume `/data`) with `RELAY_BOT_EDDIE_HMAC_SECRET` (= eddie's mmbridge wake secret), `RELAY_BOT_EDDIE_ROUTINE_URL`, `RELAY_BOT_EDDIE_ROUTINE_KEY`; `curl https://<relay>/health` -> `ok`.
2. mmbridge terminal: `python -m app.admin set-bot --name eddie --token-stdin --wake-url https://<relay>/wake/eddie` (B-s1/B-s2: without `--name`); no redeploy.
3. In Mattermost post "@eddie status?" in Town Square: Eddie answers there as Eddie within ~a minute; no second run. Reply in that thread -> answer in the thread. DM Eddie "hi" -> answer in DM.
4. `curl -X POST https://<relay>/wake/eddie -d '{}'` -> 401; Grok routine history shows no new run.
5. (B-s3) Register grok the same way; post in `dev` (grok only) -> only Grok answers; Town Square -> both answer once; revoke grok's token -> eddie still answers; `python -m app.admin status` shows grok degraded.

## Testing Strategy
- Unit (tests/unit): relay env/verify/mapping/forwarding/redaction (S1), relay dedupe/rate limit/tripwire, root_id service/MCP, payload v2 (S2), store v2 + migration, state v2 + migration, admin, filter, supervisor, dispatcher fairness, health (S3).
- Integration: relay app with httpx MockTransport upstream (S1/S2); mmbridge listener+dispatcher -> in-process relay -> fake routine (S1); fake routine -> real MCP bridge -> fake MM (S2).
- Acceptance (executable specs, ADR-0016): `tests/acceptance/specs/test_grok_multibot.py`, 20 specs tagged REQ-B1 (2), B2 (5), B3 (3), B4 (2), B5 (3), B6 (3), B7 (1), B8 (1); channel `live` (fake MM REST+WS with several bot users, real relay app/image, fake Grok routine that checks Bearer and replies through the real MCP bridge, admin CLI; container mode `LIVE_MODE=container` for both images). No UI channel (no UI; ADR-0016). A specs (`test_live_bots.py`) and MCP specs (`test_mmbridge.py`) stay green as regression. Specs not yet served by an earlier slice fail red until their slice (each slice card lists its node ids). Speclock: `python3 .eng/bin/eng-spec lock .`; CP-C row records `approved speclock sha256:<hex>` (see below).
- Traceability: each slice's verification report includes `eng-spec status .` and `eng-spec trace .`.
- Manual: per-phase checks above; CP-S live demo with a real Grok routine (fake-routine drift check, ADR-0016).

## Spec lock
- Locked files: `tests/acceptance/specs/test_grok_multibot.py`, `test_live_bots.py`, `test_mmbridge.py`, DSL public interface + assertion bodies.
- CP-C decision line: `approved speclock sha256:32118b1e5aa406c0`

## Risks, Rollback, Migration
- Relay is a separate app: stopping it only makes mmbridge retry/fail those rows; MCP path untouched. Flag `LIVE_BOTS_ENABLED` stays the kill switch.
- Fake routine drift from real Grok: B-s1 spike + live CP-S each slice.
- Bearer routine key on relay host (accepted risk ADR-0011): env only, redacted, rate limit + tripwire, rotation runbook in relay/README.md.
- Migration (B-s3): store v1->v2 and state.db v1->v2 with `.v1.bak` backups; rollback to v0.3.0 = restore both backups, deploy v0.3.0; relay unaffected.
- Rob's uncommitted `AGENTS.md`, `OWNER-GUIDE.md`, `receiver.py`, untracked `thoughts/shared/*` files are left alone by every slice; implementer must not stage them.

## References
- Design: docs/design/2026-10-28-grok-webhook-multibot.md
- Architecture: docs/architecture/2026-10-28-grok-webhook-multibot.md
- Research: thoughts/shared/research/2026-10-28-grok-webhook-multibot-current-code.md
- ADRs: docs/decisions/0011, 0013..0016 (accepted), 0012 (rejected); 0006..0010 (A), 0001 (MCP path)
- Plan review (mandatory): set in `plan_review:` by eng-run
