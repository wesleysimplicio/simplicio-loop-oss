# PROFILE — modelcontextprotocol/python-sdk

## Identity
- Upstream: `modelcontextprotocol/python-sdk` (the official MCP Python SDK, `mcp` on PyPI).
- Default branch: `main` (this is the **v2 rework** — breaking changes welcome here). Stable line is `v1.x` (security + critical bug fixes only, `[v1.x]` title prefix).
- Our GH login: `wesleysimplicio`. Fork: `wesleysimplicio/python-sdk`.
- Our record here: **0 opened / 0 merged / 0 closed** (newcomer).

## Contribution rules digest (from CONTRIBUTING.md + AGENTS.md)
- **All PRs require a corresponding issue.** No-issue PRs are closed (trivial typo/docs/broken-link excepted).
- **Buy-in gate:** having an issue does NOT authorize coding. Wait for maintainer feedback or a `ready for work` label; then **comment on the issue to get assigned** before starting (prevents duplicate effort). PRs on issues without buy-in may be closed.
- Issues labeled `needs confirmation` / `needs maintainer action` are NOT ready.
- **Small PRs only.** "A few dozen lines reviewed in minutes; hundreds of lines across many files sit in the queue." Break big work up.
- Rejected classes: no prior discussion, scope creep, misalignment with SDK direction, overengineering, undisclosed/unreviewed AI output.
- New public APIs / decorators, architectural changes, multi-module changes, spec-touching features → always issue-first (spec changes need a SEP).
- License: MIT. No CLA. **DCO not required** (no `Signed-off-by` seen in merged commits).

## ⛔ BLOCKING POLICY — autonomous-agent PRs are forbidden here
CONTRIBUTING.md "AI-Assisted Contributions" is explicit and enforced:
- AI assistance must be **disclosed** (one line in the PR/issue).
- There must be a **human who understands the change** and answers maintainer questions "in your own words, not pasted from a chat window."
- **"No drive-by agents. PRs, issues, or comments produced by an autonomous agent with no human review get closed on sight. If your agent is auto-filing PRs against our open issues, stop."**
- **"Undisclosed AI contributions get closed. Repeat offenders get banned from the `modelcontextprotocol` org."**

An unattended, scheduled simplicio-loop-oss run cannot satisfy these prerequisites (no human in the loop to own/defend the change, and self-assignment on an issue is itself an agent-authored comment the policy forbids). This is a **hard stop, analogous to an unsigned CLA**: open ZERO PRs, ZERO issues, ZERO comments autonomously in this repo. Surface candidates to the human instead.

**How a human unblocks this repo (one-time-per-issue, not org-wide):** the human personally (a) picks a `ready for work` issue, (b) comments to claim/assign it, (c) discloses AI assistance, (d) reviews and can explain the resulting change. Only then may the loop help draft the diff for that specific issue — never file on its own. Record the human's go-ahead here when given.

## Build / test / lint commands
- Toolchain: Python 3.10+, **uv only** (NEVER pip; `uv pip install` and `@latest` FORBIDDEN). CI covers 3.10–3.14.
- Install: `uv sync --frozen --all-extras --dev`
- Test: `uv run --frozen pytest` (async via anyio, not asyncio; plain `test_*` functions, no `Test*` classes for new tests)
- Types: `uv run --frozen pyright`
- Lint/format: `uv run --frozen ruff check .` / `uv run --frozen ruff format .`
- README snippets (if `docs_src/` embedded code changed): `uv run scripts/update_readme_snippets.py`
- pre-commit: `uv tool install pre-commit --with pre-commit-uv`; `pre-commit run --all-files`
- Breaking changes on `main` must be documented in `docs/migration.md`.
- Imports at top of file (inline imports only for lazy optional deps / re-import tests).

## Audit commands (Phase 3 — this is a Python repo, audit.py applies but prefer these)
- `uv run --frozen pyright` (type regressions)
- `uv run --frozen ruff check .` (lint)
- `uv run --frozen pytest -q` (must stay green)
- Deprecation/TODO greps in `src/mcp/` for hot-area context.

