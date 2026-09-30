import os
import shutil
import tempfile
import difflib
from pathlib import Path
from typing import List, Optional, Tuple


def read_file(file_path: str, max_bytes: int = 1000000, encoding: str = "utf-8") -> str:
    """Safely read content from a file."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(path, "r", encoding=encoding, errors="replace") as f:
        return f.read(max_bytes)


def write_file(file_path: str, content: str, encoding: str = "utf-8") -> None:
    """Safely write content to a file, creating parent directories if needed."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        f.write(content)


def backup_file(file_path: str) -> str:
    """Create a backup copy of a file."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Cannot backup non-existent file: {file_path}")
    
    backup_path = f"{file_path}.bugify.bak"
    shutil.copy2(path, backup_path)
    return backup_path


def restore_file(backup_path: str, target_path: Optional[str] = None) -> None:
    """Restore a file from its backup copy."""
    src = Path(backup_path)
    if not src.is_file():
        raise FileNotFoundError(f"Backup file not found: {backup_path}")
    
    if target_path is None:
        if backup_path.endswith(".bugify.bak"):
            dest = Path(backup_path[:-11])
        else:
            raise ValueError("Target path must be specified if backup does not end with .bugify.bak")
    else:
        dest = Path(target_path)
    
    shutil.copy2(src, dest)
    try:
        src.unlink()
    except OSError:
        pass


def list_files(
    directory: str,
    extensions: Optional[List[str]] = None,
    max_depth: int = 10,
    ignored_patterns: Optional[List[str]] = None
) -> List[str]:
    """List relative file paths in a directory matching extensions and ignoring common junk."""
    base = Path(directory)
    if not base.is_dir():
        return []
    
    if ignored_patterns is None:
        ignored_patterns = [
            ".git", ".venv", "venv", "__pycache__", "node_modules",
            ".pytest_cache", ".mypy_cache", ".idea", ".vscode", "dist", "build"
        ]
    
    matched = []
    
    for root, dirs, files in os.walk(base):
        # Filter dirs in-place to avoid traversing ignored folders
        dirs[:] = [d for d in dirs if d not in ignored_patterns and not d.startswith(".")]
        
        rel_root = os.path.relpath(root, base)
        depth = 0 if rel_root == "." else len(Path(rel_root).parts)
        if depth > max_depth:
            continue
            
        for file in files:
            if extensions:
                if any(file.endswith(ext) for ext in extensions):
                    rel_path = os.path.normpath(os.path.join(rel_root, file)) if rel_root != "." else file
                    matched.append(rel_path.replace("\\", "/"))
            else:
                rel_path = os.path.normpath(os.path.join(rel_root, file)) if rel_root != "." else file
                matched.append(rel_path.replace("\\", "/"))
                
    return sorted(matched)


def apply_patch_to_string(original_text: str, patch_text: str) -> str:
    """Apply a unified diff patch to a string in-memory."""
    # Basic unified diff patch applier for python strings
    orig_lines = original_text.splitlines(keepends=True)
    patch_lines = patch_text.splitlines(keepends=True)
    
    # Check if patch looks like unified diff
    in_hunk = False
    result_lines = []
    i = 0
    
    # We can use difflib or patch parsing
    for line in patch_lines:
        if line.startswith("---") or line.startswith("+++"):
            continue
        elif line.startswith("@@"):
            in_hunk = True
            continue
        elif in_hunk:
            if line.startswith("-"):
                # line deleted
                if i < len(orig_lines):
                    i += 1
            elif line.startswith("+"):
                # line added
                result_lines.append(line[1:])
            elif line.startswith(" "):
                # line unchanged
                if i < len(orig_lines):
                    result_lines.append(orig_lines[i])
                    i += 1
                else:
                    result_lines.append(line[1:])
    
    # Append any remaining lines
    while i < len(orig_lines):
        result_lines.append(orig_lines[i])
        i += 1
        
    return "".join(result_lines)
