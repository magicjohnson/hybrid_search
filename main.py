from fastapi import FastAPI
from routers import pdf_router, search_router
from db_init import init_db

app = FastAPI()

# Include routers
app.include_router(pdf_router.router)
app.include_router(search_router.router)

# Initialize database
init_db()
