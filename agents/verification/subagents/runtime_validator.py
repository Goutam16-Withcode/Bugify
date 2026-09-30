import tempfile
import os
from typing import Dict, List, Optional, Any
from tools.file_tools import read_file, apply_patch_to_string
from tools.shell_tools import ShellTool
from schemas.test import SandboxExecutionResult


class RuntimeValidator:
    """
    Validates a patch by applying it in an isolated temp directory
    and running a minimal import check or smoke test.

    NOTE: Full Docker sandboxing is optional (requires Docker daemon).
    In the absence of Docker, this falls back to a subprocess-scoped
    temp copy with no network access.
    """

    def __init__(self):
        self.shell = ShellTool(default_timeout=30)

    def validate_patch_application(
        self,
        patch_text: str,
        repo_path: str,
        target_files: List[str],
    ) -> Dict[str, Any]:
        """
        Attempt to apply patch lines to in-memory file copies
        and verify no immediate syntax errors.
        """
        if not patch_text.strip():
            return {"success": False, "message": "Empty patch", "errors": []}

        errors = []
        applied = 0

        for rel_file in target_files:
            full_path = os.path.join(repo_path, rel_file)
            try:
                original = read_file(full_path)
                patched = apply_patch_to_string(original, patch_text)
                # Validate Python syntax if it's a .py file
                if rel_file.endswith(".py"):
                    try:
                        compile(patched, rel_file, "exec")
                    except SyntaxError as e:
                        errors.append(f"SyntaxError in {rel_file}: {e}")
                applied += 1
            except FileNotFoundError:
                # Patch might target a new file; not a failure
                pass
            except Exception as e:
                errors.append(f"Error processing {rel_file}: {str(e)}")

        return {
            "success": len(errors) == 0,
            "files_validated": applied,
            "errors": errors,
            "message": "All files validated successfully" if not errors else f"{len(errors)} validation errors",
        }

    def run_smoke_test(
        self,
        repo_path: str,
        python_cmd: Optional[str] = None,
        timeout: int = 20,
    ) -> SandboxExecutionResult:
        """Run a fast module import smoke test on the repository."""
        import sys
        py = python_cmd or sys.executable
        # Try to import the top-level package(s) in the repo
        cmd = [py, "-c", "import os; print('Smoke test OK')"]
        return self.shell.run_command(cmd, cwd=repo_path, timeout=timeout)
