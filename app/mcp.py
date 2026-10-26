"""MCP server (ADR-0003): FastMCP, Streamable HTTP, stateless, JSON responses.

Tool arguments are typed Any with an explicit JSON schema: app/validate.py (not pydantic coercion)
decides what is invalid, so every bad input is `invalid_argument` with zero Mattermost calls.
"""
import math
import time
import uuid
from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import CallToolResult
from pydantic import Field, WithJsonSchema

from app import service, validate
from app.auth import current_token, token_hash
from app.errors import ToolError, tool_error, tool_ok
from app.logging import call_line, log
from app.mattermost import MATTERMOST_URL, Client, MMError

_MESSAGES = {
    "unauthorized": "Mattermost rejected this bot's credential.",
    "mattermost_unavailable": "Mattermost is unreachable right now; try again later.",
    "mattermost_error": "Mattermost refused the request.",
    "not_found": "Not found in Mattermost.",
}


def _arg(schema: dict, description: str):
    return Annotated[Any, WithJsonSchema(schema), Field(description=description)]


Username = _arg({"type": "string", "pattern": "^[a-z0-9][a-z0-9._-]{0,63}$"}, "Mattermost username (e.g. rob).")
Team = _arg({"type": "string", "pattern": "^[a-z0-9][a-z0-9._-]{0,63}$"}, "Team name (URL name, e.g. rmlab).")
Channel = _arg({"type": "string", "pattern": "^[a-z0-9][a-z0-9._-]{0,63}$"}, "Channel name (URL name, e.g. town-square).")
Message = _arg({"type": "string", "minLength": 1, "maxLength": validate.MAX_MESSAGE}, "Message text (Markdown).")
Limit = _arg({"type": "integer", "minimum": 1, "maximum": validate.MAX_LIMIT},
             "How many of the newest posts to return.")


def build(limiter, mm_transport=None, base_url: str = MATTERMOST_URL) -> FastMCP:
    server = FastMCP("mmbridge", stateless_http=True, json_response=True, streamable_http_path="/mcp",
                     transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False))
    identities = service.IdentityCache()

    async def run(tool: str, fn, check=lambda: (), write: bool = False, with_me: bool = False) -> CallToolResult:
        """check() validates the arguments (before any MM call) and returns them for fn(client, *args).
        with_me: also pass the caller's cached identity as fn(..., me=...)."""
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
            args = check()
            if write and (ra := limiter.check_write(th)):
                fields["outcome"] = "rate_limited"
                return tool_error("rate_limited", "Too many posts; slow down.", retry_after_s=math.ceil(ra))
            me = await identities.me(client, th)
            fields["bot"] = me["username"]
            result = await (fn(client, *args, me=me) if with_me else fn(client, *args))
            fields["outcome"] = "ok"
            return tool_ok(result)
        except ToolError as e:
            fields["outcome"] = e.code
            return tool_error(e.code, e.message, **e.extra)
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

    @server.tool(description="Post a message to a Mattermost channel this bot is a member of. Never joins channels.")
    async def post_channel(team: Team, channel: Channel, message: Message) -> CallToolResult:
        return await run("post_channel", service.post_channel, write=True, check=lambda: (
            validate.identifier("team", team), validate.identifier("channel", channel), validate.message(message)))

    @server.tool(description="Read the newest posts (newest first) of a Mattermost channel this bot is a member of.")
    async def read_channel(team: Team, channel: Channel, limit: Limit = validate.DEFAULT_LIMIT) -> CallToolResult:
        return await run("read_channel", service.read_channel, check=lambda: (
            validate.identifier("team", team), validate.identifier("channel", channel), validate.limit(limit)))

    @server.tool(description="Send a direct message to a Mattermost user by username (opens or reuses the DM).")
    async def dm_send(username: Username, message: Message) -> CallToolResult:
        return await run("dm_send", service.dm_send, write=True, with_me=True, check=lambda: (
            validate.identifier("username", username), validate.message(message)))

    @server.tool(description="Read the newest posts (newest first) of this bot's DM with a Mattermost user.")
    async def dm_read(username: Username, limit: Limit = validate.DEFAULT_LIMIT) -> CallToolResult:
        return await run("dm_read", service.dm_read, with_me=True, check=lambda: (
            validate.identifier("username", username), validate.limit(limit)))

    return server
