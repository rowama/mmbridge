---
id: SLICE-20261030-http-wake-internal-hosts
type: slice
phase: implement
status: done             # todo | in-progress | blocked | review | done
owner_agent: grok-bot
date: 2026-10-30
links: [thoughts/shared/slices/2026-10-28-b-s1-relay-grok-wake-one-bot.md, docs/decisions/0011-hmac-to-bearer-wake-relay.md]
plan: none - small triage (security), Rob 2026-10-30 "Tighten now"
plan_phase: none
review: "skipped: small security tighten, unit-tested; Codex advisory optional"
reqs: []
specs: none - unit tests in tests/unit/test_store.py cover the rule
---
# Slice: HTTP wake only to internal hosts

## Outcome (user-visible, demoable)
`set-bot --wake-url http://relay:8080/wake/eddie` is accepted with no env flag, while `http://<any other host>` is still refused; production compose no longer sets `LIVE_ALLOW_HTTP_WAKE`.

## Change
- `app/store.py` `https_ok`: https always OK (unchanged); plain http OK only when the parsed host is exactly in `INTERNAL_HTTP_WAKE_HOSTS = {"relay"}` (case-insensitive, no userinfo). `LIVE_ALLOW_HTTP_WAKE=true` kept as a tests-only escape hatch (acceptance driver uses a 127.0.0.1 receiver). Policy A.
- Ops/docs: removed `LIVE_ALLOW_HTTP_WAKE=true` from `coolify-service.snippet.yaml`; relay/README.md, ADR-0011 note, plan B, B-s1 slice amended.

## Acceptance criteria
- [x] https:// to any host accepted (flag unset)
- [x] http://relay:8080/wake/eddie, http://RELAY:..., http://relay/... accepted with flag unset or false
- [x] http://evil.example, relay.evil.example, relayx, relay@evil.example, 127.0.0.1, localhost, 8.8.8.8 rejected with flag unset
- [x] validate() (set-bot/load path) accepts relay, rejects public http
- [x] flag=true still allows the local test receiver; full unit suite green

## Tasks
- [x] Write failing tests (7 red for the right reason: relay rejected)
- [x] Implement host allowlist in https_ok
- [x] Unit suite green
- [x] Docs/snippet updated

## Size check
~70 changed lines.

## Progress log
- 2026-10-30 - grok-bot - tests at tail of tests/unit/test_store.py; app/store.py https_ok; snippet/docs.

- 2026-10-30 - grok-bot - CP-S approved by Rob (via Eddie); commit 8c60bc8 exercised live by the B-s1 demo (http://relay wake). Slice done.

## Blockers / deviations from plan
none