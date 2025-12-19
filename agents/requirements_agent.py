# D:\AI_testcase\agents\requirements_agent.py

from dataclasses import dataclass, field
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from agents.context import ProjectContext
from tools.rag_retriever import rag_retriever
from config.settings import settings


# ---------- Response Schema ----------
@dataclass
class RequirementItem:
    id: str
    description: str


@dataclass
class RequirementsResponse:
    functional_requirements: list[RequirementItem] = field(default_factory=list)
    non_functional_requirements: list[RequirementItem] = field(default_factory=list)


# ---------- Tool ----------
@tool(
    "fetch_requirements",
    description="Fetch functional and non-functional requirements for the project"
)
def fetch_requirements(runtime: ToolRuntime[ProjectContext]):
    return rag_retriever.invoke({
        "query": "Extract all functional and non-functional requirements",
        "project_id": runtime.context.project_id
    })


# ---------- Agent Runner ----------
def run_requirements_agent(context: ProjectContext) -> RequirementsResponse:
    llm = init_chat_model(
        model=settings.LLM_MODEL_NAME,
        model_provider="openai",
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,
        temperature=settings.LLM_TEMPERATURE,
        streaming=False
    )

    agent = create_agent(
        model=llm,
        tools=[fetch_requirements],
        system_prompt=(
            "You are a QA analyst. "
            "Always call `fetch_requirements` first and return only structured requirements."
        ),
        context_schema=ProjectContext,
        response_format=RequirementsResponse,
        checkpointer=InMemorySaver()
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Extract requirements"}]},
        context=context,
        config={"configurable": {"thread_id": context.project_id}},
        stream=False   # ✅ THIS IS THE REAL FIX
    )

    return result["structured_response"]
