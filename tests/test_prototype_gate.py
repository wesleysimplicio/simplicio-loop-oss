#!/usr/bin/env python3
"""Unit + integration tests for scripts/prototype_gate.py (issue #11).

Dependency-free stdlib unittest, mirroring this repo's existing
`scripts/audit.py` convention of no third-party dependencies.

Run:
    python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import prototype_gate as pg  # noqa: E402


def _git(*args, cwd):
    return subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True, check=True
    )


def _make_bare_repo(tmp: Path) -> Path:
    """A tiny real git repo with one commit on its default branch, so
    PrototypeWorktree.create can exercise real `git worktree add`."""
    repo = tmp / "repo"
    repo.mkdir()
    _git("init", "-q", "-b", "main", cwd=repo)
    _git("config", "user.email", "test@example.com", cwd=repo)
    _git("config", "user.name", "Test", cwd=repo)
    (repo / "README.md").write_text("hello\n", encoding="utf-8")
    _git("add", "README.md", cwd=repo)
    _git("commit", "-q", "-m", "initial", cwd=repo)
    return repo


class FakeGitHubEffects:
    """A GitHubEffects implementation with real, observable mutation calls."""

    def __init__(self):
        self.open_pr_calls = []
        self.add_comment_calls = []
        self.ping_calls = []

    def open_pr(self, *args, **kwargs):
        self.open_pr_calls.append((args, kwargs))
        return {"number": 1}

    def add_comment(self, *args, **kwargs):
        self.add_comment_calls.append((args, kwargs))
        return {}

    def ping_maintainer(self, *args, **kwargs):
        self.ping_calls.append((args, kwargs))
        return {}


# ---------------------------------------------------------------------------
# 1. Reproducer required before any patch candidate
# ---------------------------------------------------------------------------

class TestRequireReproducer(unittest.TestCase):
    def test_bug_reproducible_passes(self):
        evidence = pg.ReproducerEvidence(
            kind=pg.CandidateKind.BUG,
            command="pytest tests/test_thing.py::test_x",
            exit_code_before=1,
            output_before="AssertionError: expected 2, got 1",
        )
        result = pg.require_reproducer(evidence)
        self.assertIs(result, evidence)

    def test_bug_not_reproducible_blocks(self):
        evidence = pg.ReproducerEvidence(
            kind=pg.CandidateKind.BUG,
            command="pytest tests/test_thing.py::test_x",
            exit_code_before=0,  # green — not actually reproduced
        )
        with self.assertRaises(pg.MissingReproducerError):
            pg.require_reproducer(evidence)

    def test_bug_missing_evidence_blocks(self):
        evidence = pg.ReproducerEvidence(kind=pg.CandidateKind.BUG)
        with self.assertRaises(pg.MissingReproducerError):
            pg.require_reproducer(evidence)

    def test_bug_no_test_suite_accepts_manual_confirmation(self):
        """'target sem test suite' case from issue #11's test list: a
        documented equivalent-evidence path when no automated suite exists."""
        evidence = pg.ReproducerEvidence(
            kind=pg.CandidateKind.BUG,
            manual_confirmation=(
                "Manually ran the CLI against the upstream repo (no test "
                "suite ships for this module): crashes with KeyError on "
                "empty config, confirmed on commit abc123."
            ),
        )
        result = pg.require_reproducer(evidence)
        self.assertTrue(result.is_red())

    def test_feature_requires_design_spike(self):
        evidence = pg.ReproducerEvidence(kind=pg.CandidateKind.FEATURE)
        with self.assertRaises(pg.MissingReproducerError):
            pg.require_reproducer(evidence)

    def test_feature_with_design_spike_passes(self):
        evidence = pg.ReproducerEvidence(
            kind=pg.CandidateKind.FEATURE,
            design_spike="Adds `--foo` flag; schema documented in spike.md.",
        )
        pg.require_reproducer(evidence)  # must not raise


# ---------------------------------------------------------------------------
# 2. Zero GitHub mutation during the prototype phase
# ---------------------------------------------------------------------------

class TestReadOnlyGuard(unittest.TestCase):
    def test_mutating_calls_are_blocked_and_recorded(self):
        real = FakeGitHubEffects()
        guard = pg.ReadOnlyGuard(real)

        with self.assertRaises(pg.PrototypeMutationBlocked):
            guard.open_pr(title="x")
        with self.assertRaises(pg.PrototypeMutationBlocked):
            guard.add_comment(body="y")
        with self.assertRaises(pg.PrototypeMutationBlocked):
            guard.ping_maintainer()

        self.assertEqual(guard.blocked_call_attempts, ["open_pr", "add_comment", "ping_maintainer"])
        # The underlying real client's methods were never actually invoked.
        self.assertEqual(real.open_pr_calls, [])
        self.assertEqual(real.add_comment_calls, [])
        self.assertEqual(real.ping_calls, [])

    def test_non_mutating_access_passes_through(self):
        real = MagicMock()
        real.some_read_only_method.return_value = "ok"
        guard = pg.ReadOnlyGuard(real)
        self.assertEqual(guard.some_read_only_method(), "ok")


# ---------------------------------------------------------------------------
# 3. Isolated worktree — never the default branch
# ---------------------------------------------------------------------------

class TestPrototypeWorktree(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_refuses_default_branch(self):
        repo = _make_bare_repo(self.tmp)
        with self.assertRaises(pg.WorktreeError):
            pg.PrototypeWorktree.create(
                repo_root=repo,
                branch="main",
                worktree_dir=self.tmp / "wt",
                default_branch="main",
            )

    def test_creates_isolated_worktree_on_private_branch(self):
        repo = _make_bare_repo(self.tmp)
        worktree_dir = self.tmp / "wt-candidate-1"
        wt = pg.PrototypeWorktree.create(
            repo_root=repo,
            branch="prototype/candidate-1",
            worktree_dir=worktree_dir,
            default_branch="main",
        )
        self.assertEqual(wt.branch, "prototype/candidate-1")
        self.assertTrue(worktree_dir.exists())
        # The default branch's working tree is untouched.
        head = _git("rev-parse", "--abbrev-ref", "HEAD", cwd=repo).stdout.strip()
        self.assertEqual(head, "main")
        # The new worktree really is on the private branch.
        wt_head = _git("rev-parse", "--abbrev-ref", "HEAD", cwd=worktree_dir).stdout.strip()
        self.assertEqual(wt_head, "prototype/candidate-1")

    def test_bad_repo_raises_worktree_error(self):
        not_a_repo = self.tmp / "not-a-repo"
        not_a_repo.mkdir()
        with self.assertRaises(pg.WorktreeError):
            pg.PrototypeWorktree.create(
                repo_root=not_a_repo,
                branch="prototype/x",
                worktree_dir=self.tmp / "wt",
                default_branch="main",
            )


# ---------------------------------------------------------------------------
# 4. Double dedup — before and after prototyping
# ---------------------------------------------------------------------------

class TestDuplicateIndex(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "prototype-index.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_fresh_candidate_passes_check(self):
        index = pg.DuplicateIndex.load(self.path)
        index.check("Fix off-by-one in tokenizer")  # must not raise

    def test_duplicate_candidate_detected_before_promotion(self):
        index = pg.DuplicateIndex.load(self.path)
        index.check("Fix off-by-one in tokenizer")
        index.record("Fix off-by-one in tokenizer")

        # Same candidate again (even a second DuplicateIndex.load from disk,
        # simulating a second session/process) is rejected before promotion.
        reloaded = pg.DuplicateIndex.load(self.path)
        with self.assertRaises(pg.DuplicateCandidateError):
            reloaded.check("fix   OFF-BY-ONE in tokenizer")  # normalized match

    def test_double_dedup_before_and_after(self):
        index = pg.DuplicateIndex.load(self.path)
        title = "Handle empty config gracefully"
        index.check(title)  # before prototyping
        index.check(title)  # after prototyping, still clean
        index.record(title)
        with self.assertRaises(pg.DuplicateCandidateError):
            index.check(title)  # a third check now finds the recorded one


# ---------------------------------------------------------------------------
# 5. Independent judge
# ---------------------------------------------------------------------------

class TestIndependentJudge(unittest.TestCase):
    def test_independent_judge_accepts(self):
        verdict = pg.judge_candidate(
            candidate_id="cand-1",
            judge_id="reviewer-b",
            creator_id="implementer-a",
            kind=pg.JudgeVerdictKind.ACCEPT,
            reasons="Reproduces, fix is minimal and passes upstream tests.",
        )
        self.assertEqual(verdict.kind, pg.JudgeVerdictKind.ACCEPT)

    def test_judge_cannot_be_the_creator(self):
        with self.assertRaises(pg.JudgeIndependenceError):
            pg.judge_candidate(
                candidate_id="cand-1",
                judge_id="implementer-a",
                creator_id="implementer-a",
                kind=pg.JudgeVerdictKind.ACCEPT,
            )

    def test_reject_preserves_evidence_shape(self):
        verdict = pg.judge_candidate(
            candidate_id="cand-2",
            judge_id="reviewer-b",
            creator_id="implementer-a",
            kind=pg.JudgeVerdictKind.REJECT,
            reasons="Does not reproduce against current default branch.",
        )
        self.assertEqual(verdict.kind, pg.JudgeVerdictKind.REJECT)
        self.assertIn("does not reproduce", verdict.reasons.lower())


# ---------------------------------------------------------------------------
# 6. Delivery handoff — ACCEPT-only, exactly one owner, forged/missing blocks
# ---------------------------------------------------------------------------

class TestDeliveryHandoff(unittest.TestCase):
    def _accept_verdict(self):
        return pg.judge_candidate(
            candidate_id="cand-1",
            judge_id="reviewer-b",
            creator_id="implementer-a",
            kind=pg.JudgeVerdictKind.ACCEPT,
        )

    def test_accept_verdict_enables_delivery_by_owner(self):
        verdict = self._accept_verdict()
        handoff = pg.DeliveryHandoff(verdict=verdict, delivery_owner="delivery-bot")
        github = FakeGitHubEffects()
        result = handoff.deliver(github, "delivery-bot", title="Fix off-by-one")
        self.assertEqual(result, {"number": 1})
        self.assertEqual(len(github.open_pr_calls), 1)

    def test_non_owner_cannot_deliver(self):
        verdict = self._accept_verdict()
        handoff = pg.DeliveryHandoff(verdict=verdict, delivery_owner="delivery-bot")
        github = FakeGitHubEffects()
        with self.assertRaises(pg.DeliveryNotAuthorizedError):
            handoff.deliver(github, "implementer-a", title="Fix off-by-one")
        self.assertEqual(github.open_pr_calls, [])

    def test_reject_verdict_blocks_delivery(self):
        verdict = pg.judge_candidate(
            candidate_id="cand-1",
            judge_id="reviewer-b",
            creator_id="implementer-a",
            kind=pg.JudgeVerdictKind.REJECT,
        )
        with self.assertRaises(pg.DeliveryNotAuthorizedError):
            pg.DeliveryHandoff(verdict=verdict, delivery_owner="delivery-bot")

    def test_revise_verdict_blocks_delivery(self):
        verdict = pg.judge_candidate(
            candidate_id="cand-1",
            judge_id="reviewer-b",
            creator_id="implementer-a",
            kind=pg.JudgeVerdictKind.REVISE,
        )
        with self.assertRaises(pg.DeliveryNotAuthorizedError):
            pg.DeliveryHandoff(verdict=verdict, delivery_owner="delivery-bot")

    def test_forged_decision_blocks_delivery(self):
        class FakeVerdict:
            kind = pg.JudgeVerdictKind.ACCEPT  # pretends to be a real verdict

        with self.assertRaises(pg.DeliveryNotAuthorizedError):
            pg.DeliveryHandoff(verdict=FakeVerdict(), delivery_owner="delivery-bot")

    def test_missing_decision_blocks_delivery(self):
        with self.assertRaises(pg.DeliveryNotAuthorizedError):
            pg.DeliveryHandoff(verdict=None, delivery_owner="delivery-bot")


# ---------------------------------------------------------------------------
# 7. PROFILE.md -> prototype policy (best-effort translation)
# ---------------------------------------------------------------------------

class TestLoadPrototypePolicy(unittest.TestCase):
    def test_parses_signals_from_profile_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            profile = Path(tmp) / "PROFILE.md"
            profile.write_text(
                "## Contribution rules\n\n"
                "This project requires a signed CLA and DCO "
                "(`Signed-off-by`) on every commit. Issue-first: open an "
                "issue before a PR. Run `pytest tests/ -q` before pushing.\n",
                encoding="utf-8",
            )
            policy = pg.load_prototype_policy(profile)
        self.assertTrue(policy.requires_cla)
        self.assertTrue(policy.requires_dco)
        self.assertTrue(policy.issue_first)
        self.assertTrue(any("pytest" in c for c in policy.test_commands))

    def test_missing_profile_defaults_to_no_requirements(self):
        policy = pg.load_prototype_policy(Path("/nonexistent/PROFILE.md"))
        self.assertFalse(policy.requires_cla)
        self.assertFalse(policy.requires_dco)
        self.assertFalse(policy.issue_first)
        self.assertEqual(policy.test_commands, ())


# ---------------------------------------------------------------------------
# 7b. Observable-assertion requirement (DOD.md layer 3)
# ---------------------------------------------------------------------------

def _diff(*, changed_file=None, changed_lines=None, test_file=None, test_lines=None):
    """Build a minimal unified diff touching up to one code file and one
    test file, for exercising require_observable_assertion in isolation."""
    parts = []
    if changed_file:
        parts.append(f"diff --git a/{changed_file} b/{changed_file}")
        parts.append(f"--- a/{changed_file}")
        parts.append(f"+++ b/{changed_file}")
        parts.append("@@ -1,1 +1,%d @@" % (len(changed_lines or [])))
        for line in changed_lines or ["+    return fixed_value"]:
            parts.append(line if line.startswith(("+", "-", " ")) else f"+{line}")
    if test_file:
        parts.append(f"diff --git a/{test_file} b/{test_file}")
        parts.append(f"--- a/{test_file}")
        parts.append(f"+++ b/{test_file}")
        parts.append("@@ -1,1 +1,%d @@" % (len(test_lines or [])))
        for line in test_lines or []:
            parts.append(line if line.startswith(("+", "-", " ")) else f"+{line}")
    return "\n".join(parts) + "\n"


class TestRequireObservableAssertion(unittest.TestCase):
    def test_docs_only_diff_needs_no_test(self):
        diff = _diff(changed_file="README.md", changed_lines=["+Some doc text"])
        pg.require_observable_assertion(diff)  # must not raise

    def test_test_only_diff_needs_no_further_test(self):
        diff = _diff(
            test_file="tests/test_thing.py",
            test_lines=["+def test_x():", "+    assert 1 == 1"],
        )
        pg.require_observable_assertion(diff)  # must not raise

    def test_code_change_without_any_test_file_blocks(self):
        diff = _diff(changed_file="src/parser.py", changed_lines=["+    return lines[i]"])
        with self.assertRaises(pg.InsufficientTestAssertionError):
            pg.require_observable_assertion(diff)

    def test_code_change_with_only_weak_returncode_assertion_blocks(self):
        """Regression shape for motivating bug #2 (a line-selection regex
        that quietly swallowed a blank line): a test that only checks the
        command exited 0 would not have caught it."""
        diff = _diff(
            changed_file="src/line_selector.py",
            changed_lines=["+    return re.sub(pattern, '', text)"],
            test_file="tests/test_line_selector.py",
            test_lines=[
                "+def test_runs_ok():",
                "+    result = subprocess.run(['tool', 'in.txt'])",
                "+    assert result.returncode == 0",
            ],
        )
        with self.assertRaises(pg.InsufficientTestAssertionError):
            pg.require_observable_assertion(diff)

    def test_code_change_with_only_bare_truthy_assertion_blocks(self):
        diff = _diff(
            changed_file="src/apply_plan.py",
            changed_lines=["+    write_all(files, plan)"],
            test_file="tests/test_apply_plan.py",
            test_lines=["+def test_it_runs():", "+    assert True"],
        )
        with self.assertRaises(pg.InsufficientTestAssertionError):
            pg.require_observable_assertion(diff)

    def test_code_change_with_concrete_value_assertion_passes(self):
        """Regression shape for motivating bug #1 (silent corruption in a
        multi-file edit plan): asserting the exact resulting content of
        every touched file is what would have caught it."""
        diff = _diff(
            changed_file="src/apply_plan.py",
            changed_lines=["+    write_all(files, plan)"],
            test_file="tests/test_apply_plan.py",
            test_lines=[
                "+def test_unrelated_file_untouched():",
                "+    apply_plan(plan, files)",
                "+    self.assertEqual(read('b.txt'), 'original content')",
            ],
        )
        pg.require_observable_assertion(diff)  # must not raise

    def test_code_change_with_line_content_assertion_passes(self):
        diff = _diff(
            changed_file="src/line_selector.py",
            changed_lines=["+    return re.sub(pattern, '', text)"],
            test_file="tests/test_line_selector.py",
            test_lines=[
                "+def test_blank_line_preserved():",
                "+    lines = select(sample_text)",
                "+    self.assertEqual(lines[3], '')",
            ],
        )
        pg.require_observable_assertion(diff)  # must not raise

    def test_js_expect_tobe_assertion_passes(self):
        diff = _diff(
            changed_file="src/parser.js",
            changed_lines=["+  return lines[i];"],
            test_file="src/parser.test.js",
            test_lines=["+test('keeps blank line', () => {", "+  expect(lines[3]).toBe('');", "+});"],
        )
        pg.require_observable_assertion(diff)  # must not raise


class TestRunPrototypeStageObservableAssertion(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.repo = _make_bare_repo(self.tmp)
        self.dedup_path = self.tmp / "index.json"

    def tearDown(self):
        self._tmp.cleanup()

    def _base_kwargs(self, github, title="Fix off-by-one in tokenizer"):
        return dict(
            candidate_id="cand-1",
            title=title,
            evidence=pg.ReproducerEvidence(
                kind=pg.CandidateKind.BUG,
                command="pytest tests/test_tok.py::test_edge",
                exit_code_before=1,
                output_before="AssertionError",
            ),
            repo_root=self.repo,
            branch="prototype/cand-1",
            worktree_dir=self.tmp / "wt-cand-1",
            default_branch="main",
            dedup_index=pg.DuplicateIndex.load(self.dedup_path),
            github=github,
            creator_id="implementer-a",
            judge_id="reviewer-b",
            delivery_owner="delivery-bot",
            verdict_kind=pg.JudgeVerdictKind.ACCEPT,
        )

    def test_missing_diff_text_skips_the_check_for_back_compat(self):
        github = FakeGitHubEffects()
        result = pg.run_prototype_stage(**self._base_kwargs(github))
        self.assertIsNotNone(result.handoff)

    def test_weak_diff_blocks_before_judge_sees_the_candidate(self):
        github = FakeGitHubEffects()
        kwargs = self._base_kwargs(github)
        kwargs["diff_text"] = _diff(
            changed_file="src/apply_plan.py",
            changed_lines=["+    write_all(files, plan)"],
            test_file="tests/test_apply_plan.py",
            test_lines=["+def test_it_runs():", "+    assert True"],
        )
        with self.assertRaises(pg.InsufficientTestAssertionError):
            pg.run_prototype_stage(**kwargs)
        self.assertEqual(github.open_pr_calls, [])

    def test_meaningful_diff_reaches_delivery_handoff(self):
        github = FakeGitHubEffects()
        kwargs = self._base_kwargs(github)
        kwargs["diff_text"] = _diff(
            changed_file="src/apply_plan.py",
            changed_lines=["+    write_all(files, plan)"],
            test_file="tests/test_apply_plan.py",
            test_lines=[
                "+def test_unrelated_file_untouched():",
                "+    self.assertEqual(read('b.txt'), 'original content')",
            ],
        )
        result = pg.run_prototype_stage(**kwargs)
        self.assertIsNotNone(result.handoff)


# ---------------------------------------------------------------------------
# Integration: the full prototype stage orchestrator
# ---------------------------------------------------------------------------

class TestRunPrototypeStage(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.repo = _make_bare_repo(self.tmp)
        self.dedup_path = self.tmp / "index.json"

    def tearDown(self):
        self._tmp.cleanup()

    def _base_kwargs(self, github, title="Fix off-by-one in tokenizer"):
        return dict(
            candidate_id="cand-1",
            title=title,
            evidence=pg.ReproducerEvidence(
                kind=pg.CandidateKind.BUG,
                command="pytest tests/test_tok.py::test_edge",
                exit_code_before=1,
                output_before="AssertionError",
            ),
            repo_root=self.repo,
            branch="prototype/cand-1",
            worktree_dir=self.tmp / "wt-cand-1",
            default_branch="main",
            dedup_index=pg.DuplicateIndex.load(self.dedup_path),
            github=github,
            creator_id="implementer-a",
            judge_id="reviewer-b",
            delivery_owner="delivery-bot",
            verdict_kind=pg.JudgeVerdictKind.ACCEPT,
        )

    def test_accepted_candidate_produces_delivery_handoff_with_zero_mutation(self):
        github = FakeGitHubEffects()
        result = pg.run_prototype_stage(**self._base_kwargs(github))

        self.assertIsNotNone(result.handoff)
        self.assertEqual(result.verdict.kind, pg.JudgeVerdictKind.ACCEPT)

        # AC: prototype phase made zero GitHub-facing calls.
        self.assertEqual(github.open_pr_calls, [])
        self.assertEqual(github.add_comment_calls, [])
        self.assertEqual(github.ping_calls, [])
        self.assertEqual(result.guard.blocked_call_attempts, [])

        # Delivery is now possible, and only through the handoff/owner.
        outcome = result.handoff.deliver(github, "delivery-bot", title="Fix off-by-one")
        self.assertEqual(len(github.open_pr_calls), 1)
        self.assertEqual(outcome, {"number": 1})

    def test_rejected_candidate_blocks_delivery_with_zero_mutation(self):
        github = FakeGitHubEffects()
        kwargs = self._base_kwargs(github)
        kwargs["verdict_kind"] = pg.JudgeVerdictKind.REJECT
        result = pg.run_prototype_stage(**kwargs)

        self.assertIsNone(result.handoff)
        self.assertEqual(result.verdict.kind, pg.JudgeVerdictKind.REJECT)
        self.assertEqual(github.open_pr_calls, [])
        self.assertEqual(github.add_comment_calls, [])
        self.assertEqual(github.ping_calls, [])

    def test_no_reproducer_blocks_before_worktree_is_created(self):
        github = FakeGitHubEffects()
        kwargs = self._base_kwargs(github)
        kwargs["evidence"] = pg.ReproducerEvidence(kind=pg.CandidateKind.BUG)  # no red evidence

        with self.assertRaises(pg.MissingReproducerError):
            pg.run_prototype_stage(**kwargs)

        # No worktree/branch was ever created for an unproven bug.
        self.assertFalse((self.tmp / "wt-cand-1").exists())
        self.assertEqual(github.open_pr_calls, [])

    def test_duplicate_candidate_blocks_second_prototype_run(self):
        github = FakeGitHubEffects()
        pg.run_prototype_stage(**self._base_kwargs(github, title="Fix empty-config crash"))

        # A second session/process picks up the same candidate title.
        kwargs2 = self._base_kwargs(github, title="fix   empty-config   crash")
        kwargs2["branch"] = "prototype/cand-2"
        kwargs2["worktree_dir"] = self.tmp / "wt-cand-2"
        kwargs2["candidate_id"] = "cand-2"

        with self.assertRaises(pg.DuplicateCandidateError):
            pg.run_prototype_stage(**kwargs2)

    def test_two_sessions_same_candidate_only_one_prototypes(self):
        """DoD scenario: two sessions find the same bug; only one may
        create a reproducer/patch candidate, the other is blocked by dedup
        (a fuller "who claims first" lease mechanism is epic #1/#4
        territory — this proves the dedup half of that guarantee)."""
        shared_index_path = self.dedup_path
        github_a = FakeGitHubEffects()
        github_b = FakeGitHubEffects()

        session_a = self._base_kwargs(github_a, title="Null pointer on empty list")
        result_a = pg.run_prototype_stage(**session_a)
        self.assertIsNotNone(result_a.handoff)

        session_b = self._base_kwargs(github_b, title="null pointer on empty list")
        session_b["dedup_index"] = pg.DuplicateIndex.load(shared_index_path)
        session_b["branch"] = "prototype/cand-1-session-b"
        session_b["worktree_dir"] = self.tmp / "wt-cand-1-session-b"
        with self.assertRaises(pg.DuplicateCandidateError):
            pg.run_prototype_stage(**session_b)

        # Neither session ever touched GitHub.
        self.assertEqual(github_a.open_pr_calls, [])
        self.assertEqual(github_b.open_pr_calls, [])


if __name__ == "__main__":
    unittest.main()
