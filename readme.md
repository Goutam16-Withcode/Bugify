# Bugify

**Production-grade autonomous multi-agent AI debugging system** built on LangGraph, Groq LLaMA 3.3, Qdrant, and isolated execution sandboxes.

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2-orange?style=flat-square)](https://github.com/langchain-ai/langgraph)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3-purple?style=flat-square)](https://groq.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Tests](https://img.shields.io/badge/Tests-22%2F22%20Passing-brightgreen?style=flat-square)](./tests)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](./LICENSE)

---

## What is Bugify?

Bugify is a fully autonomous debugging system. You submit a bug report (traceback + description + repository path), and five specialized AI agents — orchestrated through a LangGraph state machine — diagnose the root cause, inspect the code, retrieve relevant fixes from a vector knowledge base, generate a reviewed patch, and verify it against your test suite.

**All without human intervention.**

```
Developer → FastAPI → LangGraph Orchestrator
                           ↓
              ┌────────────────────────┐
              │  Diagnosis Agent       │ ← Parses traceback, classifies error
              │  Code Analysis Agent   │ ← AST traversal, call graph
              │  Research Agent (RAG)  │ ← Qdrant vector search
              │  Fix Agent             │ ← LLM patch generation + review
              │  Verification Agent    │ ← Pytest in Docker sandbox
              └────────────────────────┘
                           ↓
              Verified Fix  OR  Best-Effort Report
```

---

## Verified Claims

| Claim | Verification |
|-------|-------------|
| 22/22 unit tests passing | `pytest tests/unit -v` — confirmed in `.venv` |
| LangGraph state router wired | `orchestrator/router.py` — conditional edges with 3-retry loop |
| AST traversal working | `code_analysis/ast_analyzer.py` — Python `ast` module |
| Qdrant vector store integrated | `rag/vector_store.py` — with in-memory fallback |
| Docker sandbox isolation | `sandbox/docker_manager.py` — graceful fallback to subprocess |
| FastAPI endpoints active | `app/main.py` — `/api/v1/debug`, `/health`, `/status` |
| Groq LLaMA 3.3 inference | `llm/groq_client.py` — model registry with fallback |
| Pydantic v2 schemas | `schemas/` — strict TypedDict state validation |

---

## Architecture

```
bugify/
├── app/                    # FastAPI application layer
│   ├── main.py             # ASGI server entrypoint
│   ├── routes/             # API route handlers
│   └── config.py           # Environment config
│
├── orchestrator/           # LangGraph state machine
│   ├── graph.py            # Compiled StateGraph
│   ├── state.py            # BugifyState TypedDict
│   └── router.py           # Conditional edge router
│
├── agents/                 # Five specialized agents
│   ├── diagnosis/          # Traceback parser + bug classifier
│   ├── code_analysis/      # AST traversal + dependency graph
│   ├── research/           # RAG retrieval agent
│   ├── fix/                # Patch generator + reviewer
│   └── verification/       # Pytest sandbox executor
│
├── rag/                    # Retrieval Augmented Generation
│   ├── vector_store.py     # Qdrant + in-memory fallback
│   ├── embedder.py         # sentence-transformers (384-dim)
│   └── retriever.py        # Dense search interface
│
├── code_analysis/          # Static analysis tools
│   ├── ast_analyzer.py     # Python AST walker
│   ├── dependency_analyzer.py
│   └── repo_explorer.py
│
├── sandbox/                # Isolated execution environment
│   ├── security.py         # SandboxPolicy dataclass
│   ├── docker_manager.py   # Docker SDK wrapper
│   ├── test_runner.py      # Pytest orchestrator
│   └── executor.py         # Unified sandbox API
│
├── llm/                    # LLM client abstraction
│   ├── groq_client.py      # Groq API wrapper
│   └── model_registry.py   # Model configuration
│
├── schemas/                # Pydantic data models
│   └── models.py           # BugReport, PatchResult, etc.
│
├── tools/                  # Agent tool implementations
├── knowledge/              # Seed knowledge documents
├── scripts/                # Utility scripts
└── ui/                     # Next.js dashboard (port 3000)
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for UI)
- Docker (optional, for sandbox isolation)
- Groq API key — [get one free](https://console.groq.com)
- Qdrant (optional, falls back to in-memory)

### 1. Clone & Install

```bash
git clone https://github.com/Goutam16-Withcode/Bugify.git
cd Bugify
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
GROQ_API_KEY=gsk_your_key_here
QDRANT_URL=http://localhost:6333     # optional
QDRANT_API_KEY=                      # optional
DEBUG_MODE=true
LOG_LEVEL=INFO
```

### 3. Run Tests (verify everything works)

```bash
.venv\Scripts\python.exe -m pytest tests/unit -v
# Expected: 22 passed in ~0.31s
```

### 4. Start the Backend API

```bash
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

API will be live at `http://localhost:8000`

### 5. Start the UI Dashboard

```bash
cd ui
npm install
npm run dev
```

Dashboard live at `http://localhost:3000`

---

## API Reference

### Debug a Bug

```http
POST /api/v1/debug
Content-Type: application/json

{
  "problem_description": "AttributeError when fetching user profile",
  "traceback": "Traceback (most recent call last):\n  File \"app/services/user_service.py\", line 42, in get_user_profile\n    profile = user_repo.find_by_id(user_id).get_data()\nAttributeError: 'NoneType' object has no attribute 'get_data'",
  "repo_path": "/path/to/your/repo"
}
```

**Response:**
```json
{
  "is_success": true,
  "diagnosis": { "error_type": "AttributeError", "file": "user_service.py", "line": 42 },
  "patch": {
    "diff": "--- a/app/services/user_service.py\n+++ b/app/services/user_service.py\n@@ -40,4 +40,7 @@\n-    profile = user_repo.find_by_id(user_id).get_data()\n+    user = user_repo.find_by_id(user_id)\n+    if user is None:\n+        return None\n+    profile = user.get_data()",
    "review_score": 9.8
  },
  "verification": { "tests_passed": true, "passed": 22, "total": 22, "duration_seconds": 0.31 }
}
```

### Health Check

```http
GET /api/v1/health
```

### System Status

```http
GET /api/v1/status
```

---

## The Five Agents

### 1. Diagnosis Agent
Parses multi-frame Python tracebacks, isolates the originating file and line, classifies exception severity, and structures the diagnostic payload into a `BugReport` schema.

**Key files:** `agents/diagnosis/agent.py`, `agents/diagnosis/tools.py`

### 2. Code Analysis Agent
Walks the Python Abstract Syntax Tree to identify function definitions, cyclomatic complexity, unhandled None returns, and constructs import dependency graphs.

**Key files:** `agents/code_analysis/agent.py`, `code_analysis/ast_analyzer.py`

### 3. Research Agent (RAG)
Executes 384-dimensional dense vector search against Qdrant collections. Retrieves similar bug patterns with contextual defensive guard solutions.

**Key files:** `agents/research/agent.py`, `rag/vector_store.py`, `rag/retriever.py`

### 4. Fix Agent
Synthesizes unified diff patches using Groq LLaMA 3.3, incorporating diagnosis context, code analysis, and RAG results. Runs a built-in LLM reviewer before approving patches.

**Key files:** `agents/fix/agent.py`, `agents/fix/tools.py`

### 5. Verification Agent
Executes the patch inside a Docker sandbox (`python:3.11-slim`, network disabled, 512 MB cap, 60s timeout) and runs the full pytest suite. Falls back to subprocess if Docker is unavailable.

**Key files:** `agents/verification/agent.py`, `sandbox/executor.py`

---

## Ingesting Custom Knowledge

```bash
# Ingest seed knowledge documents
.venv\Scripts\python.exe scripts/ingest_knowledge.py

# Create Qdrant collection
.venv\Scripts\python.exe scripts/create_collection.py
```

---

## UI Pages

| Page | URL | Description |
|------|-----|-------------|
| Overview | `/` | Hero, features, pipeline, stats |
| Debug Console | `/debug` | Interactive bug submission UI |
| Agents | `/agents` | Deep dive into all 5 agents |
| Architecture | `/architecture` | Animated LangGraph flow diagram |
| Knowledge Base | `/knowledge` | Vector store browser & search |
| Execution Sandbox | `/sandbox` | Security policies & test results |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Orchestration | LangGraph 0.2 — compiled state graph with conditional edges |
| LLM | Groq LLaMA 3.3 — ultra-low latency inference |
| Vector Store | Qdrant — 384-dim dense embeddings (in-memory fallback) |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` |
| API | FastAPI 0.115 — async ASGI with Pydantic v2 |
| Sandbox | Docker `python:3.11-slim` with subprocess fallback |
| Schema | Pydantic v2 TypedDict — strict state validation |
| Frontend | Next.js 14 — dark amber dashboard |
| Testing | pytest — 22/22 unit tests passing |

---

## Project Status

**v1.0 — Production Ready**

- ✅ All 22 unit tests passing
- ✅ LangGraph workflow fully wired
- ✅ Qdrant integration with in-memory fallback
- ✅ Docker sandbox with subprocess fallback
- ✅ FastAPI REST API
- ✅ Next.js dashboard with 6 pages
- ✅ Pydantic v2 schema validation
- ✅ Groq LLaMA 3.3 integration

---

## License

MIT License — see [LICENSE](./LICENSE)

---

*Built with LangGraph · Groq · Qdrant · FastAPI · Docker*
