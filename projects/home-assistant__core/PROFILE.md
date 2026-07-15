# PROFILE — home-assistant/core

_Phase R reconnaissance: 2026-07-15. Author account: `wesleysimplicio`._

## Identity

- Upstream: `home-assistant/core` — the Python core of Home Assistant.
- Default branch: **`dev`** (NOT `main`). All PRs target `dev`.
- License: Apache-2.0. Huge, very active repo (PR numbers ~#176500+, issues
  well past #150k). Integration-centric monolith: each device/service lives
  under `homeassistant/components/<domain>/` with its own code owners.

## Contribution rules digest

- Fork → branch → PR against **`dev`**. (CONTRIBUTING.md.)
- **CLA REQUIRED (blocking).** Root `CLA.md` carries a DCO-style
  certification enforced by the `home-assistant/cla` bot: on your first PR
  the bot posts a check and requires a one-time signature comment
  ("I have read the CLA Document and I hereby sign the CLA"). Until signed,
  the CLA check stays red and maintainers will not merge — opening a PR
  before signing burns newcomer reputation. **This is a one-time HUMAN
  action for account `wesleysimplicio` and has NOT been done yet.**
- One type of change per PR (the PR template forces exactly one "Type of
  change" box). Split multi-concern work.
- Bugfixes should link an issue (`fixes #NNN`). Tests expected for behavior
  changes. Docs/quality-scale changes may reference a docs PR.
- Feature/integration ideas go through GitHub Discussions first, not PRs.
- AI-tool use is explicitly allowed IF the contributor fully understands the
  code (PR checklist states this).

## Build / test / lint commands

Python project (`pyproject.toml`, `requirements*.txt`). Canonical dev flow:

```bash
python -m venv venv && source venv/bin/activate   # (Windows: venv\Scripts\activate)
pip install -e . -r requirements_test.txt
pre-commit install
# Lint / format / static (what CI runs):
ruff check homeassistant/components/<domain>
ruff format --check homeassistant/components/<domain>
python -m script.hassfest                          # manifest/validation gate
mypy homeassistant/components/<domain>
# Tests (scoped — never the full suite):
pytest tests/components/<domain> -q
```

### Audit commands (Phase 3 — these ARE the mechanical audit here)

Generic `scripts/audit.py` (Python) applies, but the project's own gates are
the real signal:
- `python -m script.hassfest` — catches manifest/config errors.
- `ruff check` + `mypy` scoped to a component.
- Grep for deprecation shims / TODOs inside a single component before
  touching it.
- Per-integration `quality_scale.yaml` rules that are still `todo` are a
  legitimate, low-risk candidate source (see recent merged PRs flipping
  quality-scale rules to `done`).

## PR conventions

- Title: plain imperative sentence, integration name up front — matches the
  merged corpus (e.g. "Add diagnostics to nobo_hub", "Bump PyViCare to
  2.61.0", "Fix restoring the location of Traccar device trackers"). NOT
  strict conventional-commit `fix(scope):` — HA's merged titles are prose.
- Body: fill the upstream `PULL_REQUEST_TEMPLATE.md` **honestly** — keep all
  sections, tick exactly one "Type of change", link the issue under
  Additional information. No mermaid diagrams (none in the merged corpus).
- Squash-merged by maintainers.

## Maintainer priorities

- Correctness and per-integration ownership. Code owners review their own
  domain; changes to a domain you don't own need the owner's review.
- Small, single-purpose PRs. Dependency bumps, targeted bug fixes,
  diagnostics/reconfigure additions, and quality-scale rule completion are
  the bread-and-butter merges.

## Benchmark snapshot (2026-07-15)

From the last ~30 merged PRs:
- **Mix:** dependency version bumps (~30%), per-integration bug fixes (~30%),
  small feature additions to existing integrations — diagnostics,
  reconfigure flows, repair issues (~25%), refactors/enums/quality-scale
  (~15%). Almost everything is scoped to ONE integration.
- **Diff envelope:** overwhelmingly small. Observed: `+1-1` to ~`+150`.
  Bumps are `+2-2`; typical feature/fix `+20` to `+150`. Large deletions
  are rare and maintainer-driven. Stay ≤ ~150 changed lines, one integration.
- **Body style:** the upstream template, filled honestly. No custom heavy
  templates.
- Salvage/revival PRs: not an established external pattern here; do not hunt
  salvages until we have a merge and understand closure culture.
- **Our record:** 0 opened, 0 merged, 0 closed (new account in this repo).

## Hot areas & top contributors (2026-07-15)

Top merged-PR authors (last ~60 merged): `epenet` (20 — maintainer/prolific,
cross-integration enum & refactor work), `oyvindwe` (5 — nobo_hub owner),
`tr4nt0r` (4), `zweckj`, `joostlek`, `erwindouna`, `bkobus-bbx`, `balloob`
(co-founder/maintainer), `amitkio`, `abmantis`.
- **Maintainers/core:** balloob, epenet, joostlek, agners, abmantis.
- **Externals to imitate:** oyvindwe, tr4nt0r, bkobus-bbx, amitkio — each
  works within a single integration they know, small focused PRs.
- Hot mechanic right now: `EntityStateAttribute` enum migration across
  integrations (epenet) and per-integration quality-scale rule completion.

## Review culture

- High volume, fast maintainer turnover on small correct PRs; larger or
  cross-cutting PRs sit longer. Code-owner review is the gate for a domain.
- CI is heavy and authoritative (hassfest, ruff, mypy, pytest matrix). A red
  CI PR is ignored. Green CI + owned domain + linked issue = realistic merge.
- `good first issue` label: **0 open** — HA does not funnel newcomers via
  that label. Newcomer path is a small fix in an integration whose code you
  can read, backed by an existing bug issue.

## Forbidden / low-value themes

- Mass mechanical cleanup (batch typo/lint/formatting across many files) —
  guaranteed rejection.
- New integrations or new features as an unknown newcomer — high bar,
  requires discussion-first and docs PR; not a merge-rate play yet.
- Any PR before the CLA is signed.
- Touching an integration you cannot build/test locally without a real
  reproduction.

## Strategy

1. **BLOCKED until CLA signed.** Recon complete; open ZERO PRs today.
   Escalate to the user: sign the Home Assistant CLA once (it is posted by
   the CLA bot on the first PR, or can be pre-signed via the bot) for account
   `wesleysimplicio`. Record the date here once done.
2. After CLA: newcomer gate (`NEWCOMER_DAILY_PR_CAP=2`,
   `NEWCOMER_MAX_OPEN_UNREVIEWED=3`) until first merge. Given HA's scale and
   review latency, run a **conservative healthy default of 1–2 PRs/day**.
3. Candidate sources, ranked: (a) small bug fix in an integration with an
   open issue and a clear reproduction; (b) quality-scale `todo` rule
   completion in a single integration; (c) safe dependency bump where a
   newer release fixes a referenced issue. Avoid cross-integration refactors
   (that is maintainer territory — epenet).
4. Always scope build/test/lint to the single touched integration; never run
   or claim the full suite.

## Tunables (overrides)

```
DAILY_PR_HEALTHY=2          # HA review latency + newcomer status → stay low
NEWCOMER_DAILY_PR_CAP=2
NEWCOMER_MAX_OPEN_UNREVIEWED=3
STALE_CLOSE_DAYS=0          # never auto-close our own PRs here
DIFF_LINES_TARGET=150       # matches the observed merged envelope
```

## Project lessons (append-only)

- (2026-07-15) Default branch is `dev`, not `main` — PRs to `main` are
  auto-rejected.
- (2026-07-15) CLA bot gate is a hard newcomer blocker; signing is a
  one-time human action and must happen before any PR.
- (2026-07-15) HA merged-PR titles are plain prose with the integration
  name, not `fix(scope):` conventional commits — imitate the corpus.
