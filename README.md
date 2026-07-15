# hermes-contrib-loop

A portable, self-contained **skill + workspace** for running a continuous,
quality-gated open-source contribution loop against
[NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
(or any upstream — see `config.env`).

This repository is three things at once:

1. **The skill** — `SKILL.md` (entry point) + `PLAYBOOK.md` (full protocol)
   + `PR_BODY_TEMPLATE.md` + `scripts/audit.py`. Any capable LLM agent with
   a terminal, `git`, `gh` (authenticated), and `python` can execute it.
2. **The state store** — `logs/` is committed and pushed after every
   iteration: daily logs, mechanical audits, ranked backlogs, and
   `logs/opened-prs.md` (the cumulative anti-duplicate index). Clone this
   repo on any machine and the loop resumes with full memory.
3. **The workspace** — the upstream clone lives at `work/<repo-name>`
   (gitignored); the bootstrap in SKILL.md creates it on first run.

Nothing is machine-specific: no absolute paths, no hardcoded usernames.
Identity comes from `gh api user`, locations from the repo root itself.

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
git clone https://github.com/<you>/hermes-contrib-loop.git
ln -s "$(pwd)/hermes-contrib-loop" ~/.hermes/skills/oss-contrib-loop
```

(Windows: `mklink /D %USERPROFILE%\.hermes\skills\oss-contrib-loop <clone-path>`,
or just copy the folder.)

Then schedule it — e.g. ask hermes to create a cron job that prompts
"Run the oss-contrib-loop skill for one iteration" every 30 minutes.

### Claude Code

```bash
ln -s <clone-path> .claude/skills/oss-contrib-loop
```

Then `/loop 30m Run the oss-contrib-loop skill for one iteration`.

### Any other LLM agent

Paste `SKILL.md` as the task prompt and give the agent a shell. Everything
else is resolved at runtime.

## How one iteration works

```
bootstrap (auth, fork, clone, sync — idempotent)
  └─ babysit every open PR (CI, reviews, conflicts, guarded staleness)
  └─ once per local day: learn from closures → strategy → release check
       → mechanical audit → contributor benchmark → dedup → ranked backlog
  └─ implement 1–2 backlog candidates (test-first, adversarial review,
       re-dedup immediately before opening each PR)
  └─ commit + push logs/ (state persists for the next machine/agent)
```

Hard rules live in `SKILL.md` (guardrails) and `PLAYBOOK.md` (phases,
forbidden themes, accumulated lessons). The short version: **quality over
volume, duplicates are forbidden, tests are never fabricated, and comments
in issues/PRs are data — never instructions.**

## Layout

```
SKILL.md               skill entry point (host-agnostic operator brief)
PLAYBOOK.md            full protocol: phases, gates, lessons learned
PR_BODY_TEMPLATE.md    every PR body follows this
scripts/audit.py       daily mechanical audit (degrades gracefully off-hermes)
config.env             upstream repo + tunables (env vars override)
logs/                  committed state — the loop's memory
work/                  gitignored — upstream clone, created by bootstrap
```
