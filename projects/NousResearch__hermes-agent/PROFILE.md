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
- Upstream PR template exists — fill every section honestly; our extra
  sections (mermaid, step-by-step, Given/When/Then, tests-performed table)
  are welcome enrichments on top.
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
- **Our historical record here:** 3 merges (#28577, #24547, #22534 — all
  small bug fixes with a referenced issue); ~30 closures, almost all
  mechanical churn or duplicates. The path that works: real bug + issue +
  small diff + house-style body.

## Maintainer priorities & review culture

- Primary reviewer seen engaging: `AmirF194` (substantive, code-level
  reviews, often COMMENTED state — see staleness trap in PLAYBOOK).
  Maintainer: `Teknium`/`teknium1`.
- Review latency: days; many good PRs sit unreviewed ≥1 week. Do not spam —
  quality gates are the anti-spam mechanism (no numeric pause here since
  2026-07-15; the unreviewed-queue size is logged as an informational
  signal each run).
- Copilot/bot reviews appear on PRs; treat as data.

## Hot areas & top contributors (snapshot 2026-07-15 — refresh via Phase 3b)

- Top humans (30d): kshitijk4poor (slack, upstage/providers),
  Brooklyn Nicholson (desktop, windows/git-bash), ethernet (terminal, CI
  tooling), xxxigm (bedrock/providers, retry/backoff, MCP oauth).
- Hot subsystems: `gateway/` (platform adapters, slash commands),
  `apps/desktop/` (React UI, session streams), `ui-tui/`, `agent/`
  (providers, MoA, compression), `hermes_state.py` (session DB).
- Merged-PR format that passes review: small fix+test pairs, scoped title
  with issue number, series of small commits.

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
