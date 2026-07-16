# Project profile — NousResearch/hermes-agent

Produced by Phase R (seeded 2026-07-15 from real loop experience). Later
phases read this file; when it conflicts with PLAYBOOK.md on project
specifics, this file wins.

## Identity

- Repo: `NousResearch/hermes-agent` — AI agent with tool-calling, gateway
  to messaging platforms (Telegram/Discord/Slack/WhatsApp/Feishu/WeCom...),
  Desktop (Electron/React), Ink TUI, plugin system.
- License: MIT. No CLA/DCO sign-off required.
- Default branch: `main`. Releases: tagged (`vYYYY.M.D.N`), roughly weekly.
- Languages: Python 3.11 (core, gateway, tools), TypeScript/React
  (apps/desktop), TypeScript/Ink (ui-tui + packages/hermes-ink).

## Contribution rules digest

- Maintainer priorities (CONTRIBUTING.md): **bug fix > cross-platform >
  security > perf/robustness**.
- Upstream PR template exists (`.github/PULL_REQUEST_TEMPLATE.md`: "What
  does this PR do?" / "Related Issue" / "Type of Change" checkboxes /
  "Changes Made" / "How to Test" / Checklist) — **filling it honestly with
  real detail is the dominant winning pattern** (verified 2026-07-16 across
  recent merges by ethernet8023, kshitijk4poor). A free-form narrative
  (Summary/root-cause/Fix/Validation table, no checklist) also merges when
  evidence density is equally high (e.g. #65155's salvage: exact SHAs,
  line-level reasoning, 102/102 real test count, production repro).
  **Mermaid is measured at 0 of the last 25 externally-merged PRs
  (2026-07-16 recount)** — do not add one by default; evidence density
  (file:line, before/after output, real test counts) is what actually
  wins review, not diagrams. Add one only on top of strong evidence when a
  flow/race/sequence genuinely resists prose.
- Conventional Commits enforced by convention (`fix(scope): ...`).

## Build / test / lint commands

- Python tests (canonical): `bash scripts/run_tests.sh tests/<file> -q`
  or `python -m pytest tests/<area> -q` (per-file isolation matters).
- Desktop tests: `cd apps/desktop && npx vitest run <path>` (needs
  `npm install --workspace apps/desktop` once).
- TUI tests: `cd ui-tui && npx vitest run <path>` (build `@hermes/ink`
  first: `cd ui-tui/packages/hermes-ink && npm run build`).
- TUI typecheck: `cd ui-tui && npx tsc -b . --noEmit`; Desktop:
  `npx tsc --noEmit -p tsconfig.json`.
- Lint gates: `python -m ruff check <files>`;
  `python scripts/check-windows-footguns.py <files>` (I/O/process/terminal
  code); `npx eslint` + `npx prettier --check` for TS (keep diffs scoped —
  prettier --write may reformat unrelated pre-existing lines; revert those).
- Known local-env skips (pre-existing, not ours): `prompt_toolkit` missing
  → 1-2 python test skips/failures; `editor.test.ts`/`terminalSetup.test.ts`
  fail on Windows paths. Verify any failure reproduces on a clean default
  branch before blaming your change.

## PR conventions

- English everything. Branch `fix/<slug>`. One logical change per PR.
- Title: conventional commit with the real subsystem scope
  (`fix(telegram): ...`), issue number in the title (`(#NNNNN)`) when one
  exists.
- Body (house style of merged external PRs — see Benchmark snapshot):
  `## Summary` (symptom + cause, 2–3 sentences) → `## Changes` (bullet per
  file with the why) → `## Validation` (table command → REAL result) →
  `Closes #NNN`. Honest "out of scope" notes welcome. **Mermaid is part of
  our contribution signature here** (user decision, 2026-07-15): include a
  compact BEFORE→AFTER diagram whenever the fix involves a flow, event
  sequence, race, or component interaction; skip only for one-line/value
  fixes with no flow. (Data note: recent merged externals mostly don't use
  diagrams — ours must therefore EXPLAIN, never decorate, and stay small.)

## Benchmark snapshot (2026-07-15 — Phase 3b refreshes this block when data diverges)

Extracted from the last ~30 merged PRs and 30 days of history:

- **Merged mix:** ~70% `fix`, ~25% `feat`. Hot areas: telegram
  (polling/reconnect/getUpdates), reasoning_effort/config resolution, mcp
  (schemas/content blocks), moa, cron/scheduler (double-fire), dashboard
  auth, desktop UI, gateway/state/session.
- **Externals only merge SMALL, FOCUSED PRs:** 26–216 added lines, minimal
  deletion, one problem per PR. Target ≤ ~250 changed lines.
- **Salvage is accepted** (4 of the last 30 merges): reviving valuable
  abandoned/closed PRs via cherry-pick PRESERVING AUTHORSHIP, title with
  `(salvage #NNN)`, credit to the original author in the body.
