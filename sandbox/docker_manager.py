"""
sandbox/docker_manager.py — Optional Docker sandbox management.

Requires: docker Python SDK (`pip install docker`) and Docker daemon running.
Falls back gracefully if Docker is unavailable.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

try:
    import docker
    from docker.errors import DockerException
    HAS_DOCKER = True
except ImportError:
    HAS_DOCKER = False


class DockerManager:
    """Manages Docker containers for isolated code execution."""

    IMAGE = "python:3.11-slim"

    def __init__(self):
        self.client = None
        self.available = False
        if HAS_DOCKER:
            try:
                self.client = docker.from_env(timeout=5)
                self.client.ping()
                self.available = True
                logger.info("Docker daemon connected successfully")
            except Exception as e:
                logger.warning(f"Docker unavailable: {e}. Falling back to subprocess sandbox.")

    def is_available(self) -> bool:
        return self.available

    def run_in_container(
        self,
        command: str,
        repo_path: str,
        timeout: int = 60,
        memory_mb: int = 512,
        network_disabled: bool = True,
    ) -> dict:
        """
        Run a command inside an isolated Docker container.

        Args:
            command: Shell command string to execute
            repo_path: Host path to mount as /workspace (read-only)
            timeout: Max execution time in seconds
            memory_mb: Memory limit for the container
            network_disabled: Disable network access

        Returns:
            {"exit_code": int, "stdout": str, "stderr": str, "timed_out": bool}
        """
        if not self.available or not self.client:
            return {
                "exit_code": -1,
                "stdout": "",
                "stderr": "Docker is not available on this host.",
                "timed_out": False,
            }

        volumes = {os.path.abspath(repo_path): {"bind": "/workspace", "mode": "ro"}}

        try:
            container = self.client.containers.run(
                image=self.IMAGE,
                command=f"timeout {timeout} sh -c '{command}'",
                working_dir="/workspace",
                volumes=volumes,
                mem_limit=f"{memory_mb}m",
                network_disabled=network_disabled,
                remove=True,
                detach=False,
                stdout=True,
                stderr=True,
            )
            if isinstance(container, bytes):
                output = container.decode("utf-8", errors="replace")
                return {"exit_code": 0, "stdout": output, "stderr": "", "timed_out": False}
            return {"exit_code": 0, "stdout": str(container), "stderr": "", "timed_out": False}

        except Exception as e:
            return {"exit_code": -1, "stdout": "", "stderr": str(e), "timed_out": False}
