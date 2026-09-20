from typing import List, Dict, Any, Tuple
import httpx
from app.core.config import settings
from app.utils.logging_config import logger
from app.schemas.query import SourceItem


SYSTEM_PROMPT = """You are a document-grounded assistant for University Computer Science documents.
Your task is to answer the user's question using ONLY the provided context snippets below.

STRICT GROUNDING RULES:
1. Base your answer STRICTLY and ONLY on the provided Context.
2. Do NOT use outside knowledge or external assumptions.
3. If the context does not contain enough information to answer the question, respond EXACTLY with:
   "I could not find this information in the provided documents."
4. When stating facts from the context, include citations referencing the source document and page number.
5. Keep your answer concise, precise, and directly relevant to the question."""


def build_grounded_prompt(question: str, chunks: List[Dict[str, Any]]) -> str:
    """Combine retrieved context chunks into a grounded prompt format."""
    if not chunks:
        context_str = "No relevant context found in documents."
    else:
        context_blocks = []
        for idx, chunk in enumerate(chunks, 1):
            doc = chunk.get("document", "Unknown")
            page = chunk.get("page", 1)
            text = chunk.get("text", "").strip()
            context_blocks.append(f"--- Context Snippet [{idx}] ---\nDocument: {doc} (Page {page})\nText:\n{text}")
        context_str = "\n\n".join(context_blocks)

    user_prompt = f"""Context:
{context_str}

Question:
{question}

Answer:"""
    return user_prompt


class GenerationService:
    def __init__(self):
        self.ollama_host = settings.OLLAMA_HOST
        self.ollama_model = settings.OLLAMA_MODEL

    async def check_ollama_health(self) -> bool:
        """Check if Ollama server is reachable and responsive."""
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"{self.ollama_host.rstrip('/')}/api/tags")
                return res.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama server check failed at {self.ollama_host}: {e}")
            return False

    async def generate_answer(
        self, question: str, chunks: List[Dict[str, Any]]
    ) -> Tuple[str, List[SourceItem]]:
        """Generate grounded answer and source citations."""
        sources: List[SourceItem] = []
        seen_sources = set()

        for chunk in chunks:
            doc = chunk.get("document", "Unknown")
            page = chunk.get("page", 1)
            snippet = chunk.get("text", "")[:150] + "..." if chunk.get("text") else None
            source_key = (doc, page)
            if source_key not in seen_sources:
                seen_sources.add(source_key)
                sources.append(SourceItem(document=doc, page=page, snippet=snippet))

        if not chunks:
            return "I could not find this information in the provided documents.", []

        prompt = build_grounded_prompt(question, chunks)

        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                payload = {
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "system": SYSTEM_PROMPT,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,  # Low temperature for precise grounded responses
                    }
                }
                res = await client.post(f"{self.ollama_host.rstrip('/')}/api/generate", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("response", "").strip()
                    if not answer:
                        answer = "I could not find this information in the provided documents."
                    return answer, sources
                else:
                    logger.error(f"Ollama returned HTTP status {res.status_code}: {res.text}")
                    return (
                        f"[Grounded Answer from Retrieved Context]\nBased on retrieved context from {sources[0].document} (Page {sources[0].page}):\n"
                        f"{chunks[0]['text'][:400]}...",
                        sources
                    )
        except httpx.ConnectError:
            logger.warning("Could not connect to local Ollama instance. Generating fallback grounded summary from retrieved chunks.")
            # Graceful fallback when Ollama service is not running locally during testing
            fallback_answer = (
                f"Based on the retrieved document context from '{sources[0].document}' (Page {sources[0].page}):\n\n"
                f"\"{chunks[0]['text'].strip()}\""
            )
            return fallback_answer, sources
        except Exception as e:
            logger.error(f"Error calling Ollama LLM: {e}")
            fallback_answer = (
                f"Retrieved context from {sources[0].document} (Page {sources[0].page}):\n\n"
                f"\"{chunks[0]['text'].strip()}\""
            )
            return fallback_answer, sources


generation_service = GenerationService()
