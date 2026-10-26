"""MCP protocol driver (layer 3): drives app.main:app over Streamable HTTP (/mcp) in-process,
with Mattermost replaced by a recording fake (/api/v4). Freely editable; implemented in slice 1
(list_channels, auth) and extended in slices 2-3. Stub until then: every call raises, so specs fail red."""


class McpDriver:
    def __getattr__(self, name):
        raise NotImplementedError("McpDriver.%s: implement in the slice that needs it" % name)

    def close(self):
        pass
