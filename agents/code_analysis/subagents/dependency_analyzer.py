from pathlib import Path
from typing import Dict, List, Set
import ast


class DependencyAnalyzer:
    """
    Analyzes Python dependencies and import relationships
    inside a repository.
    """

    IGNORED_DIRECTORIES = {
        ".git",
        ".venv",
        "venv",
        "env",
        "__pycache__",
        ".pytest_cache",
        "node_modules",
        "dist",
        "build",
    }

    def analyze(self, repository_path: str) -> Dict:
        """
        Analyze dependencies for a repository.
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

        python_files = self._find_python_files(root)

        local_modules = self._find_local_modules(
            root,
            python_files,
        )

        imports = []
        import_relationships = []

        for file_path in python_files:
            file_imports = self._extract_imports(file_path)

            relative_file = file_path.relative_to(root).as_posix()

            for imported in file_imports:
                import_name = imported["module"]

                dependency_type = self._classify_dependency(
                    import_name,
                    local_modules,
                )

                imports.append({
                    "file": relative_file,
                    "module": import_name,
                    "type": dependency_type,
                    "line": imported["line"],
                })

                import_relationships.append({
                    "source": relative_file,
                    "target": import_name,
                    "type": dependency_type,
                })

        declared_dependencies = self._read_requirements(root)

        imported_external = sorted({
            item["module"].split(".")[0]
            for item in imports
            if item["type"] == "external"
        })

        missing_dependencies = sorted(
            set(imported_external) - set(declared_dependencies)
        )

        return {
            "python_files": sorted(
                file.relative_to(root).as_posix()
                for file in python_files
            ),
            "local_modules": sorted(local_modules),
            "imports": imports,
            "import_relationships": import_relationships,
            "declared_dependencies": sorted(
                declared_dependencies
            ),
            "external_dependencies": imported_external,
            "missing_dependencies": missing_dependencies,
        }

    def _find_python_files(
        self,
        root: Path,
    ) -> List[Path]:
        """
        Find Python files while ignoring virtual environments
        and generated directories.
        """

        files = []

        for path in root.rglob("*.py"):

            if not path.is_file():
                continue

            if any(
                part in self.IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            files.append(path)

        return files

    def _find_local_modules(
        self,
        root: Path,
        python_files: List[Path],
    ) -> Set[str]:
        """
        Identify modules that belong to the repository.
        """

        modules = set()

        for file_path in python_files:

            relative = file_path.relative_to(root)

            if relative.name == "__init__.py":
                module_parts = list(relative.parts[:-1])

            else:
                module_parts = list(relative.with_suffix("").parts)

                if module_parts and module_parts[-1] == "__init__":
                    module_parts.pop()

            if module_parts:
                modules.add(".".join(module_parts))

            if relative.stem != "__init__":
                modules.add(relative.stem)

        return modules

    def _extract_imports(
        self,
        file_path: Path,
    ) -> List[Dict]:
        """
        Extract import statements from a Python file.
        """

        try:
            source = file_path.read_text(
                encoding="utf-8",
                errors="replace",
            )

            tree = ast.parse(source)

        except (SyntaxError, OSError):
            return []

        imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:
                    imports.append({
                        "module": alias.name,
                        "line": node.lineno,
                    })

            elif isinstance(node, ast.ImportFrom):

                if node.module:
                    imports.append({
                        "module": node.module,
                        "line": node.lineno,
                    })

        return imports

    def _classify_dependency(
        self,
        module: str,
        local_modules: Set[str],
    ) -> str:
        """
        Classify an imported module.
        """

        root_module = module.split(".")[0]

        if (
            module in local_modules
            or root_module in local_modules
        ):
            return "local"

        standard_library = {
            "abc",
            "argparse",
            "ast",
            "asyncio",
            "collections",
            "csv",
            "dataclasses",
            "datetime",
            "functools",
            "hashlib",
            "io",
            "itertools",
            "json",
            "logging",
            "math",
            "os",
            "pathlib",
            "re",
            "shutil",
            "sqlite3",
            "subprocess",
            "sys",
            "tempfile",
            "threading",
            "time",
            "typing",
            "unittest",
            "uuid",
            "warnings",
            "xml",
        }

        if root_module in standard_library:
            return "standard_library"

        return "external"

    def _read_requirements(
        self,
        root: Path,
    ) -> Set[str]:
        """
        Read dependencies from requirements.txt.
        """

        requirements_file = root / "requirements.txt"

        if not requirements_file.exists():
            return set()

        dependencies = set()

        for line in requirements_file.read_text(
            encoding="utf-8",
            errors="replace",
        ).splitlines():

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("-"):
                continue

            package = line

            for separator in [
                "==",
                ">=",
                "<=",
                "~=",
                ">",
                "<",
                "[",
            ]:
                if separator in package:
                    package = package.split(
                        separator,
                        1,
                    )[0]

            dependencies.add(
                package.strip().lower()
            )

        return dependencies