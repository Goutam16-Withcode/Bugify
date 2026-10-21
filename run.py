"""
Production entrypoint for Bugify web service on Render, Railway, and cloud PaaS.
Reads PORT from environment and binds to 0.0.0.0.
"""
import os
import sys
import uvicorn

if __name__ == "__main__":
    raw_port = os.environ.get("PORT", "8000")
    try:
        port = int(raw_port)
    except ValueError:
        port = 8000

    print(f"[Bugify Launcher] Starting ASGI server on 0.0.0.0:{port} (PORT={raw_port})...", flush=True)
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
