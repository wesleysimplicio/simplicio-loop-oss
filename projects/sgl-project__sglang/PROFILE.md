# PROFILE — sgl-project/sglang

## Identity
- Upstream: `sgl-project/sglang` — fast serving framework for LLMs and VLMs.
- Default branch: `main`. Slug: `sgl-project__sglang`. Fork: `wesleysimplicio/sglang`.
- Very high-velocity ML-infra repo (multiple merges/hour, heavily maintainer-driven).
- Languages: Python (core, `python/sglang/`), Rust (`sgl-model-gateway/`, `experimental/sgl-router/`), CUDA/C++ kernels (`sgl-kernel/`).

## Contribution rules digest
- `docs_new/CONTRIBUTING.md` covers **docs only** (Mintlify, `mint dev`). The real
  developer guide lives at docs.sglang.io/developer_guide/contribution_guide.html.
- **No CLA. No DCO/sign-off required** (no matches in .github or MAINTAINER.md — do
  NOT add `Signed-off-by`).
- **Heavy merge process** (`.github/MAINTAINER.md`, PR template): (1) ping Merge
  Oncalls, (2) get CODEOWNERS approvals, (3) CI is triggered by *authorized users
  only* via slash-commands (`/tag-and-rerun-ci`, `/rerun-failed-ci`), (4) merge by
  Write-permission holders. **We cannot self-trigger CI** → a newcomer PR sits until
  a maintainer engages. Plan for latency; do not ping-spam.
- Issue templates: bug-report, feature-request, playground-verified-cell.

## Build / test / lint commands
- Format (the gate that matters for newcomers): `pre-commit run --all-files` — hooks:
  `isort` (7.0.0), `ruff` (v0.15.1, `--select=F401,F821,UP037 --fix`), `black` (26.1.0),
  `codespell`, `clang-format`, trailing-whitespace/eof.
- Targeted format check without installing: run the individual tool on touched files
  (e.g. `ruff check --select F401,F821,UP037 <file>`, `black --check <file>`).
- Python package: `python/pyproject.toml`. Tests under `test/` (pytest). **Most
  runtime tests require a GPU/CUDA** — treat GPU-dependent tests as un-runnable here
  and pick candidates verifiable WITHOUT a GPU.

## Audit commands (Phase 3 — this is a mixed Python/Rust/C++ repo; audit.py only scans .py)
- `ruff check --select F401,F821,UP037 python/sglang/` — dead imports / undefined names.
- `codespell --config .codespellrc` — typos (but mass-typo PRs are FORBIDDEN, see below).
- `python -m py_compile` over changed pure-python modules for syntax sanity.
- `cargo clippy` in `sgl-model-gateway/` for Rust candidates.
- Prefer issue-driven candidates over mechanical scans in this repo.

## PR conventions
- Title style is mixed: both Conventional Commits (`feat(sgl-router): ...`,
  `fix(...)`, `docs:`, `ci:`) and bracket-tag style (`[AMD] ...`, `[PD] ...`,
  `[CI] ...`, `[misc] ...`) are merged. Match the subsystem's prevailing style.
- Body: fill the repo PR template honestly — `## Motivation` → `## Modifications`
  → `## Accuracy Tests` / `## Speed Tests` (only if outputs/perf affected; otherwise
  state N/A) → Checklist. Link the issue with `Closes #NNN` when one exists.

## Maintainer priorities
- Active hot areas (last 25 merged): ModelRunner refactors (fzyzcjy), KV-cache /
  attention backends, MoE/EP, diffusion models, sgl-router, AMD/ROCm, CI plumbing.
- Core maintainers: merrymercy (Lianmin Zheng), hnyls2002 (Liangsheng Yin),
  Cheng Wan, Mick/mickqian, fzyzcjy, Xiaoyu Zhang.

## Benchmark snapshot (2026-07-15)
- Merged mix (last 25): heavy feat/refactor from core (fzyzcjy ran a ~15-PR refactor
  chain 31154–31173), plus small external fixes.
- **Diff-size envelope for external/newcomer-viable PRs**: small & focused —
  e.g. #31199 `+1/-1` CI import path fix (mmangkad), #31234 `+14/-1` ci fix
  (alisonshao), #31258 `+8/-2` cookbook (1am9trash). Large diffs are maintainer
  refactors, not our lane. Target ≤ ~60 changed lines for a first merge.
- Salvage/revival PRs: not observed as an established pattern — do NOT salvage-hunt
  here until evidence appears.
- Our record: 0 opened / 0 merged (newcomer).

## Hot areas & top contributors (2026-07-15)
- 30-day top authors (git shortlog): Liangsheng Yin(81), Mick(64), Lianmin Zheng(55),
  Cheng Wan(55), Xiaoyu Zhang(50), fzyzcjy(40), Mohammad Miadh Angkad(39),
  Xinyuan Tong(33), Brayden Zhong(31), Michael(30). Nearly all MAINTAINERS/core.
- EXTERNAL-viable model PRs: CI/test import fixes, docs/cookbook, small correctness
  fixes tied to an open issue. Imitate those.

## Review culture
- Fast on maintainer PRs; external PRs gated behind oncall ping + CODEOWNERS +
  authorized CI trigger. Expect real latency for unknown accounts. One polite ping
  max after `STALE_PING_DAYS`.

## Forbidden / low-value themes
- Mass mechanical cleanup (batch typo/noqa/formatting/lint) — explicitly forbidden by
  the loop and low-return in fast repos.
- GPU-dependent bug "fixes" we cannot reproduce/verify locally (no GPU here) — post a
  technical comment with evidence instead of a speculative PR.
- Refactor PRs in areas core maintainers are actively churning (ModelRunner/KV-cache)
  — high conflict risk, not our lane.

## Strategy
- **Newcomer gate active** (0 merges): `NEWCOMER_DAILY_PR_CAP=2`,
  `NEWCOMER_MAX_OPEN_UNREVIEWED=3`.
- First merges should come from: (a) small correctness/CI/test-path fixes tied to an
  open issue and verifiable from reading code (no GPU), (b) docs/cookbook accuracy
  fixes. Keep diffs tiny (≤ ~60 lines).
- Because we cannot self-trigger CI and the merge process is heavy, favor QUALITY and
  patience over volume. Realistic healthy cadence here: 1 PR/day.
- Reviewing third-party PRs constructively is a valid reputation-builder.

## Tunables (overrides config.env)
- DAILY_PR_HEALTHY=1  (slow, gated review process)
- STALE_CLOSE_DAYS=0  (never auto-close our own PRs)
- MAX_SALVAGES_PER_DAY=0  (no established salvage pattern)

## Project lessons (append-only)
- (2026-07-15) Clone requires `git config core.longpaths true` on Windows — sglang
  ships triton config JSONs with very long filenames that break checkout otherwise.
- (2026-07-15) CI cannot be triggered by external contributors (authorized-users-only
  slash commands). A newcomer PR will show no CI until a maintainer engages — this is
  expected, not a failure to babysit.
