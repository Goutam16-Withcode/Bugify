"""
scripts/run_bugify.py — CLI entrypoint for running Bugify from the terminal.

Usage:
    python scripts/run_bugify.py \
        --problem "AttributeError on user.profile" \
        --traceback "$(cat error.txt)" \
        --repo /path/to/target/repo
"""

import argparse
import json
import sys
import os

# Allow imports from repo root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.graph import bugify_graph


def main():
    parser = argparse.ArgumentParser(
        description="Bugify — Autonomous AI Debugging CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--problem", required=True, help="Bug description or title")
    parser.add_argument("--traceback", default="", help="Stack trace or error traceback")
    parser.add_argument("--logs", default="", help="Relevant runtime or build logs")
    parser.add_argument("--repo", required=True, dest="repository_path", help="Path to target repository")
    parser.add_argument("--max-iterations", type=int, default=3, help="Max fix-verify cycles (default: 3)")
    parser.add_argument("--json-output", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    initial_state = {
        "problem": args.problem,
        "traceback": args.traceback,
        "logs": args.logs,
        "repository_path": args.repository_path,
        "bug_type": None,
        "bug_category": None,
        "severity": None,
        "confidence": 0.0,
        "error_type": None,
        "error_message": None,
        "error_file": None,
        "error_line": None,
        "relevant_files": [],
        "repository_info": {},
        "ast_analysis": {},
        "dependency_info": {},
        "hypotheses": [],
        "retrieved_context": [],
        "root_cause": None,
        "proposed_patches": [],
        "patch_summary": None,
        "patch_review": {},
        "test_output": None,
        "tests_passed": False,
        "regression_detected": False,
        "syntax_error": None,
        "iteration": 1,
        "max_iterations": args.max_iterations,
        "current_stage": None,
        "stage_errors": [],
        "final_answer": None,
        "verified_patch": None,
        "success": False,
    }

    print(f"\n🐞 Bugify — starting autonomous debug session")
    print(f"   Problem : {args.problem[:80]}")
    print(f"   Repo    : {args.repository_path}")
    print(f"   Max itr : {args.max_iterations}\n")

    try:
        final_state = bugify_graph.invoke(initial_state)
    except Exception as e:
        print(f"\n❌ Graph execution failed: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json_output:
        output = {
            "success": final_state.get("success"),
            "bug_type": final_state.get("bug_type"),
            "severity": final_state.get("severity"),
            "root_cause": final_state.get("root_cause"),
            "patch_summary": final_state.get("patch_summary"),
            "verified_patch": final_state.get("verified_patch"),
            "final_answer": final_state.get("final_answer"),
            "iterations": final_state.get("iteration"),
            "stage_errors": final_state.get("stage_errors", []),
        }
        print(json.dumps(output, indent=2))
    else:
        print("\n" + "=" * 60)
        print(final_state.get("final_answer", "No answer generated."))
        print("=" * 60)

    sys.exit(0 if final_state.get("success") else 1)


if __name__ == "__main__":
    main()
