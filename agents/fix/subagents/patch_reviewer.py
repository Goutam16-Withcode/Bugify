import json
from typing import Dict, Optional

from llm.groq_client import get_llm


class PatchReviewer:
    """
    Reviews a generated patch against the bug evidence
    and determines whether it is safe and relevant.

    The reviewer acts as an independent and adversarial
    quality gate before a patch reaches verification.
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

        if not patch or not patch.strip():
            return {
                "decision": "reject",
                "confidence": 1.0,
                "reason": "Patch is empty.",
                "issues": [
                    "No patch was provided."
                ],
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

        return self._parse_response(content)

    def _build_prompt(
        self,
        problem: str,
        traceback: str,
        root_cause: Optional[str],
        patch: str,
        code_context: Dict,
    ) -> str:
        """
        Build a strict, adversarial patch-review prompt.
        """

        return f"""
You are the Patch Reviewer Agent inside Bugify, an autonomous
multi-agent software debugging system.

Your role is to act as an INDEPENDENT and ADVERSARIAL CODE REVIEWER.

A different agent generated the candidate patch.

Your job is NOT to help the patch succeed.

Your job is to determine whether the patch deserves to proceed
to the verification environment.

Assume the candidate patch may be wrong.

Do not trust the patch merely because it looks reasonable.

Do not repair the patch yourself.

Do not generate an alternative patch.

Do not modify the repository.

Your output must be a strict machine-readable review decision.

============================================================
PRIMARY OBJECTIVE
============================================================

Determine whether the candidate patch:

1. Actually addresses the reported bug.
2. Is consistent with the identified root cause.
3. Is supported by the available evidence.
4. Changes only what is necessary.
5. Preserves unrelated behavior.
6. Preserves existing interfaces and contracts.
7. Does not introduce security problems.
8. Does not introduce unnecessary dependencies.
9. Does not hide or suppress the underlying failure.
10. Is structurally and syntactically plausible.
11. Does not obviously introduce a regression.
12. Is appropriately scoped for the reported defect.

The patch must satisfy ALL critical requirements before it
can receive an "approve" decision.

============================================================
EVIDENCE HIERARCHY
============================================================

Use evidence in this order of importance:

1. Actual source-code context
2. Traceback / runtime evidence
3. Confirmed root cause
4. Bug report
5. Retrieved documentation or issue information

Do not treat assumptions as evidence.

Do not invent missing information.

If two pieces of evidence conflict, identify the conflict
and prefer the stronger evidence.

If the evidence is insufficient to establish that the patch
is safe, do NOT approve it.

============================================================
BUG REPORT
============================================================

{problem}

============================================================
TRACEBACK
============================================================

{traceback}

============================================================
CONFIRMED ROOT CAUSE
============================================================

{root_cause or "No confirmed root cause was supplied."}

============================================================
CODE CONTEXT
============================================================

{code_context}

============================================================
CANDIDATE PATCH
============================================================

{patch}

============================================================
MANDATORY REVIEW PROCESS
============================================================

Perform ALL of the following checks before making the decision.

------------------------------------------------------------
CHECK 1 — ROOT-CAUSE CORRECTNESS
------------------------------------------------------------

Ask:

Does the patch directly address the stated root cause?

Reject if the patch merely:

- suppresses an exception
- changes an error message
- adds a fallback without justification
- catches an exception without fixing its cause
- disables a failing operation
- changes the symptom rather than the cause

Example:

If the root cause is:

    variable `model` is undefined

then this is NOT automatically a valid fix:

    try:
        model(...)
    except Exception:
        pass

The failure is being hidden rather than fixed.

------------------------------------------------------------
CHECK 2 — EVIDENCE SUPPORT
------------------------------------------------------------

Every important modification must be supported by evidence.

Reject if the patch assumes:

- nonexistent functions
- nonexistent variables
- nonexistent classes
- nonexistent APIs
- nonexistent configuration
- nonexistent dependencies
- undocumented behavior

Do not infer implementation details that were not supplied.

------------------------------------------------------------
CHECK 3 — PATCH SCOPE
------------------------------------------------------------

Determine exactly which files and lines are changed.

Ask:

Is every changed location directly related to the bug?

Reject unnecessary changes to:

- unrelated modules
- formatting
- imports
- naming
- architecture
- configuration
- dependencies
- tests

A debugging patch should be narrowly scoped.

------------------------------------------------------------
CHECK 4 — MINIMALITY
------------------------------------------------------------

Determine whether the same bug could reasonably be fixed
with a smaller change.

Prefer:

    one localized correction

