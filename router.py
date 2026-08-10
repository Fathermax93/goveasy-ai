import traceback
from fastapi import APIRouter, HTTPException
from passport import run_passport_agent  # Import the async function from passport.py
from pydantic import BaseModel

router = APIRouter()


class QueryRequest(BaseModel):
    message: str


@router.post("/agent/run")
async def run_agent(request: QueryRequest):
    try:
        # Await the asynchronous execution function
        result = await run_passport_agent(request.message)

        # Return response under the 'answer' key expected by index.html
        return {"answer": str(result)}

    except Exception as e:
        print("\n" + "=" * 50)
        print("CRITICAL ERROR IN AGENT EXECUTION:")
        traceback.print_exc()
        print("=" * 50 + "\n")

        raise HTTPException(
            status_code=500, detail=f"Agent Execution Error: {str(e)}"
        )