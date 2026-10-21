"""
Bugify FastAPI Application

Exposes:
  POST /api/v1/debug    — Submit a bug report and receive a diagnosis + patch
  GET  /api/v1/health   — Liveness probe
  GET  /api/v1/status   — Application metadata
"""

import logging
import time
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.config import get_settings
from orchestrator.graph import bugify_graph

# ──────────────────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────────────────
settings = get_settings()
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("bugify.api")


# ──────────────────────────────────────────────────────────
# Lifespan
# ──────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    yield
    logger.info(f"Shutting down {settings.app_name}")


# ──────────────────────────────────────────────────────────
# App factory
# ──────────────────────────────────────────────────────────
def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Autonomous Multi-Agent AI Debugging System",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()


# ──────────────────────────────────────────────────────────
# Request / Response Models
# ──────────────────────────────────────────────────────────
class DebugRequest(BaseModel):
    problem: str = Field(default="", description="Bug description or title")
    problem_description: Optional[str] = Field(default=None, description="Alias for problem")
    traceback: str = Field(default="", description="Stack trace text")
    logs: str = Field(default="", description="Relevant runtime or build logs")
    repository_path: str = Field(default=".", description="Absolute or relative path to target repository")
    repo_path: Optional[str] = Field(default=None, description="Alias for repository_path")
    max_iterations: int = Field(default=3, ge=1, le=5, description="Max fix-verify retry cycles")

    def get_problem(self) -> str:
        return self.problem or self.problem_description or "Unspecified issue"

    def get_repo_path(self) -> str:
        return self.repository_path or self.repo_path or "."


class DebugResponse(BaseModel):
    success: bool
    final_answer: str
    bug_type: Optional[str] = None
    severity: Optional[str] = None
    confidence: float = 0.0
    error_type: Optional[str] = None
    error_file: Optional[str] = None
    error_line: Optional[int] = None
    relevant_files: list[str] = []
    root_cause: Optional[str] = None
    patch_summary: Optional[str] = None
    verified_patch: Optional[str] = None
    proposed_patches: list[str] = []
    security_audit: Optional[Dict[str, Any]] = None
    complexity_analysis: Optional[Dict[str, Any]] = None
    regression_test: Optional[Dict[str, Any]] = None
    hypotheses: list[str] = []
    tests_passed: bool = False
    iterations: int = 1
    duration_seconds: float = 0.0
    stage_errors: list[str] = []


# ──────────────────────────────────────────────────────────
# Middleware: Request timing
# ──────────────────────────────────────────────────────────
@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{elapsed:.4f}s"
    return response


# ──────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────
@app.get("/", tags=["System"])
async def root():
    return {
        "status": "online",
        "service": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/v1/health",
        "agents": "/api/v1/agents",
    }


@app.get("/api/v1/health", tags=["System"])
async def health():
    return {"status": "ok", "service": settings.app_name}


@app.get("/api/v1/status", tags=["System"])
async def api_status():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "llm_provider": settings.llm_provider,
        "groq_model": settings.groq_model,
        "max_iterations": settings.max_iterations,
        "qdrant_configured": bool(settings.qdrant_url),
        "langsmith_tracing": settings.langchain_tracing_v2,
    }


