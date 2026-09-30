from pathlib import Path
from typing import Dict, List, Any
from code_analysis.file_utils import get_source_files, read_source_safely
from code_analysis.parser import CodeParser
from code_analysis.dependency import DependencyGraph


class RepositoryIndex:
    """Indexes a repository's source files, symbols, and dependencies."""

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.dep_graph = DependencyGraph(repo_path)

    def index(self) -> Dict[str, Any]:
        """Perform a structured indexing of the repository."""
        source_files = get_source_files(str(self.repo_path))
        py_files = [f for f in source_files if f.endswith(".py")]

        file_symbols = {}
        for f in py_files:
            full_path = self.repo_path / f
            code = read_source_safely(str(full_path))
            parsed = CodeParser.parse_python(code, filename=f)
            file_symbols[f] = {
                "functions": [fn["name"] for fn in parsed["functions"]],
                "classes": [cl["name"] for cl in parsed["classes"]],
                "valid": parsed["valid"],
            }

        return {
            "root": str(self.repo_path),
            "total_files": len(source_files),
            "source_files": source_files,
            "python_files": py_files,
            "declared_dependencies": self.dep_graph.extract_requirements(),
            "import_graph": self.dep_graph.build_import_graph(py_files),
            "symbols": file_symbols,
        }
