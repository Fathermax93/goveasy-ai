import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

# Opt out of CrewAI telemetry overhead
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

# Define default free model (Gemma 2 9b free model slug)
PRIMARY_MODEL = os.getenv("MODEL_NAME", "google/gemma-4-26b-a4b-it:free")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "google/gemma-4-26b-a4b-it:free")

# Format model string for LiteLLM routing
PRIMARY_SLUG = f"openrouter/{PRIMARY_MODEL}" if not PRIMARY_MODEL.startswith("openrouter/") else PRIMARY_MODEL

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is missing from environment variables.")

# Global environment overrides for LiteLLM / OpenRouter
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
os.environ["OPENAI_API_KEY"] = OPENROUTER_API_KEY
os.environ["OPENROUTER_API_KEY"] = OPENROUTER_API_KEY

# Configure LiteLLM retry limits globally to absorb free-tier delays
os.environ["LITELLM_NUM_RETRIES"] = "3"
os.environ["LITELLM_REQUEST_TIMEOUT"] = "120"

# Ensure Google/Gemini environment keys are removed to avoid direct SDK routing
os.environ.pop("GEMINI_API_KEY", None)
os.environ.pop("GOOGLE_API_KEY", None)


def get_llm() -> LLM:
    """Returns a unified CrewAI LLM instance configured for OpenRouter with Gemma free tier."""
    return LLM(
        model=PRIMARY_SLUG,
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        timeout=120.0,
        max_retries=3,  # Automatically retry on handshake or connection drops
        temperature=0.3,
        extra_body={
            "models": [
                PRIMARY_MODEL,
                FALLBACK_MODEL,
            ]
        },
    )