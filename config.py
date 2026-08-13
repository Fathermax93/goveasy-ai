import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter").lower()

MODEL_NAME = os.getenv("MODEL_NAME", "openrouter/google/gemma-4-26b-a4b-it:free")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "openrouter/google/gemma-4-31b-it:free")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Local development fallback variables
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")