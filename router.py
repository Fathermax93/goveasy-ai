import re
from fastapi import APIRouter, HTTPException
from passport import run_passport_agent
from schemas import CitizenRequest, CitizenResponse

router = APIRouter()

DISCLAIMER = (
    "\n\n---\n"
    "*Note: Passport requirements and fees may change. "
    "Please confirm the latest information on the official "
    "Nigeria Immigration Service (NIS) portal before submitting your application.*"
)

# Pre-compiled injection regex
INJECTION_REGEX = re.compile(
    r"(ignore (your|previous|all) instructions|"
    r"reveal (your|the) (system|developer) prompt|"
    r"system prompt|"
    r"disregard (your|all) rules|"
    r"repeat the text above|"
    r"you are now in dan mode|"
    r"override previous directives)",
    re.IGNORECASE,
)


def is_malicious_injection(text: str) -> bool:
    return bool(INJECTION_REGEX.search(text))


@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "GovEasy AI"}


@router.post("/agent/run", response_model=CitizenResponse)
async def run_agent(request: CitizenRequest):
    try:
        cleaned_message = request.message.strip()
        if not cleaned_message:
            return CitizenResponse(
                status="rejected",
                answer="Please enter a valid query or question before submitting.",
                required_documents=[],
                steps=[],
                escalation_required=False,
            )

        if is_malicious_injection(cleaned_message):
            return CitizenResponse(
                status="rejected",
                answer=(
                    "REJECTED: Malicious request detected. Prompt injection or system"
                    " instruction override attempts are not permitted."
                ),
                required_documents=[],
                steps=[],
                escalation_required=False,
            )

        # Directly await the async agent runner
        raw_answer = await run_passport_agent(cleaned_message)

        formatted_answer = f"{raw_answer}{DISCLAIMER}"

        return CitizenResponse(
            status="success",
            answer=formatted_answer,
            required_documents=[],
            steps=[],
            escalation_required=False,
        )
    except Exception as e:
        print(f"\n[GovEasy AI Router Error]: {e}\n")
        raise HTTPException(
            status_code=500, detail=f"Error executing agent task: {str(e)}"
        )