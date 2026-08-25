import json
import os
from config import WEBSITE_CACHE_FILE, WEBSITE_CACHE_DIR
from datetime import datetime

def load_website_cache():
    if not os.path.exists(WEBSITE_CACHE_FILE):
        return {"pages": [], "last_refreshed": None}
    try:
        with open(WEBSITE_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading website cache: {e}")
        return {"pages": [], "last_refreshed": None}

def save_website_cache(pages, last_refreshed_str):
    os.makedirs(WEBSITE_CACHE_DIR, exist_ok=True)
    try:
        with open(WEBSITE_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "pages": pages,
                "last_refreshed": last_refreshed_str
            }, f, indent=2)
    except Exception as e:
        print(f"Error saving website cache: {e}")

_WEBSITE_CACHE = None

def get_website_chunks():
    global _WEBSITE_CACHE
    if _WEBSITE_CACHE is None:
        cache_data = load_website_cache()
        
        # Convert pages to chunk format for retriever
        chunks = []
        for p in cache_data.get("pages", []):
            chunks.append({
                "source": p["url"],
                "chunk_id": p["url"],
                "content": f"{p['title']}\n{p['text']}"
            })
        _WEBSITE_CACHE = chunks
    return _WEBSITE_CACHE

def reload_website_cache():
    global _WEBSITE_CACHE
    _WEBSITE_CACHE = None
    return get_website_chunks()

def get_website_status():
    cache_data = load_website_cache()
    return {
        "cached_pages": len(cache_data.get("pages", [])),
        "last_refreshed": cache_data.get("last_refreshed")
    }
