from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from router import router

app = FastAPI(
    title="GovEasy AI",
    version="1.0.0",
    description="AI assistant for Nigerian international passport guidance"
)

# Enable browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTML templates
templates = Jinja2Templates(directory="templates")

# API routes from router.py
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )