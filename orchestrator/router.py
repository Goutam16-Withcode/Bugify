"""
Router — determines which node executes next based on the current state.
"""

from orchestrator.state import BugifyState

MAX_ITERATIONS = 3


def should_retry(state: BugifyState) -> str:
    """
    After verification, decide:
    - "finalize"  → verification passed OR retry limit hit
    - "fix"       → retry (patch failed, iterations remaining)
    """
    iteration = state.get("iteration", 1)
    tests_passed = state.get("tests_passed", False)
    max_iterations = state.get("max_iterations", MAX_ITERATIONS)

    if tests_passed:
        return "finalize"

    if iteration >= max_iterations:
        return "finalize"

    return "fix"


def route_after_diagnosis(state: BugifyState) -> str:
    """Always proceed to code analysis after diagnosis."""
    return "code_analysis"


def route_after_code_analysis(state: BugifyState) -> str:
    """Always proceed to research after code analysis."""
    return "research"


def route_after_research(state: BugifyState) -> str:
    """Always proceed to fix after research."""
    return "fix"


def route_after_fix(state: BugifyState) -> str:
    """Always proceed to verification after fix."""
    return "verification"
