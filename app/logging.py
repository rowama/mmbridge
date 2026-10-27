"""Structured JSON call logs (ADR-0005) with a redaction filter. Never log headers, tokens or bodies.

The filter also redacts registered literals (stored bot token and wake secret, ADR-0006)."""
import json
import logging
import re
import sys

_PATTERNS = [re.compile(r"(?i)bearer\s+\S+"), re.compile(r"(?i)(authorization['\"]?\s*[:=]\s*['\"]?)[^'\",}\s]+")]
_SECRETS: set[str] = set()   # stored bot token / wake secret (ADR-0006), redacted as literals


def register_secret(value: str) -> None:
    if isinstance(value, str) and len(value) >= 8:
        _SECRETS.add(value)


def _literals(s: str) -> str:
    for v in sorted(_SECRETS, key=len, reverse=True):
        s = s.replace(v, "[REDACTED]")
    return s


class RedactFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        for p in _PATTERNS:
            msg = p.sub(lambda m: (m.group(1) if m.groups() else "Bearer ") + "[REDACTED]", msg)
        record.msg, record.args = _literals(msg), None
        if record.exc_info:
            record.exc_text = _redact(logging.Formatter().formatException(record.exc_info))
            record.exc_info = None
        return True


def _redact(s: str) -> str:
    for p in _PATTERNS:
        s = p.sub("[REDACTED]", s)
    return _literals(s)


log = logging.getLogger("mmbridge")
calls = logging.getLogger("mmbridge.calls")


def setup() -> None:
    if getattr(log, "_mmb_setup", False):
        return
    log.setLevel(logging.INFO)
    f = RedactFilter()
    log.addFilter(f)
    calls.addFilter(f)
    h = logging.StreamHandler(sys.stdout)
    h.addFilter(f)
    log.addHandler(h)
    log._mmb_setup = True


def call_line(**fields) -> None:
    calls.info(json.dumps(fields, sort_keys=True))
