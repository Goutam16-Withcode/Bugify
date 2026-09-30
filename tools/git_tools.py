import os
import subprocess
from typing import Dict, List, Optional, Tuple

try:
    import git
    HAS_GITPYTHON = True
except ImportError:
    HAS_GITPYTHON = False


class GitTool:
    """Git operations tool with GitPython and subprocess fallback."""

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self._repo = None
        if HAS_GITPYTHON:
            try:
                self._repo = git.Repo(repo_path)
            except Exception:
                self._repo = None

    def is_git_repo(self) -> bool:
        if self._repo is not None:
            return True
        git_dir = os.path.join(self.repo_path, ".git")
        return os.path.exists(git_dir)

    def get_status(self) -> Dict[str, List[str]]:
        """Return modified, untracked, and staged files."""
        if not self.is_git_repo():
            return {"modified": [], "untracked": [], "staged": []}

        if self._repo:
            try:
                return {
                    "modified": [item.a_path for item in self._repo.index.diff(None)],
                    "untracked": self._repo.untracked_files,
                    "staged": [item.a_path for item in self._repo.index.diff("HEAD")] if self._repo.head.is_valid() else [],
                }
            except Exception:
                pass

        # Fallback to subprocess
        try:
            res = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10,
            )
            modified, untracked, staged = [], [], []
            for line in res.stdout.splitlines():
                if len(line) < 3:
                    continue
                code = line[:2]
                filename = line[3:].strip()
                if code.startswith("?"):
                    untracked.append(filename)
                elif code[1] == "M":
                    modified.append(filename)
                elif code[0] in ("M", "A"):
                    staged.append(filename)
            return {"modified": modified, "untracked": untracked, "staged": staged}
        except Exception:
            return {"modified": [], "untracked": [], "staged": []}

    def get_diff(self, file_path: Optional[str] = None) -> str:
        """Get git diff for repo or single file."""
        if not self.is_git_repo():
            return ""

        try:
            cmd = ["git", "diff"]
            if file_path:
                cmd.append(file_path)
            res = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True, timeout=10)
            return res.stdout
        except Exception:
            return ""

    def apply_patch(self, patch_content: str) -> Tuple[bool, str]:
        """Apply a unified diff patch to the repository."""
        if not patch_content.strip():
            return False, "Patch content is empty"

        # Try git apply via stdin
        try:
            res = subprocess.run(
                ["git", "apply", "--ignore-space-change", "--whitespace=nowarn", "-"],
                input=patch_content,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=15,
            )
            if res.returncode == 0:
                return True, "Patch applied successfully via git apply"
            return False, f"git apply failed: {res.stderr or res.stdout}"
        except Exception as e:
            return False, f"Exception during git apply: {str(e)}"

    def create_branch(self, branch_name: str) -> bool:
        """Create and checkout a new branch for testing the fix."""
        if not self.is_git_repo():
            return False
        try:
            res = subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10,
            )
            return res.returncode == 0
        except Exception:
            return False

    def reset_hard(self) -> bool:
        """Reset repository to HEAD and clean untracked files."""
        if not self.is_git_repo():
            return False
        try:
            subprocess.run(["git", "reset", "--hard", "HEAD"], cwd=self.repo_path, capture_output=True, timeout=10)
            subprocess.run(["git", "clean", "-fd"], cwd=self.repo_path, capture_output=True, timeout=10)
            return True
        except Exception:
            return False
