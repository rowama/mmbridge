---
id: RESEA-20261025-mmbridge-current-code
type: research
phase: research
status: draft            # input (pre-draft from an earlier phase) | draft | in-review | approved | discarded
owner_agent: Eddie
date: 2026-10-25
links: [docs/design/2026-10-25-mmbridge-mcp.md]
git_commit: 1fd13b4
branch: main
---
# Research: mmbridge current code
<!-- Codebase research: what the code IS, file:line, no recommendations. -->

## Research question
For REQ-1..8 of `docs/design/2026-10-25-mmbridge-mcp.md`: what does the code in `app/`, `Dockerfile`, `requirements.txt`, `.dockerignore` and `coolify-service.snippet.yaml` do today regarding (a) HTTP surface, (b) MCP, (c) Mattermost access and per-bot credentials, (d) error handling, (e) build and deployment/networking?

## Summary
The repo is a deployable FastAPI skeleton. It serves `GET /health` and a catch-all echo route that returns request metadata including all headers. `app/mcp.py` contains only a docstring; `app/mattermost.py` defines a `MATTERMOST_URL` setting and a stub `bot_token_for()` that returns `None`. No MCP protocol, no Mattermost calls, no authentication and no error handling exist. The container runs uvicorn on port 8080 as a non-root user; the Coolify snippet builds from the GitHub repo and places the service in the Mattermost compose stack with domain chats.rmlab.cloud.

## Detailed findings
### HTTP app (`app/main.py`)
- FastAPI app titled "mmbridge", version 0.1.0 (`app/main.py:9`).
- `GET /health` returns `{"ok": true}` (`app/main.py:12-14`).
- Catch-all route `/{path:path}` for GET/POST/PUT/PATCH/DELETE/OPTIONS/HEAD returns service name, a placeholder note, method, path, query, all request headers, and client host (`app/main.py:17-27`). Because it is registered after `/health`, `/health` is matched first (`app/main.py:12,17`).
- Headers are echoed verbatim, including any `Authorization` header a caller sends (`app/main.py:25`).
- `mattermost` and `mcp` modules are imported but unused (`app/main.py:7`).

### MCP (`app/mcp.py`)
- Docstring only; mentions planned streamable HTTP at `/mcp` and tools list/read/post; nothing implemented (`app/mcp.py:1-5`).
- No MCP library in dependencies (`requirements.txt:1-2`). Any request to `/mcp` today hits the echo route (`app/main.py:17`).

### Mattermost client and credentials (`app/mattermost.py`)
- `MATTERMOST_URL` from env, default `http://mattermost:8065` (`app/mattermost.py:12`).
- Docstring states intent: use `/api/v4` over the private Docker network, one Mattermost bot token per Grok Bot, mapping supplied via env/secret (`app/mattermost.py:1-9`).
- `bot_token_for(bot_id)` always returns `None` (`app/mattermost.py:15-17`).
- No HTTP client library is in dependencies (`requirements.txt:1-2`); no code calls Mattermost.

### Authentication / errors (REQ-1, REQ-7, REQ-8)
- No auth check on any route (`app/main.py:12-27`). No exception handlers or error types defined anywhere in `app/`.

### Build (`Dockerfile`, `requirements.txt`, `.dockerignore`)
- Base `python:3.12-slim`, workdir `/app` (`Dockerfile:1-4`); installs pinned `fastapi==0.115.6`, `uvicorn[standard]==0.34.0` (`Dockerfile:6-7`, `requirements.txt:1-2`).
- Copies only `app/` (`Dockerfile:9`); `.dockerignore` excludes docs, thoughts, `.eng`, `.claude`, `*.md`, `.env` (`.dockerignore:1-12`).
- Runs as `appuser` uid 10001 (`Dockerfile:11-12`); exposes 8080 (`Dockerfile:14`).
- HEALTHCHECK every 30s via urllib to `/health` (`Dockerfile:15`).
- CMD uvicorn `app.main:app` on 0.0.0.0:8080 with `--proxy-headers --forwarded-allow-ips *` (`Dockerfile:16`).

### Deployment (`coolify-service.snippet.yaml`)
- Service `mmbridge` built from `https://github.com/rowama/mmbridge.git#main` with the repo Dockerfile; registry image commented as alternative (`coolify-service.snippet.yaml:3-9`).
- Intended to replace an existing `echo` service in the Mattermost compose stack (`coolify-service.snippet.yaml:1`).
- `SERVICE_FQDN_MMBRIDGE_8080=https://chats.rmlab.cloud` maps the domain to port 8080 (`coolify-service.snippet.yaml:12`); `MATTERMOST_URL=http://mattermost:8065` (`:13`); comment that per-bot tokens are to be Coolify secrets (`:14`).
- `expose: 8080` (no host port published) (`:15-16`); compose healthcheck mirrors Dockerfile's, retries 3 (`:17-21`).
- Comment: same stack ⇒ same default network, so `mattermost` hostname resolves privately (`:22-23`).

## Code references
- `app/main.py:12-14` — health endpoint
- `app/main.py:17-27` — catch-all echo (echoes headers)
- `app/mattermost.py:12` — MATTERMOST_URL
- `app/mattermost.py:15-17` — token lookup stub
- `app/mcp.py:1-5` — MCP placeholder
- `Dockerfile:16` — uvicorn entrypoint, port 8080
- `coolify-service.snippet.yaml:12-13` — domain and Mattermost URL env

## Architecture as-is
Single FastAPI process, single module tree `app/`. Request flow: Coolify proxy (TLS, chats.rmlab.cloud) → container :8080 → uvicorn → FastAPI → `/health` or echo. Configuration is env-only (`MATTERMOST_URL`). No state, storage, outbound calls, or tests in the repo.

## Open questions
- Mattermost server version and whether bot accounts/tokens already exist: not determinable from the repo.
- Whether the current Coolify deployment matches this snippet (e.g. existing `echo` service name): not determinable from the repo.
