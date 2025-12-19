# tools/code_parser.py

from langchain.tools import tool
import os
import re


@tool
def code_parser(project_id: str) -> dict:
    """
    Parse source code to extract UI elements, APIs, validations
    """

    base_path = f"data/uploads/{project_id}"

    ui_elements = set()
    api_endpoints = set()
    validations = []

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith((".js", ".jsx", ".py", ".java")):
                with open(os.path.join(root, file), encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    ui_elements.update(re.findall(r'id=["\'](.*?)["\']', content))
                    api_endpoints.update(re.findall(r'/api/\w+', content))
                    validations += re.findall(r'len\(.*?\)\s*>=\s*\d+', content)

    return {
        "ui_elements": list(ui_elements),
        "api_endpoints": list(api_endpoints),
        "validations": validations
    }
