"""Tool error results (architecture: error codes). Messages never contain tokens or raw MM bodies."""
import json

from mcp.types import CallToolResult, TextContent


class ToolError(Exception):
    def __init__(self, code: str, message: str, **extra):
        super().__init__(code)
        self.code, self.message, self.extra = code, message, extra


def tool_error(code: str, message: str, **extra) -> CallToolResult:
    body = {"code": code, "message": message, **extra}
    return CallToolResult(isError=True, content=[TextContent(type="text", text=json.dumps(body))],
                          structuredContent=body)


def tool_ok(data: dict) -> CallToolResult:
    return CallToolResult(content=[TextContent(type="text", text=json.dumps(data))], structuredContent=data)
