import json
from typing import Dict, Optional

from llm.groq_client import get_llm


class PatchReviewer:
    """
    Reviews a generated patch against the bug evidence
    and determines whether it is safe and relevant.
    """

    ALLOWED_DECISIONS = {
        "approve",
        "reject",
        "revise",
    }

    def __init__(self):
        self.llm = get_llm()

    def review(
        self,
        problem: str,
        traceback: str,
        root_cause: Optional[str],
        patch: str,
        code_context: Dict,
    ) -> Dict:
        """
        Review a candidate patch.

        Returns:
            {
                "decision": str,
                "confidence": float,
                "reason": str,
                "issues": list[str],
            }
        """

        if not patch.strip():
            return {
                "decision": "reject",
                "confidence": 1.0,
                "reason": "Patch is empty.",
                "issues": ["No patch was provided."],
            }

        prompt = self._build_prompt(
            problem=problem,
            traceback=traceback,
            root_cause=root_cause,
            patch=patch,
            code_context=code_context,
        )

        response = self.llm.invoke(prompt)

        content = response.content.strip()

        result = self._parse_response(content)

        return result

    def _build_prompt(
        self,
        problem: str,
        traceback: str,
        root_cause: Optional[str],
        patch: str,
        code_context: Dict,
    ) -> str:

        return f"""
You are the Patch Reviewer in Bugify,
an autonomous software debugging system.

Your job is to critically review a candidate patch BEFORE
it is allowed to proceed to execution.

You are NOT the patch generator.

Do not assume the generated patch is correct.

Your responsibility is to determine whether the patch is:

1. Relevant to the reported bug
2. Consistent with the root cause
3. Minimal
4. Technically plausible
5. Safe
6. Scoped correctly
7. Consistent with the existing code
8. Free from obvious regressions

============================================================
BUG REPORT
============================================================

{problem}

============================================================
TRACEBACK
============================================================

{traceback}

============================================================
ROOT CAUSE
============================================================

{root_cause or "No confirmed root cause provided."}

============================================================
CODE CONTEXT
============================================================

{code_context}

============================================================
CANDIDATE PATCH
============================================================

{patch}

============================================================
REVIEW RULES
============================================================

REJECT the patch if:

- It does not address the root cause.
- It changes unrelated functionality.
- It modifies unrelated files.
- It introduces unnecessary dependencies.
- It invents APIs, variables, functions, or behavior.
- It suppresses the original error instead of fixing it.
- It weakens security.
- It introduces obvious unsafe behavior.
- It changes public interfaces without justification.
- It modifies tests only to make them pass.
- It contains an obviously invalid or malformed diff.
- It makes a large change when a smaller change is sufficient.
- The evidence is insufficient to justify the patch.

REQUEST REVISION if:

- The general approach is reasonable.
- The patch appears related to the root cause.
- But the implementation is unnecessarily broad,
  incomplete, or needs a small correction.

APPROVE only when:

- The patch directly addresses the root cause.
- The changes are minimal.
- The modified files are relevant.
- Existing behavior is preserved.
- No obvious security or regression issue exists.
- The patch is consistent with the provided code context.

============================================================
IMPORTANT
============================================================

Do not approve a patch simply because it looks syntactically
reasonable.

Review it against the actual bug evidence.

Do not invent test results.

Do not claim that the patch works at runtime.

Runtime correctness will be established later by the
Verification Agent.

============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

Use exactly this structure:

{{
    "decision": "approve",
    "confidence": 0.95,
    "reason": "The patch directly fixes the identified root cause with a minimal change.",
    "issues": []
}}

Allowed decisions:

- "approve"
- "reject"
- "revise"

Confidence MUST be a number between 0.0 and 1.0.

If rejecting or requesting revision, provide concrete issues.

Do not return Markdown.
Do not return code fences.
Do not return additional text.
"""

    def _parse_response(self, content: str) -> Dict:
        """
        Parse and validate the reviewer's JSON response.
        """

        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

        try:
            result = json.loads(content)

            decision = result.get("decision")
            confidence = result.get("confidence")
            reason = result.get("reason")
            issues = result.get("issues")

            if decision not in self.ALLOWED_DECISIONS:
                raise ValueError("Invalid review decision.")

            if not isinstance(
                confidence,
                (int, float),
            ):
                raise ValueError(
                    "Invalid confidence value."
                )

            if not 0.0 <= confidence <= 1.0:
                raise ValueError(
                    "Confidence must be between 0 and 1."
                )

            if not isinstance(reason, str):
                raise ValueError(
                    "Invalid review reason."
                )

            if not isinstance(issues, list):
                raise ValueError(
                    "Invalid issues list."
                )

            return {
                "decision": decision,
                "confidence": float(confidence),
                "reason": reason,
                "issues": issues,
            }

        except (
            json.JSONDecodeError,
            ValueError,
            TypeError,
        ):
            return {
                "decision": "reject",
                "confidence": 0.0,
                "reason": (
                    "Reviewer returned invalid output."
                ),
                "issues": [
                    "Invalid reviewer response format."
                ],
            }