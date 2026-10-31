"""Shared input validators for the channel and DM tools. Run before any Mattermost call.

Every failure raises ToolError("invalid_argument"). Identifiers are additionally URL-encoded
(segment()) wherever they go into a request path.
"""
import re
from urllib.parse import quote

from app.errors import ToolError

_IDENT = re.compile(r"[a-z0-9][a-z0-9._-]{0,63}")
_POST_ID = re.compile(r"[a-z0-9]{26}")   # Mattermost id: 26 chars a-z0-9
MAX_MESSAGE = 16383
DEFAULT_LIMIT, MAX_LIMIT = 20, 100


def _bad(msg: str) -> ToolError:
    return ToolError("invalid_argument", msg)


def identifier(kind: str, value) -> str:
    if not isinstance(value, str) or not _IDENT.fullmatch(value) or ".." in value:
        raise _bad("%s must be 1-64 chars of a-z, 0-9, '.', '_' or '-', starting with a letter or digit." % kind)
    return value


def message(value) -> str:
    s = value.strip() if isinstance(value, str) else ""
    if not 1 <= len(s) <= MAX_MESSAGE:
        raise _bad("message must be 1-%d characters (not blank)." % MAX_MESSAGE)
    return s


def limit(value) -> int:
    if value is None:
        return DEFAULT_LIMIT
    if type(value) is not int or not 1 <= value <= MAX_LIMIT:
        raise _bad("limit must be an integer from 1 to %d." % MAX_LIMIT)
    return value


def post_id(value) -> str | None:
    """Optional Mattermost post id (root_id, ADR-0015): None, or exactly 26 chars a-z0-9."""
    if value is None:
        return None
    if not isinstance(value, str) or not _POST_ID.fullmatch(value):
        raise _bad("root_id must be a Mattermost post id (26 characters a-z, 0-9).")
    return value


def segment(value: str) -> str:
    return quote(value, safe="")
