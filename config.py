import os
from dotenv import load_dotenv

# Load variables from a .env file if one exists
load_dotenv()

# Which provider to use:
# openai | groq | gemini | ollama | openrouter
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter").lower()

# Default model
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "google/gemma-4-31b-it:free"
)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Ollama settings
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")