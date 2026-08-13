import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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

# 1. Root route to serve your index.html UI
@app.get("/")
def serve_index():
    return FileResponse("index.html")

# 2. Health check endpoint (useful for SnapDeploy status checks)
@app.get("/health")
def health_check():
    return {"status": "ok"}

# 3. Register API routes BEFORE static mounting
app.include_router(api_router)

# 4. Serve static files ONLY if static directory exists (or mount under /static)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)