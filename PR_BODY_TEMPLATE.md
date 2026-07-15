<!-- PR body template — simplicio-loop-oss generic house-style fallback.
     The project's own merged-PR body style (PROFILE.md benchmark snapshot)
     WINS over this template. If the upstream repo injects its own PR
     template (checklist etc.), fill those sections honestly and weave
     these in — do NOT add an upstream-style checklist yourself when the
     repo doesn't inject one.
     Everything in ENGLISH. NEVER fabricate test results — run the command,
     paste the real outcome. Diagrams (mermaid) are OPTIONAL and usually
     wrong: check the benchmark snapshot — if the project's recent merged
     PRs don't use them, don't either. Only add one when the flow is
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
| Repro before fix (bug fix) | <repro/test command on pre-fix code> | <REAL failing output/assertion> |
| Repro after fix | <same command on this branch> | <REAL passing output> |
| New tests | `<project test runner> tests/<file> -q` | <REAL pasted result, e.g. ✅ 4 passed> |
| Targeted suite | `<project test runner> tests/<area> -q` | <REAL result> |
| Project gates | <lint/format/gate commands from PROFILE.md> | <REAL result> |

<!-- Pre-existing failures in the suite that are NOT caused by this change:
     declare them explicitly instead of hiding them — e.g.
     "N pre-existing failures in <file>; they reproduce identically on
     upstream/<default-branch> (verified by stashing this change)." -->

## How to Test

1. <Repro steps on the default branch — expected: the bug shows up>
2. <Check out this branch>
3. <Same steps — expected: fixed behavior>

Closes #<NNN>

<!-- Salvage variant: title carries "(salvage #NNN)". Add here:
"This salvages #NNN by @original-author — original commits cherry-picked
with authorship preserved; follow-up commits adapt it to the current
default branch: <what changed and why>." -->

<!-- Optional when genuinely useful:
## Out of scope (adjacent issues intentionally not addressed, flagged for maintainers)
-->
