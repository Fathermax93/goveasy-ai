import traceback
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passport import run_passport_agent

router = APIRouter()


class QueryRequest(BaseModel):
    message: str


@router.post("/agent/run")
async def run_agent(request: QueryRequest):
    try:
        clean_message = request.message.strip()
        if not clean_message:
            raise HTTPException(status_code=400, detail="Message cannot be empty.")

        # Directly await run_passport_agent (asyncio.to_thread is inside passport.py)
        response = await run_passport_agent(clean_message)
        
        # Ensure string format for response return
        output_text = str(response) if response else "No response generated."
        return {"answer": output_text}

    except HTTPException:
        raise

    except Exception as e:
        error_msg = str(e)
        print("\n" + "=" * 50)
        print("AGENT EXECUTION ERROR:")
        traceback.print_exc()
        print("=" * 50 + "\n")

        if any(term in error_msg.lower() for term in ["timeout", "connection", "httpcore", "connecttimeout"]):
            return {
                "answer": (
                    "GovEasy AI network service timed out while processing your request. "
                    "Please try your query again in a few seconds."
                )
            }

        return {
            "answer": "GovEasy AI is currently experiencing a temporary issue. Please try again shortly."
        }