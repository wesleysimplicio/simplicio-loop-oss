# PROFILE — browser-use/browser-use

_Phase R reconnaissance: 2026-07-15. Refresh benchmark on demand._

## Identity

- Upstream: `browser-use/browser-use` — LLM browser automation agent (Python).
- Scale: ~104.8k stars, ~314 open issues. Very high traffic, fast-moving.
- Default branch: `main`. Also `stable`, `releases/**`.
- Fork: `wesleysimplicio/browser-use` (remote `fork`). GH login: `wesleysimplicio`.

## Contribution rules digest

- CONTRIBUTING.md points to docs.browser-use.com (contribution-guide, local-setup)
  and the `help wanted` issue label (currently EMPTY — no open help-wanted issues).
- **No CLA, no DCO** found (no `-s` required; no CLA bot in workflows). Not blocking.
- Integration examples have their own guidelines (`examples/integrations/README.md`).
- Has a `@claude` GitHub Action (claude.yml) and an AI review bot on PRs — expect an
  automated review comment; address it before pinging humans.
- Stale-bot workflow exists (`stale-bot.yml`) — our PRs can be auto-flagged if idle.

## Build / test / lint commands

- Setup: `uv sync --all-extras --dev` (Python 3.11+; installs playwright/chromium extras).
- Tests: `uv run pytest -vxs tests/ci` (CI subset) / `uv run pytest -vxs tests/` (all).
  Single: `uv run pytest -vxs tests/ci/test_X.py`. pytest asyncio_mode=auto, timeout=300.
- Type check: `uv run pyright` (CI job `type-checker`).
- Lint/format: `uv run ruff check --fix` + `uv run ruff format` (line-length 130).
  Syntax gate in CI: `uv run ruff check --no-fix --select PLE`.
- Full gate: `./bin/lint.sh` or `uv run pre-commit run --all-files` (CI `code-style`).
- NOTE (env): local pytest has been reported to segfault on some setups
  (issue #5041 comment). Verify the test harness runs before promising a test result;
  if it cannot run locally, say so honestly and do not fabricate.

## Audit commands (Phase 3 — this IS the mechanical audit here, Python repo)

- `uv run ruff check --no-fix --select PLE browser_use/` (syntax/logic errors)
- `uv run pyright browser_use/` (type regressions)
- grep for deprecations / TODO/FIXME clusters in `browser_use/`
- `scripts/audit.py` also applies (Python repo) but ruff/pyright are the real signal.

## PR conventions

- Title: Conventional Commits with real scope is common for core fixes
  (`fix(browser): ...`, `fix(tests): ...`, `fix(telegram): ...`) but plain
  imperative titles also merge ("Fix visibility check mutating shared snapshot bounds").
- Body: LIGHT. Merged external/core PRs mostly use short prose, not heavy templates.
  Do NOT impose a mermaid-diagram heavy template — none of the recent merges use one.
  Keep `## Summary` + short validation; link the issue with `Closes #NNNN`.
- Issue number in title `(#NNNN)` when one exists is a plus, not required.

## Maintainer priorities

- Core team ships nearly all merges: `laithrw` (Laith Weinberger), `sauravpanda`
  (Saurav Panda), `MagMueller`/`gregpr07` (founders), `ShawnPana`, `Alezander9`.
- Hot areas (last ~30 merges): CLI 3.0 / browser-harness migration, README/docs,
  DOM/serialization correctness, MCP server, LLM output parsing robustness,
  event-bus / watchdog lifecycle, version bumps.
- sauravpanda merges the model bug-fix pattern for externals to imitate:
  small focused correctness fixes, ~50–220 changed lines, one problem per PR
  (e.g. #5151 +115/-4, #5148 +209/-5, #5146 +86/-30, #5133 +217/-50).

## Benchmark snapshot (2026-07-15)

- Merged mix: heavy on core-team infra/CLI/docs; genuine external merges are RARE.
- Diff-size envelope that merges for externals: SMALL (~3–220 added lines,
  minimal deletion, single concern). README one-liners also merge (`ShawnPana`, `Cheggin`).
- External merges observed: mostly README/docs enhancements. Bug-fix merges from
  brand-new externals are uncommon and heavily contested.
- Our record here: 0 opened / 0 merged (NEWCOMER).

## Hot areas & top contributors (2026-07-15)

- 30-day authors: Laith Weinberger (50), Saurav Panda (17), Shawn Pana (6),
  Magnus Müller (2), Alexander Yue (1) — ALL core team. No external in the top list.
- No external contributor is a regular merger → realistic path is a small, clearly
  correct, UNCONTESTED bug fix with a repro, or a genuinely useful docs fix.

## Review culture

- Fast, core-team-driven. An AI review bot comments on PRs automatically.
- **Duplicate/contention risk is EXTREME**: popular bug issues attract 3–5 newcomers
  all claiming "I'll fix it" / "I fixed it" within days (see #5041: PRs #5049, #5081
  + 3 more claimants; #4846 → PR #4993; #4877/#4868 → PR #4882). Re-dedup immediately
  before opening is mandatory here, not optional.
- Many "working on it" comments never produce a merged PR — a claim is not a PR, but
  an OPEN competing PR is a discard signal (leave a review instead).

## Forbidden / low-value themes

- Generic forbidden classes apply (mass mechanical cleanup, trivial-theme series,
  no-issue/no-symptom PRs).
- README/docs churn: low-value UNLESS it fixes a real inaccuracy — the repo already
  gets many drive-by README PRs; avoid competing there.
- Any issue that already has an OPEN third-party PR (leave a technical review, do not
  compete). Any heavily-claimed issue (#5041-style pile-ons) — avoid.
- Do not open type-var refactors (#5188) speculatively without maintainer buy-in.

## Strategy

1. NEWCOMER gate active (0 merges): cap 2 PRs/day, max 3 open unreviewed.
2. Prefer ONE small, clearly-correct, low-contention bug fix with a reproducible
   test over volume. Merge rate > volume, especially for reputation build here.
3. Every candidate: verify no open competing PR (re-dedup right before opening).
4. If local test harness can't run (segfault risk), pick a candidate whose fix is
   verifiable by reading code + a lightweight unit test, and be honest in Validation.
5. Reviewing third-party PRs / posting technical repro evidence on issues is a valid,
   reputation-positive play when no clean uncontested candidate exists.
6. Zero PRs with a logged reason is an acceptable iteration outcome.

## Tunables (overrides)

- Newcomer gate until first merge: `NEWCOMER_DAILY_PR_CAP=2`,
  `NEWCOMER_MAX_OPEN_UNREVIEWED=3` (per scheduled-task + config.env).
- `STALE_CLOSE_DAYS=0` (never auto-close our own PRs — active repo, reviews come).
- `DIFF_LINES_TARGET=220` (observed external merge envelope).

## Project lessons (append-only)

- (2026-07-15) Contention is the #1 risk here. High-signal bug issues get claimed by
  multiple newcomers fast; several already have open PRs. Re-dedup before every open.
- (2026-07-15) No CLA/DCO — no sign-off needed.
- (2026-07-15) Local pytest may segfault on some environments (#5041 comment) — never
  fabricate a "tests pass" line; run and paste real output or state the limitation.
