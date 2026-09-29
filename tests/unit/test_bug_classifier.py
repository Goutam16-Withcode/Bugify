from agents.diagnosis.subagents.bug_classifier import BugClassifier


class MockResponse:
    content = """
    {
        "bug_type": "runtime",
        "category": "undefined_variable",
        "severity": "medium",
        "confidence": 0.96
    }
    """


class MockLLM:

    def invoke(self, prompt):
        return MockResponse()


def test_bug_classifier():

    classifier = BugClassifier.__new__(BugClassifier)
    classifier.llm = MockLLM()

    result = classifier.classify(
        error_type="NameError",
        error_message="name 'model' is not defined",
        logs=["ERROR: model is not defined"],
        patterns=["undefined"],
    )

    assert result["bug_type"] == "runtime"
    assert result["category"] == "undefined_variable"
    assert result["severity"] == "medium"
    assert result["confidence"] == 0.96