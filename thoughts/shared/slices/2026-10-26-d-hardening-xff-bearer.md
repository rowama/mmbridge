---
id: SLICE-20261026-d-hardening-xff-bearer
type: slice
phase: implement
status: todo             # todo | in-progress | blocked | review | done
owner_agent: claude-code
date: 2026-10-26
links: []
plan: none - small triage (PROCESS.md 2)
plan_phase: n/a
review: codex-advisory (security-touching)
reqs: [REQ-1]   # auth / rate-limit hardening of existing reqs
specs: none - small; unit tests in tests/unit/test_app.py
---
# Slice: D hardening - trust only Coolify proxy for XFF; case-insensitive Bearer

## Request (Rob 2026-10-26)
"Do D hardening first, then triage A." D = TODOS P1 XFF, P1 conftest scope, P2 ADR-0004 burst, P2 Py3.14/3.12, P2 F2 Bearer case, P3 ruff/mcp 2.x (optional). Excludes @mentions, websockets, threads/reactions/files, multi-bot, auto-join.

## Triage: small (security risk area -> Rob confirms size)
1. Two code changes, ~2 files (Dockerfile CMD, app/auth.py) + unit tests; no new interface, no data change, revert = one commit.
2. Already-done items closed on evidence (conftest 407cf13, ADR-0004 amended to burst 60, AGENTS.md pins 3.12), so no design work remains.
3. Risk area is security (client IP spoof vs anon rate limit), hence Rob confirmation of "small" instead of sizing up to medium.

## Outcome (user-visible, demoable)
A client sending a forged X-Forwarded-For can no longer change its rate-limit IP; "bearer <token>" (any case) authenticates like "Bearer <token>".

## Acceptance criteria
- [ ] Dockerfile no longer uses `--forwarded-allow-ips *`; trusted proxy comes from env `FORWARDED_ALLOW_IPS` (default `127.0.0.1`; Coolify sets the Traefik network/IP). Documented in README/AGENTS.
- [ ] Unit test: request from untrusted peer with `X-Forwarded-For: 1.2.3.4` is keyed on peer IP for the anon limiter (spoof does not reset the bucket).
- [ ] Unit test: `bearer`, `BEARER`, `Bearer` schemes all accepted; malformed cases in test_missing_and_malformed_bearer_401_no_mm_call still 401 (drop bare `"bearer"` only if it stays 401 - it has no token).
- [ ] Full `pytest tests` green; live check after deploy: /health ok, a Grok Bot list_channels still works, anon 429 still triggers.
- [ ] Optional (only if <20 lines): `ruff check app tests` added to gate in AGENTS.md / DoD.

## Tasks
- [ ] Write failing tests (XFF spoof, Bearer case)
- [ ] auth.py: `_BEARER` regex with `(?i)` on scheme only (token stays case-sensitive)
- [ ] Dockerfile: `--forwarded-allow-ips` from `${FORWARDED_ALLOW_IPS:-127.0.0.1}` (shell-form CMD or uvicorn env `FORWARDED_ALLOW_IPS`, which uvicorn reads natively)
- [ ] Confirm Coolify Traefik source IP/subnet on rmlab and set the env in Coolify (Rob/Eddie)
- [ ] Run gate; update TODOS (close XFF + F2)

## Size check
~30-60 changed lines.

## Progress log
- 2026-10-26 - grok-bot - triaged small; card created; closed conftest/ADR-0004/3.12 TODOs on evidence.

## Blockers / deviations from plan
- Rob to confirm size small (security). Coolify proxy IP/subnet needed for the env value.
