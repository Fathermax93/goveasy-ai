import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from router import router as api_router

app = FastAPI(title="GovEasy AI")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Health check endpoint (useful for SnapDeploy status checks)
@app.get("/health")
def health_check():
    return {"status": "ok"}

# 2. Register API routes BEFORE static mounting
app.include_router(api_router)

# 3. Serve static files ONLY if static directory exists (or mount under /static)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)