import os
import re
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup
from config import KNOWLEDGE_DIR

def load_local_knowledge():
    """
    Reads all supported files from the local knowledge directory.
    Returns a list of chunks/sections with metadata.
    """
    chunks = []
    
    if not os.path.exists(KNOWLEDGE_DIR):
        os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
        return chunks

    for root, _, files in os.walk(KNOWLEDGE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            
            try:
                if ext in ['.txt', '.md']:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    chunks.extend(_chunk_text(content, file))
                elif ext == '.html':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f.read(), 'html.parser')
                        content = soup.get_text(separator='\n')
                    chunks.extend(_chunk_text(content, file))
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

    return chunks

def _chunk_text(text: str, filename: str):
    """
    Splits content into logical chunks. Very simple split by double newline.
    """
    # Clean text
    text = re.sub(r'\n{3,}', '\n\n', text)
    raw_chunks = [c.strip() for c in text.split('\n\n') if len(c.strip()) > 10]
    
    chunks = []
    for idx, c in enumerate(raw_chunks):
        chunks.append({
            "source": filename,
            "chunk_id": f"{filename}_{idx}",
            "content": c
        })
    return chunks

# Global cache for local knowledge
_LOCAL_KNOWLEDGE_CACHE = []

def get_knowledge_chunks():
    global _LOCAL_KNOWLEDGE_CACHE
    if not _LOCAL_KNOWLEDGE_CACHE:
        _LOCAL_KNOWLEDGE_CACHE = load_local_knowledge()
    return _LOCAL_KNOWLEDGE_CACHE

def reload_knowledge():
    global _LOCAL_KNOWLEDGE_CACHE
    _LOCAL_KNOWLEDGE_CACHE = load_local_knowledge()
    return len(_LOCAL_KNOWLEDGE_CACHE)
