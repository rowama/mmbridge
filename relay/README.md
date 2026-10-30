# Wake relay (Grok Bot routines)

Thin HMAC -> Bearer relay (ADR-0011). mmbridge keeps sending only signed wakes; the relay checks each one and
starts that bot's Grok Bot routine with the routine's Bearer key. Routine keys live only here (Coolify secrets),
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
- `GET /health`: `{"ok": true, "bots": n, "forwarded_24h": n, "rejected_24h": n}` (counts only).
- Logs: one JSON line per event on stdout (`relay_forwarded`, `relay_rejected{reason}`, `relay_upstream{code}`,
  `relay_delivery_ambiguous`); secrets and keys are redacted, message text is never logged.

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

## Setup on Coolify (one bot, e.g. eddie)
1. New application from this repo: build context `relay`, Dockerfile `relay/Dockerfile`, port 8080, a persistent
   volume at `/data`, its own domain (e.g. `https://relay.rmlab.cloud`). See `coolify-service.snippet.yaml`.
2. Secrets: `RELAY_BOT_EDDIE_HMAC_SECRET`, `RELAY_BOT_EDDIE_ROUTINE_URL`, `RELAY_BOT_EDDIE_ROUTINE_KEY`.
   The HMAC secret is eddie's existing mmbridge wake secret. If you don't have it any more, make a new one and
   give it to both sides (step 4 prints nothing then; paste it there too).
3. Deploy; `curl https://relay.rmlab.cloud/health` -> `"ok": true, "bots": 1`.
4. mmbridge container terminal (no redeploy; picked up within 30 s):
   `python -m app.admin set-bot --token-stdin --wake-secret-stdin --wake-url https://relay.rmlab.cloud/wake/eddie`
   and paste two lines at the prompt: eddie's Mattermost token, then the same wake secret as in step 2, then Ctrl-D.
5. Check: post in Town Square and DM eddie -> the Eddie routine starts each time (Grok Bot routine history).
   `curl -X POST https://relay.rmlab.cloud/wake/eddie -d '{}'` -> 401 and no run.

## Grok routine setup
The routine receives the wake JSON as its input: `bot`, `channel` (`name`, `type`: O/P channel, D = DM),
`sender.username`, `post` (`id`, `message`, `root_id`). Until B-s2 adds reply hints, the routine instruction
should say: "You were woken by a Mattermost post. Read `post.message` from `sender.username` in `channel`." (OWNER-GUIDE
gets this text once Rob's pending OWNER-GUIDE edits are committed.)

## Rotating a routine key (runbook)
Do this when the key may have leaked, a person with access leaves, or the relay logs `relay_upstream` with code
401/403 (key revoked or rotated on the Grok side).
1. In Grok Bot, create the new key for the routine (or rotate it).
2. Coolify relay app: set `RELAY_BOT_<NAME>_ROUTINE_KEY` to the new key; redeploy the relay (seconds; wakes in
   between get 503 and mmbridge retries them).
3. In Grok Bot, revoke the old key.
4. Post a test message; the routine starts; relay log shows `relay_forwarded` for it.

Rotating a wake secret: generate one (`python -c "import secrets;print(secrets.token_urlsafe(32))"`), set it in the
relay env and redeploy the relay, then run step 4 of Setup with the new secret. Wakes signed with the old secret in
between get 401 at the relay and show as failed in mmbridge (`python -m app.admin failed --retry <post_id>`).

## Spike (OQ-B1/B2, once, before CP-S)
`python3 relay/spike_routine.py https://<routine-url>` (paste the key at the prompt, or env `SPIKE_ROUTINE_KEY`).
It posts one marker body as valid key / wrong key / bad URL and prints only the status codes. Write down the
three codes and whether the bot saw the JSON body verbatim (the marker).
