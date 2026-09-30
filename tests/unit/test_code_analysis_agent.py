from agents.code_analysis.agent import CodeAnalysisAgent


def test_code_analysis_agent(tmp_path):

    # -----------------------------------------
    # Create repository
    # -----------------------------------------

    src = tmp_path / "src"
    tests = tmp_path / "tests"

    src.mkdir()
    tests.mkdir()

    # -----------------------------------------
    # Source files
    # -----------------------------------------

    (src / "__init__.py").write_text("")

    (src / "model.py").write_text(
        """
class Model:

    def predict(self, value):
        return value * 2
"""
    )

    (src / "main.py").write_text(
        """
import os
import numpy as np

from src.model import Model


def main():

    model = Model()

    result = np.array(
        [model.predict(10)]
    )

    return result
"""
    )

    # -----------------------------------------
    # Test file
    # -----------------------------------------

    (tests / "test_model.py").write_text(
        """
from src.model import Model


def test_model():

    model = Model()

    assert model.predict(10) == 20
"""
    )

    # -----------------------------------------
    # Dependencies
    # -----------------------------------------

    (tmp_path / "requirements.txt").write_text(
        """
numpy==2.0.0
"""
    )

    # -----------------------------------------
    # Run Code Analysis Agent
    # -----------------------------------------

    agent = CodeAnalysisAgent()

    result = agent.analyze(
        repository_path=str(tmp_path),
        relevant_files=["src/main.py"],
    )

    # -----------------------------------------
    # Check result structure
    # -----------------------------------------

    assert "repository" in result
    assert "dependencies" in result
    assert "ast_analysis" in result

    # -----------------------------------------
    # Repository checks
    # -----------------------------------------

    repository = result["repository"]

    assert repository["project_type"] == "python"

    assert "src/main.py" in repository["source_files"]

    assert "src/model.py" in repository["source_files"]

    assert "tests/test_model.py" in repository["test_files"]

    assert "requirements.txt" in repository["config_files"]

    # -----------------------------------------
    # Dependency checks
    # -----------------------------------------

    dependencies = result["dependencies"]

    assert "numpy" in dependencies["external_dependencies"]

    assert "numpy" in dependencies["declared_dependencies"]

    assert "numpy" not in dependencies["missing_dependencies"]

    # -----------------------------------------
    # AST checks
    # -----------------------------------------

    ast_result = result["ast_analysis"]

    assert "src/main.py" in ast_result

    main_analysis = ast_result["src/main.py"]

    assert main_analysis["syntax_error"] is None

    # Functions
    function_names = [
        item["name"]
        for item in main_analysis["functions"]
    ]

    assert "main" in function_names

    # Imports
    import_names = [
        item["name"]
        for item in main_analysis["imports"]
    ]

    assert "os" in import_names
    assert "numpy" in import_names
    assert "src.model.Model" in import_names

    # Variables
    variable_names = [
        item["name"]
        for item in main_analysis["variables"]
    ]

    assert "model" in variable_names
    assert "result" in variable_names

    # Calls
    call_names = [
        item["name"]
        for item in main_analysis["calls"]
    ]

    assert "Model" in call_names
    assert "np.array" in call_names
    assert "model.predict" in call_names