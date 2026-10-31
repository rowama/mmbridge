# Wake relay (Grok Bot routines)

Thin HMAC -> Bearer relay (ADR-0011). mmbridge keeps sending only signed wakes; the relay checks each one and
starts that bot's Grok Bot routine with the routine's Bearer key. Routine keys live only here (Coolify secrets on the `relay` compose service),
never in mmbridge.

```
mmbridge --signed wake--> POST /wake/<bot> --verify, dedupe, rate limit--> POST <routine URL>, Bearer <key>
```

## What it does
- `POST /wake/<bot>`: unknown bot -> 404. Bad signature or timestamp older/newer than 5 min -> 401, nothing
  forwarded. A delivery already forwarded (same `X-MMB-Delivery`, last 24 h) -> 200 `{"status": "duplicate"}`,
  nothing forwarded. Over the per-bot rate (30/min, burst 10) -> 429 (mmbridge retries later). Otherwise the body
  goes to the routine unchanged with `Authorization: Bearer <key>`, `Content-Type: application/json` and
  `X-MMB-Delivery`, 5 s timeout.
- Routine answer -> relay answer: 2xx -> 200 (run started); 408/429/5xx/timeout/no connection -> 503 (mmbridge
  retries, 5 attempts, then one failed wake in `python -m app.admin failed`); anything else (401/403/404/...) ->
  424 `{"upstream": <code>}` (permanent; usually a wrong key or URL).
- Known, accepted (Rob 2026-10-28): if the routine started but its answer was lost (timeout), or the relay died
  right after the routine said 200, mmbridge retries and the routine can start twice for one post (log
  `relay_delivery_ambiguous`). It never silently drops a post.
- `GET /health`: `{"ok": true, "bots": n, "forwarded_24h": n, "rejected_24h": n, "double_forward_24h": n}`
  (counts only).
- Logs: one JSON line per event on stdout (`relay_forwarded`, `relay_rejected{reason}`, `relay_upstream{code}`,
  `relay_delivery_ambiguous`, `relay_tripwire{reason}`, `relay_alert_failed`); secrets and keys are redacted,
  message text is never logged.

## Tripwire (B-s2)
The relay logs `relay_tripwire` with a `reason` when something looks wrong, and (optional) posts an alert to a
Mattermost channel, at most one per reason per 10 minutes:

| reason | when | what to do |
|---|---|---|
| `bad_sig` | more than 5 wakes with a bad signature or stale timestamp in 10 min | someone is probing the relay, or a bot's `HMAC_SECRET` differs from its mmbridge wake secret: compare them |
| `rate_limited` | a bot hit its rate limit (30/min, burst 10) | a runaway conversation or a flood; check that channel |
| `upstream_http_401` / `upstream_http_403` | the Grok routine refused the key | the key was rotated or revoked: see "Rotating a routine key" |
| `double_forward` | a post was forwarded again after an earlier forward may already have started the routine (lost answer, or relay crash right after the routine said 200) | the accepted-risk double wake (Rob 2026-10-28). One now and then is expected. **3 or more in 24 h** (`/health` `double_forward_24h`, and only then the alert) means it is time to revisit option C (routine-side idempotency, TODOS) |

Alert (optional, all three or none; the relay refuses to start with only some set):

