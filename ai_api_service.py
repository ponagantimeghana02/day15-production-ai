from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from typing import List, Optional
import logging
import uvicorn

# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ai_api_service")

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(title="AI API Service", version="1.0.0")

# -----------------------------
# Mock Data (for search demo)
# -----------------------------
DOCUMENTS = [
    {"id": 1, "text": "FastAPI is a modern Python web framework."},
    {"id": 2, "text": "Machine learning uses data to train models."},
    {"id": 3, "text": "Embeddings convert text into vectors."},
]

# -----------------------------
# Request Models
# -----------------------------
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    user_id: Optional[str] = None


class EmbeddingRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    top_k: int = Field(default=2, ge=1, le=10)


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health_check():
    logger.info("Health check called")
    return {
        "status": "healthy",
        "service": "AI API Service"
    }


# -----------------------------
# Chat Endpoint (Mock AI)
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        logger.info(f"Chat request: {request.message}")

        # Mock response (replace with LLM call later)
        response = f"AI Response: You said '{request.message}'"

        return {
            "response": response,
            "user_id": request.user_id
        }

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail="Chat service failed")


# -----------------------------
# Embeddings Endpoint (Mock)
# -----------------------------
@app.post("/embeddings")
def embeddings(request: EmbeddingRequest):
    try:
        logger.info("Embedding request received")

        # Mock embedding (replace with OpenAI / HF model later)
        fake_vector = [float(len(request.text) % 10) for _ in range(10)]

        return {
            "text": request.text,
            "embedding": fake_vector,
            "dimension": len(fake_vector)
        }

    except Exception as e:
        logger.error(f"Embedding error: {str(e)}")
        raise HTTPException(status_code=500, detail="Embedding generation failed")


# -----------------------------
# Document Search Endpoint
# -----------------------------
@app.post("/search")
def search(request: SearchRequest):
    try:
        logger.info(f"Search query: {request.query}")

        results = []
        query_lower = request.query.lower()

        for doc in DOCUMENTS:
            if query_lower in doc["text"].lower():
                results.append(doc)

        # fallback simple ranking
        results = results[:request.top_k]

        return {
            "query": request.query,
            "results": results,
            "count": len(results)
        }

    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail="Search failed")


# -----------------------------
# Global Exception Handler
# -----------------------------
@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}")
    return {
        "error": "Internal Server Error",
        "detail": str(exc)
    }


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    uvicorn.run("ai_api_service:app", host="0.0.0.0", port=8000, reload=True)