import asyncio
import re
from fastapi import APIRouter, HTTPException
from schemas import CitizenRequest, CitizenResponse
from passport import run_passport_agent

router = APIRouter()

DISCLAIMER = (
    "\n\n---\n"
    "*Note: Passport requirements and fees may change. "
    "Please confirm the latest information on the official "
    "Nigeria Immigration Service (NIS) portal before submitting your application.*"
)

# Common injection and prompt-leak patterns
INJECTION_PATTERNS = [
    r"ignore (your|previous|all) instructions",
    r"reveal (your|the) (system|developer) prompt",
    r"system prompt",
    r"disregard (your|all) rules",
    r"repeat the text above",
    r"you are now in dan mode",
    r"override previous directives"
]

def is_malicious_injection(text: str) -> bool:
    """Returns True if the text matches common prompt injection / leak patterns."""
    text_lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "GovEasy AI"
    }

@router.post("/agent/run", response_model=CitizenResponse)
async def run_agent(request: CitizenRequest):
    try:
        # 1. Check for empty or whitespace-only inputs
        cleaned_message = request.message.strip()
        if not cleaned_message:
            return CitizenResponse(
                status="rejected",
                answer="Please enter a valid query or question before submitting.",
                required_documents=[],
                steps=[],
                escalation_required=False
            )

        # 2. Pre-screening security check
        if is_malicious_injection(cleaned_message):
            return CitizenResponse(
                status="rejected",
                answer="REJECTED: Malicious request detected. Prompt injection or system instruction override attempts are not permitted.",
                required_documents=[],
                steps=[],
                escalation_required=False
            )

        # 3. Offload synchronous CrewAI execution to a worker thread
        raw_answer = await asyncio.to_thread(run_passport_agent, cleaned_message)

        # 4. Append the official NIS disclaimer
        formatted_answer = str(raw_answer) + DISCLAIMER

        return CitizenResponse(
            status="success",
            answer=formatted_answer,
            required_documents=[],
            steps=[],
            escalation_required=False
        )
    except Exception as e:
        print(f"\n[GovEasy AI Router Error]: {e}\n")
        raise HTTPException(
            status_code=500,
            detail=f"Error executing agent task: {str(e)}"
        )