from fastapi import APIRouter, HTTPException, status
from app.schemas.query import QueryRequest, QueryResponse, HealthResponse
from app.services.retrieval import retrieval_service
from app.services.generation import generation_service
from app.core.config import settings
from app.utils.logging_config import logger

router = APIRouter()


@router.get("/health", response_model=HealthResponse, summary="Check service health")
async def health_check():
    ollama_ok = await generation_service.check_ollama_health()
    doc_count = retrieval_service.get_document_count()
    return HealthResponse(
        status="healthy",
        vector_store_loaded=retrieval_service.is_initialized,
        ollama_connected=ollama_ok,
        embedding_model=settings.EMBEDDING_MODEL_NAME,
        collection_name=settings.COLLECTION_NAME,
        total_documents_indexed=doc_count
    )


@router.post("/query", response_model=QueryResponse, summary="Query the RAG Assistant")
async def query_rag(request: QueryRequest):
    try:
        logger.info(f"Received query request: '{request.question}'")

        # 1. Retrieve context chunks from vector store
        chunks = retrieval_service.retrieve_chunks(request.question)
        logger.info(f"Retrieved {len(chunks)} chunks for question.")

        # 2. Generate grounded answer via Ollama LLM
        answer, sources = await generation_service.generate_answer(request.question, chunks)

        return QueryResponse(
            answer=answer,
            sources=sources
        )
    except Exception as e:
        logger.error(f"Error processing query request: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your query. Please try again later."
        )
