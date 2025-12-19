# rag/vector_store.py

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List


def get_vector_store(persist_path: str):
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return Chroma(
        persist_directory=persist_path,
        embedding_function=embedding
    )


def store_chunks(
    chunks: List[str],
    metadatas: List[dict],
    persist_path: str
):
    vectordb = get_vector_store(persist_path)
    vectordb.add_texts(texts=chunks, metadatas=metadatas)
    # ❌ no persist() needed anymore
