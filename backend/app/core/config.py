import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "RAG-Powered Document Assistant"
    API_V1_STR: str = ""
    DEBUG: bool = False

    # Ollama LLM Settings
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:latest"


    # ChromaDB & Embeddings Settings
    CHROMA_PATH: str = os.getenv(
        "CHROMA_PATH",
        str(Path(__file__).resolve().parent.parent.parent / "data" / "vector_store")
    )
    COLLECTION_NAME: str = "cs_documents"
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    TOP_K: int = 4

    # CORS Settings
    CORS_ORIGINS: list[str] = ["http://localhost:8501", "http://127.0.0.1:8501", "*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
