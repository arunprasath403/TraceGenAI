import streamlit as st
import zipfile
import os
import uuid

from agents.requirements_agent import run_requirements_agent
from agents.design_agent import run_design_agent
from agents.code_agent import run_code_agent
from agents.testcase_agent import run_testcase_agent
from agents.context import ProjectContext

from tools.validation_tool import validate_test_cases
from tools.excel_generator import generate_excel

BASE_DATA_DIR = "data"


def create_project_context():
    project_id = f"project_{uuid.uuid4().hex[:8]}"

    upload_path = os.path.join(BASE_DATA_DIR, "uploads", project_id)
    vector_db_path = os.path.join(BASE_DATA_DIR, "vector_db", project_id)
    output_path = os.path.join(BASE_DATA_DIR, "outputs", project_id)

    os.makedirs(upload_path, exist_ok=True)
    os.makedirs(vector_db_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)

    return ProjectContext(
        project_id=project_id,
        upload_path=upload_path,
        vector_db_path=vector_db_path,
        output_path=output_path
    )


def save_and_extract(uploaded_files, upload_path):
    os.makedirs(upload_path, exist_ok=True)

    for file in uploaded_files:
        file_path = os.path.join(upload_path, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        if file.name.endswith(".zip"):
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(upload_path)
            os.remove(file_path)


st.set_page_config(page_title="SDLC Agentic AI Tester", layout="centered")
st.title("TraceGenAI")

uploaded_files = st.file_uploader(
    "Upload ZIP or Files",
    accept_multiple_files=True,
    type=["zip", "pdf", "docx", "txt", "py", "js", "jsx", "java", "html", "css"]
)

if uploaded_files and st.button("Generate Test Cases"):
    with st.spinner("Processing... Please wait"):
        context = create_project_context()

        save_and_extract(uploaded_files, context.upload_path)

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
            output_path=context.output_path
        )

    st.success("Test cases generated successfully!")

    with open(excel_path, "rb") as f:
        st.download_button(
            label="⬇️ Download Test Case Excel",
            data=f,
            file_name=os.path.basename(excel_path),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
