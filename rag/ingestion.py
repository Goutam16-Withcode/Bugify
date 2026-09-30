import uuid
from typing import Dict, List, Optional, Any
from rag.qdrant_client import QdrantManager
from rag.embeddings import EmbeddingService


class KnowledgeIngestionPipeline:
    """Ingests documents and technical knowledge into vector storage."""

    def __init__(self, qdrant: Optional[QdrantManager] = None, embedder: Optional[EmbeddingService] = None):
        self.qdrant = qdrant or QdrantManager()
        self.embedder = embedder or EmbeddingService()

    def ingest_document(
        self,
        collection_name: str,
        title: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        chunk_size: int = 500,
    ) -> int:
        """Chunk and ingest a document into the specified collection."""
        metadata = metadata or {}
        # Simple paragraph or fixed-size chunking
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        chunks = []
        for p in paragraphs:
            if len(p) > chunk_size:
                # Sub-split
                words = p.split()
                sub = []
                curr_len = 0
                for w in words:
                    sub.append(w)
                    curr_len += len(w) + 1
                    if curr_len >= chunk_size:
                        chunks.append(" ".join(sub))
                        sub = []
                        curr_len = 0
                if sub:
                    chunks.append(" ".join(sub))
            else:
                chunks.append(p)

        if not chunks:
            chunks = [content]

        vectors = self.embedder.embed_documents(chunks)
        points = []
        for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{title}_{i}_{chunk[:30]}"))
            payload = {
                "title": title,
                "chunk_index": i,
                "content": chunk,
                **metadata,
            }
            points.append({"id": point_id, "vector": vec, "payload": payload})

        self.qdrant.upsert_points(collection_name, points)
        return len(points)
