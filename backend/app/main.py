from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes.query import router as query_router
from app.services.retrieval import retrieval_service
from app.utils.logging_config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI Lifespan context manager to load models and DB once at startup."""
    logger.info("Starting up RAG Assistant FastAPI backend...")
    # Load ChromaDB vector store & SentenceTransformer model ONCE at startup
    retrieval_service.initialize()
    logger.info("Lifespan startup complete.")
    yield
    logger.info("Shutting down RAG Assistant FastAPI backend...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Grounded RAG Document Assistant API using Ollama, ChromaDB, and FastAPI.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(query_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
