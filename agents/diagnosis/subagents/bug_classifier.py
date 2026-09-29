import json
from typing import Dict, List, Optional

from llm.groq_client import get_llm


class BugClassifier:

    def __init__(self):
        self.llm = get_llm()

    def classify(
        self,
        error_type: Optional[str],
        error_message: Optional[str],
        logs: List[str],
        patterns: List[str],
    ) -> Dict:

        prompt = f"""
You are Bugify's Bug Classification Agent.

Your task is to classify a software bug using ONLY the evidence provided below.

You are part of a larger autonomous debugging system. Your output will be
consumed programmatically by downstream agents. Accuracy, consistency,
and strict JSON formatting are required.

CLASSIFICATION OBJECTIVE

Determine:

1. bug_type
2. category
3. severity
4. confidence

Do NOT attempt to fix the bug.
Do NOT invent missing information.
Do NOT treat warnings as errors unless the evidence indicates that
the warning caused the failure.

BUG TYPE DEFINITIONS

runtime:
The program starts executing but fails during execution.

logic:
The program executes but produces incorrect or unexpected behavior/output.

syntax:
The source code cannot be parsed or compiled because of invalid syntax.

dependency:
The failure is caused by a missing, incompatible, corrupted, or incorrectly
installed package, library, or version.

configuration:
The failure is caused by incorrect or missing configuration, environment
variables, configuration files, paths, or settings.

memory:
The failure is primarily related to memory exhaustion or memory management.

network:
The failure is primarily related to network communication.

hardware:
The failure is primarily caused by hardware, device, driver, or accelerator
incompatibility.

unknown:
There is insufficient evidence to determine the bug type reliably.

SEVERITY DEFINITIONS

low:
Minor issue with limited impact.

medium:
Significant issue affecting a feature or workflow.

high:
Major failure affecting an important workflow or application component.

critical:
Severe failure such as complete application failure, data loss,
or inability to operate the core system.

CATEGORY

Return a concise and specific category.

Examples:

"undefined_variable"
"missing_import"
"type_mismatch"
"null_reference"
"index_out_of_range"
"dependency_version_conflict"
"missing_environment_variable"
"cuda_memory_exhaustion"
"network_timeout"
"authentication_failure"
"invalid_configuration"

CONFIDENCE

Return a number between 0.0 and 1.0.

0.90 - 1.00 = strong direct evidence
0.75 - 0.89 = good evidence
0.50 - 0.74 = moderate uncertainty
0.00 - 0.49 = insufficient evidence

EVIDENCE PRIORITY

Prioritize evidence in this order:

1. Explicit exception/error type
2. Explicit error message
3. Traceback information
4. Repeated log failures
5. Detected technical patterns
6. General contextual clues

Do not infer a bug type solely from generic words such as "failed".

INPUT

Error Type:
{error_type}

Error Message:
{error_message}

Relevant Logs:
{logs}

Detected Patterns:
{patterns}

OUTPUT REQUIREMENTS

Return ONLY a valid JSON object.

The JSON object MUST contain exactly these fields:

{{
    "bug_type": "runtime",
    "category": "specific_category",
    "severity": "medium",
    "confidence": 0.85
}}

Allowed bug_type values:

"runtime"
"logic"
"syntax"
"dependency"
"configuration"
"memory"
"network"
"hardware"
"unknown"

Allowed severity values:

"low"
"medium"
"high"
"critical"

confidence MUST be between 0.0 and 1.0.

Do not return Markdown.
Do not return code fences.
Do not return explanations.
Do not return additional fields.
Do not return recommendations.
Do not return fixes.

If the evidence is insufficient, return:

{{
    "bug_type": "unknown",
    "category": "insufficient_evidence",
    "severity": "low",
    "confidence": 0.0
}}
"""

        response = self.llm.invoke(prompt)

        content = response.content.strip()

        # Handle accidental markdown code fences
        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

        try:
            result = json.loads(content)

            # Basic validation
            allowed_bug_types = {
                "runtime",
                "logic",
                "syntax",
                "dependency",
                "configuration",
                "memory",
                "network",
                "hardware",
                "unknown",
            }

            allowed_severity = {
                "low",
                "medium",
                "high",
                "critical",
            }

            if result.get("bug_type") not in allowed_bug_types:
                raise ValueError("Invalid bug_type")

            if result.get("severity") not in allowed_severity:
                raise ValueError("Invalid severity")

            confidence = result.get("confidence")

            if not isinstance(confidence, (int, float)):
                raise ValueError("Invalid confidence")

            if not 0.0 <= confidence <= 1.0:
                raise ValueError("Confidence must be between 0 and 1")

            return result

        except (json.JSONDecodeError, ValueError, TypeError):
            return {
                "bug_type": "unknown",
                "category": "invalid_classifier_output",
                "severity": "low",
                "confidence": 0.0,
            }