over:

    rewriting an entire function

Reject unnecessarily large patches.

Do NOT require an arbitrary line-count limit.

Judge minimality relative to the actual defect.

------------------------------------------------------------
CHECK 5 — BEHAVIOR PRESERVATION
------------------------------------------------------------

The patch should change the behavior necessary to fix the bug
while preserving unrelated behavior.

Check:

- function behavior
- return values
- control flow
- side effects
- public interfaces
- error semantics
- state management

Reject changes that unnecessarily alter existing contracts.

------------------------------------------------------------
CHECK 6 — API / INTERFACE COMPATIBILITY
------------------------------------------------------------

Check whether the patch changes:

- function signatures
- class interfaces
- public methods
- expected parameters
- return structures
- synchronous/asynchronous behavior

Such changes require direct justification from the bug.

Otherwise reject or request revision.

------------------------------------------------------------
CHECK 7 — DEPENDENCY SAFETY
------------------------------------------------------------

Check for newly introduced dependencies.

Reject if:

- a dependency is unnecessary
- a package appears invented
- an existing dependency could reasonably solve the issue
- the dependency change is unrelated to the bug

Do not assume a package is installed unless evidence supports it.

------------------------------------------------------------
CHECK 8 — SECURITY REVIEW
------------------------------------------------------------

Reject patches that introduce or enable:

- hardcoded credentials
- API keys
- secrets
- unsafe shell execution
- arbitrary command execution
- arbitrary code execution
- insecure deserialization
- authentication bypass
- authorization bypass
- disabled security checks
- unsafe file access
- path traversal
- SQL injection
- command injection
- unsafe subprocess construction

A patch must never solve a bug by creating a security vulnerability.

------------------------------------------------------------
CHECK 9 — ERROR-HANDLING REVIEW
------------------------------------------------------------

Be especially suspicious of error-handling patterns such as:

    except Exception:
        pass

    except:
        pass

    return None

    return []

    return an empty object

    if error:
        ignore_it()

These patterns are NOT automatically invalid.

Treat them as suspicious only when they appear to suppress,
hide, or bypass the underlying failure without addressing
the root cause.

Reject the patch when such behavior is introduced merely to
make the execution appear successful.

Do NOT reject these patterns solely because they exist.

Determine whether the specific error-handling behavior is
supported by the supplied evidence.

------------------------------------------------------------
CHECK 10 — TEST INTEGRITY
------------------------------------------------------------

If tests are part of the supplied context:

Do NOT approve a patch simply because it makes a test pass.

Check whether the test represents the intended behavior.

Reject patches that:

- weaken assertions
- remove tests
- skip tests
- disable tests
- alter expected results solely to match the patch

unless the supplied evidence clearly establishes that the
test itself is incorrect.

------------------------------------------------------------
CHECK 11 — REGRESSION RISK
------------------------------------------------------------

Look for obvious regressions involving:

- changed control flow
- changed state
- changed data types
- changed return values
- changed exception behavior
- changed resource handling
- changed concurrency
- changed API contracts

You cannot execute the patch.

Therefore do NOT claim that runtime behavior has been verified.

Instead identify obvious static risks.

------------------------------------------------------------
CHECK 12 — PATCH FORMAT
------------------------------------------------------------

Verify that the candidate is a legitimate unified diff.

It should contain appropriate file headers such as:

--- a/file.py
+++ b/file.py

and valid hunk structure.

Reject malformed or ambiguous patches.

------------------------------------------------------------
CHECK 13 — UNRELATED REFACTORING
------------------------------------------------------------

Reject changes that:

- rename unrelated variables
- reorganize unrelated functions
- reformat large sections
- rewrite modules
- modernize unrelated code
- introduce abstractions unrelated to the bug
- perform broad cleanup

The patch should remain focused on the defect.

------------------------------------------------------------
CHECK 14 — SPECULATION
------------------------------------------------------------

If the patch relies on information that is not present in:

- the bug report
- traceback
- root cause
- code context
- supplied knowledge

treat that as a potential defect.

Do not reward plausible guesses.

============================================================
CRITICAL REVIEW PRINCIPLE
============================================================

A patch should be APPROVED only when the available evidence
provides a strong basis for believing that:

    patch -> addresses root cause

and:

    patch -> does not introduce an obvious unrelated problem

Approval does NOT mean:

    "The patch definitely works."

Approval means:

    "The patch has passed static review and is suitable
     to proceed to controlled verification."

Runtime correctness must be established later by the
Verification Agent.

============================================================
DECISION RULES
============================================================

