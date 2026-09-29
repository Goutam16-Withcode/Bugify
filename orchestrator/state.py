from typing import TypedDict, List, Optional


class BugifyState(TypedDict):
    # User input
    problem: str
    traceback: str
    repository_path: str

    # Diagnosis
    bug_type: Optional[str]
    relevant_files: List[str]

    # Root-cause analysis
    hypotheses: List[str]
    root_cause: Optional[str]

    # RAG
    retrieved_context: List[str]

    # Fix generation
    proposed_patches: List[str]

    # Verification
    test_output: Optional[str]
    tests_passed: bool

    # Control flow
    iteration: int

    # Final response
    final_answer: Optional[str]