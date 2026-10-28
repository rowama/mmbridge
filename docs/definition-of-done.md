---
id: DOD
type: definition-of-done
phase: any
status: active
owner_agent: Eddie
date: 2026-10-28
links: []
---
# Definition of Done

A slice/increment is Done only when every applicable item holds, proven by commands re-run in the verifying session (a report is a claim until re-executed):

- [ ] All plan success criteria for the slice are checked: automated (re-run, exit 0) and manual (confirmed by Rob).
- [ ] New behavior has tests; a bug fix has a regression test that failed before the fix.
- [ ] No test, timeout, lint rule, or check was weakened, skipped, or suppressed without Rob's named approval.
- [ ] Build, lint/typecheck, and the full test suite pass.
- [ ] Executable specs (medium/large, when acceptance is enabled): every REQ in the approved design has a spec
      (`eng-spec trace`), all specs pass on every planned channel, and locked specs / the DSL interface were not
      changed without Rob's re-approval (`eng-spec status` clean; assertion-step changes covered by the code review).
- [ ] Error paths handled; no silent failures.
- [ ] Docs touched by the change are updated (README, AGENTS.md commands, API docs).
- [ ] CHANGELOG entry under Unreleased; VERSION bumped at ship if the project uses one.
- [ ] Durable decisions recorded as ADRs; deferrals recorded in TODOS.md.
- [ ] Verification report written with verdict PASS.
- [ ] PROJECT_STATE.md updated and a handoff written.
<!-- Project-specific additions below -->
- [ ] `pytest tests` from the repo root runs unit + acceptance with zero silent collection skips (collected count matches).
- [ ] Time/rate-dependent tests use an injected/frozen clock, never wall clock.
- [ ] No sleep/timing-based waits on threads or async tasks in tests: use events, injected clocks, or polling with a deadline. For slices with concurrency (threads, async tasks, sockets), the verifier runs the full suite 3 times and all 3 pass. (retro v0.3.0 change 3)
- [ ] Checkpoint asks (CP-C, CP-S) for any user-visible behaviour change include a one-line `Before -> After` example, and the CP-S demo shows it. (retro v0.3.0 change 1)
- [ ] Live path (retro v0.3.0 change 2): from the first slice with a live path, the slice keeps a thin live demo runnable at CP-S; earlier CP-S asks list only runnable-now checks.
