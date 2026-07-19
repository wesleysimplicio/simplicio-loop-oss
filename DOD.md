# DOD.md — Definition of Done, 4 layers

This repo already had a quality gate (`scripts/prototype_gate.py` +
`tests/test_prototype_gate.py`, issue #11) that stops a candidate from
becoming a real upstream PR unless it survives dedup, a captured reproducer,
worktree isolation, an independent judge, and a single delivery owner. This
document extends that gate with an explicit 4-layer Definition of Done, per
the ecosystem-wide rollout tracked in
[simplicio-loop#579](https://github.com/wesleysimplicio/simplicio-loop/issues/579)
and scoped to this repo in
[simplicio-loop-oss#14](https://github.com/wesleysimplicio/simplicio-loop-oss/issues/14).

## Why this matters even in a "loop that contributes to *other people's*
## repos"

It is tempting to think a correction-discipline framework like this one is
mostly relevant to a project's own core logic, and that a loop whose job is
to open small PRs against third-party repos is lower-stakes by comparison.
Two real bugs from this working session say otherwise — both happened in
tooling this exact loop depends on (`simplicio-dev-cli`'s deterministic
editor / `simplicio-mapper`'s parsing layer), and both would have shipped
silently past every check that existed before this pass:

1. **Silent corruption in a multi-file edit plan.** A deterministic
   multi-file edit applied a plan across several files; one file in the
   plan was corrupted (wrong content written) while every existing test
   stayed green, because nothing in the test suite asserted on the final
   *content* of every file the plan touched — only that the apply step
   "completed without raising". A PR built on top of a corrupting editor
   looks identical, in CI, to a PR built on a correct one, right up until
   a human (or the upstream maintainer) reads the diff.
2. **Wrong line picked because a regex swallowed a blank line.** A
   line-selection regex, used to find where to apply an edit, silently
   consumed an adjacent blank line as part of its match. The existing test
   only checked that the tool exited 0 (`returncode == 0`) — it never
   asserted on which exact line, or what exact text, was selected. The bug
   shipped for a while because "ran without error" and "did the right
   thing" are different claims, and only the first one was tested.

Both bugs share the same shape: a test that proves the code path executed,
not that it produced the *correct observable result*. This loop's whole
value proposition is "small, test-backed PRs" (PLAYBOOK.md rule 4:
"Mandatory test on bug fixes. No fail-before/pass-after test → no PR.") —
but a fail-before/pass-after test that only checks "it ran" is exactly the
shape that would have hidden both bugs above. A contribution loop that
opens PRs against other people's repos does not get to be less careful
about this than a project maintaining its own core: an upstream maintainer
trusts the diff *and* the tests that came with it; a test that only proves
"didn't crash" is a false signal of safety passed on to someone else's
codebase. `scripts/prototype_gate.py`'s new `require_observable_assertion`
gate (layer 3 below) is the direct, mechanical answer to both bugs: it
blocks promotion of any candidate that touches production code without an
added test assertion pinned to a concrete expected value.

## Layer 1 — Universal (every candidate, every language this loop touches)

Applies regardless of the target upstream repo's stack, because it is
enforced by this loop's own tooling, not the target's:

- **Reproducer before patch** (`require_reproducer`): a bug candidate needs
  a captured red command result or documented equivalent evidence; a
  feature candidate needs a design/schema spike. No patch candidate exists
  before this passes.
- **Isolation** (`PrototypeWorktree.create`): every candidate lives in its
  own `git worktree` on a private branch — never the target's default
  branch.
- **Double dedup** (`DuplicateIndex`): checked before AND after
  prototyping, against the local candidate ledger, in addition to
  PLAYBOOK.md Phase 4's real `gh search` dedup against the upstream repo.
- **Zero GitHub-facing mutation during prototyping** (`ReadOnlyGuard`): a
  candidate cannot `open_pr`/`add_comment`/`ping_maintainer` until it has
  passed every earlier gate.
- **Independent judge, single delivery owner** (`judge_candidate`,
  `DeliveryHandoff`): the judge cannot be the candidate's own creator; only
  a genuine `ACCEPT` verdict, delivered by the one named owner, can reach
  `GitHubEffects.open_pr`.

## Layer 2 — Risk-scaled (bigger surface, bigger blast radius, more gate)

This loop's own risk-scaling rules, read from PROFILE.md and PLAYBOOK.md,
rather than a fixed checklist:

- **Diff-size envelope**: reconsider any candidate above ~250 changed
  lines (PLAYBOOK.md "Operating principles" #2) — the bigger the diff, the
  harder it is for a human reviewer (ours or upstream's) to catch a
  content-level bug like the two above by inspection alone, so the
  observable-assertion requirement in layer 3 matters *more*, not less, as
  size grows.
- **Shared/public surface**: a candidate touching a shared/public file
  gets `impact_audit.py`; a change spanning frontend+backend gets
  `flow_audit.py --fail-on high` (PLAYBOOK.md Phase 5 step 2). Both are
  risk multipliers this loop already scales gate strength against.
- **CLA/DCO/issue-first prerequisites** (`load_prototype_policy`): a CLA
  requirement that is not yet signed is a hard stop, not a soft warning —
  the highest-risk category (legal exposure) gets the strictest gate.
- **Newcomer reputation gate**: a project with zero merged PRs from this
  account gets stricter daily caps (`NEWCOMER_DAILY_PR_CAP`,
  `NEWCOMER_MAX_OPEN_UNREVIEWED`) — less trust budget until a track record
  exists.

## Layer 3 — Quality of the test (the new gate this session adds)

The layer the two motivating bugs exposed as missing: passing a test is
not the same claim as the test having asserted something meaningful about
the result. `scripts/prototype_gate.py::require_observable_assertion`
implements this mechanically:

- Parses the candidate's unified diff (`git diff` inside the worktree, or
  any equivalent diff text) into per-file added lines — dependency-free,
  matching this repo's existing no-third-party-libs convention.
- Classifies files as **test** (common conventions across Python, JS/TS,
  Go, Rust, Ruby — `tests/`, `test_*`, `*_test.*`, `*.test.*`, `*.spec.*`,
  `spec/`), **doc-only** (`.md`/`.rst`/`.txt`/`LICENSE`/`CHANGELOG`/...,
  which never need a test), or **production code** (everything else).
- If the diff touches production code and adds no test file at all →
  `InsufficientTestAssertionError` (PLAYBOOK.md rule 4 already required a
  test to exist; this makes "no test file was even touched" mechanically
  unrepresentable as a passing candidate).
- If the diff touches production code and the added test lines contain
  **only** a weak assertion shape — `assert True`, `assertTrue(True)`,
  `returncode == 0`, `exit_code == 0`, a bare Jest `toBeTruthy()` — that is
  exactly the shape that let both motivating bugs through, so it does not
  count. The gate requires at least one added line matching a *meaningful*
  assertion pinned to a concrete expected value: `assertEqual(x, expected)`,
  `assert x == expected`, `assertIn(...)`, Jest's `toBe`/`toEqual`/
  `toContain`/`toMatch`, and equivalents.
- A pure test-only or doc-only diff has nothing to require and passes
  trivially — the gate only fires once behavior actually changed.
- Wired as an optional `diff_text` parameter on
  `run_prototype_stage` (defaults to `None` for backward compatibility with
  existing callers/tests that check the diff elsewhere in the loop); when
  provided, it runs right after the post-prototype dedup check and before
  the candidate ever reaches the independent judge — a candidate whose
  only coverage proves "it ran" never gets a verdict.
- Covered by `tests/test_prototype_gate.py`'s `TestRequireObservableAssertion`
  and `TestRunPrototypeStageObservableAssertion` classes, including the
  exact regression shapes of both motivating bugs (a returncode-only test
  for the swallowed-blank-line bug; a bare-truthy test for the
  silent-corruption bug) and their corrected, passing counterparts.

## Layer 4 — Ecosystem (cross-repo consistency, tracked centrally)

- This file exists because of the ecosystem-wide DoD rollout tracked at
  [simplicio-loop#579](https://github.com/wesleysimplicio/simplicio-loop/issues/579)
  (hub) and
  [simplicio-loop-oss#14](https://github.com/wesleysimplicio/simplicio-loop-oss/issues/14)
  (this repo's instance).
- Deeper hardening deliberately deferred to a follow-up issue, not bundled
  into this pass: property-based testing (Hypothesis) over the
  diff-parsing and policy-parsing logic in `scripts/`, running the gate
  against a real third-party repository/fixture instead of only synthetic
  diffs, and mutation testing on `prototype_gate.py` itself (it is the
  module that certifies everything else, so its own correctness needs an
  adversarial check beyond "the tests I wrote pass"). See the issue filed
  alongside this document for the concrete plan.
- Out of scope here, same as it was for issue #11: the full multi-machine
  E2E, a general CLA/DCO enforcement engine, and the merge-rate/
  newcomer-cap policy engine — those remain policy text in PLAYBOOK.md/
  SKILL.md, read by the loop operator, not re-implemented as code by this
  gate.
