import os
import subprocess
import time
from typing import Dict, List, Optional
from schemas.test import SandboxExecutionResult


class ShellTool:
    """Safe subprocess execution tool for running scripts and tests."""

    def __init__(self, default_timeout: int = 30):
        self.default_timeout = default_timeout

    def run_command(
        self,
        command: List[str] | str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        shell: bool = False,
    ) -> SandboxExecutionResult:
        """Run a command in a controlled subprocess."""
        timeout = timeout or self.default_timeout
        start_time = time.time()
        
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)

        try:
            process = subprocess.run(
                command,
                cwd=cwd,
                env=merged_env,
                capture_output=True,
                text=True,
                shell=shell,
                timeout=timeout,
            )
            duration = time.time() - start_time
            return SandboxExecutionResult(
                exit_code=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr,
                duration=duration,
                timed_out=False,
                isolated=False,
            )
        except subprocess.TimeoutExpired as e:
            duration = time.time() - start_time
            stdout = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
            stderr = e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
            return SandboxExecutionResult(
                exit_code=-1,
                stdout=stdout,
                stderr=f"{stderr}\nCommand timed out after {timeout} seconds.",
                duration=duration,
                timed_out=True,
                isolated=False,
            )
        except Exception as e:
            duration = time.time() - start_time
            return SandboxExecutionResult(
                exit_code=-1,
                stdout="",
                stderr=f"Error executing command: {str(e)}",
                duration=duration,
                timed_out=False,
                isolated=False,
            )
