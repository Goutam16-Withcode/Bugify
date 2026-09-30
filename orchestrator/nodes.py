"""
Orchestrator Nodes — each function maps to one LangGraph node.
Every node receives the full BugifyState, updates specific fields,
and returns the partial state update to be merged.
"""

import logging
from typing import Dict, Any
from orchestrator.state import BugifyState
from agents.diagnosis.agent import DiagnosisAgent
from agents.code_analysis.agent import CodeAnalysisAgent
from agents.research.agent import ResearchAgent
from agents.fix.agent import FixAgent
from agents.verification.agent import VerificationAgent

logger = logging.getLogger(__name__)


# ============================================================
# Node: Diagnosis
# ============================================================

def run_diagnosis(state: BugifyState) -> Dict[str, Any]:
    """Parse error, classify bug type, and identify relevant files."""
    logger.info("[Node] diagnosis_agent")
    try:
        agent = DiagnosisAgent()
        result = agent.analyze(
            problem=state["problem"],
            traceback=state.get("traceback", ""),
            logs=state.get("logs", ""),
        )
        return {
            "bug_type": result.get("bug_type"),
            "bug_category": result.get("category"),
            "severity": result.get("severity"),
            "confidence": result.get("confidence", 0.0),
            "error_type": result.get("error_type"),
            "error_message": result.get("error_message"),
            "error_file": result.get("file"),
            "error_line": result.get("line"),
            "relevant_files": result.get("relevant_files", []),
            "current_stage": "diagnosis",
            "stage_errors": [],
        }
    except Exception as e:
        logger.exception("Diagnosis stage failed")
        return {
            "current_stage": "diagnosis",
            "stage_errors": [f"Diagnosis failed: {str(e)}"],
            "relevant_files": [],
        }


# ============================================================
# Node: Code Analysis
# ============================================================

def run_code_analysis(state: BugifyState) -> Dict[str, Any]:
    """Explore repository, run AST analysis, and map dependencies."""
    logger.info("[Node] code_analysis_agent")
    try:
        agent = CodeAnalysisAgent()
        result = agent.analyze(
            repository_path=state["repository_path"],
            relevant_files=state.get("relevant_files"),
        )
        return {
            "repository_info": result.get("repository", {}),
            "ast_analysis": result.get("ast_analysis", {}),
            "dependency_info": result.get("dependencies", {}),
            "current_stage": "code_analysis",
        }
    except Exception as e:
        logger.exception("Code analysis stage failed")
        return {
            "current_stage": "code_analysis",
            "stage_errors": state.get("stage_errors", []) + [f"Code analysis failed: {str(e)}"],
        }


# ============================================================
# Node: Research (RAG)
# ============================================================

def run_research(state: BugifyState) -> Dict[str, Any]:
    """Retrieve relevant documentation, issues, and synthesize hypotheses."""
    logger.info("[Node] research_agent")
    try:
        agent = ResearchAgent()
        result = agent.research(
            problem=state["problem"],
            error_message=state.get("error_message"),
            bug_type=state.get("bug_type"),
            traceback=state.get("traceback", ""),
        )
        return {
            "hypotheses": result.get("hypotheses", []),
            "retrieved_context": result.get("retrieved_context", []),
            "root_cause": result.get("summary"),
            "current_stage": "research",
        }
    except Exception as e:
        logger.exception("Research stage failed")
        return {
            "current_stage": "research",
            "hypotheses": ["Unable to determine root cause — research agent failed"],
            "retrieved_context": [],
            "stage_errors": state.get("stage_errors", []) + [f"Research failed: {str(e)}"],
        }


# ============================================================
# Node: Fix
# ============================================================

def run_fix(state: BugifyState) -> Dict[str, Any]:
    """Generate, review, and refactor a patch for the identified bug."""
    logger.info("[Node] fix_agent")
    try:
        agent = FixAgent()
        result = agent.fix(
            problem=state["problem"],
            traceback=state.get("traceback", ""),
            root_cause=state.get("root_cause"),
            relevant_files=state.get("relevant_files", []),
            code_context=state.get("ast_analysis", {}),
            retrieved_context=state.get("retrieved_context", []),
        )
        patch = result.get("patch", "")
        patches = state.get("proposed_patches", [])
        if patch:
            patches = patches + [patch]

        return {
            "proposed_patches": patches,
            "patch_summary": result.get("summary", ""),
            "patch_review": result.get("review", {}),
            "current_stage": "fix",
        }
    except Exception as e:
        logger.exception("Fix stage failed")
        return {
            "current_stage": "fix",
            "stage_errors": state.get("stage_errors", []) + [f"Fix failed: {str(e)}"],
        }


# ============================================================
# Node: Verification
# ============================================================

def run_verification(state: BugifyState) -> Dict[str, Any]:
    """Validate the latest patch via syntax checks and optional test execution."""
    logger.info("[Node] verification_agent")
    patches = state.get("proposed_patches", [])
    if not patches:
        return {
            "tests_passed": False,
            "test_output": "No patch to verify.",
            "current_stage": "verification",
        }

    latest_patch = patches[-1]

    try:
        agent = VerificationAgent()
        verdict = agent.verify(
            repo_path=state["repository_path"],
            patch_text=latest_patch,
            target_files=state.get("relevant_files", []),
            run_tests=False,  # Disabled by default; enable in production
        )
        return {
            "tests_passed": verdict.verified,
            "test_output": verdict.reason,
            "regression_detected": verdict.regression_detected,
            "syntax_error": verdict.syntax_error,
            "verified_patch": latest_patch if verdict.verified else None,
            "current_stage": "verification",
        }
    except Exception as e:
        logger.exception("Verification stage failed")
        return {
            "tests_passed": False,
            "test_output": f"Verification error: {str(e)}",
            "current_stage": "verification",
            "stage_errors": state.get("stage_errors", []) + [f"Verification failed: {str(e)}"],
        }


# ============================================================
# Node: Finalize
# ============================================================

def finalize(state: BugifyState) -> Dict[str, Any]:
    """Compose the final human-readable answer."""
    logger.info("[Node] finalize")
    verified = state.get("tests_passed", False)
    patch = state.get("verified_patch") or (state.get("proposed_patches") or [""])[-1]
    summary = state.get("patch_summary", "No summary available.")
    root_cause = state.get("root_cause", "Unknown")
    iteration = state.get("iteration", 1)

    if verified:
        final_answer = (
            f"✅ Bug successfully diagnosed and a verified patch was generated "
            f"after {iteration} iteration(s).\n\n"
            f"**Root Cause:**\n{root_cause}\n\n"
            f"**Patch Summary:**\n{summary}\n\n"
            f"**Generated Patch:**\n```diff\n{patch}\n```"
        )
        success = True
    else:
        errors = "\n".join(state.get("stage_errors", []))
        final_answer = (
            f"⚠️ Bugify was unable to produce a verified fix after {iteration} iteration(s).\n\n"
            f"**Root Cause Hypothesis:**\n{root_cause}\n\n"
            f"**Last Proposed Patch:**\n```diff\n{patch}\n```\n\n"
            f"**Verification Output:**\n{state.get('test_output', 'N/A')}\n\n"
            f"**Stage Errors:**\n{errors or 'None'}"
        )
        success = False

    return {
        "final_answer": final_answer,
        "success": success,
        "current_stage": "complete",
    }
