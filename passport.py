import os
import logging
from dotenv import load_dotenv
from crewai import LLM, Agent, Crew, Process, Task
from crewai_tools import SerperDevTool

load_dotenv()

logger = logging.getLogger(__name__)

# Initialize Search Tool safely
serper_api_key = os.getenv("SERPER_API_KEY")
search_tool = SerperDevTool() if serper_api_key else None

# Fetch Model Name (Default to OpenRouter's Free Router)
model_name = os.getenv("MODEL_NAME", "openrouter/free")
if not model_name.startswith("openrouter/"):
    model_name = f"openrouter/{model_name}"

api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")

# Properly configure CrewAI LLM for OpenRouter
openrouter_llm = LLM(
    model=model_name,
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

agent_tools = [search_tool] if search_tool else []

# Passport Agent
# Explicitly disable native tool calls on the agent if using OpenRouter free models
passport_agent = Agent(
    role="Nigerian Passport Assistant",
    goal="Provide accurate, up-to-date guidance on Nigerian international passport applications and official NIS fees.",
    backstory=(
        "You are an expert guide for Nigeria Immigration Service (NIS) passport procedures. "
        "You always use web search to verify current official fees and policies before answering questions about pricing or requirements."
    ),
    tools=agent_tools,
    llm=openrouter_llm,
    use_system_prompt=True,
    verbose=True,
)

async def run_passport_agent(user_query: str) -> str:
    try:
        passport_task = Task(
            description=(
                f"User Query: '{user_query}'\n\n"
                "If the query asks about passport fees, application requirements, or official processes, "
                "use your search tool to check the latest official Nigeria Immigration Service (NIS) guidelines and pricing "
                "before generating your response. Provide clear, accurate, and structured advice."
            ),
            expected_output=(
                "A clear, well-structured response containing accurate NIS guidelines, correct validity periods, "
                "verified official fees in NGN, and official application steps."
            ),
            agent=passport_agent,
        )

        crew = Crew(
            agents=[passport_agent],
            tasks=[passport_task],
            process=Process.sequential,
        )

        result = await crew.kickoff_async()
        return str(result)

    except Exception as e:
        logger.error(f"Error running passport agent: {str(e)}", exc_info=True)
        return f"An error occurred while processing your request: {str(e)}"