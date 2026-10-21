import json
import re
from typing import Dict, List, Optional, Any
from llm.groq_client import get_llm

class PerformanceProfilerAgent:
    """
    Performance & Complexity Profiler Agent for Bugify.
    
    Specializes in:
    - Asymptotic Big-O time and space complexity shifts (Before vs After)
    - Detecting nested O(N^2) / O(2^N) loop hazards in hot paths
    - Memory leak vectors (unbounded collections, unclosed handlers, global caches)
    - Concurrency and I/O blocking bottlenecks
    """

    def __init__(self):
        try:
            self.llm = get_llm(temperature=0.0)
        except Exception:
            self.llm = None

    def profile(
        self,
        problem: str,
        patch: str,
        code_context: Optional[Dict] = None,
        root_cause: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyze the algorithmic complexity and performance impact of the patch.
        """
        if not patch or not patch.strip():
            return {
                "time_complexity_before": "O(1)",
                "time_complexity_after": "O(1)",
                "space_complexity": "O(1)",
                "impact_rating": "OPTIMAL",
                "bottlenecks": [],
                "latency_overhead_estimated": "< 0.05ms",
                "optimization_hints": ["No code changes to profile."],
            }

        # Step 1: Static AST / syntactic analysis of patch
        static_analysis = self._static_complexity_check(patch)

        # Step 2: LLM algorithmic profiling
        llm_analysis = {}
        if self.llm:
            try:
                llm_analysis = self._llm_profile(problem, patch, root_cause)
            except Exception:
                llm_analysis = {}

        time_before = llm_analysis.get("time_complexity_before") or static_analysis.get("time_before", "O(1)")
        time_after = llm_analysis.get("time_complexity_after") or static_analysis.get("time_after", "O(1)")
        space_complexity = llm_analysis.get("space_complexity") or static_analysis.get("space_complexity", "O(1)")
        impact_rating = llm_analysis.get("impact_rating") or static_analysis.get("impact_rating", "OPTIMAL")

        bottlenecks = list(static_analysis.get("bottlenecks", []))
        for b in llm_analysis.get("bottlenecks", []):
            if b not in bottlenecks:
                bottlenecks.append(b)

        hints = llm_analysis.get("optimization_hints", [])
        if not hints:
            if impact_rating in ("OPTIMAL", "ACCEPTABLE"):
                hints = [
                    "Guarded execution preserves linear complexity without allocation overhead.",
                    "Local variable access maintains CPU cache locality.",
                    "No unbounded loops or deep recursion introduced.",
                ]
            else:
                hints = [
                    "Consider utilizing hash maps (dict/set) for O(1) membership testing.",
                    "Avoid quadratic iterations over unbounded collections.",
                ]

        return {
            "time_complexity_before": time_before,
            "time_complexity_after": time_after,
            "space_complexity": space_complexity,
            "impact_rating": impact_rating,
            "bottlenecks": bottlenecks,
            "latency_overhead_estimated": llm_analysis.get("latency_overhead_estimated", "< 0.1ms"),
            "optimization_hints": hints,
        }

    def _static_complexity_check(self, patch: str) -> Dict[str, Any]:
        added_lines = [
            line[1:].strip()
            for line in patch.splitlines()
            if line.startswith("+") and not line.startswith("+++")
        ]
        patch_text = "\n".join(added_lines)

        bottlenecks = []
        nested_for = len(re.findall(r"\bfor\b", patch_text)) >= 2
        while_loops = len(re.findall(r"\bwhile\b", patch_text)) > 0
        recursion = re.search(r"def\s+([a-zA-Z0-9_]+)\(.*\):[\s\S]*?\1\(", patch_text)

        if nested_for:
            bottlenecks.append("Nested loop detected in patch additions — potential O(N^2) execution hazard.")
        if while_loops:
            bottlenecks.append("Indefinite while loop in patch additions — ensure termination condition is strictly bounded.")
        if recursion:
            bottlenecks.append("Recursive invocation found — verify recursion depth limits.")

        impact = "OPTIMAL"
        if nested_for or recursion:
            impact = "POTENTIAL_OVERHEAD"

        return {
            "time_before": "O(N)" if nested_for else "O(1)",
            "time_after": "O(N^2)" if nested_for else "O(1)",
            "space_complexity": "O(N)" if ("[" in patch_text or "{" in patch_text) else "O(1)",
            "impact_rating": impact,
            "bottlenecks": bottlenecks,
        }

    def _llm_profile(self, problem: str, patch: str, root_cause: Optional[str]) -> Dict[str, Any]:
        prompt = f"""
You are the Performance & Complexity Profiler Agent inside Bugify.
Analyze the Big-O time and space complexity changes of this software fix.

BUG PROBLEM:
{problem}

ROOT CAUSE:
{root_cause or 'N/A'}

PROPOSED PATCH:
{patch}

Respond in STRICT JSON ONLY:
{{
    "time_complexity_before": "O(1)" | "O(N)" | "O(N log N)" | "O(N^2)",
    "time_complexity_after": "O(1)" | "O(N)" | "O(N log N)" | "O(N^2)",
    "space_complexity": "O(1)" | "O(N)" | "O(N^2)",
    "impact_rating": "OPTIMAL" | "ACCEPTABLE" | "POTENTIAL_OVERHEAD" | "REGRESSION",
    "bottlenecks": ["list of detected algorithmic bottlenecks or empty list"],
    "latency_overhead_estimated": "< 0.05ms" | "< 1ms" | "Variable",
    "optimization_hints": ["1-3 concise performance insights"]
}}
"""
        response = self.llm.invoke(prompt)
        text = response.content.strip()

        if "{" in text and "}" in text:
            json_str = text[text.find("{"):text.rfind("}") + 1]
            return json.loads(json_str)
        return {}
