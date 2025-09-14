from fastapi import APIRouter, UploadFile, File
from services.pdf_service import extract_text_from_pdf, get_doc_id
from services.embedding_service import store_embeddings

router = APIRouter()

@router.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    doc_id = get_doc_id(file)
    text = extract_text_from_pdf(file)
    store_embeddings(text, doc_id)
    return {"doc_id": doc_id}