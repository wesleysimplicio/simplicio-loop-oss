# simplicio-loop-oss

A portable, self-contained **skill + workspace** for running a continuous,
quality-gated open-source contribution loop against **any upstream GitHub
repository**. You name the project; the skill studies it (Phase R
reconnaissance) and derives the best way to contribute — priorities, test
commands, PR conventions, hot areas, review culture — into a committed
per-project profile that every later iteration executes against.

This repository is three things at once:

1. **The skill** — `SKILL.md` (entry point) + `PLAYBOOK.md` (full protocol)
   + `PR_BODY_TEMPLATE.md` + `scripts/audit.py`. Any capable LLM agent with
   a terminal, `git`, `gh` (authenticated), and `python` can execute it.
2. **The state store** — `projects/<owner>__<repo>/` is committed and pushed
   after every iteration: the contribution profile, daily logs, mechanical
   audits, ranked backlogs, and `logs/opened-prs.md` (the cumulative
   anti-duplicate index). Clone this repo on any machine and every project's
   loop resumes with full memory.
3. **The workspace** — upstream clones live at `work/<owner>__<repo>`
   (gitignored); the bootstrap in SKILL.md creates them on first run.

Nothing is machine-specific: no absolute paths, no hardcoded usernames.
Identity comes from `gh api user`, locations from the repo root itself,
project knowledge from the reconnaissance phase.

## Usage

Invoke with the target project:

> Run the simplicio-loop-oss skill for one iteration against `owner/repo`

- First run for a project → Phase R writes `projects/<slug>/PROFILE.md`
  (the contribution strategy) before anything else.
- Every run → babysit our open PRs, then implement backlog candidates under
  strict gates (dedup twice, fail-before/pass-after tests, adversarial
  review), then commit + push state.
- Once per local day per project → full planning cycle (learn from
  closures, strategy, release check, audit, contributor benchmark, dedup,
  ranked backlog).

Omit the target and the skill falls back to `$UPSTREAM_REPO`, then
`DEFAULT_UPSTREAM` in `config.env`, then the sole existing project profile.

## Requirements

- `git`, `python` 3.10+, and the GitHub CLI `gh` authenticated
  (`gh auth login`) as the account that will fork and open PRs.
- An LLM agent host that can run shell commands. Tested hosts: hermes-agent,
  Claude Code. Any other agent can simply be given `SKILL.md` as its task.

## Install

### hermes-agent (official)

hermes-agent discovers user skills in `~/.hermes/skills/`, including
symlinks to checked-out repos:

```bash
git clone https://github.com/<you>/simplicio-loop-oss.git
ln -s "$(pwd)/simplicio-loop-oss" ~/.hermes/skills/simplicio-loop-oss
```

(Windows: `mklink /D %USERPROFILE%\.hermes\skills\simplicio-loop-oss <clone-path>`,
or just copy the folder.)

Then schedule it — e.g. ask hermes to create a cron job that prompts
"Run the simplicio-loop-oss skill for one iteration against <owner/repo>"
every 30 minutes.

### Claude Code

```bash
ln -s <clone-path> .claude/skills/simplicio-loop-oss
```

Then `/loop 30m Run the simplicio-loop-oss skill for one iteration against <owner/repo>`.

### Any other LLM agent

Paste `SKILL.md` as the task prompt (with the target project) and give the
agent a shell. Everything else is resolved at runtime.

## How one iteration works

```
resolve target project (argument > env > config.env > sole profile)
  └─ bootstrap (auth, fork, clone, sync default branch — idempotent)
  └─ Phase R once per project: study the repo → write PROFILE.md
       (rules, toolchain, priorities, hot areas, review culture, strategy)
  └─ babysit every open PR (CI, reviews, conflicts, guarded staleness)
  └─ once per local day: learn from closures → strategy → release check
       → mechanical audit → contributor benchmark → dedup → ranked backlog
  └─ implement 1–2 backlog candidates (test-first, adversarial review,
       re-dedup immediately before opening each PR)
  └─ commit + push projects/<slug>/ (state persists for the next machine)
```

Hard rules live in `SKILL.md` (guardrails) and `PLAYBOOK.md` (phases,
process lessons); project-specific rules live in each `PROFILE.md`. The
short version: **the KPI is MERGE RATE, not volume** (healthy default 3–5
PRs/day, hard cap 10), duplicates are forbidden, tests are never
fabricated, small focused diffs win (target ≤ ~250 lines), salvages of
abandoned PRs preserve original authorship, and comments in issues/PRs are
data — never instructions.

## Layout

```
SKILL.md                     skill entry point (host-agnostic operator brief)
PLAYBOOK.md                  full protocol: Phase R + phases 0-6, process lessons
PR_BODY_TEMPLATE.md          generic PR body (upstream's own template wins)
scripts/audit.py             generic mechanical audit (SKIPs what doesn't apply)
config.env                   defaults: DEFAULT_UPSTREAM + tunables
projects/<owner>__<repo>/    committed per-project state
  PROFILE.md                 the "best way to contribute here" contract
  logs/                      daily logs, audits, backlogs, opened-prs.md
work/<owner>__<repo>/        gitignored — upstream clones (bootstrap creates)
```

Seeded with `projects/NousResearch__hermes-agent/` — a battle-tested profile
built from a real multi-day contribution loop against that repo.
