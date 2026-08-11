import traceback
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passport import run_passport_agent

# THIS IS THE MISSING VARIABLE Python was looking for!
router = APIRouter()


class QueryRequest(BaseModel):
    message: str


@router.post("/agent/run")
async def run_agent(request: QueryRequest):
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty.")

        response = await run_passport_agent(request.message)
        return {"answer": response}

    except Exception as e:
        print("\n" + "=" * 50)
        print("AGENT EXECUTION ERROR:")
        traceback.print_exc()
        print("=" * 50 + "\n")

        raise HTTPException(
            status_code=500, detail=f"Agent Execution Error: {str(e)}"
        )