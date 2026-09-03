from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts import check_coverage_gate as gate


def _report(**totals):
    return {"meta": {"version": "7.6.12"}, "totals": totals}


class CoverageGateTests(unittest.TestCase):
    def _cli_result(self, totals):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "coverage.json"
            report.write_text(json.dumps(_report(**totals)), encoding="utf-8")
            return gate.main(
                [
                    "--coverage-file",
                    str(report),
                    "--min-line",
                    "90",
                    "--min-branch",
                    "80",
                ]
            )

    def test_passes_when_line_and_branch_thresholds_are_met(self):
        metrics = gate.evaluate_report(
            _report(
                num_statements=100,
                covered_lines=95,
                num_branches=20,
                covered_branches=17,
            ),
            min_line=90,
            min_branch=80,
        )
        self.assertTrue(metrics["line_pass"])
        self.assertTrue(metrics["branch_pass"])
        self.assertEqual(metrics["line_rate"], 95.0)
        self.assertEqual(metrics["branch_rate"], 85.0)

    def test_rejects_below_threshold_line_coverage(self):
        metrics = gate.evaluate_report(
            _report(
                num_statements=10,
                covered_lines=8,
                num_branches=2,
                covered_branches=2,
            ),
            min_line=90,
            min_branch=80,
        )
        self.assertFalse(metrics["line_pass"])
        self.assertTrue(metrics["branch_pass"])

    def test_rejects_below_threshold_branch_coverage(self):
        metrics = gate.evaluate_report(
            _report(
                num_statements=10,
                covered_lines=10,
                num_branches=4,
                covered_branches=3,
            ),
            min_line=90,
            min_branch=80,
        )
        self.assertTrue(metrics["line_pass"])
        self.assertFalse(metrics["branch_pass"])

    def test_rejects_impossible_counts(self):
        with self.assertRaisesRegex(gate.CoverageGateError, "exceeds"):
            gate.evaluate_report(
                _report(
                    num_statements=2,
                    covered_lines=3,
                    num_branches=0,
                    covered_branches=0,
                ),
                min_line=90,
                min_branch=80,
            )

    def test_cli_fails_closed_for_missing_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = gate.main(
                [
                    "--coverage-file",
                    str(Path(tmp) / "missing.json"),
                    "--min-line",
                    "90",
                    "--min-branch",
                    "80",
                ]
            )
        self.assertEqual(result, 2)

    def test_cli_accepts_valid_coverage_json(self):
        self.assertEqual(
            self._cli_result(
                dict(
                    num_statements=4,
                    covered_lines=4,
                    num_branches=2,
                    covered_branches=2,
                )
            ),
            0,
        )

    def test_cli_returns_failure_when_threshold_is_missed(self):
        self.assertEqual(
            self._cli_result(
                dict(
                    num_statements=10,
                    covered_lines=9,
                    num_branches=10,
                    covered_branches=7,
                )
            ),
            1,
        )
