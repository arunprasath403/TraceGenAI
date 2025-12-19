import uuid
from utils.project_context import resolve_project_context

from agents.requirements_agent import run_requirements_agent
from agents.design_agent import run_design_agent
from agents.code_agent import run_code_agent
from agents.testcase_agent import run_testcase_agent
from tools.validation_tool import validate_test_cases
from tools.excel_generator import generate_excel
from config.logging_config import setup_logger


if __name__ == "__main__":

    # Generate unique project
    project_id = f"project_{uuid.uuid4().hex[:8]}"
    context = resolve_project_context(project_id)

    logger = setup_logger(project_id)

    requirements = run_requirements_agent(context)
    design = run_design_agent(context)
    code = run_code_agent(context)

    testcases = run_testcase_agent(
        requirements_output=requirements,
        design_output=design,
        code_output=code
    )

    validate_test_cases(testcases["test_cases"])

    excel_path = generate_excel(
        testcase_output=testcases,
        output_path=context["output_path"]
    )

    logger.info(f"Excel generated at: {excel_path}")
