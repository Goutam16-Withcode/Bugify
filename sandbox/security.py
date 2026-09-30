"""
sandbox/security.py — Security policies for sandbox execution.

Defines what is permitted in isolated execution environments.
Full Docker isolation is controlled here.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SandboxPolicy:
    """Execution security policy for the sandbox."""

    # Maximum wall-clock time in seconds
    timeout_seconds: int = 60

    # Disable network access (only enforced in Docker)
    network_disabled: bool = True

    # Maximum memory in MB (only enforced in Docker)
    memory_limit_mb: int = 512

    # Allowed environment variable names (whitelist)
    allowed_env_vars: List[str] = field(default_factory=lambda: ["PATH", "PYTHONPATH", "HOME"])

    # Read-only filesystem mounts (Docker only)
    readonly_mounts: List[str] = field(default_factory=list)

    # Run as non-root (Docker only)
    run_as_nonroot: bool = True

    # Maximum output bytes before truncation
    max_output_bytes: int = 1_000_000

    @classmethod
    def permissive(cls) -> "SandboxPolicy":
        """Relaxed policy for local development."""
        return cls(
            timeout_seconds=120,
            network_disabled=False,
            memory_limit_mb=2048,
            run_as_nonroot=False,
        )

    @classmethod
    def strict(cls) -> "SandboxPolicy":
        """Strict production policy."""
        return cls(
            timeout_seconds=30,
            network_disabled=True,
            memory_limit_mb=256,
            run_as_nonroot=True,
        )
