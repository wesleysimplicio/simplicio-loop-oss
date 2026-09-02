#!/usr/bin/env python3
"""Fail-closed line and branch coverage gate for CI.

The input is the JSON report emitted by coverage.py with ``--branch``.  The
gate computes rates from counts instead of trusting derived percentage fields,
so a truncated or hand-written report cannot silently pass.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


class CoverageGateError(ValueError):
    """Raised when a coverage report is missing or structurally invalid."""


def _count(totals: dict[str, Any], name: str) -> int:
    value = totals.get(name)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise CoverageGateError(f"totals.{name} must be a non-negative integer")
    return value


def _threshold(value: float, name: str) -> float:
    if not math.isfinite(value) or not 0 <= value <= 100:
        raise CoverageGateError(f"{name} must be finite and between 0 and 100")
    return value


def _rate(covered: int, total: int) -> float:
    # A branchless project has no branch opportunities to miss; it is fully
    # covered for the purpose of a branch threshold. Missing branch fields are
    # still rejected by _count, so coverage must have been run with --branch.
    return 100.0 if total == 0 else 100.0 * covered / total


def evaluate_report(
    report: Any, *, min_line: float, min_branch: float
) -> dict[str, float | int | bool]:
    """Validate a coverage.py report and return deterministic gate metrics."""
    min_line = _threshold(min_line, "min_line")
    min_branch = _threshold(min_branch, "min_branch")
    if not isinstance(report, dict) or not isinstance(report.get("totals"), dict):
        raise CoverageGateError("report must contain a totals object")

    totals = report["totals"]
    statements = _count(totals, "num_statements")
    covered_lines = _count(totals, "covered_lines")
    branches = _count(totals, "num_branches")
    covered_branches = _count(totals, "covered_branches")
    if statements == 0:
        raise CoverageGateError("totals.num_statements must be greater than zero")
    if covered_lines > statements:
        raise CoverageGateError("totals.covered_lines exceeds num_statements")
    if covered_branches > branches:
        raise CoverageGateError("totals.covered_branches exceeds num_branches")

    line_rate = 100.0 * covered_lines / statements
    branch_rate = _rate(covered_branches, branches)
    return {
        "covered_lines": covered_lines,
        "num_statements": statements,
        "line_rate": line_rate,
        "covered_branches": covered_branches,
        "num_branches": branches,
        "branch_rate": branch_rate,
        "line_pass": line_rate >= min_line,
        "branch_pass": branch_rate >= min_branch,
    }


def read_report(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as stream:
            return json.load(stream)
    except FileNotFoundError as exc:
        raise CoverageGateError(f"coverage report not found: {path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise CoverageGateError(f"cannot read coverage report {path}: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage-file", type=Path, required=True)
    parser.add_argument("--min-line", type=float, required=True)
    parser.add_argument("--min-branch", type=float, required=True)
    args = parser.parse_args(argv)

    try:
        metrics = evaluate_report(
            read_report(args.coverage_file),
            min_line=args.min_line,
            min_branch=args.min_branch,
        )
    except CoverageGateError as exc:
        print(f"coverage gate: invalid report: {exc}", file=sys.stderr)
        return 2

    print(
        "coverage gate: "
        f"lines={metrics['line_rate']:.2f}% "
        f"({metrics['covered_lines']}/{metrics['num_statements']}), "
        f"branches={metrics['branch_rate']:.2f}% "
        f"({metrics['covered_branches']}/{metrics['num_branches']})"
    )
    failures = []
    if not metrics["line_pass"]:
        failures.append(f"line coverage below {args.min_line:.2f}%")
    if not metrics["branch_pass"]:
        failures.append(f"branch coverage below {args.min_branch:.2f}%")
    if failures:
        print("coverage gate: FAILED — " + "; ".join(failures), file=sys.stderr)
        return 1
    print("coverage gate: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
