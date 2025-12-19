# rag/chunking.py

from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.constants import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_text(text)
