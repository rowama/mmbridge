# mmbridge

Public HTTPS **MCP bridge** between Grok Bots and Rob's self-hosted Mattermost (on Coolify).

**Status:** deployable skeleton. `GET /health` returns `{"ok": true}`; every other path echoes the
request (method, path, headers) as JSON. MCP endpoints and the Mattermost client are stubs
(`app/mcp.py`, `app/mattermost.py`).

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

### Private network (later)
The bridge will call Mattermost at `http://mattermost:8065` over the stack's private Docker
network, never the public URL. Each Grok Bot will get its own Mattermost bot token, supplied as
Coolify secrets (not committed).

## Process
This repo uses the eng-process kit; start at [PROJECT_STATE.md](PROJECT_STATE.md).
