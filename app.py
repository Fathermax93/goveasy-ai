import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from router import router as api_router

load_dotenv()

if not os.getenv("OPENROUTER_API_KEY"):
    raise RuntimeError(
        "CRITICAL: OPENROUTER_API_KEY is missing from your .env file."
    )

app = FastAPI(
    title="GovEasy AI",
    description="Backend API and web UI for government service inquiries.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Serves the index.html user interface directly at root."""
    html_file = Path(__file__).parent.resolve() / "index.html"

    if not html_file.exists():
        raise HTTPException(
            status_code=404,
            detail=(
                f"index.html not found at: {html_file}. Please ensure"
                " index.html exists in your project root."
            ),
        )

    return html_file.read_text(encoding="utf-8")


@app.get("/health")
async def health():
    return {"status": "online", "message": "GovEasy AI Backend Ready"}