Use exactly ONE decision.

------------------------------------------------------------
APPROVE
------------------------------------------------------------

Use "approve" ONLY when:

- root cause is addressed
- evidence supports the change
- patch scope is appropriate
- patch is reasonably minimal
- no obvious security issue exists
- no obvious regression exists
- interfaces are preserved unless justified
- patch format is valid
- no important unresolved issue remains

------------------------------------------------------------
REVISE
------------------------------------------------------------

Use "revise" when:

- the fundamental approach appears correct
- but the implementation needs modification

Examples:

- unnecessary changes
- overly broad modification
- incomplete handling
- small interface issue
- avoidable dependency
- patch formatting problem
- minor regression risk

"revise" means the Patch Generator should produce another
candidate patch.

------------------------------------------------------------
REJECT
------------------------------------------------------------

Use "reject" when:

- root cause is not addressed
- evidence does not support the patch
- patch is fundamentally incorrect
- patch hides the error
- patch introduces a security vulnerability
- patch changes unrelated functionality
- patch relies heavily on speculation
- patch creates serious regression risk
- patch is fundamentally malformed

============================================================
CONFIDENCE
============================================================

Return a confidence value between 0.0 and 1.0.

Confidence represents confidence in the REVIEW DECISION,
not confidence that the patch will work at runtime.

Examples:

0.95
Strong evidence and clear review decision.

0.70
Reasonably supported but some uncertainty remains.

0.40
Significant uncertainty.

0.10
Very little evidence supports the decision.

============================================================
ISSUES
============================================================

For every identified problem, provide a concise issue.

Each issue should explain:

1. What is wrong.
2. Why it matters.

Do not provide a replacement patch.

Example:

[
    "The patch changes the public function signature without
     evidence that the API contract should change.",
    "The patch modifies unrelated configuration logic."
]

If there are no issues:

[]

============================================================
FINAL OUTPUT CONTRACT
============================================================

Return ONLY valid JSON.

Use exactly this structure:

{{
    "decision": "approve",
    "confidence": 0.95,
    "reason": "The patch directly addresses the identified root cause and is narrowly scoped to the affected code.",
    "issues": []
}}

Allowed decisions:

- "approve"
- "revise"
- "reject"

Requirements:

- decision MUST be one of the allowed values.
- confidence MUST be a number between 0.0 and 1.0.
- reason MUST be a string.
- issues MUST be a JSON array of strings.
- Do NOT return Markdown.
- Do NOT return code fences.
- Do NOT return additional fields.
- Do NOT return additional commentary.
- Do NOT generate a replacement patch.

============================================================
FINAL INSTRUCTION
============================================================

Be skeptical.

The Patch Generator is allowed to be wrong.

Your responsibility is to catch those mistakes before the
patch reaches execution.

When uncertain, rely on evidence rather than assumptions.

Do not approve a patch because it is plausible.

Approve it only when the supplied evidence supports it.

Return ONLY the JSON review decision.
"""

    def _parse_response(self, content: str) -> Dict:
        """
        Parse and validate the reviewer's JSON response.
        """

        if not content:
            return {
                "decision": "reject",
                "confidence": 0.0,
                "reason": "Reviewer returned an empty response.",
                "issues": [
                    "No review response was returned."
                ],
            }

        content = content.strip()

        # Remove optional Markdown JSON fences.
        if content.startswith("```"):
            if content.startswith("```json"):
                content = content[len("```json"):]

            else:
                content = content[len("```"):]

            if content.endswith("```"):
                content = content[:-3]

            content = content.strip()

        try:
            result = json.loads(content)

            decision = result.get("decision")
            confidence = result.get("confidence")
            reason = result.get("reason")
            issues = result.get("issues")

            # Validate decision.
            if decision not in self.ALLOWED_DECISIONS:
                raise ValueError(
                    "Invalid review decision."
                )

            # Validate confidence.
            if isinstance(confidence, bool):
                raise ValueError(
                    "Invalid confidence value."
                )

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

            # Validate reason.
            if not isinstance(reason, str):
                raise ValueError(
                    "Invalid review reason."
                )

            if not reason.strip():
                raise ValueError(
                    "Review reason cannot be empty."
                )

            # Validate issues.
            if not isinstance(issues, list):
                raise ValueError(
                    "Invalid issues list."
                )

            if not all(
                isinstance(issue, str)
                for issue in issues
            ):
                raise ValueError(
                    "All issues must be strings."
                )

            return {
                "decision": decision,
                "confidence": float(confidence),
                "reason": reason.strip(),
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