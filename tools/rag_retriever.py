# tools/rag_retriever.py

from langchain.tools import tool
from typing import List
from utils.project_context import resolve_project_context
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from utils.project_context import resolve_project_context

import os


@tool
def rag_retriever(query: str, project_id: str) -> str:
    """
    Retrieve relevant document chunks from vector DB
    """

    context = resolve_project_context(project_id)
    vector_db_path = context["vector_db_path"]

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=vector_db_path,
        embedding_function=embedding
    )

    results = vectordb.similarity_search(query, k=5)

    return "\n".join(doc.page_content for doc in results)
