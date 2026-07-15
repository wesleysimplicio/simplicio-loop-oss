# PROFILE — vllm-project/vllm

## Identity
- Upstream: `vllm-project/vllm` (default branch `main`).
- Our login: `wesleysimplicio`; fork `wesleysimplicio/vllm`.
- Status (2026-07-15): **newcomer** — 0 PRs of ours (open/closed/merged). Newcomer gate applies.

## Contribution rules digest
- CONTRIBUTING.md points to https://docs.vllm.ai/en/latest/contributing.
- **DCO required** (repo has a `DCO` file; sign-off enforced). → commit with `git commit -s`. Ours to handle; no human action.
- **No CLA** — DCO only. No human-blocking prerequisite.
- PR template (`.github/PULL_REQUEST_TEMPLATE.md`): `## Purpose` → `## Test Plan` → `## Test Result`, plus an "Essential Elements" checklist. Fill honestly; text below the marker line is stripped by GH Actions.
- Issue-first is not strictly mandatory but real user-visible symptom / linked issue is expected; bug reports use structured issue templates.

## Build / test / lint commands
- Package: `pyproject.toml` + `setup.py` (CUDA/C++ ext build is heavy; not required for pure-Python fixes).
- Lint/format (pre-commit is the truth, `.pre-commit-config.yaml`):
  - `ruff check <files>` and `ruff format <files>` (Python)
  - `typos` (spelling), `markdownlint-cli2` (docs), `actionlint` (workflows), `clang-format` (C++/CUDA)
  - `pre-commit run --files <changed files>` runs the applicable subset.
- Tests: `pytest tests/<path>` — most tests are GPU-heavy / require model downloads. **Audit commands (Phase 3) = ruff/typos/actionlint + targeted pure-Python pytest**; do not claim GPU test results we cannot run.

## PR conventions
- **Title = bracketed-tag style**, NOT conventional commits. Observed merged tags: `[Bugfix]`, `[CI]`, `[Core]`, `[Model]`, `[LoRA]`, `[ROCm]`, `[XPU]`, `[Misc]`, `[Doc]`, often stacked (`[Bugfix][CI]`). Format: `[Tag] Short description`. Link issues in the Purpose section (`Fixes #NNN`).
- Body = the repo template (Purpose / Test Plan / Test Result). No mermaid diagrams (none of the sampled merged PRs use them).

## Maintainer priorities
- Core maintainers: Woosuk Kwon, Nick Hill, Michael Goin (mgoin), Harry Mellor, Jee Jee Li (jeejeelee). They merge their own work under different rules — imitate EXTERNALS.

## Benchmark snapshot (2026-07-15)
- Sampled last 30 merged PRs. Mix is heavily **[Bugfix] + [CI]**, plus [Model]/[LoRA]/[Core] feature enablement.
- **Diff-size envelope for merged externals**: very wide but the majority are small — many merged at +2/-0, +4/-1, +6/-4, +8/-0, +11/-3, +13/-1, +18/-18, +20/-2, +32/-2. Larger merges (+425, +631, +813) are from recognized contributors. **Newcomer target: stay ≤ ~50 changed lines, one problem per PR.**
- Body style of merged externals = the template's Purpose/Test Plan/Test Result, terse, with real commands.
- Salvage/revival PRs: not confirmed as an accepted pattern here — do NOT hunt salvages until observed.
- Our historical record here: none yet.

## Hot areas & top contributors (2026-07-15)
- Top human contributors 30d: Nick Hill, Wentao Ye (yewentao256), Bugen Zhao (BugenZhao), Andreas Karatzas, Harry Mellor, Ting SUN, Micah Williamson (micah-wil), Woosuk Kwon, Michael Goin, Jee Jee Li.
- Hot areas: ROCm/AMD CI, LoRA, MLA/KV-cache, quantization (fp8/head_dtype), FlashInfer/FlashAttention backends, MoE, model enablement.
- **Externals** getting merged (imitate): micah-wil, divakar-amd, jperezdealgaba, gangula-karthik, hnt2601, joerowell, gcanlin, KKothuri — small targeted bugfixes with a concrete symptom.

## Review culture
- Very fast-moving, high PR volume (PR numbers in the 48000s). Merges happen quickly for small, clearly-scoped, tested fixes. Unknown accounts opening many PRs read as spam → newcomer gate is essential.

## Forbidden / low-value themes
- Generic forbidden classes apply: mass mechanical cleanup (batch noqa/typos/format/lint), trivial-theme series, PRs with no issue/no symptom.
- Avoid GPU-behavior "fixes" we cannot reproduce or test here — vLLM CI requires GPUs and model downloads. Prefer pure-Python, CPU-verifiable bugs (arg parsing, validation, error messages, docs correctness with a real defect, type/logic bugs readable from source).

## Strategy
- Newcomer gate: `NEWCOMER_DAILY_PR_CAP=2`, `NEWCOMER_MAX_OPEN_UNREVIEWED=3` until first merge.
- Realistic path: one small, CPU-verifiable bugfix with a linked issue and a genuine fail-before/pass-after test using a non-GPU pytest. No speculative GPU fixes.
- Candidate sources ranked: (1) open [Bug] issues with a pure-Python reproduction; (2) readable logic/validation bugs; (3) doc defects tied to a real code mismatch. Refactor/RFC "good first issues" are heavy — deprioritize.

## Tunables
- Inherit config.env. Newcomer caps in force (0 merges). `STALE_CLOSE_DAYS=0` (never auto-close our own PRs here).

## Project lessons
- (2026-07-15) vLLM is DCO-only (no CLA) — no human blocker; always `git commit -s`.
- (2026-07-15) Title convention is bracket-tags (`[Bugfix]`), not conventional commits — do not impose `fix(scope):` here.
- (2026-07-15) Most tests need GPUs/model weights. Only take candidates with a CPU-runnable fail-before/pass-after test; never fabricate GPU results.
