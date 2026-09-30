from agents.fix.subagents.patch_reviewer import PatchReviewer


class MockResponse:
    def __init__(self, content):
        self.content = content


class MockLLM:
    def __init__(self, response):
        self.response = response

    def invoke(self, prompt):
        return MockResponse(self.response)


def test_patch_reviewer_approves_valid_patch():

    reviewer = PatchReviewer.__new__(
        PatchReviewer
    )

    reviewer.llm = MockLLM(
        """
{
    "decision": "approve",
    "confidence": 0.95,
    "reason": "The patch directly fixes the identified root cause.",
    "issues": []
}
"""
    )

    result = reviewer.review(
        problem="Variable uses incorrect identifier.",
        traceback="NameError: name 'model' is not defined",
        root_cause=(
            "The code references model instead of Model."
        ),
        patch="""--- a/train.py
+++ b/train.py
@@
-model(image)
+Model(image)
""",
        code_context={
            "train.py": {
                "classes": ["Model"],
                "functions": ["train"],
            }
        },
    )

    assert result["decision"] == "approve"
    assert result["confidence"] == 0.95
    assert result["issues"] == []


def test_patch_reviewer_rejects_invalid_output():

    reviewer = PatchReviewer.__new__(
        PatchReviewer
    )

    reviewer.llm = MockLLM(
        "this is not json"
    )

    result = reviewer.review(
        problem="Broken code.",
        traceback="RuntimeError",
        root_cause="Incorrect implementation.",
        patch="some patch",
        code_context={},
    )

    assert result["decision"] == "reject"
    assert result["confidence"] == 0.0
    assert result["issues"]


def test_patch_reviewer_rejects_empty_patch():

    reviewer = PatchReviewer.__new__(
        PatchReviewer
    )

    result = reviewer.review(
        problem="Broken code.",
        traceback="RuntimeError",
        root_cause="Incorrect implementation.",
        patch="",
        code_context={},
    )

    assert result["decision"] == "reject"
    assert result["confidence"] == 1.0