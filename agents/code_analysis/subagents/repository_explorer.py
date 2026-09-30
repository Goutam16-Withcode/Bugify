from pathlib import Path
from typing import Dict, List


class RepositoryExplorer:
    """
    Explores a repository and identifies:
    - Project type
    - Source files
    - Test files
    - Configuration files
    - Entry points
    """

    IGNORED_DIRECTORIES = {
        ".git",
        ".venv",
        "venv",
        "env",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "node_modules",
        "dist",
        "build",
        ".idea",
        ".vscode",
        ".tox",
        ".eggs",
    }

    SOURCE_EXTENSIONS = {
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".go",
        ".rs",
    }

    CONFIG_FILES = {
        "requirements.txt",
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
        "Pipfile",
        "Pipfile.lock",
        "poetry.lock",
        "environment.yml",
        "environment.yaml",
        "package.json",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        ".env.example",
    }

    ENTRY_POINT_NAMES = {
        "main.py",
        "app.py",
        "server.py",
        "run.py",
        "__main__.py",
        "main.js",
        "app.js",
        "server.js",
        "index.js",
        "main.ts",
        "app.ts",
        "server.ts",
        "index.ts",
    }

    def explore(self, repository_path: str) -> Dict:
        """
        Explore a repository and return a structured summary.
        """

        root = Path(repository_path)

        if not root.exists():
            raise FileNotFoundError(
                f"Repository does not exist: {repository_path}"
            )

        if not root.is_dir():
            raise NotADirectoryError(
                f"Repository path is not a directory: {repository_path}"
            )

        source_files: List[str] = []
        test_files: List[str] = []
        config_files: List[str] = []
        entry_points: List[str] = []

        for path in root.rglob("*"):

            if not path.is_file():
                continue

            relative_path = path.relative_to(root)
            parts = set(relative_path.parts)

            if parts.intersection(self.IGNORED_DIRECTORIES):
                continue

            relative = relative_path.as_posix()

            # Configuration files
            if path.name in self.CONFIG_FILES:
                config_files.append(relative)

            # Source files
            if path.suffix.lower() in self.SOURCE_EXTENSIONS:
                if not self._is_test_file(path):
                    source_files.append(relative)

            # Test files
            if self._is_test_file(path):
                test_files.append(relative)

            # Entry points
            if path.name in self.ENTRY_POINT_NAMES:
                entry_points.append(relative)

        project_type = self._detect_project_type(
            root=root,
            source_files=source_files,
            config_files=config_files,
        )

        return {
            "project_type": project_type,
            "source_files": sorted(source_files),
            "test_files": sorted(test_files),
            "config_files": sorted(config_files),
            "entry_points": sorted(entry_points),
        }

    def _is_test_file(self, path: Path) -> bool:
        """
        Determine whether a file is a test file.
        """

        name = path.name.lower()
        path_parts = {part.lower() for part in path.parts}

        if "tests" in path_parts or "test" in path_parts:
            return True

        if name.startswith("test_"):
            return True

        if name.endswith("_test.py"):
            return True

        if name.endswith(".test.js"):
            return True

        if name.endswith(".test.ts"):
            return True

        if name.endswith(".spec.js"):
            return True

        if name.endswith(".spec.ts"):
            return True

        return False

    def _detect_project_type(
        self,
        root: Path,
        source_files: List[str],
        config_files: List[str],
    ) -> str:
        """
        Detect the primary project type.
        """

        config_set = set(config_files)

        if "pyproject.toml" in config_set:
            return "python"

        if "requirements.txt" in config_set:
            return "python"

        if "setup.py" in config_set:
            return "python"

        if "package.json" in config_set:
            return "javascript"

        extensions = {
            Path(file).suffix.lower()
            for file in source_files
        }

        if ".py" in extensions:
            return "python"

        if ".ts" in extensions or ".tsx" in extensions:
            return "typescript"

        if ".js" in extensions or ".jsx" in extensions:
            return "javascript"

        if ".java" in extensions:
            return "java"

        if ".go" in extensions:
            return "go"

        if ".rs" in extensions:
            return "rust"

        if ".cpp" in extensions or ".c" in extensions:
            return "cpp"

        return "unknown"