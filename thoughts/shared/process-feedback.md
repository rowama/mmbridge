---
id: FEEDBACK-process
type: process-feedback
phase: any
status: open             # open | closed
owner_agent: Eddie
date: 2026-10-25
links: [PROJECT_STATE.md]
---
# Process friction log

Append friction with the eng-process kit as it happens. Read in every eng-retro and every advisor consultation.
Format: `- YYYY-MM-DD - <confusing | redundant | missing | broken> - <what happened> - <suggested fix>`.

## Design adoption
<!-- One line each time a kit step (skill, template section, gate) is adopted or skipped on this project:
     - YYYY-MM-DD - <step> - adopted | skipped - <reason> - safety: yes|no - informed-owner: yes|no
     Rules (eng-retro applies them):
     - A skip Rob decided knowingly (informed-owner: yes) is recorded but NOT counted against the design.
     - Two counted non-safety skips of the same step -> REDESIGN FLAG for that step (raise in eng-retro / kit feedback).
     - Any skip of a safety gate (personal data handling, mandatory plan review, CP approvals) -> escalate to Rob immediately,
       even if it happened once. -->
- 2026-10-25 - slice-diff cross review (s3) - skipped - DM reuses reviewed paths (plan-review F10) - safety: no - informed-owner: yes
- 2026-10-25 - acceptance against externally deployed system - skipped - in-process ASGI OK for v1 (plan-review F5) - safety: no - informed-owner: yes
- 2026-10-25 - api-channel acceptance - skipped - MCP is the API surface (plan-review F4) - safety: no - informed-owner: yes
- 2026-10-25 - mandatory plan review - adopted - codex plan review, 12 findings dispositioned - safety: yes - informed-owner: yes

## Entries
- 2026-10-26 - broken - eng-run implement for s3 killed by SIGHUP under nohup (exit 129) - handled: kit v2.5.4 setsid + starter-owns-completion (retro 2026-10-26-v0.2.0: closed)
- 2026-10-26 - broken - headless Claude permission mode refused every python/pytest command; s2 run blocked until bypassPermissions in .eng/runners.toml - handled: retro change 1 + kit lesson L1 (proposed)
- 2026-10-26 - confusing - container port 8080 vs 8000 during docker/Coolify checks - handled: retro change 1 (proposed)
- 2026-10-26 - confusing - Grok Bot MCP tool list stale after redeploy until MCP servers restarted - handled: retro change 1 + kit lesson L4 (proposed)
- 2026-10-26 - broken - acceptance conftest scoped repo-wide so `pytest tests` skipped unit tests; rate-limit tests flaked on wall clock - handled: fixed 407cf13; retro change 3 (proposed)
- 2026-10-26 - redundant - push_permission ask round trip before every slice live check - handled: retro change 2 (Rob decides)
- 2026-10-26 - confusing - eng-ship text expects PR/CP-D; project ships main + tag + CP-P - handled: deferred to kit feedback, kit lesson L2
- 2026-10-26 - confusing - CopyFromBox / PowerShell quoting friction for planner edits on Merkle - handled: deferred, kit lesson L5
- 2026-10-26 - missing - friction lived in handoffs; this log and Design adoption were empty at retro - handled: kit lesson L6; back-filled by retro
- 2026-10-27 - broken - `eng-run code-review` from Claude Code's non-login shell: `codex` not on PATH (installed under ~/.nvm/versions/node/*/bin); exit 127 until PATH was prefixed - handled: worked around per run (lb2); fix: add nvm bin to PATH in runner env or .eng/runners.toml
- 2026-10-27 - claude-code - eng-run code-review (Codex) sandbox cannot bind localhost ports, so uvicorn-backed integration tests (lb3 listener vs fake WS) error there and Codex reports "partial validation" with "No findings". Verifiers should not treat Codex's test run as coverage for socket tests; consider a runner option allowing loopback binds.
