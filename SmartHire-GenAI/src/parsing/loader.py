from pathlib import Path

from pypdf import PdfReader
from docx import Document


def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n".join(pages).strip()


def load_docx(file_path: str) -> str:
    document = Document(file_path)
    paragraphs = []
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            paragraphs.append(text)
    return "\n".join(paragraphs).strip()


def load_resume(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Resume not found: {file_path}")
    extension = path.suffix.lower()
    if extension == ".pdf":
        return load_pdf(str(path))
    if extension == ".docx":
        return load_docx(str(path))
    raise ValueError("Unsupported resume format. Please use PDF or DOCX.")
