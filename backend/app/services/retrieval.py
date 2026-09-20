import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
import chromadb
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.utils.logging_config import logger


class RetrievalService:
    def __init__(self):
        self.embedding_model: SentenceTransformer | None = None
        self.chroma_client: chromadb.PersistentClient | None = None
        self.collection = None
        self.is_initialized = False

    def initialize(self):
        """Initialize embedding model and load persistent ChromaDB collection."""
        try:
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL_NAME}")
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

            db_path = Path(settings.CHROMA_PATH).resolve()
            logger.info(f"Connecting to ChromaDB at: {db_path}")
            db_path.mkdir(parents=True, exist_ok=True)
            self.chroma_client = chromadb.PersistentClient(path=str(db_path))

            self.collection = self.chroma_client.get_or_create_collection(
                name=settings.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            self.is_initialized = True
            logger.info(f"Vector store initialized successfully. Document count: {self.collection.count()}")
        except Exception as e:
            logger.error(f"Failed to initialize RetrievalService: {e}")
            self.is_initialized = False

    def retrieve_chunks(self, question: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Retrieve top_k most relevant document chunks for a question."""
        if not self.is_initialized or self.collection is None or self.embedding_model is None:
            logger.warning("RetrievalService called before full initialization.")
            return []

        k = top_k or settings.TOP_K
        query_embedding = self.embedding_model.encode([question]).tolist()

        try:
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=k,
                include=["documents", "metadatas", "distances"]
            )
        except Exception as e:
            logger.error(f"Error executing ChromaDB query: {e}")
            return []

        retrieved = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if "metadatas" in results else [{}] * len(docs)
            dists = results["distances"][0] if "distances" in results else [0.0] * len(docs)

            for doc, meta, dist in zip(docs, metas, dists):
                retrieved.append({
                    "text": doc,
                    "document": meta.get("document", "Unknown Document"),
                    "page": meta.get("page", 1),
                    "chunk_id": meta.get("chunk_id", 0),
                    "distance": dist
                })

        return retrieved

    def get_document_count(self) -> int:
        if self.collection:
            try:
                return self.collection.count()
            except Exception:
                return 0
        return 0


# Singleton instance
retrieval_service = RetrievalService()
