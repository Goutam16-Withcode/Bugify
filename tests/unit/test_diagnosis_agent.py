from agents.diagnosis.agent import DiagnosisAgent


class MockBugClassifier:

    def classify(
        self,
        error_type,
        error_message,
        logs,
        patterns,
    ):
        return {
            "bug_type": "runtime",
            "category": "undefined_variable",
            "severity": "medium",
            "confidence": 0.96,
        }


def test_diagnosis_agent():

    agent = DiagnosisAgent()

    # Replace real Groq classifier with mock
    agent.bug_classifier = MockBugClassifier()

    traceback = """
    Traceback (most recent call last):
      File "train.py", line 42, in train_model
        output = model(image)
    NameError: name 'model' is not defined
    """

    logs = """
    Starting training...
    WARNING: Deprecated API usage
    ERROR: model is not defined
    """

    result = agent.analyze(
        problem="Model prediction is failing",
        traceback=traceback,
        logs=logs,
    )

    assert result["bug_type"] == "runtime"
    assert result["category"] == "undefined_variable"
    assert result["severity"] == "medium"
    assert result["confidence"] == 0.96

    assert result["error_type"] == "NameError"
    assert result["file"] == "train.py"
    assert result["line"] == "42"
    assert result["function"] == "train_model"

    assert "train.py" in result["relevant_files"]
    assert len(result["errors"]) == 1
    assert len(result["warnings"]) == 1