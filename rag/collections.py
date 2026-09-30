from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class CollectionConfig:
    name: str
    dimension: int
    distance: str
    description: str


COLLECTIONS = {
    "bug_knowledge": CollectionConfig(
        name="bug_knowledge",
        dimension=384,
        distance="Cosine",
        description="Known bugs, root causes, and verified fixes across Python libraries."
    ),
    "error_patterns": CollectionConfig(
        name="error_patterns",
        dimension=384,
        distance="Cosine",
        description="Stack traces, exceptions, and runtime error patterns."
    ),
    "documentation": CollectionConfig(
        name="documentation",
        dimension=384,
        distance="Cosine",
        description="Official documentation, API references, and syntax guides."
    ),
}
