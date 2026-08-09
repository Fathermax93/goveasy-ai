from crewai import Agent, Crew, Process, Task
from llm import get_llm


def create_passport_crew() -> Crew:
    """Factory function to generate a fresh Crew instance per request using OpenRouter."""
    passport_agent = Agent(
        role="Passport Services Assistant",
        goal=(
            "Provide clear, step-by-step guidance on Nigerian passport"
            " applications, renewals, and current official fee schedules."
        ),
        backstory=(
            "You are a dedicated civic assistant specializing in helping Nigerian"
            " citizens navigate international passport procedures, documentation"
            " requirements, and accurate government fee structures."
        ),
        verbose=False,
        allow_delegation=False,
        llm=get_llm(),
    )

    passport_task = Task(
        description=(
            "Provide full application guidance and a document checklist for:"
            " {user_query}. When explaining costs, you MUST use the following"
            " updated Nigeria Immigration Service (NIS) fee schedule:\n-"
            " **Applications within Nigeria:**\n  - 32-Page Passport (5-Year"
            " Validity): ₦100,000\n  - 64-Page Passport (10-Year Validity):"
            " ₦200,000\n- **Applications from Diaspora:**\n  - 32-Page Passport"
            " (5-Year Validity): $150\n  - 64-Page Passport (10-Year Validity):"
            " $230\nEnsure all details clearly state these exact figures."
        ),
        expected_output=(
            "A structured guide covering updated fees (₦100k/₦200k in Nigeria,"
            " $150/$230 Diaspora), eligibility, required documents, step-by-step"
            " application instructions, and key warnings."
        ),
        agent=passport_agent,
    )

    return Crew(
        agents=[passport_agent],
        tasks=[passport_task],
        process=Process.sequential,
        verbose=False,
    )


async def run_passport_agent(query: str) -> str:
    """Asynchronously executes the passport agent crew using kickoff_async()."""
    crew = create_passport_crew()
    result = await crew.kickoff_async(inputs={"user_query": query})
    return str(result)