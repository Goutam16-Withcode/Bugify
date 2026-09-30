"""
scripts/ingest_knowledge.py — Ingest seed knowledge into Bugify's vector store.

Usage:
    python scripts/ingest_knowledge.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.qdrant_client import QdrantManager
from rag.ingestion import KnowledgeIngestionPipeline

SEED_KNOWLEDGE = [
    {
        "collection": "bug_knowledge",
        "title": "AttributeError: NoneType has no attribute",
        "content": (
            "This error commonly occurs when a variable expected to hold an object is None. "
            "Check all code paths that assign the variable. Ensure database queries handle "
            "missing rows (e.g., use .first() with None guard). Add defensive None checks "
            "or use Optional typing with early returns."
        ),
    },
    {
        "collection": "bug_knowledge",
        "title": "KeyError in dictionary access",
        "content": (
            "KeyError occurs when accessing a dictionary with a key that doesn't exist. "
            "Prefer dict.get(key, default) for safe access. Use key in dict checks before "
            "direct access. setdefault() or defaultdict are good alternatives for missing keys."
        ),
    },
    {
        "collection": "error_patterns",
        "title": "ImportError: cannot import name",
        "content": (
            "This typically indicates a circular import, a renamed symbol, or a missing "
            "package. Check for circular imports by reviewing the import chain. Verify the "
            "package version in requirements.txt. Use absolute imports where possible."
        ),
    },
    {
        "collection": "error_patterns",
        "title": "RecursionError: maximum recursion depth exceeded",
        "content": (
            "Infinite or deeply nested recursive calls exceed Python's default stack limit. "
            "Add a base case to recursive functions. Consider converting recursion to an "
            "iterative approach. sys.setrecursionlimit() is a last resort."
        ),
    },
    {
        "collection": "documentation",
        "title": "Python Exception Hierarchy",
        "content": (
            "BaseException → Exception → (ValueError, TypeError, AttributeError, KeyError, "
            "IndexError, RuntimeError, OSError, ImportError, ...). Catching Exception is "
            "generally safe. Never silently catch BaseException unless intentional."
        ),
    },
]


def main():
    print("Ingesting seed knowledge into Bugify vector store...")
    mgr = QdrantManager()
    mgr.init_collections()
    pipeline = KnowledgeIngestionPipeline(qdrant=mgr)

    total = 0
    for item in SEED_KNOWLEDGE:
        n = pipeline.ingest_document(
            collection_name=item["collection"],
            title=item["title"],
            content=item["content"],
        )
        total += n
        print(f"  ✓ [{item['collection']}] {item['title']!r} → {n} chunk(s)")

    print(f"\nTotal chunks ingested: {total}")
    print("Done.")


if __name__ == "__main__":
    main()
