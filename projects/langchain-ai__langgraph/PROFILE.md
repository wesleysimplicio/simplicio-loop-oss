# PROFILE — langchain-ai/langgraph

Reconnaissance: 2026-07-15 (Phase R). SLUG `langchain-ai__langgraph`.

## Identity
- Upstream: `langchain-ai/langgraph` — framework for stateful, multi-actor LLM
  agents. Python monorepo under `libs/` + JS/TS SDKs. Default branch `main`.
- Our GitHub login: `wesleysimplicio`. Fork: `wesleysimplicio/langgraph`.
- Merged PRs by us so far: **0** → newcomer reputation gate is ACTIVE.

## Contribution rules digest
- **Contributing guide**: https://docs.langchain.com/oss/python/contributing/overview
  (no root CONTRIBUTING.md; guidance lives in `AGENTS.md`, `CLAUDE.md`, PR template).
- **English only** — enforced by language policy; AI-looking PR descriptions
  may be IGNORED or CLOSED (PR template says so explicitly).
- **DCO/CLA**: none observed (no CLA bot, no `Signed-off-by` requirement). Commit
  normally. (Re-verify on first PR.)
- **One package per PR** — "PRs should not touch more than one package unless
  absolutely necessary."
- **Do NOT edit `uv.lock` or add deps to `pyproject.toml`** (even optional)
  without explicit maintainer permission.

## ⚠️ BLOCKING PREREQUISITE — issue-link + assignment gate (issue-first)
`.github/workflows/require_issue_link.yml` has `ENFORCE_ISSUE_LINK: "true"`.
Every PR labeled `external` (applied automatically by `tag-external-prs.yml`)
MUST:
1. Reference an approved issue via `Fixes/Closes/Resolves #NNN` in the body, AND
2. Have the **PR author assigned to that issue** by a maintainer.

If either is missing, the PR is auto-labeled `missing-issue-link`, commented on,
and **CLOSED** (and its CI runs cancelled). Maintainer override = reopen or
remove the label.

**Consequence for us**: we cannot open a mergeable PR until a maintainer has
assigned us to an issue. Blind PRs = instant auto-close = burned reputation.
The realistic path is: find/confirm an approved `help wanted` issue → request
assignment on the issue → wait for a maintainer to assign → THEN implement and
open the PR with `Fixes #NNN`. Phase 4 MUST reject any candidate where we are
not (yet) the assignee of a linked, maintainer-approved issue.

## Build / test / lint commands
Monorepo; run per-library from `libs/<lib>/`:
- Install: `uv sync --frozen --all-extras --all-packages --group dev`
- Format: `make format`   Lint: `make lint`   Test: `make test`
- Single test: `TEST=path/to/test.py make test` (from the lib dir).
- Root `make lint|format|test` fans out to each lib's Makefile.
- CI that must pass (from PR template): `make format`, `make lint`, `make test`
  in each modified package. Extra CI: `pr_lint.yml` (semantic PR title),
  `require_issue_link.yml`, `_test.yml`, `_lint.yml`, `_integration_test.yml`.

