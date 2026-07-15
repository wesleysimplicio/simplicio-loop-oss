# PROFILE — pydantic/pydantic

_Reconnaissance date: 2026-07-15. Author: wesleysimplicio (newcomer, 0 merges here)._

## Identity
- Upstream: `pydantic/pydantic` (SLUG `pydantic__pydantic`), default branch `main`.
- Popular data-validation library. Python front-end (`pydantic/`) + Rust core in
  the **separate** repo `pydantic/pydantic-core` (many runtime bugs live there,
  not here). V1 is maintenance-only on branch `1.10.X-fixes`; new work targets V2/V3.
- Fork: `wesleysimplicio/pydantic`, remote `fork`. Clone: `work/pydantic__pydantic`.

## Contribution rules digest
- **Issue-first + assignment-first (HARD)**: "Any pull request fixing an existing
  issue without being assigned first will be automatically closed." → to fix an
  issue you must first comment and get it assigned to you. Trivial changes
  (typo, docs tweak, stale docstring) are exempt from the issue requirement.
- **AI policy**: AI-assisted contributions welcome, BUT they reserve the right to
  close PRs that look like mass cross-repo submissions (spam), fail quality, or
  have AI-generated incoherent descriptions. Ban risk for spam. → be selective,
  human-coherent, one genuine problem per PR.
- No CLA. DCO not required (no sign-off seen on merged commits).
- "please review" comment assigns reviewers; PR title becomes the changelog line.

## Build / test / lint commands
- Prereqs: Python 3.10–3.14, `uv`, `make`, Rust stable, pre-commit.
- `make install` → setup. `make format` → ruff format+fix. `make` → tests+lint.
- Sub-targets: `make test`, `make testcov`, `make lint` (lint-python + lint-rust),
  `make typecheck`, `make codespell`, `make docs`, `make test-mypy`.
- Tests use pytest. Python-only changes don't require compiling the Rust core.

## Audit commands (Phase 3 mechanical audit — Python repo)
- `scripts/audit.py` (generic Python scan) applies here.
- Extra: `ruff check pydantic tests`, stale-docstring greps (docstring params vs
  signature — the proven external-merge theme, see Benchmark), `make codespell`.

## PR conventions
- Title: concise imperative summary (used verbatim in changelog); scope prefix
  optional (`docs:`, `fix(mypy):` seen). Reference issue as `fix #NNN` in body.
- Body: PR template = `## Change Summary` → `## Related issue number` →
  `## Checklist`. Merged external PRs keep it short and concrete; no heavy
  templates, no mermaid diagrams.

## Maintainer priorities
- Active maintainers (do NOT imitate their large/internal PRs): **Viicos**
  (=Victorien, most prolific), **davidhewitt** (David Hewitt). They handle core
  fixes, mypy plugin, caching, typing internals.

## Benchmark snapshot (2026-07-15)
- Sampled last 30 merged PRs. Mix: heavy dependabot/CI bumps, maintainer bug
  fixes, and a steady stream of **small external docs/docstring fixes**.
- **Merged EXTERNAL envelope** (our realistic path): 1–175 changed lines, most
  are 1–10 lines. Examples:
  - Kropiunig #13415 (+0/-2) remove duplicated docstring entries; #13373 (+0/-1)
    remove stale `field_name` param from `apply_validators()` docstring.
  - Srivatsa03 #13374 (+9/-0) real bug fix (`json_schema_extra` dropped) WITH test.
  - dhruvatr #13400, lkk7 #13395, Yadidiah-k #13375 — 1-line docs/example fixes.
  - strawgate #13430 (+175/-0) new troubleshooting doc.
- One problem per PR, minimal deletions, correctness verified.

## Review culture
- **Very competitive / high closure rate for newcomers.** Recent closed-unmerged
  external PRs (13440,13439,13434,13433,13429,13426,13421,13417,13407,13402,13398,
  13397,13396...) show many AI-shaped "fix" PRs get closed. #13396 "add stacklevel
  to 21 warnings.warn()" = mass mechanical cleanup → closed. #13397 "fix 2
  docstrings" → closed (so even docstring PRs must be genuinely correct/needed).
- Maintainers (Viicos, davidhewitt) review fast but reject drive-by / duplicate /
  low-value PRs aggressively. Bar for merge is HIGH.

## Forbidden / low-value themes (project-specific, adds to global list)
- Mass mechanical edits (batch stacklevel/typo/lint/noqa) — proven-rejected (#13396).
- Fixing an existing issue WITHOUT first getting assigned — auto-closed.
- Speculative "fix" PRs for bugs that actually live in `pydantic-core` (Rust).
- Duplicating an already-open external PR (many overlapping fix PRs exist — always
  re-dedup against open PRs before opening).

## Strategy
1. Newcomer gate active (0 merges): NEWCOMER_DAILY_PR_CAP=2, NEWCOMER_MAX_OPEN_UNREVIEWED=3.
2. First-merge play: ONE genuinely-correct, self-evident **docs/docstring
   correctness** fix (a real stale/incorrect docstring param or a broken doc
   link/example) — exempt from issue-first, matches the proven external merge
   pattern, low reputation risk. Must be verifiably correct (not cosmetic) or it
   gets closed like #13397.
3. For bug fixes: only after picking an **unassigned** issue, commenting to get
   assigned, and confirming the bug reproduces in the Python layer (not core).
   Mandatory fail-before/pass-after pytest.
4. Always re-dedup against OPEN PRs (competitive repo, minutes-fresh duplicates).
5. Quality over volume — a closed PR here hurts the newcomer reputation; skipping
   with a logged reason beats shipping an AI-shaped PR.

## Tunables (overrides)
- Newcomer gate until first merge: NEWCOMER_DAILY_PR_CAP=2, NEWCOMER_MAX_OPEN_UNREVIEWED=3.
- DIFF_LINES_TARGET: keep externals small — target ≤ ~50 lines for first merges.
- STALE_CLOSE_DAYS=0 (never auto-close our own PRs here).

## Project lessons (append-only)
- (2026-07-15) Recon: issue-first+assignment-first is enforced by auto-close;
  high newcomer-PR closure rate; runtime bugs frequently belong to pydantic-core.
