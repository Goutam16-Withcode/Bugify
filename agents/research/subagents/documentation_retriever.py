import os
from typing import Dict, List, Optional, Any
from rag.retriever import KnowledgeRetriever

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


class DocumentationRetriever:
    """Retrieves documentation context from vector store and optional web search."""

    def __init__(self, retriever: Optional[KnowledgeRetriever] = None):
        self.retriever = retriever or KnowledgeRetriever()
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")

    def retrieve(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant documentation articles or docstrings."""
        results = []
        # 1. Vector store documentation collection
        local_results = self.retriever.retrieve(query, collection_name="documentation", limit=limit)
        for r in local_results:
            results.append({
                "source": "local_vector_db",
                "title": r.get("payload", {}).get("title", "Doc"),
                "content": r.get("payload", {}).get("content", ""),
                "score": r.get("score", 0.0),
            })

        # 2. If Tavily API is configured and available, augment with official docs
        if self.tavily_api_key and len(results) < limit and HAS_HTTPX:
            try:
                web_docs = self._search_tavily(f"python documentation {query}", max_results=limit - len(results))
                results.extend(web_docs)
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
            "include_answer": False,
        }
        resp = httpx.post(url, json=payload, timeout=8.0)
        if resp.status_code == 200:
            data = resp.json()
            out = []
            for item in data.get("results", []):
                out.append({
                    "source": "tavily_web",
                    "title": item.get("title", "Web Doc"),
                    "url": item.get("url"),
                    "content": item.get("content", ""),
                    "score": item.get("score", 0.8),
                })
            return out
        return []
