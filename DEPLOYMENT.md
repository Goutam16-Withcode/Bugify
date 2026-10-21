# Bugify Cloud PaaS Deployment Guide 🚀

Deploy Bugify across cloud platforms with a free-tier compatible architecture:
- **Backend API**: Deployed to [Render](https://render.com) or [Railway](https://railway.app) (FastAPI + LangGraph + Groq)
- **Frontend Studio**: Deployed to [Vercel](https://vercel.com) (Next.js 14 App Router)

---

## Architecture Overview

```
                      ┌────────────────────────────────────────┐
                      │             Vercel Cloud               │
                      │    Next.js 14 Luxury Studio UI         │
                      │       https://bugify.vercel.app        │
                      └──────────────────┬─────────────────────┘
                                         │
                 Server-Side Rewrites (/api/* ──► BACKEND_API_URL)
                                         │
                                         ▼
                      ┌────────────────────────────────────────┐
                      │        Render / Railway Cloud          │
                      │       FastAPI ASGI Web Service         │
                      │  https://bugify-api.onrender.com       │
                      │  ├── LangGraph 8-Agent Swarm           │
                      │  ├── Groq High-Throughput Inference    │
                      │  └── In-Memory Vector Store / Qdrant   │
                      └────────────────────────────────────────┘
```

---

## Part 1: Deploy Backend to Render (Recommended Free Option)

### Option A: Blueprint Auto-Deploy (Easiest)
1. Fork or push this repository to your GitHub account (`Goutam16-Withcode/Bugify`).
2. Log into [Render Dashboard](https://dashboard.render.com).
3. Click **New +** → **Blueprint**.
4. Connect your GitHub repository. Render will automatically detect `render.yaml`.
5. Enter your `GROQ_API_KEY` when prompted.
6. Click **Apply**. Render will build and deploy the web service.

---

### Option B: Manual Web Service Creation
1. In Render Dashboard, click **New +** → **Web Service**.
2. Select your repository.
3. Configure the settings:
   - **Name**: `bugify-api`
   - **Language / Runtime**: `Python`
   - **Branch**: `main` (or your active branch)
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`
4. Under **Environment Variables**, add:
   - `PYTHON_VERSION`: `3.11.9`
   - `GROQ_API_KEY`: *(your Groq API key from console.groq.com)*
   - `GROQ_MODEL`: `qwen/qwen3.8-27b`
   - `DEBUG_MODE`: `false`
   - `LOG_LEVEL`: `INFO`
5. Click **Create Web Service**.
6. Once deployed, copy your backend URL:
   `https://bugify-api-xxxx.onrender.com`
7. Test the health endpoint in your browser:
   `https://bugify-api-xxxx.onrender.com/api/v1/health`
   *(Should return `{"status": "ok", "service": "bugify-api", "version": "1.0.0"}`)*

---

## Part 2: Deploy Backend to Railway (Alternative)

1. Go to [railway.app](https://railway.app) and sign in with GitHub.
2. Click **New Project** → **Deploy from GitHub repo**.
3. Select `Goutam16-Withcode/Bugify`.
4. Railway will automatically detect `railway.json` and `Procfile`.
5. Under **Variables**, add:
   - `GROQ_API_KEY`: *(your Groq API key)*
   - `GROQ_MODEL`: `qwen/qwen3.8-27b`
6. Click **Settings** → **Networking** → **Generate Domain** to get your public URL (e.g. `https://bugify-production.up.railway.app`).

---

## Part 3: Deploy Frontend to Vercel

1. Log into [Vercel](https://vercel.com).
2. Click **Add New...** → **Project**.
3. Import your GitHub repository (`Goutam16-Withcode/Bugify`).
4. In the configuration screen:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: Click **Edit** and choose `ui`
5. Expand the **Environment Variables** section and add:
   - **Key**: `BACKEND_API_URL`
   - **Value**: *(Your Render or Railway URL from Part 1/2, e.g. `https://bugify-api-xxxx.onrender.com` without trailing slash)*
   - *(Optional)* Add `NEXT_PUBLIC_BACKEND_URL` with the same URL.
6. Click **Deploy**.
7. Vercel will build the Next.js 14 frontend and provision your production URL (e.g. `https://bugify.vercel.app`).

---

## Part 4: Verification Checklist

Once both services are deployed:
1. Open your Vercel URL in your browser: `https://your-bugify-app.vercel.app`
2. Navigate to **Debug Studio** (`/debug`).
3. Check the **Backend Pipeline** badge in the top right. It should display:
   `API Status: Online` with a green pulsing dot.
4. Click any of the 6 quick bug presets (e.g., *NoneType AttributeError* or *Dict KeyError*).
5. Click **Run Autonomous Debugger →**.
6. The 8-agent LangGraph swarm will execute on your Render/Railway backend, stream state updates, and return the verified unified diff, security audit, Big-O profile, and test harness right inside your browser!

---

## Production Environment Variables Summary

### Backend (Render / Railway)
| Variable | Required | Default | Description |
|---|---|---|---|
| `GROQ_API_KEY` | **Yes** | — | High-throughput LLM API key |
| `GROQ_MODEL` | No | `qwen/qwen3.8-27b` | Primary model for code & diff generation |
| `DEBUG_MODE` | No | `false` | Enable verbose diagnostic logging |
| `LOG_LEVEL` | No | `INFO` | Logger verbosity |
| `QDRANT_URL` | No | *empty* | Optional external Qdrant instance (falls back to memory) |
| `QDRANT_API_KEY` | No | *empty* | Optional Qdrant cloud token |

### Frontend (Vercel)
| Variable | Required | Default | Description |
|---|---|---|---|
| `BACKEND_API_URL` | **Yes** | `http://localhost:8000` | Public URL of your deployed Render/Railway backend |
| `NEXT_PUBLIC_BACKEND_URL` | No | *same as above* | Fallback public URL |
