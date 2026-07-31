import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

# Explicitly disable telemetry in code runtime as well
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

# Options from your live OpenRouter model payload:
# 1. "openrouter/inclusionai/ling-3.0-flash:free" (Fast MoE model)
# 2. "openrouter/poolside/laguna-s-2.1:free" (Great for structured logic)
# 3. "openrouter/openrouter/free" (Auto-routes to currently active free models)
MODEL_NAME = "openrouter/inclusionai/ling-3.0-flash:free"

def get_llm() -> LLM:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing from your .env file.")

    os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
    os.environ["OPENAI_API_KEY"] = api_key

    return LLM(
        model=MODEL_NAME,
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        timeout=60.0,
        temperature=0.3
    )