from agents.fix.agent import FixAgent


class MockPatchGenerator:
    def __init__(self, patches):
        self.patches = patches
        self.call_count = 0

    def generate(
        self,
        problem,
        traceback,
        root_cause,
        relevant_files,
        code_context,
        retrieved_context,
    ):
        patch = self.patches[
            min(
                self.call_count,
                len(self.patches) - 1,
            )
        ]

        self.call_count += 1

        return {
            "patch": patch,
            "summary": "Mock patch generated.",
        }


class MockPatchReviewer:
    def __init__(self, reviews):
        self.reviews = reviews
        self.call_count = 0

    def review(
        self,
        problem,
        traceback,
        root_cause,
        patch,
        code_context,
    ):
        review = self.reviews[
            min(
                self.call_count,
                len(self.reviews) - 1,
            )
        ]

        self.call_count += 1

        return review


class MockRefactoringAgent:
    def __init__(self, result):
        self.result = result
        self.call_count = 0

    def refactor(
        self,
        problem,
        root_cause,
        approved_patch,
        code_context,
        relevant_files,
    ):
        self.call_count += 1
        return self.result


def create_fix_agent(
    patch_generator,
    patch_reviewer,
    refactoring_agent,
    max_retries=2,
):
    agent = FixAgent.__new__(FixAgent)

    agent.patch_generator = patch_generator
    agent.patch_reviewer = patch_reviewer
    agent.refactoring_agent = refactoring_agent
    agent.max_retries = max_retries

    return agent


def test_fix_agent_approve_without_refactoring():

    patch = """--- a/app.py
+++ b/app.py
@@
-old_code
+fixed_code
"""

    patch_generator = MockPatchGenerator(
        [patch]
    )

    patch_reviewer = MockPatchReviewer(
        [
            {
                "decision": "approve",
                "confidence": 0.95,
                "reason": (
                    "Patch directly fixes the root cause."
                ),
                "issues": [],
            }
        ]
    )

    refactoring_agent = MockRefactoringAgent(
        {
            "required": False,
            "patch": "",
            "summary": (
                "No refactoring is required."
            ),
        }
    )

    agent = create_fix_agent(
        patch_generator,
        patch_reviewer,
        refactoring_agent,
    )

    result = agent.fix(
        problem="Application crashes.",
        traceback="RuntimeError",
        root_cause="Incorrect implementation.",
        relevant_files=["app.py"],
        code_context={
            "app.py": {
                "functions": ["main"],
            }
        },
    )

    assert result["success"] is True
    assert result["patch"] == patch
    assert result["attempts"] == 1

    assert result["review"]["decision"] == "approve"

    assert result["refactoring"]["required"] is False

    assert patch_generator.call_count == 1
    assert patch_reviewer.call_count == 1
    assert refactoring_agent.call_count == 1


def test_fix_agent_revise_then_approve():

    first_patch = """--- a/app.py
+++ b/app.py
@@
-old_code
+bad_fix
"""

    second_patch = """--- a/app.py
+++ b/app.py
@@
-old_code
+correct_fix
"""

    patch_generator = MockPatchGenerator(
        [
            first_patch,
            second_patch,
        ]
    )

    patch_reviewer = MockPatchReviewer(
        [
            {
                "decision": "revise",
                "confidence": 0.80,
                "reason": "Patch is too broad.",
                "issues": [
                    "The patch changes unnecessary code."
                ],
            },
            {
                "decision": "approve",
                "confidence": 0.95,
                "reason": (
                    "The revised patch is minimal."
                ),
                "issues": [],
            },
        ]
    )

    refactoring_agent = MockRefactoringAgent(
        {
            "required": False,
            "patch": "",
            "summary": (
                "No refactoring is required."
            ),
        }
    )

    agent = create_fix_agent(
        patch_generator,
        patch_reviewer,
        refactoring_agent,
    )

    result = agent.fix(
        problem="Application crashes.",
        traceback="RuntimeError",
        root_cause="Incorrect implementation.",
        relevant_files=["app.py"],
        code_context={},
    )

    assert result["success"] is True
    assert result["patch"] == second_patch
    assert result["attempts"] == 2

    assert result["review"]["decision"] == "approve"

    assert patch_generator.call_count == 2
    assert patch_reviewer.call_count == 2


def test_fix_agent_rejects_patch():

    patch = """--- a/app.py
+++ b/app.py
@@
-old_code
+unsafe_fix
"""

    patch_generator = MockPatchGenerator(
        [patch]
    )

    patch_reviewer = MockPatchReviewer(
        [
            {
                "decision": "reject",
                "confidence": 0.98,
                "reason": (
                    "Patch does not address the root cause."
                ),
                "issues": [
                    "The patch only hides the error."
                ],
            }
        ]
    )

    refactoring_agent = MockRefactoringAgent(
        {
            "required": False,
            "patch": "",
            "summary": (
                "Refactoring was not attempted."
            ),
        }
    )

    agent = create_fix_agent(
        patch_generator,
        patch_reviewer,
        refactoring_agent,
    )

    result = agent.fix(
        problem="Application crashes.",
        traceback="RuntimeError",
        root_cause="Incorrect implementation.",
        relevant_files=["app.py"],
        code_context={},
    )

    assert result["success"] is False
    assert result["patch"] == patch
    assert result["review"]["decision"] == "reject"
    assert result["attempts"] == 1

    assert patch_generator.call_count == 1
    assert patch_reviewer.call_count == 1

    # Refactoring must never run after rejection.
    assert refactoring_agent.call_count == 0


