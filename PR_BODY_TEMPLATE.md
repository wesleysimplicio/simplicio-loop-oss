<!-- PR body template — simplicio-loop-oss generic house-style fallback.
     The project's own merged-PR body style (PROFILE.md benchmark snapshot)
     WINS over this template; when the upstream repo ships a PR template,
     fill its sections honestly and weave these in.
     Everything in ENGLISH. NEVER fabricate test results — run the command,
     paste the real outcome. Diagrams (mermaid) only when the flow is
     genuinely hard to explain in text. -->

## Summary

<Symptom + root cause in 2–3 sentences. What breaks, why it breaks, why this
is the right fix. Plain English, no marketing prose.>

## Changes

- `path/to/file.py`: <specific change and why>
- `tests/test_x.py`: <test added, what it locks in>

## Validation

| Check | Command | Result |
|---|---|---|
| New tests | `<project test runner> tests/<file> -q` | <REAL pasted result, e.g. ✅ 4 passed> |
| Targeted suite | `<project test runner> tests/<area> -q` | <REAL result> |
| Project gates | <lint/format/gate commands from PROFILE.md> | <REAL result> |
| Fail-before/pass-after | New tests run against pre-fix code | <REAL failing assertion, then pass> |

Closes #<NNN>

<!-- Salvage variant: title carries "(salvage #NNN)". Add here:
"This salvages #NNN by @original-author — original commits cherry-picked
with authorship preserved; follow-up commits adapt it to current <branch>:
<what changed and why>." -->

<!-- Optional sections when they genuinely add value:
## How to Test  (manual repro steps: on default branch → broken; here → fixed)
## Out of scope (adjacent issues intentionally not addressed, flagged for maintainers)
-->
