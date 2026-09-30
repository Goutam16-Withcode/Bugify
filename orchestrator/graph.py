"""
LangGraph Orchestrator Graph — wires all nodes into a stateful workflow.
"""

from langgraph.graph import StateGraph, END
from orchestrator.state import BugifyState
from orchestrator.nodes import (
    run_diagnosis,
    run_code_analysis,
    run_research,
    run_fix,
    run_verification,
    finalize,
)
from orchestrator.router import should_retry


def increment_iteration(state: BugifyState) -> dict:
    """Helper node to increment the iteration counter before retrying fix."""
    return {"iteration": state.get("iteration", 1) + 1}


def build_bugify_graph() -> StateGraph:
    """Construct and compile the Bugify LangGraph workflow."""

    graph = StateGraph(BugifyState)

    # -------------------------------------------------------
    # Register nodes
    # -------------------------------------------------------
    graph.add_node("diagnosis", run_diagnosis)
    graph.add_node("code_analysis", run_code_analysis)
    graph.add_node("research", run_research)
    graph.add_node("fix", run_fix)
    graph.add_node("verification", run_verification)
    graph.add_node("increment_iteration", increment_iteration)
    graph.add_node("finalize", finalize)

    # -------------------------------------------------------
    # Linear edges
    # -------------------------------------------------------
    graph.set_entry_point("diagnosis")
    graph.add_edge("diagnosis", "code_analysis")
    graph.add_edge("code_analysis", "research")
    graph.add_edge("research", "fix")
    graph.add_edge("fix", "verification")

    # -------------------------------------------------------
    # Conditional retry loop
    # -------------------------------------------------------
    graph.add_conditional_edges(
        "verification",
        should_retry,
        {
            "fix": "increment_iteration",
            "finalize": "finalize",
        },
    )

    graph.add_edge("increment_iteration", "fix")
    graph.add_edge("finalize", END)

    return graph.compile()


# Module-level compiled graph (singleton)
bugify_graph = build_bugify_graph()