def test_fix_agent_max_retries():

    patch = """--- a/app.py
+++ b/app.py
@@
-old_code
+another_fix
"""

    patch_generator = MockPatchGenerator(
        [patch]
    )

    patch_reviewer = MockPatchReviewer(
        [
            {
                "decision": "revise",
                "confidence": 0.80,
                "reason": "Patch needs revision.",
                "issues": [
                    "Patch is not sufficiently minimal."
                ],
            }
        ]
    )

    refactoring_agent = MockRefactoringAgent(
        {
            "required": False,
            "patch": "",
            "summary": (
                "Refactoring was not attempted."
            ),
        }
    )

    agent = create_fix_agent(
        patch_generator,
        patch_reviewer,
        refactoring_agent,
        max_retries=2,
    )

    result = agent.fix(
        problem="Application crashes.",
        traceback="RuntimeError",
        root_cause="Incorrect implementation.",
        relevant_files=["app.py"],
        code_context={},
    )

    assert result["success"] is False
    assert result["attempts"] == 3
    assert result["review"]["decision"] == "revise"

    assert patch_generator.call_count == 3
    assert patch_reviewer.call_count == 3

    assert refactoring_agent.call_count == 0


def test_fix_agent_approved_refactoring():

    original_patch = """--- a/app.py
+++ b/app.py
@@
-old_code
+fixed_code
"""

    refactored_patch = """--- a/app.py
+++ b/app.py
@@
-old_code
+cleaner_fixed_code
"""

    patch_generator = MockPatchGenerator(
        [original_patch]
    )

    patch_reviewer = MockPatchReviewer(
        [
            {
                "decision": "approve",
                "confidence": 0.95,
                "reason": "Original patch is correct.",
                "issues": [],
            },
            {
                "decision": "approve",
                "confidence": 0.93,
                "reason": (
                    "Refactored patch remains correct."
                ),
                "issues": [],
            },
        ]
    )

    refactoring_agent = MockRefactoringAgent(
        {
            "required": True,
            "patch": refactored_patch,
            "summary": (
                "Localized refactoring proposed."
            ),
        }
    )

    agent = create_fix_agent(
        patch_generator,
        patch_reviewer,
        refactoring_agent,
    )

    result = agent.fix(
        problem="Application crashes.",
        traceback="RuntimeError",
        root_cause="Incorrect implementation.",
        relevant_files=["app.py"],
        code_context={},
    )

    assert result["success"] is True
    assert result["patch"] == refactored_patch
    assert result["attempts"] == 1

    # The final review belongs to the refactored patch.
    assert result["review"]["decision"] == "approve"
    assert result["review"]["confidence"] == 0.93
    assert result["review"]["issues"] == []

    assert result["refactoring"]["required"] is True
    assert result["refactoring"]["patch"] == refactored_patch
    assert (
        result["refactoring"]["summary"]
        == "Localized refactoring proposed."
    )

    assert patch_generator.call_count == 1

    # Original patch + refactored patch.
    assert patch_reviewer.call_count == 2

    assert refactoring_agent.call_count == 1


def test_fix_agent_keeps_original_patch_when_refactoring_rejected():

    original_patch = """--- a/app.py
+++ b/app.py
@@
-old_code
+fixed_code
"""

    refactored_patch = """--- a/app.py
+++ b/app.py
@@
-old_code
+bad_refactor
"""

    patch_generator = MockPatchGenerator(
        [original_patch]
    )

    patch_reviewer = MockPatchReviewer(
        [
            {
                "decision": "approve",
                "confidence": 0.95,
                "reason": "Original patch is correct.",
                "issues": [],
            },
            {
                "decision": "reject",
                "confidence": 0.98,
                "reason": (
                    "Refactoring introduces unrelated changes."
                ),
                "issues": [
                    "The refactoring is too broad."
                ],
            },
        ]
    )

    refactoring_agent = MockRefactoringAgent(
        {
            "required": True,
            "patch": refactored_patch,
            "summary": (
                "Localized refactoring proposed."
            ),
        }
    )

    agent = create_fix_agent(
        patch_generator,
        patch_reviewer,
        refactoring_agent,
    )

    result = agent.fix(
        problem="Application crashes.",
        traceback="RuntimeError",
        root_cause="Incorrect implementation.",
        relevant_files=["app.py"],
        code_context={},
    )

    assert result["success"] is True

    # Original approved patch must be preserved.
    assert result["patch"] == original_patch

    assert result["review"]["decision"] == "approve"

    assert result["refactoring"]["required"] is True

    assert (
        result["refactoring"]["review"]["decision"]
        == "reject"
    )

    assert patch_generator.call_count == 1
    assert patch_reviewer.call_count == 2
    assert refactoring_agent.call_count == 1


def test_fix_agent_handles_empty_generated_patch():

    patch_generator = MockPatchGenerator(
        [""]
    )

    patch_reviewer = MockPatchReviewer(
        []
    )

    refactoring_agent = MockRefactoringAgent(
        {
            "required": False,
            "patch": "",
            "summary": (
                "Refactoring was not attempted."
            ),
        }
    )

    agent = create_fix_agent(
        patch_generator,
        patch_reviewer,
        refactoring_agent,
    )

    result = agent.fix(
        problem="Application crashes.",
        traceback="RuntimeError",
        root_cause="Unknown.",
        relevant_files=["app.py"],
        code_context={},
    )

    assert result["success"] is False
    assert result["patch"] == ""
    assert result["review"]["decision"] == "reject"
    assert result["attempts"] == 1

    assert patch_generator.call_count == 1
    assert patch_reviewer.call_count == 0
    assert refactoring_agent.call_count == 0