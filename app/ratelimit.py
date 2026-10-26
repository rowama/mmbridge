"""In-memory token buckets (ADR-0004): calls and writes per token hash, anonymous per IP.

Capacity equals the per-minute limit (plan: the 61st call in a minute is limited).
"""
import os
import time


class Bucket:
    def __init__(self, per_min: int, clock=time.monotonic):
        self.cap = float(per_min)
        self.rate = per_min / 60.0
        self.tokens = self.cap
        self.clock = clock
        self.t = clock()

    def take(self) -> float:
        """0 if allowed, else seconds until a token is available."""
        now = self.clock()
        self.tokens = min(self.cap, self.tokens + (now - self.t) * self.rate)
        self.t = now
        if self.tokens >= 1:
            self.tokens -= 1
            return 0
        return max(0.001, (1 - self.tokens) / self.rate)


class RateLimiter:
    def __init__(self, calls_per_min: int | None = None, anon_per_min: int | None = None,
                 writes_per_min: int | None = None, clock=time.monotonic):
        self.calls_per_min = calls_per_min or int(os.getenv("RL_CALLS_PER_MIN", "60"))
        self.writes_per_min = writes_per_min or int(os.getenv("RL_WRITES_PER_MIN", "20"))
        self.anon_per_min = anon_per_min or int(os.getenv("RL_ANON_PER_MIN", "30"))
        self.clock = clock
        self._calls: dict[str, Bucket] = {}
        self._writes: dict[str, Bucket] = {}
        self._anon: dict[str, Bucket] = {}

    def _take(self, d, key, per_min) -> float:
        b = d.get(key)
        if b is None:
            if len(d) > 10000:
                d.clear()
            b = d[key] = Bucket(per_min, self.clock)
        return b.take()

    def check_call(self, token_hash: str) -> float:
        return self._take(self._calls, token_hash, self.calls_per_min)

    def check_write(self, token_hash: str) -> float:
        return self._take(self._writes, token_hash, self.writes_per_min)

    def check_anon(self, ip: str) -> float:
        return self._take(self._anon, ip, self.anon_per_min)
