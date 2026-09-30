from typing import Dict, List, Optional, Any
from agents.research.subagents.documentation_retriever import DocumentationRetriever
from agents.research.subagents.issue_retriever import IssueRetriever
from agents.research.subagents.knowledge_synthesizer import KnowledgeSynthesizer


class ResearchAgent:
    """
    Research / RAG Agent.

    Coordinates:
    - DocumentationRetriever: fetches official docs and references
    - IssueRetriever: finds known bugs and similar issues
    - KnowledgeSynthesizer: LLM-driven synthesis into hypotheses
    """

    def __init__(self):
        self.doc_retriever = DocumentationRetriever()
        self.issue_retriever = IssueRetriever()
        self.synthesizer = KnowledgeSynthesizer()

    def research(
        self,
        problem: str,
        error_message: Optional[str] = None,
        bug_type: Optional[str] = None,
        traceback: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Perform RAG-augmented research on a bug.

        Returns:
            {
                "hypotheses": List[str],
                "retrieved_context": List[str],
                "summary": str,
                "docs_found": int,
                "issues_found": int,
            }
        """
        query = " ".join(filter(None, [bug_type, error_message, problem]))[:512]

        # 1. Retrieve relevant documentation
        docs = self.doc_retriever.retrieve(query, limit=3)

        # 2. Retrieve similar resolved issues
        issues = self.issue_retriever.retrieve(
            error_message=error_message or problem,
            bug_type=bug_type,
            limit=3,
        )

        # 3. Synthesize findings
        synthesis = self.synthesizer.synthesize(
            problem=problem,
            error_message=error_message,
            docs=docs,
            issues=issues,
        )

        retrieved_snippets = synthesis.get("context_snippets", [])

        # Also add raw doc and issue content as context strings
        for d in docs:
            content = d.get("content", "")
            if content:
                retrieved_snippets.append(f"[DOC] {d.get('title', '')}: {content[:400]}")

        for i in issues:
            content = i.get("content", "")
            if content:
                retrieved_snippets.append(f"[ISSUE] {i.get('title', '')}: {content[:400]}")

        return {
            "hypotheses": synthesis.get("hypotheses", []),
            "retrieved_context": list(dict.fromkeys(retrieved_snippets)),  # deduplicate
            "summary": synthesis.get("summary", ""),
            "docs_found": len(docs),
            "issues_found": len(issues),
        }
