from agents.fix.subagents.patch_generator import PatchGenerator


class MockResponse:
    def __init__(self, content):
        self.content = content


class MockLLM:
    def invoke(self, prompt):
        return MockResponse(
            """```diff
--- a/train.py
+++ b/train.py
@@ -1,3 +1,3 @@
 def train():
-    output = model(image)
+    output = Model(image)
"""
        )


def test_patch_generator():

    generator = PatchGenerator.__new__(
        PatchGenerator
    )

    generator.llm = MockLLM()

    result = generator.generate(
        problem="Model is not defined.",
        traceback=(
            'File "train.py", line 2, in train\n'
            "NameError: name 'model' is not defined"
        ),
        root_cause=(
            "The code references `model`, but the "
            "defined class is `Model`."
        ),
        relevant_files=[
            "train.py"
        ],
        code_context={
            "train.py": {
                "functions": ["train"],
                "classes": ["Model"],
            }
        },
        retrieved_context=[],
    )

    assert "patch" in result
    assert "summary" in result

    patch = result["patch"]

    assert patch != ""

    assert "--- a/train.py" in patch
    assert "+++ b/train.py" in patch

    assert "-    output = model(image)" in patch
    assert "+    output = Model(image)" in patch

    assert "train.py" in result["summary"]