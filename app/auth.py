"""Bearer auth for /mcp (ADR-0001). The caller's Mattermost token is never stored or logged.

ASGI middleware: missing/malformed Bearer -> 401 {"error":"unauthorized"} (anon rate limit, 429)
before any Mattermost call. Valid-looking token goes into a ContextVar, reset in finally.
"""
import hashlib
import json
import math
import re
from contextvars import ContextVar

current_token: ContextVar[str] = ContextVar("mm_token")
_BEARER = re.compile(r"^Bearer ([A-Za-z0-9._~+/=-]{8,512})$")


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def extract(header: str | None) -> str | None:
    m = _BEARER.match(header or "")
    return m.group(1) if m else None


class BearerAuth:
    def __init__(self, app, limiter, path: str = "/mcp"):
        self.app, self.limiter, self.path = app, limiter, path

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["path"].rstrip("/") != self.path:
            return await self.app(scope, receive, send)
        headers = {k.decode().lower(): v.decode() for k, v in scope["headers"]}
        token = extract(headers.get("authorization"))
        if token is None:
            ip = (scope.get("client") or ("unknown", 0))[0]
            ra = self.limiter.check_anon(ip)
            if ra:
                return await _json(send, 429, {"error": "rate_limited", "retry_after_s": math.ceil(ra)})
            return await _json(send, 401, {"error": "unauthorized"})
        reset = current_token.set(token)
        try:
            await self.app(scope, receive, send)
        finally:
            current_token.reset(reset)


async def _json(send, status, body):
    data = json.dumps(body).encode()
    await send({"type": "http.response.start", "status": status,
                "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(data)).encode())]})
    await send({"type": "http.response.body", "body": data})
