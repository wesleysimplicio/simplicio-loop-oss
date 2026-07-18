#!/usr/bin/env python3
"""Prototype-First gate — adapter for simplicio-loop epic #568.

Implements simplicio-loop-oss#11 ("[P0][Prototype-First][Loop #568] Exigir
reproducer e patch experimental antes de abrir PR OSS"), scoped to what that
issue's own acceptance criteria ask for. This module does NOT reimplement
simplicio-loop's coordinator/scheduler/ledger — it is a small, dependency-free
local adapter that:

1. Requires and captures a failing reproducer (bug) or a policy-compatible
   design/schema spike (feature) BEFORE any patch candidate is created
   (``require_reproducer``).
2. Guarantees zero GitHub-facing mutation during the prototype phase —
   ``ReadOnlyGuard`` wraps the real GitHub-effects client so
   ``open_pr``/``add_comment``/``ping_maintainer`` calls raise instead of
   silently no-opping, and callers can assert they were never even attempted.
3. Creates the candidate in an isolated ``git worktree`` on a private branch,
   never the target's default branch (``PrototypeWorktree``).
4. Runs double dedup — before AND after prototyping
   (``DuplicateIndex.check``/``record``) — against a small local ledger that
   mirrors the ``projects/SLUG/logs/opened-prs.md`` convention this repo
   already uses. This is deliberately NOT a reimplementation of PLAYBOOK.md
   Phase 4's real GitHub-side ``gh search`` dedup (still the source of truth
   for "is this a duplicate upstream") — it only prevents the same local
   candidate from being prototyped/promoted twice.
5. Requires an independent judge (``judge_candidate``) — the judge identity
   must differ from the candidate's creator identity.
6. Gates delivery behind a genuine ACCEPT verdict and exactly one delivery
   owner (``DeliveryHandoff``) — REJECT/REVISE, or a forged/missing verdict,
   blocks delivery; delivery is the only path allowed to call
   ``GitHubEffects.open_pr``.

Deliberately OUT of scope for this pass (deferred to the parent epic #1 and
upstream simplicio-loop#568, per issue #11's own "scope realistically" note):
the full multi-machine E2E, CLA/DCO enforcement mechanics, and the merge-rate
/ newcomer-cap policy engine. Those already exist as *policy text* in
SKILL.md/PLAYBOOK.md and are read, not reinvented, by ``load_prototype_policy``
below.

Usage (library, not a CLI):
    from prototype_gate import (
        CandidateKind, ReproducerEvidence, require_reproducer,
        DuplicateIndex, PrototypeWorktree, judge_candidate,
        JudgeVerdictKind, DeliveryHandoff, run_prototype_stage,
    )
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, Optional, Protocol


# ---------------------------------------------------------------------------
# 1. Reproducer / design-spike requirement (AC: no patch candidate without it)
# ---------------------------------------------------------------------------

class CandidateKind(str, Enum):
    BUG = "bug"
    FEATURE = "feature"


class MissingReproducerError(RuntimeError):
    """Raised when a candidate has no captured red evidence yet."""


@dataclass(frozen=True)
class ReproducerEvidence:
    """Evidence captured BEFORE any patch candidate exists.

    Bug candidates: either a real command + a non-zero "before" exit code
    (the common case — a red test), or, when the target repo has no usable
    test suite for this bug, a documented ``manual_confirmation`` of
    equivalent evidence (the "target sem test suite" case from issue #11's
    test list).

    Feature candidates: a policy-compatible design/schema spike (text is
    enough for this pass — it is reviewed by the independent judge below,
    it does not need to be executable).
    """

    kind: CandidateKind
    command: str = ""
    exit_code_before: Optional[int] = None
    output_before: str = ""
    manual_confirmation: str = ""
    design_spike: str = ""

    def is_red(self) -> bool:
        """True if this evidence actually demonstrates a failing/red state."""
        if self.kind == CandidateKind.BUG:
            if self.command and self.exit_code_before not in (None, 0):
                return True
            return bool(self.manual_confirmation.strip())
        return bool(self.design_spike.strip())


def require_reproducer(evidence: ReproducerEvidence) -> ReproducerEvidence:
    """Gate: no patch candidate may be created without this passing.

    Raises ``MissingReproducerError`` when the evidence does not establish a
    red/failing state. Returns the evidence unchanged so callers can chain it
    into the candidate record (this is deliberately not a no-op passthrough:
    the whole point is that this call can and does block).
    """
    if evidence.is_red():
        return evidence
    if evidence.kind == CandidateKind.BUG:
        raise MissingReproducerError(
            "bug candidate requires a captured failing reproducer (a red "
            "command result) or documented equivalent evidence before any "
            "patch candidate is created"
        )
    raise MissingReproducerError(
        "feature candidate requires a policy-compatible design/schema spike "
        "before any patch candidate is created"
    )


# ---------------------------------------------------------------------------
# 2. Zero GitHub-facing mutation during the prototype phase
# ---------------------------------------------------------------------------

class GitHubEffects(Protocol):
    """The GitHub-calling layer. Real implementations shell out to `gh`;
    tests pass a mock/stub implementing the same surface."""

    def open_pr(self, *args, **kwargs) -> dict: ...
    def add_comment(self, *args, **kwargs) -> dict: ...
    def ping_maintainer(self, *args, **kwargs) -> dict: ...


class PrototypeMutationBlocked(RuntimeError):
    """Raised the instant prototype-phase code attempts a GitHub mutation."""


MUTATING_METHODS = ("open_pr", "add_comment", "ping_maintainer")


class ReadOnlyGuard:
    """Wraps a real ``GitHubEffects`` client for the prototype phase.

    Any attempted call to a mutating method raises immediately instead of
    silently no-opping (a silent no-op would hide a real defect and could
    mask an accidental mutation path in a future refactor). Non-mutating
    attribute access passes through to the wrapped client unchanged.
    """

    def __init__(self, real: "GitHubEffects"):
        self._real = real
        self.blocked_call_attempts: list = []

    def __getattr__(self, name):
        if name in MUTATING_METHODS:
            def _blocked(*_args, **_kwargs):
                self.blocked_call_attempts.append(name)
                raise PrototypeMutationBlocked(
                    f"prototype phase attempted a GitHub mutation: {name}()"
                )
            return _blocked
        return getattr(self._real, name)


# ---------------------------------------------------------------------------
# 3. Isolated worktree/branch — never the target's default branch
# ---------------------------------------------------------------------------

class WorktreeError(RuntimeError):
    pass


@dataclass
class PrototypeWorktree:
    repo_root: Path
    branch: str
    path: Path

    @classmethod
    def create(
        cls,
        repo_root: Path,
        branch: str,
        worktree_dir: Path,
        default_branch: str,
        runner: Callable[..., "subprocess.CompletedProcess"] = subprocess.run,
    ) -> "PrototypeWorktree":
        if branch == default_branch:
            raise WorktreeError(
                f"refusing to prototype directly on the default branch "
                f"{default_branch!r} — candidates must live in an isolated "
                f"worktree/branch"
            )
        result = runner(
            ["git", "worktree", "add", "-b", branch, str(worktree_dir), default_branch],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise WorktreeError(f"git worktree add failed: {result.stderr.strip()}")
        return cls(repo_root=repo_root, branch=branch, path=worktree_dir)

    def remove(self, runner: Callable[..., "subprocess.CompletedProcess"] = subprocess.run) -> None:
        runner(
            ["git", "worktree", "remove", "--force", str(self.path)],
            cwd=str(self.repo_root),
            capture_output=True,
            text=True,
        )


# ---------------------------------------------------------------------------
# 4. Double dedup — before AND after prototyping
# ---------------------------------------------------------------------------

class DuplicateCandidateError(RuntimeError):
    pass


def _candidate_key(title: str) -> str:
    normalized = " ".join(title.strip().lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


@dataclass
class DuplicateIndex:
    """Local double-dedup ledger for prototype candidates.

    Mirrors the ``projects/SLUG/logs/opened-prs.md`` anti-duplicate
    convention this repo already uses for opened PRs, scoped instead to
    prototype candidates so the same candidate cannot be prototyped or
    promoted twice. This is NOT a substitute for PLAYBOOK.md Phase 4's real
    ``gh search`` dedup against the upstream repo — that remains the source
    of truth for "does this duplicate something upstream"; this index only
    catches "did WE already run a prototype for this locally".
    """

    path: Path
    _seen: dict = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> "DuplicateIndex":
        seen: dict = {}
        if path.exists():
            seen = json.loads(path.read_text(encoding="utf-8"))
        return cls(path=path, _seen=seen)

    def check(self, title: str) -> None:
        key = _candidate_key(title)
        if key in self._seen:
            raise DuplicateCandidateError(
                f"candidate {title!r} was already recorded at "
                f"{self._seen[key]} — duplicate prototype work is forbidden"
            )

    def record(self, title: str) -> None:
        key = _candidate_key(title)
        self._seen[key] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self._seen, indent=2, sort_keys=True), encoding="utf-8"
        )


# ---------------------------------------------------------------------------
# 5. Independent judge — must not be the candidate's own creator
# ---------------------------------------------------------------------------

class JudgeVerdictKind(str, Enum):
    ACCEPT = "accept"
    REVISE = "revise"
    REJECT = "reject"


class JudgeIndependenceError(RuntimeError):
    pass


@dataclass(frozen=True)
class JudgeVerdict:
    candidate_id: str
    judge_id: str
    creator_id: str
    kind: JudgeVerdictKind
    reasons: str = ""

    def __post_init__(self) -> None:
        if not self.judge_id or not self.creator_id:
            raise JudgeIndependenceError("judge_id and creator_id are both required")
        if self.judge_id == self.creator_id:
            raise JudgeIndependenceError(
                "the judge must be independent of the candidate's own creator "
                f"(both were {self.judge_id!r})"
            )


def judge_candidate(
    candidate_id: str,
    judge_id: str,
    creator_id: str,
    kind: JudgeVerdictKind,
    reasons: str = "",
) -> JudgeVerdict:
    return JudgeVerdict(
        candidate_id=candidate_id,
        judge_id=judge_id,
        creator_id=creator_id,
        kind=kind,
        reasons=reasons,
    )


# ---------------------------------------------------------------------------
# 6. Delivery handoff — ACCEPT-only, exactly one delivery owner
# ---------------------------------------------------------------------------

class DeliveryNotAuthorizedError(RuntimeError):
    pass


@dataclass
class DeliveryHandoff:
    """The only object capable of authorizing a mutating GitHub call.

    Requires a genuine ``JudgeVerdict`` with ``kind == ACCEPT`` — a forged
    object (not a real ``JudgeVerdict``), a missing verdict, or a
    REJECT/REVISE verdict all raise ``DeliveryNotAuthorizedError`` instead of
    producing a handoff. Binds to exactly one ``delivery_owner`` identity;
    ``deliver`` refuses any other caller.
    """

    verdict: JudgeVerdict
    delivery_owner: str

    def __post_init__(self) -> None:
        if not isinstance(self.verdict, JudgeVerdict):
            raise DeliveryNotAuthorizedError(
                "delivery requires a genuine JudgeVerdict — none was provided "
                "(forged or missing decision)"
            )
        if self.verdict.kind != JudgeVerdictKind.ACCEPT:
            raise DeliveryNotAuthorizedError(
                f"delivery blocked: verdict is {self.verdict.kind.value!r}, "
                "not accept"
            )
        if not self.delivery_owner:
            raise DeliveryNotAuthorizedError("delivery requires exactly one named owner")

    def deliver(self, github: "GitHubEffects", requester_id: str, *args, **kwargs) -> dict:
        if requester_id != self.delivery_owner:
            raise DeliveryNotAuthorizedError(
                f"{requester_id!r} is not the authorized delivery owner "
                f"({self.delivery_owner!r})"
            )
        return github.open_pr(*args, **kwargs)


# ---------------------------------------------------------------------------
# 7. PROFILE.md -> prototype policy (best-effort translation, this pass only)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PrototypePolicy:
    requires_cla: bool
    requires_dco: bool
    issue_first: bool
    test_commands: tuple


def load_prototype_policy(profile_path: Path) -> PrototypePolicy:
    """Best-effort translation of a project's PROFILE.md into prototype
    policy. Deliberately shallow for this pass — full per-target policy
    modeling is epic #1 / upstream simplicio-loop#568 territory; this just
    lets the prototype stage read the same signals a human already records
    in PROFILE.md (CLA/DCO/issue-first, test commands) instead of asking a
    second time."""
    text = ""
    if profile_path.exists():
        text = profile_path.read_text(encoding="utf-8", errors="replace")
    lower = text.lower()
    test_commands = tuple(
        dict.fromkeys(
            m.group(1)
            for m in re.finditer(r"`([^`\n]*\b(?:test|pytest)\b[^`\n]*)`", lower)
        )
    )
    return PrototypePolicy(
        requires_cla=("cla" in lower) and ("no cla" not in lower),
        requires_dco=("dco" in lower) or ("signed-off-by" in lower),
        issue_first=("issue-first" in lower) or ("issue first" in lower),
        test_commands=test_commands,
    )


# ---------------------------------------------------------------------------
# Orchestrator — sequences 1-6 for one candidate
# ---------------------------------------------------------------------------

@dataclass
class PrototypeStageResult:
    candidate_id: str
    evidence: ReproducerEvidence
    worktree: PrototypeWorktree
    guard: ReadOnlyGuard
    verdict: Optional[JudgeVerdict] = None
    handoff: Optional[DeliveryHandoff] = None


def run_prototype_stage(
    *,
    candidate_id: str,
    title: str,
    evidence: ReproducerEvidence,
    repo_root: Path,
    branch: str,
    worktree_dir: Path,
    default_branch: str,
    dedup_index: DuplicateIndex,
    github: "GitHubEffects",
    creator_id: str,
    judge_id: str,
    delivery_owner: str,
    verdict_kind: JudgeVerdictKind,
    verdict_reasons: str = "",
    runner: Callable[..., "subprocess.CompletedProcess"] = subprocess.run,
) -> PrototypeStageResult:
    """The full prototype-first sequence for one candidate:

    double dedup (before) -> reproducer/spike required -> isolated worktree
    -> double dedup (after) -> independent judge -> (ACCEPT only) delivery
    handoff. ``github`` is wrapped in a ``ReadOnlyGuard`` for the whole call
    so no code path in this function — nor anything it calls — can reach a
    mutating GitHub effect; the returned ``guard`` lets callers assert zero
    attempted mutations, and the underlying mock/stub passed in as
    ``github`` will show zero actual calls.
    """
    guard = ReadOnlyGuard(github)

    # Double dedup, part 1: before prototyping.
    dedup_index.check(title)

    # No patch candidate without a captured red reproducer / design spike.
    require_reproducer(evidence)

    # Isolated worktree/branch — never the default branch.
    worktree = PrototypeWorktree.create(
        repo_root, branch, worktree_dir, default_branch, runner=runner
    )

    # Double dedup, part 2: after prototyping, before promotion.
    dedup_index.check(title)
    dedup_index.record(title)

    # Independent judge decides ACCEPT | REVISE | REJECT.
    verdict = judge_candidate(candidate_id, judge_id, creator_id, verdict_kind, verdict_reasons)

    result = PrototypeStageResult(
        candidate_id=candidate_id,
        evidence=evidence,
        worktree=worktree,
        guard=guard,
        verdict=verdict,
    )

    if verdict.kind == JudgeVerdictKind.ACCEPT:
        result.handoff = DeliveryHandoff(verdict=verdict, delivery_owner=delivery_owner)

    return result
