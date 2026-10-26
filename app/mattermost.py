"""Placeholder: Mattermost REST client.

Later: talk to http://mattermost:8065/api/v4 over the private Docker network
(same Coolify compose stack). Never via the public URL.

Per-bot tokens: each Grok Bot gets its own Mattermost bot account + token.
Planned mapping (TBD in eng-discover): bridge credential -> Mattermost bot token,
supplied via env/secret, never committed.
"""
import os

MATTERMOST_URL = os.getenv("MATTERMOST_URL", "http://mattermost:8065")


def bot_token_for(bot_id: str) -> str | None:
    """Stub. Will resolve a Grok Bot's Mattermost bot token. Not implemented."""
    return None
