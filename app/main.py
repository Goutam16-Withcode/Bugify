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
    problem: str = Field(..., min_length=5, description="Bug description or title")
    traceback: str = Field(default="", description="Stack trace text")
    logs: str = Field(default="", description="Relevant runtime or build logs")
    repository_path: str = Field(..., description="Absolute or relative path to the target repository")
    max_iterations: int = Field(default=3, ge=1, le=5, description="Max fix-verify retry cycles")


class DebugResponse(BaseModel):
    success: bool
    final_answer: str
    bug_type: Optional[str]
    severity: Optional[str]
    root_cause: Optional[str]
    patch_summary: Optional[str]
    verified_patch: Optional[str]
    iterations: int
    duration_seconds: float
    stage_errors: list[str]


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


@app.post("/api/v1/debug", response_model=DebugResponse, tags=["Debugging"])
async def debug_bug(request: DebugRequest):
    """
    Submit a bug report and receive an autonomous diagnosis and patch.

    The workflow runs: Diagnosis → Code Analysis → Research (RAG) → Fix → Verification
    """
    logger.info(f"Received debug request: {request.problem[:80]!r}")
    start_time = time.perf_counter()

    initial_state = {
        "problem": request.problem,
        "traceback": request.traceback,
        "logs": request.logs,
        "repository_path": request.repository_path,
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
        root_cause=final_state.get("root_cause"),
        patch_summary=final_state.get("patch_summary"),
        verified_patch=final_state.get("verified_patch"),
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