@app.get("/api/v1/agents", tags=["System"])
async def list_agents():
    """Return the registry of all 8 specialized agents in the Bugify Swarm."""
    return {
        "count": 8,
        "swarm_status": "ONLINE",
        "agents": [
            {
                "id": "diagnosis",
                "name": "Diagnosis Agent",
                "stage": "STAGE 1 / ROOT CAUSE",
                "role": "Traceback Parsing & Fault Isolation",
                "model": settings.groq_model,
                "status": "ACTIVE",
                "capabilities": ["Multi-frame stack trace extraction", "Deterministic bug typing", "Regex AST line pointer"],
            },
            {
                "id": "code_analysis",
                "name": "Code Analysis Agent",
                "stage": "STAGE 2 / REPO EXPLORATION",
                "role": "AST Syntax Traversal & Dependency Graphing",
                "model": "Python AST Engine",
                "status": "ACTIVE",
                "capabilities": ["Abstract syntax tree walking", "Import dependency resolution", "Cyclic dependency guard"],
            },
            {
                "id": "research",
                "name": "Research Agent",
                "stage": "STAGE 3 / KNOWLEDGE RETRIEVAL",
                "role": "Dense Vector Search & Hypothesis Formulation",
                "model": "Qdrant + Tavily",
                "status": "ACTIVE",
                "capabilities": ["Semantic cosine similarity search", "Official documentation retrieval", "Hypothesis synthesis"],
            },
            {
                "id": "fix",
                "name": "Fix Synthesis Agent",
                "stage": "STAGE 4 / PATCH GENERATION",
                "role": "Adversarial Patch Synthesis & Refactoring",
                "model": settings.groq_model,
                "status": "ACTIVE",
                "capabilities": ["Minimal unified diff generation", "Adversarial patch reviewer", "Localized AST refactorer"],
            },
            {
                "id": "security_audit",
                "name": "Security Audit Agent",
                "stage": "STAGE 5 / SECURITY & VULNERABILITY",
                "role": "OWASP Top 10 & CWE Exploit Scanning",
                "model": f"{settings.groq_model} + Static CWE Engine",
                "status": "ACTIVE",
                "capabilities": ["SQLi & Command injection detection", "Path traversal audit", "Insecure deserialization guard"],
            },
            {
                "id": "complexity_profiler",
                "name": "Performance Profiler Agent",
                "stage": "STAGE 6 / PERFORMANCE & BIG-O",
                "role": "Asymptotic Complexity & Hotspot Analysis",
                "model": "Asymptotic AST Profiler",
                "status": "ACTIVE",
                "capabilities": ["Big-O time complexity (Before vs After)", "Space footprint estimation", "Loop nesting hazard detection"],
            },
            {
                "id": "test_generator",
                "name": "Test Generator Agent",
                "stage": "STAGE 7 / SELF-HEALING REGRESSION",
                "role": "Automated Pytest Suite Synthesis",
                "model": settings.groq_model,
                "status": "ACTIVE",
                "capabilities": ["Regression test synthesis", "Boundary edge-case generation", "Pytest fixture mocking"],
            },
            {
                "id": "verification",
                "name": "Verification Agent",
                "stage": "STAGE 8 / ISOLATED SANDBOX",
                "role": "Sandbox Execution & Regression Testing",
                "model": "Docker / Subprocess Isolation",
                "status": "ACTIVE",
                "capabilities": ["In-memory compilation test", "Docker container sandboxing", "Pytest runner with baseline comparison"],
            },
        ],
    }


@app.post("/api/v1/debug", response_model=DebugResponse, tags=["Debugging"])
async def debug_bug(request: DebugRequest):
    """
    Submit a bug report and receive an autonomous diagnosis and patch.

    The workflow runs: Diagnosis → Code Analysis → Research → Fix → Security Audit →
    Complexity Profiler → Test Generator → Verification
    """
    problem = request.get_problem()
    repo_path = request.get_repo_path()
    logger.info(f"Received debug request: {problem[:80]!r} (repo: {repo_path})")
    start_time = time.perf_counter()

    initial_state = {
        "problem": problem,
        "traceback": request.traceback,
        "logs": request.logs,
        "repository_path": repo_path,
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
        "security_audit": None,
        "complexity_analysis": None,
        "regression_test": None,
        "agent_telemetry": [],
        "test_output": None,
        "tests_passed": False,
        "regression_detected": False,
        "syntax_error": None,
        "iteration": 1,
        "max_iterations": request.max_iterations,
        "current_stage": None,
        "stage_errors": [],
        "final_answer": None,
        "verified_patch": None,
        "success": False,
    }

    try:
        final_state = bugify_graph.invoke(initial_state)
    except Exception as e:
        logger.exception("Graph execution failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Bugify graph execution error: {str(e)}",
        )

    duration = time.perf_counter() - start_time
    logger.info(f"Debug completed in {duration:.2f}s — success={final_state.get('success')}")

    return DebugResponse(
        success=final_state.get("success", False),
        final_answer=final_state.get("final_answer", "No answer generated."),
        bug_type=final_state.get("bug_type"),
        severity=final_state.get("severity"),
        confidence=final_state.get("confidence", 0.0),
        error_type=final_state.get("error_type"),
        error_file=final_state.get("error_file"),
        error_line=final_state.get("error_line"),
        relevant_files=final_state.get("relevant_files", []),
        root_cause=final_state.get("root_cause"),
        patch_summary=final_state.get("patch_summary"),
        verified_patch=final_state.get("verified_patch"),
        proposed_patches=final_state.get("proposed_patches", []),
        security_audit=final_state.get("security_audit"),
        complexity_analysis=final_state.get("complexity_analysis"),
        regression_test=final_state.get("regression_test"),
        hypotheses=final_state.get("hypotheses", []),
        tests_passed=final_state.get("tests_passed", False),
        iterations=final_state.get("iteration", 1),
        duration_seconds=round(duration, 3),
        stage_errors=final_state.get("stage_errors", []),
    )


# ──────────────────────────────────────────────────────────
# Dev entry point
# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