## PR conventions
- Title: conventional-commit-ish with real subsystem scope; many maintainer merges use plain imperative sentences too. Examples merged: `fix: reject trailing newline in tool-name validation`, `docs: pin mkdocs<2`. `[v1.x]` prefix for backports.
- Body: no heavy template observed; concise summary + link the issue (`Closes #NNN`). Disclose AI assistance. No mermaid diagrams in recent merged PRs — don't add one.
- One logical change per PR; keep diffs small.

## Benchmark snapshot (2026-07-15)
- Last ~30 merged PRs: **overwhelmingly maintainer-authored.** `maxisbey` (Max) authored ~24/30; `Kludex` (Marcelo Trylesinski) and `localden` (Den Delimarsky) also maintainers.
- **External merges are rare and tiny:** `Otis0408` — `fix: reject trailing newline in tool-name validation` (+9/-2); `冯基魁` (1 commit). That is the realistic external envelope: **single-digit to low-tens line, one focused bug fix, tied to an issue.**
- Maintainer PRs are large (hundreds–thousands of lines, v2/SEP work) — NOT a model to imitate.
- Mix skew: heavy docs + v2 transport/protocol feature work (maintainer), plus small external bug fixes.
- Salvage/revival PRs: none observed among recent merges — do not assume accepted.

## Hot areas & top contributors (2026-07-15)
- Top 30d committers: Max (68, maintainer), Marcelo Trylesinski/Kludex (28, maintainer), then long tail of 1-commit externals.
- Hot areas: v2 transports (2026-07-28 era stream loop), client extension/cache APIs, OAuth/DCR, docs migration, conformance CI.
- MAINTAINERS: maxisbey, Kludex, localden. EXTERNALS to imitate: Otis0408-style tiny issue-linked bug fixes.

## Review culture
- Active, opinionated, maintainer-driven. Fast on small focused fixes; large/unaligned PRs sit or get closed. Strong stance against unreviewed AI output.
- 540 open issues; healthy `ready for work` and `good first issue` queues exist (candidates for a HUMAN to pick up).

## Forbidden / low-value themes
- **Autonomous PRs/issues/comments of any kind (policy hard stop — see above).**
- No-issue PRs; PRs on issues lacking maintainer buy-in / `ready for work`.
- Mass mechanical cleanup (lint/typo/format batches), trivial-theme series.
- Large refactors / new public APIs without a SEP or approved issue.
- `pip` usage; raising dependency floors for CVEs alone (see AGENTS.md).

## Strategy
- **This iteration and every unattended iteration: open nothing.** The project's enforced anti-autonomous-agent policy makes autonomous contribution a reputation/ban risk with negative expected merge rate.
- Ongoing value the loop CAN provide safely: maintain a shortlist of realistic `ready for work` / `good first issue` candidates (Otis-sized, single bug, tied to an issue) in the daily backlog **for the human to pick up personally**, and keep the profile/benchmark fresh.
- If/when the human opts in on a specific issue (claims + discloses + will own it), the loop may help draft that one diff — never file autonomously.

## Tunables (override config.env)
- `NEWCOMER_DAILY_PR_CAP=0` — no autonomous PRs (policy).
- `NEWCOMER_MAX_OPEN_UNREVIEWED=0`
- `MAX_SALVAGES_PER_DAY=0` — salvages not shown accepted; still autonomous-forbidden.
- `STALE_CLOSE_DAYS=0` (auto-close disabled; moot at 0 PRs).

## Project lessons (append-only)
- (2026-07-15) modelcontextprotocol org **enforces** an anti-autonomous-agent policy with org-wide bans for repeat offenders. Treat this like an unsigned CLA: autonomous PR/issue/comment filing is a HARD STOP. The loop's job here is candidate scouting + profile upkeep for a human, not autonomous filing.
