from typing import Dict, List, Optional, Any
from rag.qdrant_client import QdrantManager
from rag.embeddings import EmbeddingService


class KnowledgeRetriever:
    """Retrieves relevant context for bugs, errors, and documentation."""

    def __init__(self, qdrant: Optional[QdrantManager] = None, embedder: Optional[EmbeddingService] = None):
        self.qdrant = qdrant or QdrantManager()
        self.embedder = embedder or EmbeddingService()

    def retrieve(
        self,
        query: str,
        collection_name: str = "bug_knowledge",
        limit: int = 4,
        score_threshold: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant entries from vector store."""
        if not query.strip():
            return []

        query_vec = self.embedder.embed_query(query)
        results = self.qdrant.search(collection_name, query_vec, limit=limit)
        filtered = [r for r in results if r["score"] >= score_threshold]
        return filtered

    def retrieve_formatted(
        self,
        query: str,
        collection_names: Optional[List[str]] = None,
        limit_per_collection: int = 3,
    ) -> List[str]:
        """Retrieve and format items as context strings for LLM prompts."""
        collections = collection_names or ["bug_knowledge", "error_patterns", "documentation"]
        formatted_snippets = []

        for col in collections:
            results = self.retrieve(query, collection_name=col, limit=limit_per_collection)
            for r in results:
                payload = r.get("payload", {})
                title = payload.get("title", "Reference")
                content = payload.get("content", "")
                if content:
                    formatted_snippets.append(f"[{col.upper()} - {title}]:\n{content}")

        return formatted_snippets
