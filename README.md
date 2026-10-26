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
