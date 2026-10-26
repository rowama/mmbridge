---
id: HANDO-20261026-s2-implemented-review
type: handoff
phase: implement
status: complete
owner_agent: claude-code
date: 2026-10-26T01:41:10-05:00
links: [thoughts/shared/slices/2026-10-25-s2-post-read-channel.md, thoughts/shared/plans/2026-10-25-mmbridge-mcp.md]
git_commit: 8334f40
branch: main
next_skill: eng-verify
---
# Handoff: Slice 2 implemented, status review

## Task(s)
- Slice 2 (SLICE-20261025-s2-post-read-channel, plan Phase 2): **completed, status `review`**. Automated verification passes; Phase 2 manual verification (Rob) is pending.
- Slice 3 (DM, Phase 3): planned, not started.

## Critical References
- thoughts/shared/slices/2026-10-25-s2-post-read-channel.md (Progress log has every command and exit code)
- thoughts/shared/plans/2026-10-25-mmbridge-mcp.md (Phase 2)
- thoughts/shared/verification/2026-10-26-slice-20261025-s2-post-read-channel-review.md

## Recent changes
- `app/validate.py:1` (new): shared validators `identifier`, `message`, `limit`, `segment` (URL-encode). They raise `ToolError("invalid_argument")`. Identifiers use `re.fullmatch` (so a trailing `\n` can't slip through `$`) and also reject `..`.
- `app/ratelimit.py:50`: `check_write` sets up the write bucket, `RL_WRITES_PER_MIN` default 20 (ADR-0004).
- `app/service.py:42` `_member_channel`: does the by-name lookup (403/404 → `unknown_channel`), then `members/me` (403/404 → `not_member`), and never joins. `:59` `post_channel` → `POST /posts`. `:65` `read_channel` → `channels/{id}/posts?page=0&per_page=limit` + `POST /users/ids`. `create_at` is ISO-8601 UTC with ms and `Z`.
- `app/mcp.py:46` `run(tool, fn, check, write)`: the order is call bucket → `check()` validators → write bucket → identity → tool. It now also maps `ToolError`. `:30-40`: tool args are typed `Annotated[Any, WithJsonSchema(...)]`, so the advertised schema stays typed but pydantic doesn't coerce (`true` → `1`) or produce its own errors. Every bad input becomes `invalid_argument` with zero MM calls. `:89`, `:94`: the two new tools.
- `app/mattermost.py:44`: `post()` json type widened to `dict | list` (for `/users/ids`). No behaviour change.
- `tests/acceptance/drivers/fake_mattermost.py`: added channel by name, `members/me`, `POST /posts`, channel posts, and `POST /users/ids`. Posts made through the API are recorded in `changes`; seeding isn't.
- `tests/acceptance/drivers/mcp.py`: added `given_channel_posts`, `given_no_channel`, `channel_posts`, `newest_posts`, and `world_changes`.
- `tests/unit/test_channels.py` (new): 23 tests covering validators, write bucket, invalid_argument with zero MM calls, not_member with no POST and no posts GET, unknown_channel, read format, and the 21st post being rate limited.
- **No edits** to locked specs, the DSL public interface, or any DSL assertion step body. `eng-spec status`: specs and DSL match the lock.

## Learnings
- `.venv` didn't exist. The box's `python3` is 3.14, and on 3.14 the pins conflict (`fastapi==0.115.6` needs starlette<0.42; `mcp==1.30.0` needs starlette>=0.48 on py3.14). I built `.venv` with Python 3.12 (same as the Dockerfile) using uv: `python3 -m venv /tmp/uvtool && /tmp/uvtool/bin/pip install uv && /tmp/uvtool/bin/uv venv .venv --python 3.12 && VIRTUAL_ENV=.venv /tmp/uvtool/bin/uv pip install -r requirements.txt -r requirements-dev.txt`. Filed in TODOS.md.
- FastMCP validates tool args with pydantic before the function runs. Plain `int` annotations would accept `true` and `"5"` and bypass our `invalid_argument` codes, hence the `Any` + `WithJsonSchema` pattern. Slice 3 (dm_send/dm_read) should reuse the `Message`/`Limit` aliases plus a username alias.
- `eng-run code-review` defaults to `--base main`. Since we work on main, pass `--base <commit before slice code>` (here 644ed0e).

## Artifacts
- app/validate.py, app/service.py, app/mcp.py, app/ratelimit.py, app/mattermost.py
- tests/unit/test_channels.py, tests/acceptance/drivers/fake_mattermost.py, tests/acceptance/drivers/mcp.py
- CHANGELOG.md (Unreleased / Added entry)
- TODOS.md (Python 3.14 install entry)
- thoughts/shared/slices/2026-10-25-s2-post-read-channel.md (status review, checkboxes, Progress log)
- thoughts/shared/plans/2026-10-25-mmbridge-mcp.md (Phase 2 automated checkboxes ticked)
- thoughts/shared/verification/2026-10-26-slice-20261025-s2-post-read-channel-review.md (Codex: no findings; addressed)
- thoughts/shared/runs/2026-10-26-code-review-slice-20261025-s2-post-read-channel.md
- PROJECT_STATE.md, this handoff
- Commits: 644ed0e (previous blocked-run docs), 8334f40 (slice code), plus the docs commit for this handoff

## Approvals
- None requested or granted in this session. pending_approvals unchanged (empty). Nothing pushed (push_permission: ask).
- Next is **CP-S** for slice 2 (manual verification), which the planner requests after eng-verify.

## Action Items & Next Steps
1. Planner: run **eng-verify** for slice 2. Re-run `.venv/bin/pytest tests/unit -q`, `.venv/bin/pytest tests/acceptance -q -k "not dm"`, `python3 .eng/bin/eng-check .`, and `python3 .eng/bin/eng-spec status .`.
2. Planner: request `CP-S: thoughts/shared/slices/2026-10-25-s2-post-read-channel.md - manual verification`. The Phase 2 manual steps need a Coolify redeploy of main, so local commits must be pushed first, and that needs Rob's OK.
3. After CP-S, start slice 3 (DM).

## Other Notes
- `.eng/runners.toml` has an uncommitted change by Rob (`[runners.claude] implement_args = ["--permission-mode", "bypassPermissions"]`). That change is what let this run execute commands. I left it uncommitted; it's Rob's to commit.
- Docker: `docker build -t mmbridge .` exit 0; the container served `/health` → `{"ok":true}` and `/foo` → 404.
- Full acceptance run: 12 passed, 4 failed. The 4 failures are the DM specs for slice 3, as expected.
