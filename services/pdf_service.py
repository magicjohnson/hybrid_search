from fastapi import UploadFile
from PyPDF2 import PdfReader
from pathlib import Path

def extract_text_from_pdf(file: UploadFile) -> str:
    pdf_reader = PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_doc_id(file: UploadFile) -> str:
    return str(Path(file.filename).stem)