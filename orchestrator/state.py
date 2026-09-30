from typing import TypedDict, List, Optional, Dict, Any


class BugifyState(TypedDict):
    # -------------------------------------------------------
    # User Input
    # -------------------------------------------------------
    problem: str
    traceback: str
    logs: str
    repository_path: str

    # -------------------------------------------------------
    # Diagnosis Stage
    # -------------------------------------------------------
    bug_type: Optional[str]
    bug_category: Optional[str]
    severity: Optional[str]
    confidence: float
    error_type: Optional[str]
    error_message: Optional[str]
    error_file: Optional[str]
    error_line: Optional[int]
    relevant_files: List[str]

    # -------------------------------------------------------
    # Code Analysis Stage
    # -------------------------------------------------------
    repository_info: Dict[str, Any]
    ast_analysis: Dict[str, Any]
    dependency_info: Dict[str, Any]

    # -------------------------------------------------------
    # Research / RAG Stage
    # -------------------------------------------------------
    hypotheses: List[str]
    retrieved_context: List[str]
    root_cause: Optional[str]

    # -------------------------------------------------------
    # Fix Stage
    # -------------------------------------------------------
    proposed_patches: List[str]
    patch_summary: Optional[str]
    patch_review: Dict[str, Any]

    # -------------------------------------------------------
    # Verification Stage
    # -------------------------------------------------------
    test_output: Optional[str]
    tests_passed: bool
    regression_detected: bool
    syntax_error: Optional[str]

    # -------------------------------------------------------
    # Control Flow
    # -------------------------------------------------------
    iteration: int
    max_iterations: int
    current_stage: Optional[str]
    stage_errors: List[str]

    # -------------------------------------------------------
    # Final Response
    # -------------------------------------------------------
    final_answer: Optional[str]
    verified_patch: Optional[str]
    success: bool