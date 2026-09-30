from typing import Dict, Optional
from schemas.test import TestSuiteResult


class RegressionTester:
    """Detects regressions by comparing test results before and after a patch."""

    def compare(
        self,
        baseline: TestSuiteResult,
        patched: TestSuiteResult,
    ) -> Dict:
        """
        Compare baseline and post-patch test results.

        Returns a regression report indicating whether any previously
        passing tests now fail.
        """
        baseline_passing = {c.name for c in baseline.cases if c.status.value == "passed"}
        patched_failing = {c.name for c in patched.cases if c.status.value == "failed"}

        regressions = list(baseline_passing & patched_failing)
        newly_passing = [
            c.name for c in patched.cases
            if c.status.value == "passed"
            and c.name not in {x.name for x in baseline.cases if x.status.value == "passed"}
        ]

        regression_detected = len(regressions) > 0

        return {
            "regression_detected": regression_detected,
            "regressed_tests": regressions,
            "newly_passing_tests": newly_passing,
            "baseline_passed": baseline.passed,
            "patched_passed": patched.passed,
            "baseline_failed": baseline.failed,
            "patched_failed": patched.failed,
            "summary": (
                f"{'REGRESSION DETECTED: ' + str(len(regressions)) + ' tests newly failing.' if regression_detected else 'No regressions detected.'} "
                f"Pass rate: {baseline.passed} → {patched.passed} | Fail rate: {baseline.failed} → {patched.failed}"
            ),
        }
