import httpx
import pytest

from app.mattermost import Client, MMError


class Counting(httpx.AsyncBaseTransport):
    def __init__(self, *behaviours):
        self.b = list(behaviours)
        self.n = 0

    async def handle_async_request(self, request):
        self.n += 1
        b = self.b[min(self.n - 1, len(self.b) - 1)]
        if isinstance(b, type) and issubclass(b, Exception):
            raise b("boom", request=request)
        return httpx.Response(b, json={"ok": 1, "message": "raw upstream body"})


async def _err(coro):
    with pytest.raises(MMError) as e:
        await coro
    return e.value


async def test_post_connect_error_never_retried():
    t = Counting(httpx.ConnectError)
    e = await _err(Client("t", transport=t).post("/posts", json={}))
    assert e.code == "mattermost_unavailable" and t.n == 1


async def test_get_connect_error_retried_once_then_fails():
    t = Counting(httpx.ConnectError)
    e = await _err(Client("t", transport=t).get("/users/me"))
    assert e.code == "mattermost_unavailable" and t.n == 2


async def test_get_connect_error_retry_succeeds():
    t = Counting(httpx.ConnectError, 200)
    assert await Client("t", transport=t).get("/users/me") == {"ok": 1, "message": "raw upstream body"}
    assert t.n == 2


@pytest.mark.parametrize("b,code", [(httpx.ReadTimeout, "mattermost_unavailable"), (httpx.ConnectTimeout, "mattermost_unavailable"),
                                    (500, "mattermost_unavailable"), (503, "mattermost_unavailable"),
                                    (401, "unauthorized"), (404, "not_found"), (403, "mattermost_error")])
async def test_get_no_retry_and_mapping(b, code):
    t = Counting(b)
    e = await _err(Client("t", transport=t).get("/x"))
    assert e.code == code and t.n == 1
    assert "raw upstream body" not in str(e)
    if code == "mattermost_error":
        assert e.status == 403


async def test_bearer_header_sent():
    seen = {}

    class T(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            seen["a"] = request.headers["authorization"]
            seen["url"] = str(request.url)
            return httpx.Response(200, json=[])
    await Client("abc", base_url="http://mm:8065", transport=T()).get("/users/me/teams")
    assert seen == {"a": "Bearer abc", "url": "http://mm:8065/api/v4/users/me/teams"}
