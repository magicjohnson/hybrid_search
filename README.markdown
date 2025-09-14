# PDF Search API

A FastAPI-based application for extracting text from PDFs, generating embeddings, and performing hybrid search with RAG.

## Features
- Extract text from PDFs using PyPDF2
- Generate embeddings with SentenceTransformers
- Store embeddings in PostgreSQL with pgvector
- Index text in Elasticsearch for keyword search
- Hybrid search combining keyword and semantic results
- RAG pipeline with LangChain for contextual responses
- Cache results with Redis for performance

## Prerequisites
- Python 3.10+
- PostgreSQL with pgvector extension
- Elasticsearch
- Redis
- OpenAI API key

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hybrid_search
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Set up environment variables:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

4. Ensure PostgreSQL, Elasticsearch, and Redis are running.

5. Initialize the database:
   ```bash
   poetry run python -m database.db_init
   ```

6. Start the FastAPI server:
   ```bash
   poetry run uvicorn main:app --reload
   ```

## Usage
- **Upload PDF**: `POST /upload_pdf/` with a PDF file to extract text and store embeddings.
- **Search**: `POST /search/` with a JSON payload `{ "query": "your query", "top_k": 5 }` to perform hybrid search.

## Project Structure
```
pdf-search-api/
├── database/
│   └── db_init.py
├── services/
│   ├── pdf_service.py
│   ├── embedding_service.py
│   └── search_service.py
├── routers/
│   ├── pdf_router.py
│   └── search_router.py
├── main.py
├── pyproject.toml
└── README.md
```

## Testing
Run tests with:
```bash
poetry run pytest
```

## Notes
- Ensure PostgreSQL has the pgvector extension installed.
- Configure Elasticsearch and Redis connection settings as needed.
- Adjust `top_k` in search queries for desired result count.
