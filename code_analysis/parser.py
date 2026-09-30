import ast
from typing import Dict, List, Optional, Any


class CodeParser:
    """AST parser for extracting functions, classes, imports, and calls."""

    @staticmethod
    def parse_python(code: str, filename: str = "<unknown>") -> Dict[str, Any]:
        """Parse Python code into structural elements."""
        try:
            tree = ast.parse(code, filename=filename)
        except SyntaxError as e:
            return {
                "valid": False,
                "error": str(e),
                "lineno": e.lineno,
                "offset": e.offset,
                "functions": [],
                "classes": [],
                "imports": [],
            }

        functions = []
        classes = []
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "end_lineno": getattr(node, "end_lineno", node.lineno),
                    "args": [a.arg for a in node.args.args],
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                })
            elif isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "end_lineno": getattr(node, "end_lineno", node.lineno),
                    "bases": [ast.unparse(b) for b in node.bases if hasattr(ast, "unparse")],
                })
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({"module": alias.name, "alias": alias.asname})
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append({"module": node.module, "name": alias.name, "alias": alias.asname})

        return {
            "valid": True,
            "error": None,
            "functions": functions,
            "classes": classes,
            "imports": imports,
        }
