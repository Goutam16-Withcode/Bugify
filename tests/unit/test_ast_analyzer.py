from agents.code_analysis.subagents.ast_analyzer import ASTAnalyzer


def test_ast_analyzer():

    source = """
import os
import numpy as np
from pathlib import Path

class Model:

    def predict(self, data):
        return np.array(data)


def train_model(data, epochs):
    model = Model()
    result = model.predict(data)

    for epoch in range(epochs):
        print(epoch)

    return result
"""

    analyzer = ASTAnalyzer()

    result = analyzer.analyze_source(
        source=source,
        file_path="train.py",
    )

    assert result["file"] == "train.py"
    assert result["syntax_error"] is None

    # Imports
    import_names = [
        item["name"]
        for item in result["imports"]
    ]

    assert "os" in import_names
    assert "numpy" in import_names
    assert "pathlib.Path" in import_names

    # Classes
    class_names = [
        item["name"]
        for item in result["classes"]
    ]

    assert "Model" in class_names

    # Functions
    function_names = [
        item["name"]
        for item in result["functions"]
    ]

    assert "predict" in function_names
    assert "train_model" in function_names

    # Variables
    variable_names = [
        item["name"]
        for item in result["variables"]
    ]

    assert "model" in variable_names
    assert "result" in variable_names

    # Calls
    call_names = [
        item["name"]
        for item in result["calls"]
    ]

    assert "Model" in call_names
    assert "model.predict" in call_names