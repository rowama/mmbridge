"""Which Mattermost websocket events wake the live bot (architecture Filter rules, REQ-A1/A2/A3).

Pure apart from the `event_invalid` log line: no I/O, no state. Drop own posts (A3), system posts (type set),
group DMs (G) and open/private channels not chosen (A1); wake on DMs (D, A2) and chosen channels. Thread
replies are new posts and wake, carrying root_id. Malformed `posted` events drop and log `event_invalid`
(reason only; never the message text).
"""
import json
from dataclasses import dataclass

from app import logging as mlog


@dataclass(frozen=True)
class WakeIntent:
    post_id: str
    channel_id: str
    channel_type: str        # O | P | D
    user_id: str
    message: str
    create_at: int           # Mattermost ms
    root_id: str | None
    hints: dict              # event fields (channel_name, channel_display_name, sender_name, team_id) for fallbacks


def _invalid(reason: str) -> None:
    mlog.log.warning(json.dumps({"event": "event_invalid", "reason": reason}))


def _post(data: dict) -> dict | None:
    post = data.get("post")
    if isinstance(post, str):
        try:
            post = json.loads(post)
        except ValueError:
            return None
    return post if isinstance(post, dict) else None


def decide(event: dict, bot_user_id: str, chosen: set[str]) -> WakeIntent | None:
    if not isinstance(event, dict):
        _invalid("not_object")
        return None
    if event.get("event") != "posted":
        return None
    data = event.get("data")
    if not isinstance(data, dict):
        _invalid("data")
        return None
    post = _post(data)
    if post is None:
        _invalid("post")
        return None
    for f in ("id", "channel_id", "user_id"):
        if not isinstance(post.get(f), str) or not post[f]:
            _invalid(f)
            return None
    create_at, message, ctype = post.get("create_at"), post.get("message", ""), data.get("channel_type")
    if not isinstance(create_at, int) or isinstance(create_at, bool):
        _invalid("create_at")
        return None
    if not isinstance(message, str):
        _invalid("message")
        return None
    if ctype not in ("O", "P", "D", "G"):
        _invalid("channel_type")
        return None

    if post["user_id"] == bot_user_id or post.get("type") or ctype == "G":
        return None
    if ctype in ("O", "P") and post["channel_id"] not in chosen:
        return None
    hints = {k: data.get(k) for k in ("channel_name", "channel_display_name", "sender_name", "team_id")}
    return WakeIntent(post["id"], post["channel_id"], ctype, post["user_id"], message, create_at,
                      post.get("root_id") or None, hints)
