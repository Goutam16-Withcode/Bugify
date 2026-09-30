import os
from pathlib import Path
from typing import List, Optional, Set


def get_source_files(
    repo_path: str,
    allowed_extensions: Optional[Set[str]] = None,
    exclude_dirs: Optional[Set[str]] = None,
) -> List[str]:
    """Find all source files in repository path."""
    allowed = allowed_extensions or {".py", ".json", ".yaml", ".yml", ".md", ".txt", ".toml"}
    excluded = exclude_dirs or {
        ".git", ".venv", "venv", "__pycache__", "node_modules",
        ".pytest_cache", ".mypy_cache", ".idea", ".vscode", "dist", "build"
    }

    base = Path(repo_path)
    if not base.exists():
        return []

    source_files = []
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in excluded and not d.startswith(".")]
        for file in files:
            path = Path(root) / file
            if path.suffix.lower() in allowed:
                try:
                    rel = path.relative_to(base).as_posix()
                    source_files.append(rel)
                except ValueError:
                    pass

    return sorted(source_files)


def read_source_safely(file_path: str, max_lines: int = 2000) -> str:
    """Read source file contents safely with line cap."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = [f.readline() for _ in range(max_lines)]
            return "".join(lines)
    except Exception as e:
        return f"# Error reading file {file_path}: {e}"
