from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import config
import os

from services.knowledge_loader import reload_knowledge, get_knowledge_chunks
from services.website_cache import get_website_status
from services.website_crawler import start_crawl
from services.chatbot import answer_question

app = FastAPI(title="MST Academy Support Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directory exists
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_widget_test():
    """Serves the index.html test page from the static directory."""
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "MST Academy API is running."}

class ChatRequest(BaseModel):
    message: str
    history: list = []
    provider: str = "openai"

@app.on_event("startup")
async def startup_event():
    # Load initial knowledge on startup
    get_knowledge_chunks()

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/knowledge/status")
def knowledge_status():
    chunks = get_knowledge_chunks()
    return {
        "files_loaded": len(set(c["source"] for c in chunks)),
        "chunks": len(chunks),
        "status": "Ready" if chunks else "No files loaded"
    }

@app.post("/api/knowledge/reload")
def reload_local_knowledge():
    count = reload_knowledge()
    return {"message": f"Reloaded {count} chunks."}

@app.get("/api/website/status")
def website_status():
    status = get_website_status()
    return {
        "url": config.WEBSITE_URL,
        "cached_pages": status["cached_pages"],
        "last_refreshed": status["last_refreshed"],
        "status": "Ready" if status["cached_pages"] > 0 else "Not Cached"
    }

@app.post("/api/website/refresh")
def refresh_website():
    try:
        result = start_crawl()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crawl failed: {str(e)}")

@app.post("/api/chat")
def chat(request: ChatRequest, http_request: Request):
    # Server-side Origin validation
    origin = http_request.headers.get("origin")
    if not origin or origin not in config.ALLOWED_ORIGINS:
        raise HTTPException(status_code=403, detail="Unauthorized request origin")

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    result = answer_question(request.message, request.history, request.provider)
    return result

