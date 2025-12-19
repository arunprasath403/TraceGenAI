# rag/document_loader.py

from pypdf import PdfReader
from docx import Document
from typing import List
import os


def load_pdf(file_path: str) -> List[str]:
    reader = PdfReader(file_path)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return pages


def load_docx(file_path: str) -> List[str]:
    doc = Document(file_path)
    return [para.text for para in doc.paragraphs if para.text.strip()]


def load_txt(file_path: str) -> List[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        return [f.read()]


def load_document(file_path: str) -> List[str]:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".docx":
        return load_docx(file_path)
    elif ext == ".txt":
        return load_txt(file_path)
    else:
        return []
