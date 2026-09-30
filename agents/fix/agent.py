from typing import Dict, List, Optional

from agents.fix.subagents.patch_generator import PatchGenerator
from agents.fix.subagents.patch_reviewer import PatchReviewer
from agents.fix.subagents.refactoring_agent import RefactoringAgent


class FixAgent:
    """
    Main Fix Agent.

    Coordinates:
    - Patch Generator
    - Patch Reviewer
    - Refactoring Agent

    The Fix Agent proposes and reviews patches but NEVER
    modifies the repository directly.

    Actual patch application and runtime verification are
    handled later by the Verification Agent.
    """

    MAX_RETRIES = 2

    def __init__(
        self,
        max_retries: int = MAX_RETRIES,
    ):
        self.patch_generator = PatchGenerator()
        self.patch_reviewer = PatchReviewer()
        self.refactoring_agent = RefactoringAgent()

        if max_retries < 0:
            raise ValueError(
                "max_retries cannot be negative."
            )

        self.max_retries = max_retries

    def fix(
        self,
        problem: str,
        traceback: str,
        root_cause: Optional[str],
        relevant_files: List[str],
        code_context: Dict,
        retrieved_context: Optional[List[str]] = None,
    ) -> Dict:
        """
        Generate, review, and optionally refactor a patch.

        Returns:
            {
                "success": bool,
                "patch": str,
                "summary": str,
                "review": dict,
                "refactoring": dict,
                "attempts": int,
            }
        """

        retrieved_context = retrieved_context or []

        last_review = {
            "decision": "reject",
            "confidence": 0.0,
            "reason": "No patch generated.",
            "issues": [],
        }

        last_patch = ""

        attempts = 0

        while attempts <= self.max_retries:

            attempts += 1

            # -------------------------------------------------
            # STEP 1: Generate patch
            # -------------------------------------------------

            generated = self.patch_generator.generate(
                problem=problem,
                traceback=traceback,
                root_cause=root_cause,
                relevant_files=relevant_files,
                code_context=code_context,
                retrieved_context=retrieved_context,
            )

            candidate_patch = generated.get(
                "patch",
                "",
            )

            last_patch = candidate_patch

            # -------------------------------------------------
            # STEP 2: Validate generated patch
            # -------------------------------------------------

            if not candidate_patch.strip():

                return {
                    "success": False,
                    "patch": "",
                    "summary": (
                        "Patch Generator did not produce "
                        "a valid patch."
                    ),
                    "review": {
                        "decision": "reject",
                        "confidence": 1.0,
                        "reason": (
                            "No valid patch was generated."
                        ),
                        "issues": [
                            "Patch Generator returned an empty patch."
                        ],
                    },
                    "refactoring": {
                        "required": False,
                        "patch": "",
                        "summary": (
                            "Refactoring was not attempted."
                        ),
                    },
                    "attempts": attempts,
                }

            # -------------------------------------------------
            # STEP 3: Review patch
            # -------------------------------------------------

            review = self.patch_reviewer.review(
                problem=problem,
                traceback=traceback,
                root_cause=root_cause,
                patch=candidate_patch,
                code_context=code_context,
            )

            last_review = review

            decision = review.get(
                "decision",
                "reject",
            )

            # -------------------------------------------------
            # STEP 4: APPROVE
            # -------------------------------------------------

            if decision == "approve":

                return self._handle_approved_patch(
                    problem=problem,
                    root_cause=root_cause,
                    approved_patch=candidate_patch,
                    code_context=code_context,
                    relevant_files=relevant_files,
                    review=review,
                    attempts=attempts,
                )

            # -------------------------------------------------
            # STEP 5: REJECT
            # -------------------------------------------------

            if decision == "reject":

                return {
                    "success": False,
                    "patch": candidate_patch,
                    "summary": (
                        "Patch was rejected by the Patch Reviewer."
                    ),
                    "review": review,
                    "refactoring": {
                        "required": False,
                        "patch": "",
                        "summary": (
                            "Refactoring was not attempted."
                        ),
                    },
                    "attempts": attempts,
                }

            # -------------------------------------------------
            # STEP 6: REVISE
            # -------------------------------------------------

            if decision == "revise":

                if attempts > self.max_retries:
                    return {
                        "success": False,
                        "patch": candidate_patch,
                        "summary": (
                            "Maximum patch-generation attempts "
                            "were reached."
                        ),
                        "review": review,
                        "refactoring": {
                            "required": False,
                            "patch": "",
                            "summary": (
                                "Refactoring was not attempted."
                            ),
                        },
                        "attempts": attempts,
                    }

                # Continue loop and generate a new patch.
                continue

            # -------------------------------------------------
            # UNKNOWN REVIEW DECISION
            # -------------------------------------------------

            return {
                "success": False,
                "patch": candidate_patch,
                "summary": (
                    "Patch Reviewer returned an "
                    "unknown decision."
                ),
                "review": review,
                "refactoring": {
                    "required": False,
                    "patch": "",
                    "summary": (
                        "Refactoring was not attempted."
                    ),
                },
                "attempts": attempts,
            }

        return {
            "success": False,
            "patch": last_patch,
            "summary": (
                "Fix Agent could not produce an approved patch."
            ),
            "review": last_review,
            "refactoring": {
                "required": False,
                "patch": "",
                "summary": (
                    "Refactoring was not attempted."
                ),
            },
            "attempts": attempts,
        }

    def _handle_approved_patch(
        self,
        problem: str,
        root_cause: Optional[str],
        approved_patch: str,
        code_context: Dict,
        relevant_files: List[str],
        review: Dict,
        attempts: int,
    ) -> Dict:
        """
        Handle a patch that passed review.

        The Refactoring Agent is optional. If it determines
        that no refactoring is necessary, the approved patch
        becomes the final patch.
        """

        refactoring = self.refactoring_agent.refactor(
            problem=problem,
            root_cause=root_cause,
            approved_patch=approved_patch,
            code_context=code_context,
            relevant_files=relevant_files,
        )

        if not refactoring.get("required", False):

            return {
                "success": True,
                "patch": approved_patch,
                "summary": (
                    "Patch approved. No additional "
                    "refactoring is required."
                ),
                "review": review,
                "refactoring": refactoring,
                "attempts": attempts,
            }

        refactoring_patch = refactoring.get(
            "patch",
            "",
        )

        if not refactoring_patch.strip():

            return {
                "success": True,
                "patch": approved_patch,
                "summary": (
                    "Patch approved. Refactoring was requested "
                    "but produced no usable patch, so the "
                    "original approved patch is retained."
                ),
                "review": review,
                "refactoring": refactoring,
                "attempts": attempts,
            }

        # -----------------------------------------------------
        # Review the refactored patch independently.
        # -----------------------------------------------------

        refactoring_review = self.patch_reviewer.review(
            problem=problem,
            traceback="",
            root_cause=root_cause,
            patch=refactoring_patch,
            code_context=code_context,
        )

        if refactoring_review.get("decision") == "approve":

            return {
                "success": True,
                "patch": refactoring_patch,
                "summary": (
                    "Patch approved and localized "
                    "refactoring also passed review."
                ),
                "review": refactoring_review,
                "refactoring": refactoring,
                "attempts": attempts,
            }

        # If refactoring fails review, retain the original
        # approved patch rather than losing a valid fix.

        return {
            "success": True,
            "patch": approved_patch,
            "summary": (
                "Original patch was approved. The proposed "
                "refactoring did not pass review, so the "
                "original approved patch is retained."
            ),
            "review": review,
            "refactoring": {
                **refactoring,
                "review": refactoring_review,
            },
            "attempts": attempts,
        }