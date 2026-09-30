from typing import Dict, List, Optional, Any
from llm.groq_client import get_llm

try:
    from langchain_core.messages import SystemMessage, HumanMessage
    HAS_LC = True
except ImportError:
    HAS_LC = False


class KnowledgeSynthesizer:
    """Synthesizes raw retrieved issues and documentation into debugging insights."""

    def __init__(self):
        try:
            self.llm = get_llm()
        except Exception:
            self.llm = None

    def synthesize(
        self,
        problem: str,
        error_message: Optional[str],
        docs: List[Dict[str, Any]],
        issues: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Synthesize retrieved information into root-cause hypotheses and fix recommendations."""
        doc_texts = [f"- {d.get('title', '')}: {d.get('content', '')[:300]}" for d in docs]
        issue_texts = [f"- {i.get('title', '')}: {i.get('content', '')[:300]}" for i in issues]

        combined_context = []
        if doc_texts:
            combined_context.append("Documentation findings:\n" + "\n".join(doc_texts))
        if issue_texts:
            combined_context.append("Similar resolved issues:\n" + "\n".join(issue_texts))

        context_str = "\n\n".join(combined_context) if combined_context else "No external references found."

        if self.llm and HAS_LC and (docs or issues):
            prompt = (
                f"You are the Research Agent in an autonomous debugging system.\n"
                f"Problem: {problem}\n"
                f"Error: {error_message or 'Unknown'}\n\n"
                f"Retrieved Context:\n{context_str}\n\n"
                f"Provide:\n"
                f"1. 2-3 concise root cause hypotheses.\n"
                f"2. Suggested architectural or code fix strategy.\n"
                f"Format as clear bullet points."
            )
            try:
                response = self.llm.invoke([
                    SystemMessage(content="You analyze programming bugs and synthesize technical solutions."),
                    HumanMessage(content=prompt),
                ])
                summary = response.content if hasattr(response, "content") else str(response)
                hypotheses = [
                    line.strip("- *")
                    for line in summary.splitlines()
                    if line.strip().startswith(("-", "*", "1.", "2.", "3."))
                ][:3]
                return {
                    "summary": summary,
                    "hypotheses": hypotheses if hypotheses else ["Investigate potential type or state inconsistency"],
                    "context_snippets": [context_str],
                }
            except Exception:
                pass

        # Deterministic fallback synthesis
        hypotheses = [
            f"Error '{error_message or 'runtime error'}' might be caused by unhandled None or missing attribute",
            "Potential type mismatch or invalid parameter passed to function",
            "Missing dependency or version incompatibility",
        ]
        return {
            "summary": f"Synthesized analysis for {problem}. Based on {len(docs)} docs and {len(issues)} issues.",
            "hypotheses": hypotheses,
            "context_snippets": [context_str] if context_str != "No external references found." else [],
        }
