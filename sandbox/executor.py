"""
sandbox/executor.py — High-level sandbox execution API.
"""

from typing import Optional, List
from sandbox.docker_manager import DockerManager
from sandbox.security import SandboxPolicy
from sandbox.test_runner import SandboxTestRunner
from tools.shell_tools import ShellTool
from schemas.test import SandboxExecutionResult, TestSuiteResult


class SandboxExecutor:
    """Unified API for executing code and tests in an isolated environment."""

    def __init__(self, policy: Optional[SandboxPolicy] = None):
        self.policy = policy or SandboxPolicy()
        self.docker = DockerManager()
        self.shell = ShellTool(default_timeout=self.policy.timeout_seconds)
        self.test_runner = SandboxTestRunner(policy=self.policy)

    def run_command(
        self,
        command: str | List[str],
        repo_path: str,
        use_docker: bool = False,
    ) -> SandboxExecutionResult:
        """Run an arbitrary command in the sandbox."""
        if use_docker and self.docker.is_available():
            cmd_str = command if isinstance(command, str) else " ".join(command)
            result = self.docker.run_in_container(
                command=cmd_str,
                repo_path=repo_path,
                timeout=self.policy.timeout_seconds,
                memory_mb=self.policy.memory_limit_mb,
                network_disabled=self.policy.network_disabled,
            )
            return SandboxExecutionResult(
                exit_code=result["exit_code"],
                stdout=result["stdout"],
                stderr=result["stderr"],
                timed_out=result.get("timed_out", False),
                isolated=True,
            )
        else:
            cmd = command.split() if isinstance(command, str) else command
            result = self.shell.run_command(cmd, cwd=repo_path, timeout=self.policy.timeout_seconds)
            return result

    def run_tests(
        self,
        repo_path: str,
        test_target: Optional[str] = None,
    ) -> TestSuiteResult:
        """Execute test suite in isolated sandbox environment."""
        return self.test_runner.run(repo_path=repo_path, test_target=test_target)
