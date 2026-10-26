"""mmbridge: MCP bridge between Grok Bots and self-hosted Mattermost.

/health (public liveness) and /mcp (Bearer auth, MCP Streamable HTTP). Everything else 404.
"""
import contextlib

from fastapi import FastAPI

from app import logging as mlog
from app import mcp as mcp_server
from app.auth import BearerAuth
from app.ratelimit import RateLimiter


def create_app(mm_transport=None, limiter: RateLimiter | None = None) -> FastAPI:
    mlog.setup()
    limiter = limiter or RateLimiter()
    server = mcp_server.build(limiter, mm_transport=mm_transport)
    mcp_app = server.streamable_http_app()

    @contextlib.asynccontextmanager
    async def lifespan(_):
        async with server.session_manager.run():
            yield

    app = FastAPI(title="mmbridge", version="0.2.0", lifespan=lifespan,
                  docs_url=None, redoc_url=None, openapi_url=None)

    @app.get("/health")
    async def health() -> dict:
        return {"ok": True}

    app.router.routes.extend(mcp_app.routes)
    app.add_middleware(BearerAuth, limiter=limiter)
    return app


app = create_app()
