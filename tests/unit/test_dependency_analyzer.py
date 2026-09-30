from agents.code_analysis.subagents.dependency_analyzer import (
    DependencyAnalyzer,
)


def test_dependency_analyzer(tmp_path):

    src = tmp_path / "src"
    src.mkdir()

    (src / "__init__.py").write_text("")

    (src / "utils.py").write_text(
        """
def helper():
    return True
"""
    )

    (src / "main.py").write_text(
        """
import os
import json
import numpy
from src.utils import helper

def main():
    helper()
"""
    )

    (tmp_path / "requirements.txt").write_text(
        """
numpy==2.0.0
"""
    )

    analyzer = DependencyAnalyzer()

    result = analyzer.analyze(str(tmp_path))

    # Python files
    assert "src/main.py" in result["python_files"]
    assert "src/utils.py" in result["python_files"]

    # Standard library
    standard_library = [
        item
        for item in result["imports"]
        if item["module"] == "os"
    ]

    assert standard_library[0]["type"] == "standard_library"

    # External dependency
    external = [
        item
        for item in result["imports"]
        if item["module"] == "numpy"
    ]

    assert external[0]["type"] == "external"

    # Local dependency
    local = [
        item
        for item in result["imports"]
        if item["module"] == "src.utils"
    ]

    assert local[0]["type"] == "local"

    # requirements.txt
    assert "numpy" in result["declared_dependencies"]

    # NumPy is declared, so it should not be missing
    assert "numpy" not in result["missing_dependencies"]

    # External dependency list
    assert "numpy" in result["external_dependencies"]