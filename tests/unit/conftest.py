import httpx
import pytest

from drivers.fake_mattermost import FakeMattermost


@pytest.fixture
def mm():
    m = FakeMattermost()
    m.add_user("eddie", bot=True)
    m.add_user("ada", bot=True)
    m.add_channel("rmlab", "dev", ["eddie"])
    m.add_channel("rmlab", "ops", ["ada"])
    m.add_channel("rmlab", "secret", ["eddie"], ctype="P")
    m.add_channel("rmlab", "eddie__rob", ["eddie"], ctype="D")
    return m


@pytest.fixture
async def bridge(mm):
    from app.main import create_app
    app = create_app(mm_transport=mm.transport())
    import asyncio
    started, stop = asyncio.Event(), asyncio.Event()

    async def hold():  # lifespan enter/exit in one task (anyio cancel scopes)
        async with app.router.lifespan_context(app):
            started.set()
            await stop.wait()
    task = asyncio.create_task(hold())
    await started.wait()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app, client=("10.0.0.1", 1234)),
                                 base_url="http://testserver") as c:
        yield c
    stop.set()
    await task


def tok(mm, name):
    return mm.user_by_name(name)["token"]


async def call(c, tool="list_channels", args=None, token=None, raw_auth=None):
    h = {"accept": "application/json, text/event-stream", "content-type": "application/json"}
    if token:
        h["authorization"] = "Bearer " + token
    if raw_auth is not None:
        h["authorization"] = raw_auth
    return await c.post("/mcp", headers=h, json={"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                                  "params": {"name": tool, "arguments": args or {}}})


def payload(r):
    import json
    res = r.json()["result"]
    data = res.get("structuredContent")
    if data is None:
        data = json.loads(res["content"][0]["text"])
    if "result" in data and len(data) == 1:
        data = data["result"]
    return res.get("isError", False), data
