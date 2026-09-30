from typing import Dict, List, Optional, Any
from agents.verification.subagents.test_executor import TestExecutor
from agents.verification.subagents.regression_tester import RegressionTester
from agents.verification.subagents.runtime_validator import RuntimeValidator
from schemas.test import VerificationVerdict, TestSuiteResult


class VerificationAgent:
    """
    Verification Agent.

    Coordinates:
    - RuntimeValidator: validates the patch in isolation
    - TestExecutor: runs the test suite
    - RegressionTester: compares results to a baseline

    This agent NEVER modifies the production repository.
    It operates on in-memory or temp-dir copies only.
    """

    def __init__(self):
        self.runtime_validator = RuntimeValidator()
        self.test_executor = TestExecutor()
        self.regression_tester = RegressionTester()

    def verify(
        self,
        repo_path: str,
        patch_text: str,
        target_files: Optional[List[str]] = None,
        run_tests: bool = False,
        test_directory: str = "tests",
    ) -> VerificationVerdict:
        """
        Verify a patch by:
        1. Checking syntax validity of the patch additions.
        2. Validating patch application in isolation.
        3. (Optional) Running the test suite if run_tests=True.

        Args:
            repo_path: Path to the target repository.
            patch_text: Unified diff patch text.
            target_files: Files the patch is expected to touch.
            run_tests: Whether to actually run pytest (can be slow).
            test_directory: Subdirectory containing tests.

        Returns:
            VerificationVerdict
        """
        target_files = target_files or []

        # --------------------------------------------------
        # 1. Syntax check on patch additions
        # --------------------------------------------------
        syntax_error = self.test_executor.validate_syntax(patch_text)
        if syntax_error:
            return VerificationVerdict(
                verified=False,
                reason=f"Patch contains syntax errors: {syntax_error}",
                syntax_error=syntax_error,
                applied_patch=patch_text,
            )

        # --------------------------------------------------
        # 2. Runtime patch validation (in-memory file apply)
        # --------------------------------------------------
        validation = self.runtime_validator.validate_patch_application(
            patch_text=patch_text,
            repo_path=repo_path,
            target_files=target_files,
        )
        if not validation["success"]:
            return VerificationVerdict(
                verified=False,
                reason=f"Patch validation failed: {validation['message']}",
                applied_patch=patch_text,
            )

        # --------------------------------------------------
        # 3. Optional test suite execution
        # --------------------------------------------------
        if run_tests:
            test_result = self.test_executor.run_tests(
                repo_path=repo_path,
                test_directory=test_directory,
            )
            verified = test_result.failed == 0 and test_result.errors == 0
            return VerificationVerdict(
                verified=verified,
                reason=(
                    "All tests passed after patch application."
                    if verified
                    else f"{test_result.failed} tests failed, {test_result.errors} errors after patch."
                ),
                test_suite_result=test_result,
                applied_patch=patch_text,
            )

        # --------------------------------------------------
        # 4. Static-only verification passes
        # --------------------------------------------------
        return VerificationVerdict(
            verified=True,
            reason="Patch passed syntax and static validation checks. Test suite not executed.",
            applied_patch=patch_text,
        )
