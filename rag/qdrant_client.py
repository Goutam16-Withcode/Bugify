import os
import uuid
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from rag.collections import COLLECTIONS, CollectionConfig

load_dotenv()

try:
    from qdrant_client import QdrantClient as RealQdrantClient
    from qdrant_client.http.models import Distance, VectorParams, PointStruct
    HAS_QDRANT = True
except ImportError:
    HAS_QDRANT = False


class InMemoryVectorStore:
    """In-memory vector store fallback when Qdrant Cloud is unreachable or not installed."""

    def __init__(self):
        self.collections: Dict[str, List[Dict[str, Any]]] = {}

    def create_collection(self, collection_name: str, dimension: int = 384, distance: str = "Cosine"):
        if collection_name not in self.collections:
            self.collections[collection_name] = []

    def upsert(self, collection_name: str, points: List[Dict[str, Any]]):
        if collection_name not in self.collections:
            self.collections[collection_name] = []
        for p in points:
            # remove existing point with same id
            self.collections[collection_name] = [
                x for x in self.collections[collection_name] if x.get("id") != p.get("id")
            ]
            self.collections[collection_name].append(p)

    def search(self, collection_name: str, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        points = self.collections.get(collection_name, [])
        if not points:
            return []

        def cosine_similarity(v1: List[float], v2: List[float]) -> float:
            dot = sum(a * b for a, b in zip(v1, v2))
            norm1 = sum(a * a for a in v1) ** 0.5
            norm2 = sum(b * b for b in v2) ** 0.5
            if norm1 == 0 or norm2 == 0:
                return 0.0
            return dot / (norm1 * norm2)

        scored = []
        for p in points:
            score = cosine_similarity(query_vector, p.get("vector", []))
            scored.append({
                "id": p.get("id"),
                "score": score,
                "payload": p.get("payload", {}),
            })
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:limit]


class QdrantManager:
    """Manages Qdrant Cloud or in-memory vector storage seamlessly."""

    def __init__(self):
        self.url = os.getenv("QDRANT_URL")
        self.api_key = os.getenv("QDRANT_API_KEY")
        self.client = None
        self.is_cloud = False
        self.memory_store = InMemoryVectorStore()

        if HAS_QDRANT and self.url:
            try:
                self.client = RealQdrantClient(url=self.url, api_key=self.api_key, timeout=5)
                # Verify connectivity
                self.client.get_collections()
                self.is_cloud = True
            except Exception:
                self.client = None
                self.is_cloud = False

    def init_collections(self):
        """Ensure all required collections exist."""
        for name, cfg in COLLECTIONS.items():
            if self.is_cloud and self.client:
                try:
                    exists = False
                    colls = self.client.get_collections().collections
                    for c in colls:
                        if c.name == name:
                            exists = True
                            break
                    if not exists:
                        dist = Distance.COSINE if cfg.distance == "Cosine" else Distance.DOT
                        self.client.create_collection(
                            collection_name=name,
                            vectors_config=VectorParams(size=cfg.dimension, distance=dist),
                        )
                except Exception:
                    self.memory_store.create_collection(name, cfg.dimension, cfg.distance)
            else:
                self.memory_store.create_collection(name, cfg.dimension, cfg.distance)

    def upsert_points(self, collection_name: str, points: List[Dict[str, Any]]):
        """Upsert points: list of dicts with 'id', 'vector', and 'payload'."""
        if self.is_cloud and self.client:
            try:
                q_points = [
                    PointStruct(
                        id=p.get("id", str(uuid.uuid4())),
                        vector=p["vector"],
                        payload=p.get("payload", {})
                    )
                    for p in points
                ]
                self.client.upsert(collection_name=collection_name, points=q_points)
                return
            except Exception:
                pass
        self.memory_store.upsert(collection_name, points)

    def search(self, collection_name: str, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search similar vectors in a collection."""
        if self.is_cloud and self.client:
            try:
                results = self.client.search(
                    collection_name=collection_name,
                    query_vector=query_vector,
                    limit=limit,
                )
                return [
                    {
                        "id": str(r.id),
                        "score": float(r.score),
                        "payload": r.payload,
                    }
                    for r in results
                ]
            except Exception:
                pass
        return self.memory_store.search(collection_name, query_vector, limit)
