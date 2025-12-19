# rag/ingest.py

import os
from rag.document_loader import load_document
from rag.chunking import chunk_text
from rag.vector_store import store_chunks


def ingest_documents(project_context: dict):
    upload_path = project_context["upload_path"]
    vector_db_path = project_context["vector_db_path"]

    all_chunks = []
    all_metadatas = []

    for root, _, files in os.walk(upload_path):
        for file in files:
            file_path = os.path.join(root, file)
            pages = load_document(file_path)

            if not pages:
                continue  # 🚫 skip empty documents

            for page_no, page_text in enumerate(pages, start=1):

                if not page_text.strip():
                    continue  # 🚫 skip empty pages

                chunks = chunk_text(page_text)

                if not chunks:
                    continue  # 🚫 skip empty chunk results

                for chunk in chunks:
                    all_chunks.append(chunk)
                    all_metadatas.append({
                        "project_id": project_context["project_id"],
                        "source_file": file,
                        "page": page_no
                    })

    #  FINAL SAFETY CHECK
    if not all_chunks:
        raise ValueError(
            "No valid text chunks found. Check uploaded documents."
        )

    store_chunks(
        chunks=all_chunks,
        metadatas=all_metadatas,
        persist_path=vector_db_path
    )
