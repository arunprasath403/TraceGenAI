# agents/design_agent.py

from dataclasses import dataclass, field
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from agents.context import ProjectContext
from config.settings import settings
from tools.rag_retriever import rag_retriever


@dataclass
class DesignResponse:
    architecture_components: list[str] = field(default_factory=list)
    ui_flows: list[str] = field(default_factory=list)
    api_flows: list[str] = field(default_factory=list)
    integrations: list[str] = field(default_factory=list)


@tool(
    "fetch_design",
    description=(
        "Retrieve system design details such as architecture components, "
        "UI flows, API flows, and external integrations for the given project."
    )
)
def fetch_design(runtime: ToolRuntime[ProjectContext]):
    return rag_retriever.invoke({
        "query": "Extract system design, UI flows, API flows, and integrations",
        "project_id": runtime.context.project_id
    })


def run_design_agent(context: ProjectContext):
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
        tools=[fetch_design],
        system_prompt="You are a system analyst. Always call `fetch_design`.",
        context_schema=ProjectContext,
        response_format=DesignResponse,
        checkpointer=InMemorySaver()
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Extract system design"}]},
        context=context,
        config={"configurable": {"thread_id": context.project_id}},
        stream=False   
    )

    return result["structured_response"]
