import re
import sys
import tempfile
import os
from typing import Dict, List, Optional, Any
from tools.shell_tools import ShellTool
from tools.test_tools import TestTool
from schemas.test import VerificationVerdict, TestSuiteResult


class TestExecutor:
    """Executes test suites against a repository and optionally applies a patch first."""

    def __init__(self):
        self.shell = ShellTool(default_timeout=120)
        self.test_tool = TestTool(self.shell)

    def run_tests(
        self,
        repo_path: str,
        test_directory: str = "tests",
        timeout: int = 120,
        patch_applied: bool = False,
    ) -> TestSuiteResult:
        """Run pytest inside the given repository."""
        test_path = os.path.join(repo_path, test_directory) if test_directory else repo_path
        if not os.path.exists(test_path):
            # Fall back to repo root
            test_path = repo_path

        return self.test_tool.run_pytest(
            repo_path=repo_path,
            test_target=test_path,
            timeout=timeout,
        )

    def validate_syntax(self, patch_text: str) -> Optional[str]:
        """Attempt to detect Python syntax errors inside a patch."""
        # Extract added lines from the patch
        added_lines = []
        for line in patch_text.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                added_lines.append(line[1:])

        code_to_check = "\n".join(added_lines)
        try:
            compile(code_to_check, "<patch>", "exec")
            return None  # No syntax error
        except SyntaxError as e:
            return f"SyntaxError in patch at line {e.lineno}: {e.msg}"
