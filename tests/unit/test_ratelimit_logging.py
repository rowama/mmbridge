import logging

from conftest import call, payload, tok
from app.ratelimit import Bucket, RateLimiter
from app.logging import RedactFilter


def test_bucket_61st_call_limited():
    now = [0.0]
    b = Bucket(60, clock=lambda: now[0])
    assert all(b.take() == 0 for _ in range(60))
    ra = b.take()
    assert ra > 0
    now[0] += ra
    assert b.take() == 0


def test_buckets_independent_per_key():
    rl = RateLimiter(calls_per_min=2, anon_per_min=1, clock=lambda: 0.0)
    assert rl.check_call("a") == 0 and rl.check_call("a") == 0 and rl.check_call("a") > 0
    assert rl.check_call("b") == 0


async def test_call_rate_limit_no_mm_call(bridge, mm, monkeypatch):
    from app import main
    t = tok(mm, "eddie")
    for _ in range(60):
        r = await call(bridge, token=t)
        assert not payload(r)[0]
    n = len(mm.calls)
    is_err, d = payload(await call(bridge, token=t))
    assert is_err and d["code"] == "rate_limited" and d["retry_after_s"] > 0
    assert len(mm.calls) == n
    assert not payload(await call(bridge, token=tok(mm, "ada")))[0]


async def test_anon_rate_limit_429(bridge, mm):
    for _ in range(30):
        assert (await call(bridge)).status_code == 401
    r = await call(bridge)
    assert r.status_code == 429 and r.json()["error"] == "rate_limited" and r.json()["retry_after_s"] > 0
    assert mm.calls == []


def test_redaction_filter():
    rec = logging.LogRecord("mmbridge", logging.INFO, "", 0, "auth Bearer abcdefghijklmnop123 and %s", ("Bearer zzzzyyyyxxxx1111",), None)
    RedactFilter().filter(rec)
    msg = rec.getMessage()
    assert "abcdefghijklmnop123" not in msg and "zzzzyyyyxxxx1111" not in msg and "[REDACTED]" in msg
