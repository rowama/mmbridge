"""MCP server (ADR-0003): FastMCP, Streamable HTTP, stateless, JSON responses. Slice 1: list_channels."""
import math
import time
import uuid

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import CallToolResult

from app import service
from app.auth import current_token, token_hash
from app.errors import tool_error, tool_ok
from app.logging import call_line, log
from app.mattermost import MATTERMOST_URL, Client, MMError

_MESSAGES = {
    "unauthorized": "Mattermost rejected this bot's credential.",
    "mattermost_unavailable": "Mattermost is unreachable right now; try again later.",
    "mattermost_error": "Mattermost refused the request.",
    "not_found": "Not found in Mattermost.",
}


def build(limiter, mm_transport=None, base_url: str = MATTERMOST_URL) -> FastMCP:
    server = FastMCP("mmbridge", stateless_http=True, json_response=True, streamable_http_path="/mcp",
                     transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False))
    identities = service.IdentityCache()

    async def run(tool: str, fn) -> CallToolResult:
        token = current_token.get()
        th = token_hash(token)
        fields = {"request_id": uuid.uuid4().hex[:12], "tool": tool, "token_hash": th[:8], "bot": None,
                  "mm_status": None}
        t0 = time.monotonic()
        client = Client(token, base_url=base_url, transport=mm_transport)
        try:
            ra = limiter.check_call(th)
            if ra:
                fields["outcome"] = "rate_limited"
                return tool_error("rate_limited", "Too many calls; slow down.", retry_after_s=math.ceil(ra))
            me = await identities.me(client, th)
            fields["bot"] = me["username"]
            result = await fn(client)
            fields["outcome"] = "ok"
            return tool_ok(result)
        except MMError as e:
            fields["outcome"] = e.code
            extra = {"status": e.status} if e.code == "mattermost_error" else {}
            return tool_error(e.code, _MESSAGES.get(e.code, "Mattermost error."), **extra)
        except Exception:
            fields["outcome"] = "internal_error"
            log.exception("internal error request_id=%s", fields["request_id"])
            return tool_error("internal_error", "Internal bridge error (request %s)." % fields["request_id"])
        finally:
            fields["mm_status"] = client.last_status
            fields["latency_ms"] = round((time.monotonic() - t0) * 1000)
            call_line(**fields)

    @server.tool(description="List the Mattermost channels (public and private) this bot is a member of, across its teams.")
    async def list_channels() -> CallToolResult:
        return await run("list_channels", service.list_channels)

    return server
