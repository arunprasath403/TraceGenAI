# agents/testcase_agent.py

from dataclasses import dataclass, field
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from agents.context import ProjectContext
from config.settings import settings


@dataclass
class TestCase:
    id: str
    description: str
    linked_requirement: str


@dataclass
class TestCaseResponse:
    test_cases: list[TestCase] = field(default_factory=list)


def run_testcase_agent(context: ProjectContext, reqs, design, code):
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
        tools=[],  # no tools, but still MUST disable streaming
        system_prompt="Generate enterprise-grade test cases with strict traceability.",
        context_schema=ProjectContext,
        response_format=TestCaseResponse,
        checkpointer=InMemorySaver()
    )

    result = agent.invoke(
        {
            "messages": [{
                "role": "user",
                "content": f"""
REQUIREMENTS:
{reqs}

DESIGN:
{design}

CODE:
{code}
"""
            }]
        },
        context=context,
        config={"configurable": {"thread_id": context.project_id}},
        stream=False  # LangGraph default is streaming
    )

    return result["structured_response"]
