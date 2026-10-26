import asyncio
import logging

from conftest import call, payload, tok
from app import auth


async def test_health_unchanged(bridge):
    r = await bridge.get("/health")
    assert r.status_code == 200 and r.json() == {"ok": True}


async def test_echo_gone(bridge):
    r = await bridge.get("/anything", headers={"authorization": "Bearer secret-xyz"})
    assert r.status_code == 404
    assert "secret-xyz" not in r.text and "authorization" not in r.text.lower()


async def test_missing_and_malformed_bearer_401_no_mm_call(bridge, mm):
    for raw in (None, "Basic abc", "Bearer ", "Bearer a b", "bearer"):
        r = await call(bridge, raw_auth=raw)
        assert r.status_code == 401, raw
        assert r.json() == {"error": "unauthorized"}
    assert mm.calls == []


async def test_invalid_token_unauthorized_not_leaked(bridge, mm, caplog):
    caplog.set_level(logging.INFO, logger="mmbridge")
    bad = "zzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    r = await call(bridge, token=bad)
    is_err, data = payload(r)
    assert is_err and data["code"] == "unauthorized" and data["message"]
    assert bad not in r.text and bad not in caplog.text


async def test_list_channels_only_member_open_private(bridge, mm):
    is_err, data = payload(await call(bridge, token=tok(mm, "eddie")))
    assert not is_err
    assert sorted((c["team"], c["name"], c["type"]) for c in data["channels"]) == [
        ("rmlab", "dev", "O"), ("rmlab", "secret", "P")]
    assert set(data["channels"][0]) == {"team", "name", "display_name", "type"}


async def test_caller_isolation_alternating_and_concurrent(bridge, mm):
    te, ta = tok(mm, "eddie"), tok(mm, "ada")
    for t, want in ((te, {"dev", "secret"}), (ta, {"ops"}), (te, {"dev", "secret"})):
        _, d = payload(await call(bridge, token=t))
        assert {c["name"] for c in d["channels"]} == want
    mm.calls.clear()
    rs = await asyncio.gather(*[call(bridge, token=t) for t in [te, ta] * 5])
    for i, r in enumerate(rs):
        _, d = payload(r)
        assert {c["name"] for c in d["channels"]} == ({"dev", "secret"} if i % 2 == 0 else {"ops"})
    # every outbound call carries one of the callers' own tokens, and per-caller counts match
    assert {t for _, _, t in mm.calls} <= {te, ta}
    assert auth.current_token.get(None) is None


async def test_identity_cache_keyed_by_token(bridge, mm):
    te, ta = tok(mm, "eddie"), tok(mm, "ada")
    await call(bridge, token=te)
    await call(bridge, token=te)
    me_calls = [c for c in mm.calls if c[1] == "/api/v4/users/me"]
    assert len(me_calls) == 1  # cached for eddie
    _, d = payload(await call(bridge, token=ta))
    assert {c["name"] for c in d["channels"]} == {"ops"}
    assert [c[2] for c in mm.calls if c[1] == "/api/v4/users/me"] == [te, ta]


async def test_contextvar_reset_on_error(bridge, mm):
    mm.down = True
    await call(bridge, token=tok(mm, "eddie"))
    assert auth.current_token.get(None) is None


async def test_mm_down_maps_unavailable(bridge, mm, caplog):
    caplog.set_level(logging.INFO, logger="mmbridge")
    mm.down = True
    t = tok(mm, "eddie")
    r = await call(bridge, token=t)
    is_err, d = payload(r)
    assert is_err and d["code"] == "mattermost_unavailable"
    assert t not in r.text and t not in caplog.text


async def test_log_line_per_call_with_hash_prefix(bridge, mm, caplog):
    import json, hashlib
    caplog.set_level(logging.INFO, logger="mmbridge")
    t = tok(mm, "eddie")
    await call(bridge, token=t)
    lines = [json.loads(r.getMessage()) for r in caplog.records if r.name == "mmbridge.calls"]
    assert len(lines) == 1
    l = lines[0]
    assert l["tool"] == "list_channels" and l["outcome"] == "ok" and l["bot"] == "eddie"
    assert l["token_hash"] == hashlib.sha256(t.encode()).hexdigest()[:8]
    assert "latency_ms" in l and "request_id" in l
