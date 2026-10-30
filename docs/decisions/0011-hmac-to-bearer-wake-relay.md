---
id: ADR-0011
type: adr
phase: architecture
status: accepted         # proposed | accepted | partially-accepted | deferred | rejected | deprecated | superseded
owner_agent: grok-bot
date: 2026-10-28
links: [docs/design/2026-10-28-grok-webhook-multibot.md, docs/architecture/2026-10-28-grok-webhook-multibot.md]
supersedes: earlier ADR-0011 draft "Grok Bot routine wake target kind" (Bearer-in-mmbridge, never accepted; commit e9c8bc7)
superseded_by: none
revisit: when moving the relay onto the Grok Bot computer (future)
---
# ADR-0011: HMAC->Bearer wake relay beside mmbridge

## Status
proposed (rewritten 2026-10-28 after Rob's authenticity decision; replaces the Bearer-in-mmbridge draft)

## Context
REQ-B1/B2/B4. The Grok Bot routine wake contract (locked at CP-A): POST to a per-routine URL, `Authorization: Bearer <routine key>`, any JSON body, 200 = run started. The routine cannot verify HMAC, timestamps or replays. ADR-0008 signs wakes with HMAC and sends no Authorization (research Q1, app/wake.py:131-137). The earlier draft added a `grok` wake kind so mmbridge would send the Bearer key itself, plus `claim_wake` (ADR-0012) to recover authenticity. Rob decided instead: keep mmbridge HMAC-only and put a thin relay beside it.

## Decision
- mmbridge keeps sending only ADR-0008 signed wakes (no wake `kind`, no Bearer key in the store). Payload gains v2 fields (bot, reply hints) inside the signed body.
- New small service, the **wake relay**, deployed as its own container on the same VPS (since 2026-10-30: service `relay` in the Mattermost Docker Compose stack, see note): `POST /wake/<bot>` verifies HMAC (per-bot secret, constant time), timestamp window 300 s, and delivery-id dedupe (24 h); then forwards the verified body unchanged to that bot's Grok routine URL with `Authorization: Bearer <routine key>`.
- Status mapping back to mmbridge: upstream 2xx -> 200; 408/429/5xx/timeout -> 503 (mmbridge retries); other upstream 4xx -> 424 (permanent); bad sig/stale -> 401; duplicate -> 200 without forwarding.
- Routine URL/key and HMAC secrets live only in relay Coolify secrets; redacted in logs.
- Per-bot rate limit (default 30/min, burst 10) and a tripwire alert (HMAC failure bursts, rate-limit hits, upstream 401/403, forwarded vs mmbridge delivered count drift).
- Future only (not this increment): run the relay on the Grok Bot computer.

## Alternatives
- Bearer-in-mmbridge (`grok` wake kind, previous draft): rejected by Rob; mmbridge would hold routine keys and lose HMAC authenticity end to end.
- `claim_wake` MCP tool: rejected for this increment (ADR-0012).
- Polling by Grok Bot: rejected (latency).

## Consequences
Positive: mmbridge wire format and ADR-0008 unchanged (one format to test); authenticity, tamper and replay checks happen before the routine is woken; Bearer keys isolated from Mattermost tokens and the store key. Negative: one more deploy to run and monitor; the relay holds Bearer keys, and a leaked key lets an attacker wake the routine directly, bypassing HMAC - **accepted risk** (low probability; key only in relay secrets; rate limit + tripwire + rotation runbook). Neutral: retry mapping for undocumented Grok codes verified in the B-s1 spike.

## Prediction (scored in a later eng-retro)
- Expected outcome: a real Grok routine starts on every qualifying post via the relay in B-s1 CP-S; forged/replayed wakes are rejected at the relay; tripwire never fires in normal use.
- Check date: after the increment B ship
- What would prove it wrong: the routine rejects or mangles relayed POSTs, the relay becomes a reliability bottleneck, or a key leak is observed.

## Note 2026-10-28: delivery guarantee (accepted risk, Rob 2026-10-28)
Relay dedupe records a delivery id only after the upstream routine returns 2xx (option A). A lost upstream response or a relay crash after upstream 2xx can cause a rare double wake; accepted because marking before forwarding (option B, rejected) can lose posts. Routine-side idempotency on `X-MMB-Delivery` (option C) is deferred; revisit if the relay's count-drift tripwire (`double_forward`) fires often (>= 3 in 24 h). Plan: thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md "Delivery guarantee".

## Note 2026-10-30: deploy in the compose stack (Rob 2026-10-30)
Relay runs as service `relay` in the same Coolify Docker Compose as Mattermost + mmbridge + Postgres (Coolify service pbrl8nkssi6dnanfxofnftkc), not a separate Coolify app. mmbridge wake URL `http://relay:8080/wake/<bot>` on the private network (mmbridge allows plain http only to host `relay`, no flag; amended 2026-10-30, Rob: tighten, do not open LIVE_ALLOW_HTTP_WAKE globally); no public relay domain required. Rob installs/updates the compose; Ulrik does VPS wiring. Relay code unchanged.

## Observed 2026-10-30: B-s1 spike (OQ-B1/B2)
`relay/spike_routine.py` against Rob's real Eddie routine: valid key -> 200, wrong key -> 401, bad URL -> 401. Marker `mmb-spike-262ca3a7` reached the bot intact (body passthrough verbatim). Matches the assumed mapping (401 -> relay 424, tripwire); no OQ-B1/B2 fallback needed. Note: a bad routine URL answers 401 (not 404), so 424 `{"upstream":401}` can mean wrong key or wrong URL.
