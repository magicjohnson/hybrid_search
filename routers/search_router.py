from fastapi import APIRouter
from pydantic import BaseModel
from services.search_service import hybrid_search

router = APIRouter()

class SearchQuery(BaseModel):
    query: str
    top_k: int = 5

@router.post("/search/")
async def search(query: SearchQuery):
    result = hybrid_search(query.query, query.top_k)
    return result