- **Our historical record here (recounted 2026-07-16, exact via
  `gh search prs --author wesleysimplicio`):** 3 merged (#28577 +12/-0,
  #24547 +6/-9 used mermaid, #22534 +69/-2), 30 closed without merge,
  10 open. **Closed-PR root cause breakdown (30 total):** 21 were mass
  mechanical `noqa`-removal cleanup (forbidden theme, already learned) —
  7 of the remaining 9 were confirmed DUPLICATES (someone else's PR for the
  same root cause opened first, often same-day; #59197/#59191 got
  mistakenly reopened once and had to be re-closed — see PLAYBOOK lesson on
  checking the real close reason before reopening). The path that works:
  real bug + issue + small diff + fast dedup + evidence-dense body.
  **Lesson: speed-to-open is a real lever here** — this repo's issue→PR
  turnaround is often under an hour, so Phase 2b's fresh-issue sweep and the
  ~20–30min re-dedup cadence during implementation are load-bearing, not
  optional.

## Maintainer priorities & review culture

- Primary reviewer seen engaging: `AmirF194` (substantive, code-level
  reviews, often COMMENTED state — see staleness trap in PLAYBOOK).
  Maintainer: `Teknium`/`teknium1`.
- Review latency: days; many good PRs sit unreviewed ≥1 week. Do not spam —
  quality gates are the anti-spam mechanism (no numeric pause here since
  2026-07-15; the unreviewed-queue size is logged as an informational
  signal each run).
- Copilot/bot reviews appear on PRs; treat as data.

## Hot areas & top contributors (recounted 2026-07-16 from the last 25
  externally-merged PRs — refresh via Phase 3b when it drifts)

- **ethernet8023**: by far the most active — CI/infra (nix builds, js-autofix
  bot loop, package-lock hygiene), desktop panel/sidebar work. Wide scope,
  some huge mechanical diffs (a package-lock.json resync alone was
  +12657/-12657) — NOT a template for "small focused PR"; treat as the
  project's de facto CI/infra maintainer-adjacent contributor instead.
