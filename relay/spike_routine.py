"""OQ-B1/B2 spike (plan Phase 1): POST one marker JSON body to a real Grok Bot routine and print status codes.

Not in the relay image. The routine key is read from env SPIKE_ROUTINE_KEY or, if unset, from stdin (never
argv, never printed). Cases: valid key, wrong key, bad URL (routine URL with a junk suffix). Prints the case,
the HTTP status (or the error class) and the marker; never the key or response bodies.

    python3 relay/spike_routine.py https://<routine-url>          # paste the key at the prompt
Then check in Grok Bot: did the "valid key" run start, and does the bot see the JSON body verbatim (marker)?
"""
import getpass
import json
import os
import secrets
import sys

import httpx


def post(url: str, key: str, body: bytes) -> str:
    try:
        r = httpx.post(url, content=body, timeout=15, headers={
            "Authorization": "Bearer " + key, "Content-Type": "application/json", "X-MMB-Delivery": "spike"})
        return str(r.status_code)
    except httpx.HTTPError as e:
        return "error " + type(e).__name__


def main(argv) -> int:
    if len(argv) != 2 or not argv[1].startswith("https://"):
        print("usage: python3 relay/spike_routine.py https://<routine-url>  (key via SPIKE_ROUTINE_KEY or prompt)")
        return 2
    url = argv[1]
    key = os.environ.get("SPIKE_ROUTINE_KEY") or getpass.getpass("routine key (not echoed): ").strip()
    marker = "mmb-spike-" + secrets.token_hex(4)
    body = json.dumps({"version": 1, "kind": "post", "delivery_id": marker, "marker": marker,
                       "post": {"id": marker, "message": "spike %s: please echo this marker" % marker}},
                      separators=(",", ":")).encode()
    print("marker:", marker)
    for case, u, k in (("valid key", url, key), ("wrong key", url, "wrong-" + secrets.token_hex(8)),
                       ("bad URL", url.rstrip("/") + "-does-not-exist-" + secrets.token_hex(3), key)):
        print("%-10s -> %s" % (case, post(u, k, body)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
