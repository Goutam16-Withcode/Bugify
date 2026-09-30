import os
from typing import Dict, List, Optional, Any
from rag.retriever import KnowledgeRetriever

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


class IssueRetriever:
    """Retrieves known issues, bug reports, and solutions matching error patterns."""

    def __init__(self, retriever: Optional[KnowledgeRetriever] = None):
        self.retriever = retriever or KnowledgeRetriever()
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")

    def retrieve(self, error_message: str, bug_type: Optional[str] = None, limit: int = 3) -> List[Dict[str, Any]]:
        """Search for matching bug solutions and historical issues."""
        query = f"{bug_type or ''} {error_message}".strip()
        if not query:
            return []

        results = []
        # 1. Check local bug knowledge base
        kb_results = self.retriever.retrieve(query, collection_name="bug_knowledge", limit=limit)
        for r in kb_results:
            results.append({
                "source": "bug_knowledge_base",
                "title": r.get("payload", {}).get("title", "Resolved Issue"),
                "content": r.get("payload", {}).get("content", ""),
                "score": r.get("score", 0.0),
            })

        # 2. Check error patterns
        err_results = self.retriever.retrieve(query, collection_name="error_patterns", limit=limit)
        for r in err_results:
            results.append({
                "source": "error_patterns",
                "title": r.get("payload", {}).get("title", "Error Pattern"),
                "content": r.get("payload", {}).get("content", ""),
                "score": r.get("score", 0.0),
            })

        # 3. Optional web lookup via Tavily if needed
        if self.tavily_api_key and len(results) < limit and HAS_HTTPX:
            try:
                search_q = f"github issue python {error_message[:100]}"
                web_issues = self._search_tavily(search_q, max_results=limit - len(results))
                results.extend(web_issues)
            except Exception:
                pass

        return results

    def _search_tavily(self, query: str, max_results: int = 2) -> List[Dict[str, Any]]:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": self.tavily_api_key,
            "query": query,
            "search_depth": "basic",
            "max_results": max_results,
        }
        resp = httpx.post(url, json=payload, timeout=8.0)
        if resp.status_code == 200:
            data = resp.json()
            out = []
            for item in data.get("results", []):
                out.append({
                    "source": "github_web_search",
                    "title": item.get("title", "GitHub Discussion"),
                    "url": item.get("url"),
                    "content": item.get("content", ""),
                    "score": item.get("score", 0.75),
                })
            return out
        return []
