import re
import sys
from typing import Optional, List
from schemas.test import TestSuiteResult, TestCaseResult, TestStatus
from tools.shell_tools import ShellTool


class TestTool:
    """Tool for running Python tests and parsing structured outputs."""

    def __init__(self, shell_tool: Optional[ShellTool] = None):
        self.shell = shell_tool or ShellTool(default_timeout=60)

    def run_pytest(
        self,
        repo_path: str,
        test_target: Optional[str] = None,
        timeout: int = 60,
        extra_args: Optional[List[str]] = None,
    ) -> TestSuiteResult:
        """Run pytest in the given repo path and parse outcomes."""
        python_exe = sys.executable
        cmd = [python_exe, "-m", "pytest", "-v", "--tb=short"]
        if extra_args:
            cmd.extend(extra_args)
        if test_target:
            cmd.append(test_target)

        res = self.shell.run_command(cmd, cwd=repo_path, timeout=timeout)
        return self._parse_pytest_output(res.stdout, res.stderr, res.exit_code, res.duration)

    def _parse_pytest_output(
        self,
        stdout: str,
        stderr: str,
        exit_code: int,
        duration: float,
    ) -> TestSuiteResult:
        combined = f"{stdout}\n{stderr}"
        cases: List[TestCaseResult] = []

        # Parse test lines like: tests/test_foo.py::test_bar PASSED [ 50%]
        line_pattern = re.compile(r"^([\w/\\._\-:]+)\s+(PASSED|FAILED|SKIPPED|ERROR)", re.MULTILINE)
        for match in line_pattern.finditer(stdout):
            name, status_str = match.groups()
            status_map = {
                "PASSED": TestStatus.PASSED,
                "FAILED": TestStatus.FAILED,
                "SKIPPED": TestStatus.SKIPPED,
                "ERROR": TestStatus.ERROR,
            }
            cases.append(TestCaseResult(name=name, status=status_map.get(status_str, TestStatus.FAILED)))

        # Summary line pattern: 2 failed, 10 passed, 1 skipped in 1.23s
        passed = len([c for c in cases if c.status == TestStatus.PASSED])
        failed = len([c for c in cases if c.status == TestStatus.FAILED])
        skipped = len([c for c in cases if c.status == TestStatus.SKIPPED])
        errors = len([c for c in cases if c.status == TestStatus.ERROR])

        summary_match = re.search(r"(=+)\s*(.*?)\s*in\s*([\d\.]+)s", stdout)
        if summary_match:
            summary_text = summary_match.group(2)
            passed_m = re.search(r"(\d+)\s+passed", summary_text)
            failed_m = re.search(r"(\d+)\s+failed", summary_text)
            skipped_m = re.search(r"(\d+)\s+skipped", summary_text)
            error_m = re.search(r"(\d+)\s+error", summary_text)

            if passed_m:
                passed = int(passed_m.group(1))
            if failed_m:
                failed = int(failed_m.group(1))
            if skipped_m:
                skipped = int(skipped_m.group(1))
            if error_m:
                errors = int(error_m.group(1))

        total = passed + failed + skipped + errors
        if total == 0 and exit_code != 0:
            # Maybe collection error or module import failure
            errors = 1
            total = 1

        return TestSuiteResult(
            total=total,
            passed=passed,
            failed=failed,
            skipped=skipped,
            errors=errors,
            duration=duration,
            cases=cases,
            raw_output=combined.strip(),
            exit_code=exit_code,
        )
