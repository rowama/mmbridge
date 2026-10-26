"""mmbridge: future MCP bridge between Grok Bots and self-hosted Mattermost.

Today this is a deployable skeleton: /health plus a catch-all echo.
"""
from fastapi import FastAPI, Request

from app import mattermost, mcp  # noqa: F401  (placeholders for upcoming work)

app = FastAPI(title="mmbridge", version="0.1.0")


@app.get("/health")
async def health() -> dict:
    return {"ok": True}


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
async def echo(request: Request, path: str = "") -> dict:
    return {
        "service": "mmbridge",
        "note": "Echo placeholder. This service will become the Grok Bot <-> Mattermost MCP bridge.",
        "method": request.method,
        "path": request.url.path,
        "query": str(request.url.query),
        "headers": dict(request.headers),
        "client": request.client.host if request.client else None,
    }
