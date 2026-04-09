"""
Main API server using FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .search_api import router as search_router
from .pdf_processor import router as pdf_router
from .summarizer import router as summarizer_router
from .database import init_db

app = FastAPI(title="Universal Local Research Assistant API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routers
app.include_router(search_router, prefix="/search", tags=["search"])
app.include_router(pdf_router, prefix="/pdf", tags=["pdf"])
app.include_router(summarizer_router, prefix="/summarize", tags=["summarize"])

@app.get("/")
async def root():
    return {"message": "Welcome to Universal Local Research Assistant API"}
