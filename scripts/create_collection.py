"""
scripts/create_collection.py — Create Qdrant vector collections for Bugify.

Usage:
    python scripts/create_collection.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.qdrant_client import QdrantManager
from rag.collections import COLLECTIONS


def main():
    print("Initializing Qdrant collections for Bugify...")
    mgr = QdrantManager()
    mgr.init_collections()

    mode = "Qdrant Cloud" if mgr.is_cloud else "In-Memory (no Qdrant Cloud configured)"
    print(f"Mode: {mode}")
    print(f"Collections initialized: {', '.join(COLLECTIONS.keys())}")
    print("Done.")


if __name__ == "__main__":
    main()