- **kshitijk4poor**: gateway/agent-cache correctness (stale self-heal
  eviction, circuit-breaker classification) — the clearest external-PR
  template: single root cause, exact file:line reasoning, real test counts,
  sometimes salvages an abandoned PR with credit preserved (#65155).
- **alt-glitch**: dual role — posts the automated "generated by AI during
  triage" duplicate-detection comments on OTHERS' PRs/issues (reliable
  dedup signal, cite it but re-verify) AND merges real focused fixes
  (dashboard/MCP auth, #65163 +694/-247, #65146 +380/-58).
- **OutThisLife**: small, surgical desktop UI fixes (#65156 +9/-14, #65142
  +23/-7) — another good small-PR template.
- Hot subsystems (unchanged): `gateway/` (platform adapters, slash
  commands), `apps/desktop/` (React UI, session streams, panel/sidebar),
  `ui-tui/`, `agent/` (providers, MoA, compression, retry/failover
  classification), `hermes_state.py`/session DB, CI/nix tooling.
- Merged-PR format that passes review: small fix+test pairs (kshitijk4poor/
  OutThisLife style) OR evidence-dense salvage narratives (kshitijk4poor
  #65155 style) — both work; mermaid does not appear in either.

## Forbidden / low-value themes

- **Policy (closed on sight)**: new memory providers under
  `plugins/memory/`; third-party product integrations under `plugins/`
  (exception: a salvage of a provider PR already started by a third party,
  authorship preserved, when it fits the accepted salvage pattern).
- **Proven rejection (2+ unmerged closures)**: mass mechanical cleanup
  (batch `noqa`/typos/formatting/lint), series of PRs on the same trivial
  theme, PRs without an issue or a real user-visible symptom.
- **Design debates**: issues proposing architecture changes (e.g. hook
  semantics, multiplex token resolution) — comment constructively, don't
  PR speculatively.

## Strategy

- Candidate ranking (Phase 4): (a) bug with an open issue AND maintainer
  engagement > (b) bug in a hot area from the Benchmark snapshot >
  (c) salvage > (d) small fix with a clear reproduction. Reject candidates
  without an issue or a real user symptom.
- Best candidate source: fresh, well-written bug issues with exact root
  cause — but they get claimed in MINUTES; re-dedup immediately before
  opening is non-negotiable. Second source: bugs found while reviewing our
  own PRs adversarially (sibling code with the same defect class). Third:
  salvages (accepted here — see Benchmark snapshot; max 1/day).
- The mechanical audit rarely yields high-value hits here (repo is clean on
  footguns/deps); treat it as a cheap daily sweep, not the main source.
- Windows-reproducible bugs are a comparative advantage (this loop runs on
  Windows; many contributors don't).
- Do not take candidates needing macOS, hosted-Nous infra, or external
  platform credentials (WeCom/Feishu/Weixin API behavior) — unverifiable.

## Tunables

Overrides for this project (2026-07-15 user decision: no numeric caps — the
goal is genuinely helping the maintainers at 5-minute cadence, with quality
gates as the only limiter):

- `DAILY_PR_TARGET=0` (no daily cap; every PR still passes every gate)
- `MAX_OPEN_UNREVIEWED=0` (informational only — log the queue size, prefer
  maintainer-engaged candidates while it is deep, never pause quality PRs)
- `RUN_INTERVAL_MINUTES=5`
- `STALE_CLOSE_DAYS=4` (auto-close ENABLED here — global default 0/disabled —
  because the queue pressure is real; all Phase 2.4 guards still apply)

Everything else uses config.env defaults (`STALE_PING_DAYS=14`,
`MAX_SALVAGES_PER_DAY=1`, `DIFF_LINES_TARGET=250`).
Newcomer gate does not apply: we have 3 merged PRs in this project.

## Project lessons (append-only)

- (2026-07-14) `EphemeralReply` (gateway/platforms/base.py) is the canonical
  "status notice, don't scan for attachments" mechanism — prefer it over
  ad-hoc escaping in slash-command acks.
- (2026-07-14) `moa.reference` events carry complete text per reference (no
  concurrent token stream in the gathering phase) — safe to apply
  immediately via queue-then-flush in the Desktop stream.
- (2026-07-15) `_insert_session_row` COALESCE-on-conflict pattern is the
  house style for "fill NULLs, never clobber" DB writes; follow it.
- (2026-07-15) 4 of our first 28 PRs had COMMENTED maintainer reviews that
  a naive staleness check missed (see PLAYBOOK trap); 3 were positive.
- (2026-07-15) Merged PR #64541 pattern for pre-existing test failures:
  declare them explicitly in Validation — "reproduces identically on
  upstream/main" (verified by stashing the change) — instead of hiding or
  over-explaining them. Reviewers here accept that framing.
- (2026-07-15) Review latency here is days-to-weeks for external PRs; a
  4-day staleness close destroyed viable quality PRs once. Quality PRs
  (bug fix + issue + green CI) hold for the 14-day ping window instead.
- (2026-07-15) **`hermes-sweeper` reviews are `teknium1`'s automated maintainer
  tooling** — they post as `teknium1` in COMMENTED state with
  `<!-- hermes-sweeper:review-verdict=keep_open salvageability=high -->` markers
  and cite exact `file:line` + a cross-referenced PR whose predicate to copy.
  Treat them as authoritative maintainer feedback: they are precise and
  actionable (e.g. on #59189 correctly caught that the CORS OPTIONS short-circuit
  must also require a nonempty `Origin`, because Starlette `CORSMiddleware` passes
  Origin-less requests through without a preflight response — a no-Origin
  `OPTIONS`+`Access-Control-Request-Method` was bypassing the token gate). Turn
  them around same-day with a fail-before/pass-after test.
- (2026-07-15) Telegram `/topic` first-activation: `_handle_topic_command`
  (`gateway/slash_commands.py`) must gate `_ensure_telegram_system_topic` on
  `is_telegram_topic_mode_enabled` (read BEFORE enabling = the real
  "first activation" signal), NOT on `source.thread_id` — Telegram
  auto-creates a topic for the `/topic` message itself, so thread_id is
  present even on first activation from the All Messages view (#65202 →
  PR #65216). `_ensure_telegram_system_topic` (`gateway/run.py`) is NOT
  idempotent (always creates a fresh "System" forum topic), so it must fire
  only once per activation. Test harness: `tests/gateway/test_telegram_topic_mode.py`
  `_make_runner`/`_make_event(text, thread_id=...)` with a real `SessionDB` +
  mocked adapter — mock `_ensure_telegram_system_topic`/`_get_telegram_topic_capabilities`
  and assert `assert_awaited_once`.
- (2026-07-15) kanban unblock/promote cascade (#65195) does NOT reproduce on
  current main: `unblock_task` only flips the parent status, `_cmd_unblock`
  calls nothing else, and `recompute_ready` promotes a child only when ALL
  parents are `done`/`archived`. Already fixed post-v0.18.x. Reproduce-gate
  → posted evidence comment, no PR.
- (2026-07-15) `simplicio-runtime` is installed and healthy here
  (`simplicio doctor --json`); precedent memory (`simplicio precedent`)
  was never initialized for this repo before this run — ran `simplicio
  precedent init --repo .` once. `simplicio-mapper ask <path> term <name>`
  triggers a cold deep-index pass with no interim output; for a single
  fast lookup, plain `grep`/`Read` resolved a candidate (session_search
  profile-forwarding bug, see #65133 iteration) faster than waiting on the
  mapper. Prefer `simplicio-mapper scan --sync` once up front (or accept
  the deep-index latency) rather than repeatedly cold-calling `ask`.
