# GovEasy AI 🇳🇬

**GovEasy AI** is an AI-powered Nigerian International Passport Assistant built with **CrewAI** and **FastAPI**. It helps citizens understand passport requirements, application procedures, renewal, replacement, fees, and other passport-related information in a clear and user-friendly manner.

---

## Features

* AI-powered Nigerian passport guidance
* FastAPI REST API
* Simple browser interface
* CrewAI agent workflow
* OpenRouter LLM support
* Configurable for OpenAI, Groq, Gemini, Ollama, and OpenRouter
* Environment variable configuration
* Railway-ready deployment
* Scope restriction for passport-related questions only
* Prompt injection protection
* Friendly, structured responses with official source references

Guardrails
✅ Rejects unrelated government services
✅ Rejects prompt injection attempts
✅ Keeps responses within passport scope
✅ Gives verification disclaimer

---

🛠️ Tech Stack
Language: Python 3.11+

Framework: FastAPI

Agentic Framework: CrewAI

ASGI Server: Uvicorn

LLM Provider Gateway: OpenRouter / LiteLLM

Frontend: HTML5, CSS3, JavaScript (Fetch API, Marked.js)

---

📁 Project Structure
Plaintext
goveasy-ai/
├── app.py              # Main FastAPI application entrypoint
├── router.py           # API endpoints & route handlers
├── passport.py         # CrewAI Agent, Task, & Crew execution setup
├── llm.py              # Centralized LLM configuration & OpenRouter provider binding
├── config.py           # Global environment settings & configuration
├── requirements.txt    # Python package dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Git exclusion rules
├── README.md           # Project documentation
└── assets/             # Static UI resources & images

🏗️ Architecture Flow

               ┌───────────────────────┐
               │    Citizen / User     │
               └───────────┬───────────┘
                           │  HTTP Request
                           ▼
               ┌───────────────────────┐
               │ FastAPI App / Web UI  │
               └───────────┬───────────┘
                           │  POST /agent/run
                           ▼
               ┌───────────────────────┐
               │  Agent API Router     │
               └───────────┬───────────┘
                           │  run_passport_agent()
                           ▼
               ┌───────────────────────┐
               │     CrewAI Engine     │
               └───────────┬───────────┘
                           │  Executes Task
                           ▼
     ┌───────────────────────────────────────────┐
     │   GovEasy AI Nigerian Passport Advisor    │
     │   (LLM: OpenRouter / Llama / Ling Flash)  │
     └─────────────────────┬─────────────────────┘
                           │  Formatted Response
                           ▼
               ┌───────────────────────┐
               │ Response to Citizen   │
               └───────────────────────┘

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Fathermax93/goveasy-ai.git
cd goveasy-ai
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Windows:

```bash
.venv\Scripts\activate

macOS/Linux:

Bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the example environment file:

```bash
copy .env.example .env
```

Edit `.env` and add your API key.

---
## Running the Project

Start the Server
Bash
python -m uvicorn app:app --reload
Navigate to http://127.0.0.1:8000 in your browser to view the application interface.

Sample Prompts to Try
"How much is a Nigerian passport?"

"What documents do I need to renew my 32-page passport?"

"Do I need a NIN before applying for a passport?"

"How do I replace a damaged passport?"

🛡️ #Security & Scope Directives

GovEasy AI is configured with guardrails to ensure reliability:

Scope Restriction: Automatically declines off-topic inquiries (e.g., CAC business registration, visas, driver's licenses) to conserve compute and avoid giving misinformed guidance.

Data Privacy: Suppresses execution stack traces in production error messages to prevent internal backend exposure.

Official Attributable Output: Appends mandatory official verification sources (passport.immigration.gov.ng and nimc.gov.ng) to every response card.

## Environment Variables

Example:

```env
LLM_PROVIDER=openrouter

MODEL_NAME=google/gemma-4-26b-a4b-it:free

OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY

CREWAI_TRACING_ENABLED=false

OPENAI_API_KEY=

GROQ_API_KEY=

GEMINI_API_KEY=

OLLAMA_HOST=http://localhost:11434

OLLAMA_MODEL=llama3


---

## Deployment

This project is designed for deployment on Railway.

Required environment variables:

* LLM_PROVIDER
* MODEL_NAME
* OPENROUTER_API_KEY

---

## Official Sources

* Nigeria Immigration Service (NIS): passport.immigration.gov.ng
* National Identity Management Commission (NIMC): nimc.gov.ng

Always verify the latest passport fees and requirements using the official Nigeria Immigration Service portal before submitting an application.

---

## License

This project was developed for educational purposes as an Agentic AI course project.
