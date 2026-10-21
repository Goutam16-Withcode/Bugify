"""
Production entrypoint for Bugify web service on Render, Railway, and cloud PaaS.
Reads PORT from environment and binds to 0.0.0.0.
"""
import os
import sys

# Force unbuffered standard streams so logs appear instantly on Render/Docker
os.environ["PYTHONUNBUFFERED"] = "1"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(line_buffering=True)

if __name__ == "__main__":
    raw_port = os.environ.get("PORT", "10000")
    try:
        port = int(raw_port)
    except ValueError:
        port = 10000

    print(f"[Bugify Launcher] Starting ASGI service on 0.0.0.0:{port} (PORT={raw_port})...", flush=True)

    try:
        print("[Bugify Launcher] Pre-loading FastAPI application...", flush=True)
        from app.main import app
        print("[Bugify Launcher] FastAPI application loaded successfully!", flush=True)
    except Exception as exc:
        print(f"[Bugify Launcher FATAL] Failed to load FastAPI app: {exc}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    import uvicorn
    print(f"[Bugify Launcher] Binding Uvicorn HTTP server to 0.0.0.0:{port}...", flush=True)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
