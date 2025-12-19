# agents/context.py
from dataclasses import dataclass

@dataclass
class ProjectContext:
    project_id: str
    upload_path: str
    vector_db_path: str
    output_path: str