### Audit commands (Phase 3 — this is a Python repo; audit.py applies)
- `python scripts/audit.py` over `libs/*/` (Python footguns).
- `make lint` per lib (ruff), `make test` per lib (pytest).
- Type check: libs use `ty`/mypy via `make lint` (issue #5020 tracks enabling `ty`).

## PR conventions
- **Title**: `TYPE(SCOPE): description` — semantic-PR lint enforced.
  - TYPES: feat, fix, docs, style, refactor, perf, test, build, ci, chore,
    revert, release.
  - SCOPES: checkpoint, checkpoint-postgres, checkpoint-sqlite, cli, langgraph,
    prebuilt, scheduler-kafka, sdk-py, docs, ci, deps, deps-dev. (`requireScope: false`.)
- **Body**: keep the template's `Fixes #NN` at top, then 1–2 sentence summary.
  Describe breaking changes; `Depends on #PR` if chained. Short, human-written,
  no large AI-generated walls of text.

## Maintainer priorities
- Core team merges dominate: Nick Hollon (`hntrl`), Quanzheng Long
  (`longquanzheng`), Sydney Runkle, Mason Daugherty, David Duong, Josh Rogers.
- v1 is current (`release(langgraph): 1.2.x`). Roadmap: issue #4973.

## Benchmark snapshot (2026-07-15)
Last 30 merged PRs mix:
- **~60% dependabot** dep bumps (`chore(deps)`), **~15% release** PRs
  (maintainers only), rest are maintainer/external `fix`.
- **External human merges are rare**. Examples: `HugoDurand`
  fix(sdk-py) +73-8; `jdrogers940` chore(cli) +4-4.
- **Diff-size envelope for externals**: small & single-package — roughly
  +4 to +75 lines, minimal deletions, one problem per PR. Anything large is
  maintainer-authored.
- **Body style of merged PRs**: terse — `Fixes #NN` + 1–2 sentences. No
  heavy templated sections. Match this (do NOT paste our generic multi-section
  template here; it reads as AI slop and risks closure).

## Hot areas & top contributors (2026-07-15)
- Hot subsystems: `libs/langgraph` core (delta channels, checkpoints, state
  updates), `sdk-py`, `cli`, checkpoint savers (postgres/sqlite).
- Top authors 60d: dependabot (77), Nick Hollon (39), Quanzheng Long (7),
  Sydney Runkle (4), Mason Daugherty (4), Josh Rogers (4) — nearly all
  maintainers. Externals: a long tail of 1–2 commit authors.

## Review culture
- Fast-moving, maintainer-driven. Strict automated gates (title lint, issue
  link + assignment, tests). External PRs without an approved+assigned issue
  are closed by a bot within minutes. Assume weeks for human review otherwise.

## Forbidden / low-value themes
- Any PR without a maintainer-approved issue we are ASSIGNED to (auto-closed).
- Editing `uv.lock` / adding dependencies (needs maintainer permission).
- Multi-package PRs.
- Mass mechanical cleanup (typos/formatting/noqa) — note #5021 exists
  specifically to STOP docs-typo-fix PRs via codespell. Do not send typo PRs.
- AI-generated-looking descriptions.
- Dep bumps (owned by dependabot) and release PRs (maintainers only).

## Strategy
1. This is a **gated, maintainer-controlled repo**. The only realistic path to
   a merge for a newcomer is the issue-assignment loop:
   pick a strong, well-scoped `help wanted` issue → request assignment →
   after assignment, implement the smallest correct fix with a
   fail-before/pass-after test → open PR with `Fixes #NN` and a terse
   human-written body.
2. Candidate `help wanted` issues (open, unassigned as of 2026-07-15):
   #6412 (`ToolNode.ainvoke` freezes with `sse_read_timeout`),
   #5225 (default value of state var not working with reducer),
   #5077 (pandas msgpack serialization), #5029 (add Windows build to CI),
   #2555 (Pydantic state with aliased fields). Investigate reproducibility
   before requesting assignment — only request on one we can actually fix.
3. Until assigned, open ZERO PRs. Requesting assignment is the gating action;
   do it deliberately on ONE candidate, not in bulk (fresh account = spam risk).
4. Keep PRs single-package, tiny, terse, tested.

## Tunables (overrides config.env)
- `NEWCOMER_DAILY_PR_CAP=2`, `NEWCOMER_MAX_OPEN_UNREVIEWED=3` (active until 1st merge).
- `DAILY_PR_HEALTHY=1` — gated repo; at most one carefully-chosen assigned PR/day.
- `STALE_CLOSE_DAYS=0` (never auto-close our own PRs here).

## Project lessons (append-only)
- (2026-07-15) Hard issue-link + assignment gate enforced by CI bot; blind PRs
  are auto-closed within minutes. Assignment-first is mandatory, not optional.
- (2026-07-15) Merged PR bodies are terse (`Fixes #NN` + 1–2 lines). Our
  generic multi-section PR template would read as AI slop here — use the
  project's minimal style.
