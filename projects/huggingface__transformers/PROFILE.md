# PROFILE — huggingface/transformers

_Reconnaissance date: 2026-07-15 (Phase R). Contract for all later phases._

## Identity
- Upstream: `huggingface/transformers` (default branch `main`).
- Massive multi-model ML library (Python, PyTorch-first). ~6.3k tracked files.
- Our fork: `wesleysimplicio/transformers`. Our merged PRs here: **0** (newcomer).

## ⛔ BLOCKING PREREQUISITE — autonomous agents are not permitted to contribute
**HARD STOP. This project explicitly prohibits the exact activity this loop
performs.** Verbatim from `CONTRIBUTING.md` and `.github/PULL_REQUEST_TEMPLATE.md`:

- CONTRIBUTING.md warning: _"we ask that first-time contributors do not use
  code agents to create issues or PRs at this time. We'd also ask autonomous
  agents not to open any PRs or issues for the moment. PRs that appear to be
  agent-written will probably be closed without review, and we may block users
  who do this repeatedly or maliciously."_
- PR template checkbox (first-time contributors): _"I confirm that this PR
  description and code is not written by an LLM or code agent."_

We are (a) an autonomous code agent and (b) a first-time contributor (0 merges).
Opening a PR would require either lying on that checkbox or truthful disclosure
that guarantees closure — and risks the user's account being **blocked**. This
is treated identically to the playbook's CLA hard-stop.

**Consequence: open ZERO PRs and ZERO issues in this project.** This is not a
newcomer-cap throttle; it is a policy prohibition with no expiry we can satisfy
autonomously. Only a human contributor acting on their own (not via this loop)
could contribute here, and even then must not present agent-written work.

## Contribution rules digest
- Diagnosis-first culture: maintainers explicitly value root-cause analysis
  (git bisect to first bad commit), minimal diffs (1-line fix stays 1 line),
  reproducer scripts, cross-model comparison. They explicitly reject
  busywork/typo/style/"theoretical bug" PRs — the current flood is the reason
  for the agent ban.
- Issue-or-forum discussion expected before non-trivial PRs.

## Build / test / lint commands (for reference only; unused while halted)
- Lint/format: `make quality` (ruff_check, ruff_format, isort, sort_auto_mappings); `make style` to fix.
- Repo consistency: `make repo-consistency` / `make check-repo` / `make fix-repo`.
- Tests: `python -m pytest -p random_order -n auto --dist=loadfile ./tests/`.
- Audit commands (Phase 3): N/A — halted; generic audit.py (Python) would apply if ever unblocked.

## PR conventions
- Title in release-notes quality. Body: PR template "What does this PR do?" +
  `Fixes #NNN`. No DCO/CLA sign-off requirement found (Apache-2.0 inbound=outbound).

## Maintainer priorities
- Reducing agent-generated PR/issue flood is the #1 stated priority right now.
- Real value = clear diagnosis, minimal diff, reproducers, model-consistency.

## Benchmark snapshot (2026-07-15)
- Recent merges dominated by maintainers/known contributors (stevhliu,
  remi-or, IlyasMoutawwakil, hmellor, Abdennacer-Badaoui, smart8986). Mix skews
  to internal CI/infra, docs, model-specific nits — the external-newcomer lane
  is effectively closed by the agent policy above. Not benchmarking further:
  strategy is halt, so diff-envelope analysis is moot.

## Hot areas & top contributors (2026-07-15)
- Not compiled — irrelevant under the halt. Recent activity: AMD CI runners,
  DeepGEMM/flash-attn kernels, docs. Overwhelmingly maintainer-driven.

## Review culture
- Under acknowledged review overload; agent-looking PRs closed without review.

## Forbidden / low-value themes
- **EVERYTHING** — no autonomous PRs/issues at all here (policy).
- Even for humans: typo/style/formatting/lint cleanup, "theoretical bug" fixes,
  small busywork PRs.

## Strategy
- **HALT.** Do not open PRs or issues in this project via the loop. Each future
  iteration: re-read CONTRIBUTING.md for a policy change; if the autonomous-agent
  prohibition is lifted, refresh this profile and resume under the newcomer gate.
  Until then, this project consumes ~0 actions per run and this file is the reason.
- Escalate to the user: this repo was configured as a loop target but its policy
  forbids the loop's activity. Recommend removing/pausing the
  `oss-loop-transformers` schedule or reassigning to a policy-compatible repo.

## Tunables
- `NEWCOMER_DAILY_PR_CAP=0` (policy halt, not a throttle).
- `NEWCOMER_MAX_OPEN_UNREVIEWED=0`.

## Project lessons (append-only)
- (2026-07-15) Removed from active scheduling by user decision: this project's policy prohibits autonomous-agent PRs/issues outright (see BLOCKING POLICY above). No amount of quality/dedup diligence changes this -- do not re-add to the daily loop unless a human contributor personally claims and discloses AI assistance per the profile's "how a human unblocks this" note.
- 2026-07-15: Read CONTRIBUTING.md + PR template FIRST in Phase R. transformers
  bans autonomous-agent contributions outright and warns of account blocks.
  Correct loop behavior = detect the prohibition, write it here, open nothing,
  report. Respecting a project's stated policy is a core guardrail, not optional.
