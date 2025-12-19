# utils/project_context.py

import os

BASE_DATA_DIR = "data"


def resolve_project_context(project_id: str) -> dict:
    """
    Resolve all filesystem paths for a given project_id
    """
    return {
        "project_id": project_id,
        "upload_path": os.path.join(BASE_DATA_DIR, "uploads", project_id),
        "vector_db_path": os.path.join(BASE_DATA_DIR, "vector_db", project_id),
        "output_path": os.path.join(BASE_DATA_DIR, "outputs", project_id),
    }
