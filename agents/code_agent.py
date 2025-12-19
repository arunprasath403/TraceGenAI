# agents/code_agent.py

from dataclasses import dataclass, field
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from agents.context import ProjectContext
from tools.code_parser import code_parser
from config.settings import settings


@dataclass
class CodeResponse:
    ui_elements: list[str] = field(default_factory=list)
    api_endpoints: list[str] = field(default_factory=list)
    business_validations: list[str] = field(default_factory=list)


@tool(
    "parse_code",
    description=(
        "Parse the project source code to extract UI elements, "
        "API endpoints, and business validation rules relevant for QA test case generation."
    )
)
def parse_code(runtime: ToolRuntime[ProjectContext]):
    return code_parser.invoke({
        "project_id": runtime.context.project_id
    })


def run_code_agent(context: ProjectContext):
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
        tools=[parse_code],
        system_prompt="You are a QA automation architect. Always call `parse_code`.",
        context_schema=ProjectContext,
        response_format=CodeResponse,
        checkpointer=InMemorySaver()
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Extract code-level QA facts"}]},
        context=context,
        config={"configurable": {"thread_id": context.project_id}},
        stream=False   
    )

    return result["structured_response"]
