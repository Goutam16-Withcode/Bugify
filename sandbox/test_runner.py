"""
sandbox/test_runner.py — Runs tests inside the sandbox (Docker or subprocess).
"""

import sys
from typing import Optional, List
from sandbox.docker_manager import DockerManager
from sandbox.security import SandboxPolicy
from tools.test_tools import TestTool
from tools.shell_tools import ShellTool
from schemas.test import TestSuiteResult


class SandboxTestRunner:
    """
    Runs test suites in the most isolated environment available.

    Priority: Docker → subprocess
    """

    def __init__(self, policy: Optional[SandboxPolicy] = None):
        self.policy = policy or SandboxPolicy()
        self.docker = DockerManager()
        self.shell_tool = ShellTool(default_timeout=self.policy.timeout_seconds)
        self.test_tool = TestTool(self.shell_tool)

    def run(
        self,
        repo_path: str,
        test_target: Optional[str] = None,
        extra_args: Optional[List[str]] = None,
    ) -> TestSuiteResult:
        """Run tests and return structured results."""
        if self.docker.is_available():
            cmd = "python -m pytest -v --tb=short"
            if test_target:
                cmd += f" {test_target}"
            result = self.docker.run_in_container(
                command=cmd,
                repo_path=repo_path,
                timeout=self.policy.timeout_seconds,
                memory_mb=self.policy.memory_limit_mb,
                network_disabled=self.policy.network_disabled,
            )
            return self.test_tool._parse_pytest_output(
                result["stdout"], result["stderr"],
                result["exit_code"], 0.0
            )
        else:
            return self.test_tool.run_pytest(
                repo_path=repo_path,
                test_target=test_target,
                timeout=self.policy.timeout_seconds,
                extra_args=extra_args,
            )
