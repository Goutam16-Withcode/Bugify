import re
from typing import Dict, List, Optional

from llm.groq_client import get_llm


class RefactoringAgent:
    """
    Performs narrowly scoped refactoring related to a bug fix.

    The agent does not directly modify repository files.
    It proposes a unified diff that can later be reviewed
    and verified by the Bugify pipeline.
    """

    def __init__(self):
        self.llm = get_llm()

    def refactor(
        self,
        problem: str,
        root_cause: Optional[str],
        approved_patch: str,
        code_context: Dict,
        relevant_files: List[str],
    ) -> Dict:
        """
        Generate a localized refactoring if necessary.

        Returns:
            {
                "required": bool,
                "patch": str,
                "summary": str,
            }
        """

        if not approved_patch.strip():
            return {
                "required": False,
                "patch": "",
                "summary": "No approved patch was provided.",
            }

        prompt = self._build_prompt(
            problem=problem,
            root_cause=root_cause,
            approved_patch=approved_patch,
            code_context=code_context,
            relevant_files=relevant_files,
        )

        response = self.llm.invoke(prompt)

        content = response.content.strip()

        return self._parse_response(content)

    def _build_prompt(
        self,
        problem: str,
        root_cause: Optional[str],
        approved_patch: str,
        code_context: Dict,
        relevant_files: List[str],
    ) -> str:
        """
        Build a strict refactoring prompt.
        """

        files = "\n".join(
            f"- {file}"
            for file in relevant_files
        )

        return f"""
You are the Refactoring Agent inside Bugify.

Your responsibility is to determine whether a bug fix requires
a SMALL, LOCALIZED structural refactoring.

You are NOT a general-purpose code cleanup agent.

The candidate bug fix has already passed an initial patch review.

Your job is NOT to redesign the application.

Your job is to determine whether a narrowly scoped refactoring
is genuinely necessary or clearly beneficial for the correctness
and maintainability of the approved fix.

============================================================
BUG REPORT
============================================================

{problem}

============================================================
ROOT CAUSE
============================================================

{root_cause or "No root cause was supplied."}

============================================================
RELEVANT FILES
============================================================

{files or "No relevant files supplied."}

============================================================
CODE CONTEXT
============================================================

{code_context}

============================================================
APPROVED PATCH
============================================================

{approved_patch}

============================================================
CORE PRINCIPLE
============================================================

DO NOT REFACTOR FOR THE SAKE OF REFACTORING.

If the approved patch is already sufficiently clear,
localized, and maintainable, return:

NO_REFACTOR

A smaller patch is preferred over a larger refactoring.

============================================================
WHEN REFACTORING IS ALLOWED
============================================================

A refactoring may be proposed ONLY when there is strong evidence
that it addresses one of the following:

1. The approved fix creates clear duplicated logic.

2. The approved fix introduces an obvious structural problem
   that can be removed with a small localized change.

3. The bug cannot be safely fixed without a small restructuring
   of the affected code.

4. Existing code already contains an appropriate abstraction
   that should be reused instead of duplicating logic.

5. The approved fix creates a clear violation of an existing
   local code pattern that is directly relevant to correctness.

============================================================
WHEN REFACTORING IS FORBIDDEN
============================================================

DO NOT:

- redesign the architecture
- rewrite modules
- reorganize the repository
- rename unrelated functions
- rename unrelated variables
- change public APIs
- change database schemas
- introduce new frameworks
- introduce unnecessary dependencies
- modernize unrelated code
- optimize unrelated code
- reformat entire files
- change coding style globally
- perform broad cleanup
- rewrite working code
- change tests merely for style
- introduce abstractions without clear evidence

The bug fix must remain the primary purpose of the change.

============================================================
SCOPE CONTROL
============================================================

Every changed line must have a direct relationship to:

- the original bug
- the approved patch
- or a clearly necessary structural consequence of the fix

If the refactoring cannot be justified using the supplied
evidence, return:

NO_REFACTOR

============================================================
BEHAVIOR PRESERVATION
============================================================

The refactoring MUST preserve:

- public interfaces
- function signatures
- return values
- input/output behavior
- exception semantics
- side effects
- state behavior
- concurrency behavior
- configuration behavior

unless changing one of these is absolutely necessary for
the original bug and is explicitly supported by the evidence.

============================================================
DEPENDENCY RULE
============================================================

Do not introduce a dependency.

Do not change dependency versions.

Do not add a framework.

Use the existing project structure and dependencies.

============================================================
SECURITY RULE
============================================================

The refactoring must not introduce:

- hardcoded secrets
- unsafe subprocess execution
- arbitrary command execution
- authentication bypass
- authorization bypass
- insecure deserialization
- unsafe file access
- SQL injection
- command injection
- path traversal

============================================================
MINIMALITY
============================================================

The refactoring must be smaller than a normal architectural
refactor.

Prefer:

    local extraction
    local reuse
    removal of duplication
    small structural correction

Avoid:

    large-scale redesign
    module restructuring
    architectural changes

If the refactoring is larger than the original bug fix,
strongly prefer:

NO_REFACTOR

============================================================
DECISION PROCESS
============================================================

First determine:

Does the approved patch actually require refactoring?

If NO:

    return NO_REFACTOR

If YES:

    generate the smallest safe unified diff.

Do not generate a refactoring merely because the code could
be cleaner.

============================================================
OUTPUT CONTRACT
============================================================

Return ONLY one of the following.

OPTION 1:

NO_REFACTOR

OPTION 2:

Return a valid unified diff.

Example:

--- a/src/example.py
+++ b/src/example.py
@@ -10,6 +10,8 @@
 existing code
+new localized structure
 existing code

Do NOT return:

- explanations
- Markdown
- code fences
- reasoning
- alternative solutions
- comments outside the diff

============================================================
FINAL QUALITY CHECK
============================================================

Before returning a refactoring, verify:

[ ] Is it directly related to the approved bug fix?
[ ] Is it genuinely necessary or strongly justified?
[ ] Is it minimal?
[ ] Does it preserve behavior?
[ ] Does it preserve public interfaces?
[ ] Does it avoid new dependencies?
[ ] Does it avoid unrelated cleanup?
[ ] Does it avoid security risks?
[ ] Is the unified diff valid?
[ ] Could the system safely skip this refactoring?

If the final answer to the last question is YES:

Return:

NO_REFACTOR

Do not refactor code simply because it can be improved.

Return ONLY NO_REFACTOR or the unified diff.
"""

    def _parse_response(self, content: str) -> Dict:
        """
        Parse the LLM response.

        Supports:
        - NO_REFACTOR
        - unified diff
        """

        if not content:
            return {
                "required": False,
                "patch": "",
                "summary": "No refactoring was proposed.",
            }

        content = content.strip()

        if content.upper() == "NO_REFACTOR":
            return {
                "required": False,
                "patch": "",
                "summary": "No refactoring is required.",
            }

        content = re.sub(
            r"^```(?:diff|patch)?\s*",
            "",
            content,
            flags=re.IGNORECASE,
        )

        content = re.sub(
            r"\s*```$",
            "",
            content,
        )

        content = content.strip()

        if (
            "--- " not in content
            or "+++ " not in content
        ):
            return {
                "required": False,
                "patch": "",
                "summary": (
                    "Invalid refactoring response. "
                    "No refactoring will be applied."
                ),
            }

        return {
            "required": True,
            "patch": content,
            "summary": self._create_summary(content),
        }

    def _create_summary(
        self,
        patch: str,
    ) -> str:
        """
        Create a deterministic summary from the diff.
        """

        changed_files = []

        for line in patch.splitlines():

            if line.startswith("+++ b/"):
                file_path = line[6:].strip()

                if file_path not in changed_files:
                    changed_files.append(file_path)

        if not changed_files:
            return "Localized refactoring proposed."

        if len(changed_files) == 1:
            return (
                "Localized refactoring proposed for "
                f"{changed_files[0]}."
            )

        return (
            "Localized refactoring proposed for "
            f"{len(changed_files)} files."
        )