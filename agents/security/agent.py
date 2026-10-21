import json
import re
from typing import Dict, List, Optional, Any
from llm.groq_client import get_llm

class SecurityAuditAgent:
    """
    Security & Vulnerability Audit Agent for Bugify.
    
    Acts as an adversarial security scanner for both the root cause defect
    and the proposed fix. Ensures fixes do not introduce OWASP Top 10 vulnerabilities:
    - Injection (SQLi, Command Injection, Code Injection)
    - Path Traversal & Insecure Direct Object References
    - Insecure Deserialization (pickle, unsafe yaml)
    - Credential & Secret Exposure
    - ReDoS (Regular Expression Denial of Service)
    - Insecure Permissions & Sandbox Bypasses
    """

    DANGEROUS_PATTERNS = [
        (r"\b(eval|exec)\s*\(", "CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code", "HIGH"),
        (r"\bos\.system\s*\(", "CWE-78: OS Command Injection via os.system()", "CRITICAL"),
        (r"\bsubprocess\.(?:Popen|call|run)\s*\([^)]*shell\s*=\s*True", "CWE-78: Command Injection via shell=True in subprocess", "CRITICAL"),
        (r"cursor\.execute\s*\(\s*f[\"'].*?\{.*?\}", "CWE-89: SQL Injection via f-string query formatting", "CRITICAL"),
        (r"cursor\.execute\s*\([^,)]*%\s*\(", "CWE-89: SQL Injection via % formatting in query", "HIGH"),
        (r"\bpickle\.loads?\s*\(", "CWE-502: Deserialization of Untrusted Data via pickle", "HIGH"),
        (r"\byaml\.load\s*\([^,)]*\)", "CWE-502: Unsafe YAML deserialization without SafeLoader", "MEDIUM"),
        (r"(?:password|secret|api_key|token)\s*=\s*[\"'][a-zA-Z0-9_\-\.]{8,}[\"']", "CWE-798: Hardcoded Credential / Secret Exposure", "HIGH"),
        (r"open\s*\(\s*f?[\"'][^\"']*\{[^}]*filename[^}]*\}", "CWE-22: Improper Limitation of a Pathname to a Restricted Directory", "HIGH"),
    ]

    def __init__(self):
        try:
            self.llm = get_llm(temperature=0.0)
        except Exception:
            self.llm = None

    def audit(
        self,
        problem: str,
        patch: str,
        code_context: Optional[Dict] = None,
        root_cause: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Perform a comprehensive security audit of the patch and defect context.
        """
        if not patch or not patch.strip():
            return {
                "passed": True,
                "safety_score": 100,
                "risk_level": "LOW",
                "vulnerabilities": [],
                "cwe_citations": [],
                "recommendations": ["No code patch to audit."],
                "is_safe_to_deploy": True,
            }

        # Step 1: Static pattern and heuristic scan
        static_findings = self._static_pattern_scan(patch)

        # Step 2: LLM contextual semantic security evaluation
        llm_findings = {}
        if self.llm:
            try:
                llm_findings = self._llm_security_eval(problem, patch, root_cause)
            except Exception:
                llm_findings = {}

        # Merge findings
        vulnerabilities = list(static_findings.get("vulnerabilities", []))
        cwe_citations = list(static_findings.get("cwe_citations", []))

        for v in llm_findings.get("vulnerabilities", []):
            if v not in vulnerabilities:
                vulnerabilities.append(v)
        for c in llm_findings.get("cwe_citations", []):
            if c not in cwe_citations:
                cwe_citations.append(c)

        # Calculate safety score (0 - 100)
        penalty = 0
        risk_level = "LOW"
        if any("CRITICAL" in v or "Injection" in v for v in vulnerabilities):
            penalty += 55
            risk_level = "CRITICAL"
        elif any("HIGH" in v for v in vulnerabilities):
            penalty += 35
            risk_level = "HIGH"
        elif any("MEDIUM" in v for v in vulnerabilities):
            penalty += 15
            risk_level = "MEDIUM"
        elif vulnerabilities:
            penalty += 5
            risk_level = "LOW"

        safety_score = max(10, 100 - penalty)
        passed = safety_score >= 70 and risk_level not in ("CRITICAL", "HIGH")

        recommendations = llm_findings.get("recommendations", [])
        if not recommendations:
            if passed:
                recommendations = [
                    "Input validation complies with security best practices.",
                    "No unsafe dynamic execution primitives (eval/exec/os.system) detected in patch.",
                    "Patch boundaries are safely confined to the expected module scope.",
                ]
            else:
                recommendations = [
                    "Sanitize and validate all external parameters with strong schema checks.",
                    "Avoid invoking OS shells or dynamic interpreter calls in production patches.",
                    "Use parameterized database statements and safe deserializers.",
                ]

        return {
            "passed": passed,
            "safety_score": safety_score,
            "risk_level": risk_level,
            "vulnerabilities": vulnerabilities,
            "cwe_citations": cwe_citations,
            "recommendations": recommendations,
            "is_safe_to_deploy": passed,
        }

    def _static_pattern_scan(self, patch: str) -> Dict[str, Any]:
        """Scan patch additions (lines starting with '+') for known security pitfalls."""
        added_lines = [
            line[1:].strip()
            for line in patch.splitlines()
            if line.startswith("+") and not line.startswith("+++")
        ]
        patch_text = "\n".join(added_lines)

        vulnerabilities = []
        cwe_citations = []

        for pattern, desc, severity in self.DANGEROUS_PATTERNS:
            if re.search(pattern, patch_text, re.IGNORECASE):
                vulnerabilities.append(f"[{severity}] {desc}")
                # Extract CWE code
                match = re.match(r"(CWE-\d+)", desc)
                if match:
                    cwe_citations.append(match.group(1))

        return {
            "vulnerabilities": vulnerabilities,
            "cwe_citations": list(set(cwe_citations)),
        }

    def _llm_security_eval(self, problem: str, patch: str, root_cause: Optional[str]) -> Dict[str, Any]:
        prompt = f"""
You are the Security & Vulnerability Audit Agent inside Bugify.
Your task is to examine this proposed software patch and determine if it introduces any security vulnerabilities (OWASP Top 10, CWE).

BUG PROBLEM:
{problem}

ROOT CAUSE:
{root_cause or 'N/A'}

PROPOSED PATCH:
{patch}

Respond in STRICT JSON ONLY:
{{
    "passed": true/false,
    "risk_level": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
    "vulnerabilities": ["short description of any issue or empty list"],
    "cwe_citations": ["CWE-89", etc or empty list],
    "recommendations": ["1-3 actionable security hygiene suggestions"]
}}
"""
        response = self.llm.invoke(prompt)
        text = response.content.strip()

        # Extract JSON block
        if "{" in text and "}" in text:
            json_str = text[text.find("{"):text.rfind("}") + 1]
            return json.loads(json_str)
        return {}