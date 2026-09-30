from agents.fix.subagents.refactoring_agent import (
    RefactoringAgent,
)


class MockResponse:
    def __init__(self, content):
        self.content = content


class MockLLM:
    def __init__(self, response):
        self.response = response

    def invoke(self, prompt):
        return MockResponse(self.response)


def test_refactoring_agent_returns_no_refactor():

    agent = RefactoringAgent.__new__(
        RefactoringAgent
    )

    agent.llm = MockLLM(
        "NO_REFACTOR"
    )

    result = agent.refactor(
        problem="Incorrect variable name.",
        root_cause=(
            "The wrong variable is referenced."
        ),
        approved_patch="""--- a/train.py
+++ b/train.py
@@
-model(image)
+Model(image)
""",
        code_context={
            "train.py": {
                "functions": ["train"],
                "classes": ["Model"],
            }
        },
        relevant_files=[
            "train.py"
        ],
    )

    assert result["required"] is False
    assert result["patch"] == ""
    assert "No refactoring" in result["summary"]


def test_refactoring_agent_returns_patch():

    agent = RefactoringAgent.__new__(
        RefactoringAgent
    )

    agent.llm = MockLLM(
        """```diff
--- a/train.py
+++ b/train.py
@@
 def train():
-    result = model(image)
+    result = Model(image)
     return result
```"""
    )

    result = agent.refactor(
        problem="Model reference is incorrect.",
        root_cause=(
            "The implementation references the wrong symbol."
        ),
        approved_patch="""--- a/train.py
+++ b/train.py
@@
-model(image)
+Model(image)
""",
        code_context={
            "train.py": {
                "functions": ["train"],
                "classes": ["Model"],
            }
        },
        relevant_files=[
            "train.py"
        ],
    )

    assert result["required"] is True
    assert result["patch"] != ""
    assert "--- a/train.py" in result["patch"]
    assert "+++ b/train.py" in result["patch"]
    assert "train.py" in result["summary"]


def test_refactoring_agent_rejects_invalid_response():

    agent = RefactoringAgent.__new__(
        RefactoringAgent
    )

    agent.llm = MockLLM(
        "This code should be refactored."
    )

    result = agent.refactor(
        problem="Broken implementation.",
        root_cause="Incorrect implementation.",
        approved_patch="""--- a/app.py
+++ b/app.py
@@
-old
+new
""",
        code_context={},
        relevant_files=[
            "app.py"
        ],
    )

    assert result["required"] is False
    assert result["patch"] == ""
    assert "Invalid" in result["summary"]