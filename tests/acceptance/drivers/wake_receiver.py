"""HMAC-verifying wake receiver (test harness only; ADR-0008 receiver side).

POST /wake: records every request (headers, raw body, status), verifies the signature with app.wake.verify
(401 when invalid), drops repeats of X-MMB-Delivery (idempotency key) and answers 204. Controls: `down`
(503 to everything), `hang` (asyncio.Event the handler waits on, to cancel a dispatcher mid-POST).
`transport()` routes an httpx.AsyncClient to it in-process.
"""
import json
import time

import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from app.wake import verify


class WakeReceiver:
    def __init__(self, secret: str | None = None, clock=time.time):
        self.secret, self.clock = secret, clock
        self.requests = []        # {"headers", "body", "status"} for every request received
        self.accepted = {}        # delivery id -> payload of the first valid request
        self.down = False
        self.hang = None
        self.app = Starlette(routes=[Route("/wake", self._wake, methods=["POST"])])

    async def _wake(self, request: Request):
        body = await request.body()
        rec = {"headers": dict(request.headers), "body": body, "status": None}
        self.requests.append(rec)
        if self.hang is not None:
            await self.hang.wait()
        if self.down:
            rec["status"] = 503
        elif not (self.secret and verify(self.secret, request.headers, body, int(self.clock()))):
            rec["status"] = 401
        else:
            rec["status"] = 204
            self.accepted.setdefault(request.headers["x-mmb-delivery"], json.loads(body))
        return Response(status_code=rec["status"])

    def attempts(self, delivery_id: str) -> list[dict]:
        return [r for r in self.requests if r["headers"].get("x-mmb-delivery") == delivery_id]

    def transport(self) -> httpx.AsyncBaseTransport:
        return httpx.ASGITransport(app=self.app)
