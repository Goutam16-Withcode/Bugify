import ast
from pathlib import Path
from typing import Dict, List, Optional


class ASTAnalyzer:
    """
    Analyzes Python source code using the built-in AST module.
    """

    def analyze_file(self, file_path: str) -> Dict:
        """
        Analyze a Python source file.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File does not exist: {file_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Path is not a file: {file_path}"
            )

        if path.suffix.lower() != ".py":
            raise ValueError(
                f"ASTAnalyzer currently supports Python files only: {file_path}"
            )

        source = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        return self.analyze_source(
            source=source,
            file_path=file_path,
        )

    def analyze_source(
        self,
        source: str,
        file_path: Optional[str] = None,
    ) -> Dict:
        """
        Analyze Python source code directly.
        """

        if not source.strip():
            return self._empty_result(file_path)

        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            return {
                "file": file_path,
                "syntax_error": {
                    "message": exc.msg,
                    "line": exc.lineno,
                    "column": exc.offset,
                },
                "imports": [],
                "classes": [],
                "functions": [],
                "calls": [],
                "variables": [],
            }

        imports = []
        classes = []
        functions = []
        calls = []
        variables = []

        for node in ast.walk(tree):

            # Imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "name": alias.name,
                        "alias": alias.asname,
                        "line": node.lineno,
                    })

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""

                for alias in node.names:
                    imports.append({
                        "name": f"{module}.{alias.name}"
                        if module
                        else alias.name,
                        "alias": alias.asname,
                        "line": node.lineno,
                    })

            # Classes
            elif isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "end_line": getattr(
                        node,
                        "end_lineno",
                        node.lineno,
                    ),
                    "bases": [
                        self._get_name(base)
                        for base in node.bases
                    ],
                })

            # Functions
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append({
                    "name": node.name,
                    "line": node.lineno,
                    "end_line": getattr(
                        node,
                        "end_lineno",
                        node.lineno,
                    ),
                    "async": isinstance(
                        node,
                        ast.AsyncFunctionDef,
                    ),
                    "arguments": [
                        arg.arg
                        for arg in node.args.args
                    ],
                })

            # Function / method calls
            elif isinstance(node, ast.Call):
                calls.append({
                    "name": self._get_call_name(node.func),
                    "line": node.lineno,
                })

            # Variable assignments
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    name = self._get_name(target)

                    if name:
                        variables.append({
                            "name": name,
                            "line": node.lineno,
                        })

            elif isinstance(node, ast.AnnAssign):
                name = self._get_name(node.target)

                if name:
                    variables.append({
                        "name": name,
                        "line": node.lineno,
                    })

        return {
            "file": file_path,
            "syntax_error": None,
            "imports": imports,
            "classes": classes,
            "functions": functions,
            "calls": calls,
            "variables": variables,
        }

    def _get_name(self, node: ast.AST) -> Optional[str]:
        """
        Extract a readable name from an AST node.
        """

        if isinstance(node, ast.Name):
            return node.id

        if isinstance(node, ast.Attribute):
            parent = self._get_name(node.value)

            if parent:
                return f"{parent}.{node.attr}"

            return node.attr

        return None

    def _get_call_name(self, node: ast.AST) -> Optional[str]:
        """
        Extract a readable function/method call name.
        """

        return self._get_name(node)

    def _empty_result(
        self,
        file_path: Optional[str],
    ) -> Dict:
        """
        Return a consistent result for empty source.
        """

        return {
            "file": file_path,
            "syntax_error": None,
            "imports": [],
            "classes": [],
            "functions": [],
            "calls": [],
            "variables": [],
        }