---
id: PLANREV-20261028-grok-webhook-multibot-plan-review
type: review-findings
phase: plan
status: open
owner_agent: eng-run
date: 2026-10-28
links: [thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md]
review_kind: plan
subject: "thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md + slice cards"
diff: n.a.
reviewer: codex
command: "codex exec --sandbox read-only -o thoughts/shared/runs/2026-10-28-plan-review-grok-webhook-multibot.last-message.txt '<prompt: see run log>'"
run_log: thoughts/shared/runs/2026-10-28-plan-review-grok-webhook-multibot.md
---
# Independent review: plan-review grok-webhook-multibot
<!-- Written by eng-run (prompt plan-review v2). Each finding row starts 'open': set disposition fixed (where) |
     accepted-risk (ONLY with Rob's approval, e.g. "Rob 2026-10-28") | rejected (reason). Plan reviews gate
     implementation (medium/large); slice reviews are advisory. -->

## Findings
| # | Severity | Location | Finding | Disposition | Reason / approval |
|---|---|---|---|---|---|
| 1 | high | thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, Phase 1 / Phase 2 | B-s1 deploys a public relay without delivery dedupe or rate limiting; a captured valid wake can repeatedly start the routine within 300 seconds, violating REQ-B2 before B-s2 - Move persistent dedupe, concurrent-delivery protection, and per-bot rate limiting into B-s1, with replay tests required before its live demo. | open | |
| 2 | high | thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, Seen contract and upstream timeout handling | Recording delivery only after upstream success cannot guarantee REQ-B3 at-most-once behavior: the routine may start before its response is lost, or the relay may crash before recording success; retry then starts another run - Add tests for both ambiguous outcomes and establish upstream idempotency, or obtain Rob’s explicit decision on the delivery guarantee and update the design/ADR accordingly. | open | |
| 3 | high | thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, Phase 1 Automated Verification | The required full live acceptance command collects B-s2/B-s3 specs that the plan explicitly expects to remain red, making B-s1’s exit criteria impossible - Provide exact commands selecting A regression specs plus completed B slice specs; expand coverage at each subsequent slice without suppressing failures. | open | |
| 4 | medium | thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, Testing Strategy; tests/acceptance/specs/test_grok_multibot.py:8 | All B specs run exclusively on `live`; the requested large-work API channel and Playwright journey are absent. ADR-0016 explicitly chooses no UI, but the plan does not reconcile that exception with PROCESS section 13 - Record Rob’s explicit channel exception or provide the required API coverage and web journey; identify how `live` satisfies API-channel intent. | open | |
| 5 | medium | tests/acceptance/specs/test_grok_multibot.py, REQ-B8 coverage; thoughts/shared/slices/2026-10-28-b-s3-multi-bot-registry-routing.md | B8 has a revoked-token spec but no executable scenario proving another bot continues waking while one wake target remains down; the planned fairness unit test does not verify operator-visible failure reporting end to end - Add a two-bot outage spec asserting healthy-bot delivery and failing-bot visibility, and list it in B-s3. | open | |
| 6 | medium | tests/acceptance/specs/test_grok_multibot.py, REQ-B2 scenarios | Assertions such as `assert_relay_rejected("bad_sig"/"stale"/"duplicate")` lock internal rejection classifications into behavioral specs, including calling a successful duplicate response a rejection - Assert that forged, altered, and replayed wakes cause no additional routine runs; keep relay reason-code assertions in protocol/unit tests. | open | |
| 7 | medium | thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, Automated Verification; all three slice cards, Tasks | Verification contains non-executable placeholders, omits image-selection settings despite the existing driver defaulting to `mmbridge:lb5`, and omits the DoD’s three full-suite runs for concurrency changes - Supply pasteable commands with explicit modes, current bridge/relay image selection, exact spec selections, and three verification runs covering every planned channel. | open | |
| 8 | medium | thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, Phase 2 root_id tests | Planned tests cover ID format and upstream errors but do not explicitly prove that a valid root from another channel or inaccessible conversation cannot redirect or authorize a reply - Add negative tests using valid foreign root IDs for both posting tools, asserting rejection and no post creation. | open | |

## Reviewer raw output
```
1. [high] thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, Phase 1 / Phase 2 - B-s1 deploys a public relay without delivery dedupe or rate limiting; a captured valid wake can repeatedly start the routine within 300 seconds, violating REQ-B2 before B-s2 - Move persistent dedupe, concurrent-delivery protection, and per-bot rate limiting into B-s1, with replay tests required before its live demo.
2. [high] thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, Seen contract and upstream timeout handling - Recording delivery only after upstream success cannot guarantee REQ-B3 at-most-once behavior: the routine may start before its response is lost, or the relay may crash before recording success; retry then starts another run - Add tests for both ambiguous outcomes and establish upstream idempotency, or obtain Rob’s explicit decision on the delivery guarantee and update the design/ADR accordingly.
3. [high] thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, Phase 1 Automated Verification - The required full live acceptance command collects B-s2/B-s3 specs that the plan explicitly expects to remain red, making B-s1’s exit criteria impossible - Provide exact commands selecting A regression specs plus completed B slice specs; expand coverage at each subsequent slice without suppressing failures.
4. [medium] thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, Testing Strategy; tests/acceptance/specs/test_grok_multibot.py:8 - All B specs run exclusively on `live`; the requested large-work API channel and Playwright journey are absent. ADR-0016 explicitly chooses no UI, but the plan does not reconcile that exception with PROCESS section 13 - Record Rob’s explicit channel exception or provide the required API coverage and web journey; identify how `live` satisfies API-channel intent.
5. [medium] tests/acceptance/specs/test_grok_multibot.py, REQ-B8 coverage; thoughts/shared/slices/2026-10-28-b-s3-multi-bot-registry-routing.md - B8 has a revoked-token spec but no executable scenario proving another bot continues waking while one wake target remains down; the planned fairness unit test does not verify operator-visible failure reporting end to end - Add a two-bot outage spec asserting healthy-bot delivery and failing-bot visibility, and list it in B-s3.
6. [medium] tests/acceptance/specs/test_grok_multibot.py, REQ-B2 scenarios - Assertions such as `assert_relay_rejected("bad_sig"|"stale"|"duplicate")` lock internal rejection classifications into behavioral specs, including calling a successful duplicate response a rejection - Assert that forged, altered, and replayed wakes cause no additional routine runs; keep relay reason-code assertions in protocol/unit tests.
7. [medium] thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, Automated Verification; all three slice cards, Tasks - Verification contains non-executable placeholders, omits image-selection settings despite the existing driver defaulting to `mmbridge:lb5`, and omits the DoD’s three full-suite runs for concurrency changes - Supply pasteable commands with explicit modes, current bridge/relay image selection, exact spec selections, and three verification runs covering every planned channel.
8. [medium] thoughts/shared/plans/2026-10-28-grok-webhook-multibot.md, Phase 2 root_id tests - Planned tests cover ID format and upstream errors but do not explicitly prove that a valid root from another channel or inaccessible conversation cannot redirect or authorize a reply - Add negative tests using valid foreign root IDs for both posting tools, asserting rejection and no post creation.
```
