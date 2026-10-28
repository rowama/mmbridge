# Verification: SLICE-20261027-lb4b-drop-allowlist

- Date: 2026-10-27
- Verifier: Grok Bot executor (for Eddie), Merkle WSL
- Code SHA: 14ecd18 (docs 2d7105d), base cb4e711 (local kit v2.5.9 upgrade, not pushed)
- Verdict: PASS (pending CP-S)

## Re-run checks
| Check | Result |
|---|---|
| Unit x3 | 234 passed (x3, stable) |
| lb4b spec node ids | 12 passed |
| Live all | 13 passed, 2 failed (lb5 connection-drop specs, NotImplementedError; expected, out of slice) |
| Default acceptance | 16 passed, 15 skipped |
| eng-check | OK, 0 errors, 3 warnings (no on_complete hook, latest artifacts > 12, approval log size) |
| eng-spec status | lock ok; specs and DSL match lock |
| Implicit-join grep (app/) | no join calls; only membership check `GET /channels/{id}/members/me` (service.py:51) |

## Security-focused cross-model review (membership = wake boundary)
`eng-run code-review --base cb4e711` (Codex): No findings
(thoughts/shared/verification/2026-10-27-slice-20261027-lb4b-drop-allowlist-review-2.md).
Removal of allow-list consistent across config, admin (`--channels` rejected), and filter; legacy `channels` key ignored.

## CP-S demo (for Rob)
1. Admin `add` bot without `--channels`; confirm `--channels` returns `invalid_argument: channels no longer used`.
2. Post in public, private channel and thread reply where bot is a member -> one wake each (thread keeps root_id).
3. Post in a channel bot is not a member of -> no wake; bridge never joins.
