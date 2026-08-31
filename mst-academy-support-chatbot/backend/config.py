import os
from dotenv import load_dotenv

# Load environment variables from backend/.env or root .env
_env_backend = os.path.join(os.path.dirname(__file__), ".env")
_env_root = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(_env_backend):
    load_dotenv(_env_backend)
if os.path.exists(_env_root):
    load_dotenv(_env_root)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

WEBSITE_URL = os.getenv("WEBSITE_URL", "https://masterstroke.academy/")
MAX_CRAWL_PAGES = int(os.getenv("MAX_CRAWL_PAGES", "30"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
LOCAL_RELEVANCE_THRESHOLD = float(os.getenv("LOCAL_RELEVANCE_THRESHOLD", "0.35"))
WEBSITE_RELEVANCE_THRESHOLD = float(os.getenv("WEBSITE_RELEVANCE_THRESHOLD", "0.35"))

_allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if _allowed_origins_env.strip():
    ALLOWED_ORIGINS = [o.strip() for o in _allowed_origins_env.split(",") if o.strip()]
else:
    ALLOWED_ORIGINS = [
        "https://masterstroke.academy",
        "https://www.masterstroke.academy",
        "http://localhost:3000",
        "http://localhost:3000/"
    ]

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "data", "knowledge")
WEBSITE_CACHE_DIR = os.path.join(os.path.dirname(__file__), "data", "website_cache")
WEBSITE_CACHE_FILE = os.path.join(WEBSITE_CACHE_DIR, "website_content.json")
