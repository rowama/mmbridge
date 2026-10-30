# mmbridge

Public HTTPS **MCP bridge** between Grok Bots and Rob's self-hosted Mattermost (on Coolify).

**Status:** v0.2.0. `GET /health` returns `{"ok": true}` (public). `POST /mcp` is an MCP
Streamable HTTP endpoint (stateless, JSON responses); every other path returns 404.

## MCP tools
Connect with `Authorization: Bearer <this bot's Mattermost bot token>`; the bridge acts as that bot.

| Tool | Arguments | What it does |
|---|---|---|
| `list_channels` | none | Public and private channels the bot is a member of, across its teams |
| `post_channel` | `team`, `channel`, `message` | Post to a channel the bot belongs to (never auto-joins; non-member -> `not_member`) |
| `read_channel` | `team`, `channel`, `limit` (optional) | Newest posts first from a member channel |
| `dm_send` | `username`, `message` | DM a user by username (opens or reuses the DM; unknown -> `unknown_user`) |
| `dm_read` | `username`, `limit` (optional) | Newest posts first of the bot's DM with that user |

Writes (`post_channel`, `dm_send`) are limited to 20 per minute per bot token (in memory);
all tool calls are limited to 60 per minute per token;
over a limit returns `rate_limited` with `retry_after_s`. Bad arguments return
`invalid_argument` before any Mattermost call.

## Run locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
curl localhost:8080/health
```
Or: `docker build -t mmbridge . && docker run -p 8080:8080 mmbridge`

## Deploying on Coolify
- **Coolify builds from this Git repo's `Dockerfile`.** GitHub is the source, not a container registry;
  no image is published anywhere. Coolify clones, builds, and runs the image on the server.
- The container listens on plain HTTP **port 8080**; Coolify's proxy terminates TLS for
  **https://chats.rmlab.cloud**.

### Replacing the echo service in the Mattermost compose stack
1. In the Mattermost stack's compose, remove the `echo` service.
2. Paste the `mmbridge` service from [`coolify-service.snippet.yaml`](coolify-service.snippet.yaml)
   (build context = this repo, Dockerfile build).
3. Move the domain `chats.rmlab.cloud` onto `mmbridge`, port 8080.
4. Redeploy and check `https://chats.rmlab.cloud/health`.

(Alternative: deploy as a standalone Coolify "Public/Private Repository" resource with build pack
"Dockerfile", port 8080. But it must share a network with Mattermost for the later step below.)

### Private network
The bridge calls Mattermost at `MATTERMOST_URL` (default `http://mattermost:8065`) over the stack's
private Docker network, never the public URL. The bridge stores no tokens: each Grok Bot sends its
own Mattermost bot token per call.

## Process
This repo uses the eng-process kit; start at [PROJECT_STATE.md](PROJECT_STATE.md).

## Live bots (deploy)
Off by default: with `LIVE_BOTS_ENABLED` unset the bridge is the MCP bridge only and `/health` says
`"listener": "disabled"`. To turn it on (Coolify):
1. Persistent volume mounted at `/data` (writable by uid 10001; the image's `/data` already is). Replicas stay 1.
2. Env secret `MMB_STORE_KEY`: generate one with
   `python -c "from cryptography.fernet import Fernet;print(Fernet.generate_key().decode())"`.
3. Container terminal: `python -m app.admin set-bot --token-stdin --wake-url https://<receiver>/wake`, paste the
   bot token at the prompt. Copy the printed wake secret into your receiver (shown once). No channel list: add the
   bot to channels in Mattermost; it wakes on every post by someone else in those channels and on DMs.
4. Env `LIVE_BOTS_ENABLED=true`, redeploy. `curl https://chats.rmlab.cloud/health` shows
   `{"ok": true, "listener": "ok", "wake_failed_24h": 0}`.

`listener` is `disabled` (flag off), `off` (store key wrong/missing, no bot stored, or `/data` not writable; see the
`store_unreadable` / `state_unwritable` log line; fix it, then restart: e.g. the flag was on before the first
`set-bot`), `connecting`, `ok`, or `degraded` (bot token refused by
Mattermost, retried every 5 min, or a crashed task restarting). Drops reconnect on their own (1-60 s backoff);
posts made while disconnected are caught up from the REST API (window `LIVE_CATCHUP_MINUTES`, default 15) and
still wake exactly once. Edits made with `admin set-bot` while running are picked up within 30 s (a new token
reconnects); a store that no longer decrypts keeps the previous config and logs `store_reload_failed`.
`python -m app.admin failed` lists wakes the receiver never accepted; `--retry <post_id>` sends one again.

## Grok Bot routines (wake relay)
Grok Bot routines take a Bearer key, not a signed wake, so a small relay sits beside mmbridge: it checks each
signed wake (signature, 5-minute window, no repeats, per-bot rate limit) and starts the bot's routine with its key.
Point the bot at it with `python -m app.admin set-bot --token-stdin --wake-secret-stdin --wake-url
https://<relay>/wake/<bot>` (no redeploy). Setup, env and key rotation: [relay/README.md](relay/README.md).

## Wake receiver (live bots)

With live bots on, mmbridge POSTs each wake to the bot's `wake_url` with headers `X-MMB-Delivery`, `X-MMB-Timestamp` and `X-MMB-Signature: v1=<hex HMAC-SHA256(secret, ts + "." + body)>`. A receiver must check the signature before acting:

```python
# pip install fastapi uvicorn ; WAKE_SECRET=<secret printed by admin set-bot> uvicorn receiver:app --port 9000
import os, time
from fastapi import FastAPI, Request, Response
from app.wake import verify          # or copy verify() from app/wake.py

app, seen = FastAPI(), set()

@app.post("/wake")
async def wake(request: Request):
    body = await request.body()
    if not verify(os.environ["WAKE_SECRET"], request.headers, body, int(time.time())):
        return Response(status_code=401)   # bad signature, stale timestamp, or X-MMB-Delivery != signed delivery_id
    if request.headers["x-mmb-delivery"] in seen:
        return Response(status_code=204)   # repeat delivery: already handled
    seen.add(request.headers["x-mmb-delivery"])
    print(body.decode())                   # hand the wake to your bot here
    return Response(status_code=204)
```

Tamper test: copy a logged request, change one byte of the body, the timestamp or `X-MMB-Delivery`, and resend it; the receiver answers 401.
