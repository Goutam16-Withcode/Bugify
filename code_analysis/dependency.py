import re
from pathlib import Path
from typing import Dict, List, Set


class DependencyGraph:
    """Extracts internal and external dependencies across python files."""

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def extract_requirements(self) -> List[str]:
        """Extract declared dependencies from requirements.txt or pyproject.toml."""
        req_file = self.repo_path / "requirements.txt"
        packages = []
        if req_file.exists():
            with open(req_file, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and not line.startswith("-"):
                        # Extract pkg name without version specs
                        pkg = re.split(r"[><=~]", line)[0].strip()
                        if pkg:
                            packages.append(pkg)
        return packages

    def build_import_graph(self, files: List[str]) -> Dict[str, List[str]]:
        """Map each file to modules it imports."""
        graph = {}
        for rel_file in files:
            full_path = self.repo_path / rel_file
            if not full_path.is_file() or full_path.suffix != ".py":
                continue
            
            imports = set()
            try:
                with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("import "):
                            parts = line[7:].split(",")
                            for p in parts:
                                mod = p.strip().split()[0].split(".")[0]
                                imports.add(mod)
                        elif line.startswith("from "):
                            parts = line[5:].split(" import ")
                            if parts:
                                mod = parts[0].strip().split(".")[0]
                                imports.add(mod)
            except Exception:
                pass
            graph[rel_file] = sorted(list(imports))
        return graph
