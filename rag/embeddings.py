import os
import hashlib
from typing import List

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False


class EmbeddingService:
    """Provides dense embeddings with fallback for offline/isolated environments."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", dimension: int = 384):
        self.dimension = dimension
        self.model_name = model_name
        self._model = None
        if HAS_SENTENCE_TRANSFORMERS and os.getenv("BUGIFY_OFFLINE", "false").lower() != "true":
            try:
                # Lazy load model only when called to avoid startup delay
                pass
            except Exception:
                self._model = None

    def _get_model(self):
        if self._model is None and HAS_SENTENCE_TRANSFORMERS:
            try:
                self._model = SentenceTransformer(self.model_name)
            except Exception:
                self._model = None
        return self._model

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string."""
        return self.embed_documents([text])[0]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of text strings into vector lists."""
        model = self._get_model()
        if model is not None:
            try:
                embeddings = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
                return [emb.tolist() for emb in embeddings]
            except Exception:
                pass

        # Fallback deterministic pseudo-embedding based on sha256
        results = []
        for text in texts:
            vec = [0.0] * self.dimension
            tokens = text.lower().split()
            if not tokens:
                results.append(vec)
                continue
            for i, token in enumerate(tokens):
                h = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
                idx = h % self.dimension
                vec[idx] += 1.0 / (1.0 + (i * 0.1))
            norm = sum(x * x for x in vec) ** 0.5
            if norm > 0:
                vec = [x / norm for x in vec]
            results.append(vec)
        return results