| Variable | Value |
|---|---|
| `RELAY_ALERT_URL` | Mattermost base URL, in the stack `http://mattermost:8065` |
| `RELAY_ALERT_TOKEN` | token of a dedicated alert bot (not a Grok bot's token), member of the alert channel |
| `RELAY_ALERT_CHANNEL` | the alert channel's id (26 characters) |

The alert says only the reason, the bot name and counts; never a key, secret or message text. If the post fails the
relay logs `relay_alert_failed` and carries on (wakes are never held up by alerts).

## Configuration (env only)
Per bot, `<NAME>` = bot name upper-cased with `-` -> `_` (bot `eddie` -> `RELAY_BOT_EDDIE_*`). Use the same name
everywhere: Mattermost bot, mmbridge wake URL `/wake/<name>`, relay env, Grok routine.

| Variable | Value |
|---|---|
| `RELAY_BOT_<NAME>_HMAC_SECRET` | the bot's mmbridge wake secret (>= 32 chars), copied exactly |
| `RELAY_BOT_<NAME>_ROUTINE_URL` | the Grok Bot routine webhook URL (https) |
| `RELAY_BOT_<NAME>_ROUTINE_KEY` | the routine's Bearer key |
| `RELAY_DATA_DIR` | `/data` (default; mount a volume, holds `relay.db`) |
| `RELAY_RATE_PER_MIN`, `RELAY_BURST` | 30, 10 (defaults) |
| `RELAY_UPSTREAM_TIMEOUT_S` | 5 (default) |

The relay refuses to start if a bot is missing a field, its secret is shorter than 32 characters, or its routine
URL is not https (`RELAY_ALLOW_HTTP_UPSTREAM=true` is for tests only). Replicas: 1.

## Setup: service in the Mattermost compose stack (one bot, e.g. eddie)
The relay is **not** a separate Coolify application (Rob 2026-10-30). It is one more service, `relay`, in the same
Coolify Docker Compose as Mattermost, mmbridge and Postgres (Coolify service `pbrl8nkssi6dnanfxofnftkc`), on the
same private network, so mmbridge reaches it at `http://relay:8080` (plain HTTP is fine on the private Docker
network; no public domain needed). See the `relay:` block in `coolify-service.snippet.yaml`.

1. Rob, in the Coolify UI (Mattermost service -> Docker Compose): add the `relay:` service and the `relay-data`
   volume from `coolify-service.snippet.yaml` (build `https://github.com/rowama/mmbridge.git#main:relay`,
   Dockerfile, `expose: 8080`, no published port, volume `relay-data:/data`, separate from mmbridge's `mmbridge-data:/data`, which must stay to keep bots.enc). No mmbridge env change: mmbridge accepts plain
   `http://` wake URLs only for the in-stack host `relay` (do **not** set `LIVE_ALLOW_HTTP_WAKE`; it is tests-only).
2. Rob, same screen, environment/secrets: `RELAY_BOT_EDDIE_HMAC_SECRET`, `RELAY_BOT_EDDIE_ROUTINE_URL`,
   `RELAY_BOT_EDDIE_ROUTINE_KEY`. The HMAC secret is eddie's existing mmbridge wake secret (if lost, make a new one
   and use it in step 4 too). Redeploy: the whole stack restarts (short Mattermost blip).
3. Check from the mmbridge container terminal:
   `python -c "import urllib.request;print(urllib.request.urlopen('http://relay:8080/health').read())"` ->
   `"ok": true, "bots": 1`.
4. mmbridge container terminal (no redeploy; picked up within 30 s):
   `python -m app.admin set-bot --token-stdin --wake-secret-stdin --wake-url http://relay:8080/wake/eddie`
   and paste two lines: eddie's Mattermost token, then the same wake secret as in step 2, then Ctrl-D.
5. Check: post in Town Square and DM eddie -> the Eddie routine starts each time (Grok Bot routine history).
   From inside the stack, a POST to `http://relay:8080/wake/eddie` with body `{}` -> 401 and no run.

Optional: a public Traefik domain (e.g. `relay.rmlab.cloud`) for ops only; mmbridge never needs it.

## Grok routine setup
The routine receives the wake JSON verbatim as its input (B-s1 spike): `version` 2, `bot`, `channel` (`name`,
`type`: O/P channel, D = DM), `sender.username`, `post` (`id`, `message`, `root_id`) and `reply`, which says how to
answer:

- channel post: `{"tool": "post_channel", "team": "<team>", "channel": "<channel>", "root_id": null}`
- reply in a thread: the same, with `root_id` = the thread's root post id (answer in that thread)
- DM: `{"tool": "dm_send", "username": "<sender>", "root_id": null}`

The routine's bot uses the mmbridge MCP server with **its own** Mattermost bot token (the same bot as the wake URL
name). Its own answer never wakes it again. Routine instruction text (paste into the Grok Bot routine):

> You were woken by a Mattermost post. The input is JSON. Read `post.message` from `sender.username`. Answer it
> with the mmbridge tool named in `reply.tool`, passing exactly the fields of `reply`: for `post_channel` use
> `team` and `channel`, for `dm_send` use `username`; if `reply.root_id` is not null pass it as `root_id` so the
> answer lands in that thread. Do not post anywhere else. If the tool returns `invalid_root`, answer once without
> `root_id`.

(OWNER-GUIDE gets this text once Rob's pending OWNER-GUIDE edits are committed.)

## Rotating a routine key (runbook)
Do this when the key may have leaked, a person with access leaves, or the relay logs `relay_upstream` with code
401/403 (key revoked or rotated on the Grok side).
1. In Grok Bot, create the new key for the routine (or rotate it).
2. Coolify, Mattermost compose stack, `relay` service: set `RELAY_BOT_<NAME>_ROUTINE_KEY` to the new key; redeploy
   (restarts the stack; wakes in between get 503 and mmbridge retries them).
3. In Grok Bot, revoke the old key.
4. Post a test message; the routine starts; relay log shows `relay_forwarded` for it.

Rotating a wake secret: generate one (`python -c "import secrets;print(secrets.token_urlsafe(32))"`), set it in the
relay env and redeploy the relay, then run step 4 of Setup with the new secret. Wakes signed with the old secret in
between get 401 at the relay and show as failed in mmbridge (`python -m app.admin failed --retry <post_id>`).

## Spike (OQ-B1/B2, optional; done 2026-10-30: 200/401/401, marker intact)
`python3 relay/spike_routine.py https://<routine-url>` (paste the key at the prompt, or env `SPIKE_ROUTINE_KEY`).
It posts one marker body as valid key / wrong key / bad URL and prints only the status codes. Write down the
three codes and whether the bot saw the JSON body verbatim (the marker).
