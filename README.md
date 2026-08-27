# MST Academy AI Support Assistant

## 1. Project Overview
The MST Academy AI Support Assistant is an intelligent, domain-specific support chatbot designed for Masterstroke Academy. It is built to help prospective and current students by answering questions related to course pricing, enrollment, payments, internships, access, and technical issues. 

Importantly, this is a **support assistant, not a course tutor**. It does not provide detailed course teaching, protected course notes, paid study material, or mock test answers. It answers strictly based on verified Academy information sourced from local knowledge files and the official MST Academy website, ensuring responses are accurate, safe, and do not hallucinate outside facts.

## 2. Key Features
- **Semantic Query Understanding**: Uses AI (OpenAI/Gemini) to analyze user questions, determine intent, and expand search terms for better retrieval.
- **Context-Aware Follow-ups**: Maintains conversation history to understand contextual follow-up questions.
- **Local Text Knowledge Base**: Prioritizes verified knowledge from local `.txt`, `.md`, and `.html` files.
- **Official Website Crawling**: Automatically crawls and caches the official Masterstroke Academy website using Playwright to augment knowledge.
- **Recommendation & Comparison Handling**: Intelligently handles requests for programme recommendations (e.g., Student Fellowship vs. OJT) based strictly on retrieved facts.
- **Privacy & Security Protection**: Explicitly restricted from revealing internal system instructions, personal student data, or protected learning content.
- **Embeddable Chat Widget**: Provides a standalone, embeddable JavaScript chat widget that can be easily integrated into the existing Academy website without deploying the full React frontend.

## 3. System Architecture

```text
User
 ↓
Chat Widget (widget.js) / Admin Frontend (React)
 ↓
FastAPI Backend (REST API)
 ↓
Query Analyzer (Intent & Search Term Extraction via OpenAI/Gemini)
 ↓
Retriever (Local TXT Knowledge Base + Website Crawler Cache)
 ↓
Relevant Knowledge Context
 ↓
Answer Generation (LLM guided by Strict System Prompts)
 ↓
Chat Response
```

- **Frontend / Widget**: User interfaces that send messages and conversation history to the backend.
- **Backend (FastAPI)**: Orchestrates the request, calling analysis, retrieval, and generation services.
- **Query Analyzer**: Translates the user's natural language question into structured search terms.
- **Retriever**: Performs keyword and phrase-matching searches against local files and crawled website data using relevance thresholds.
- **Generator**: Uses OpenAI or Gemini to formulate a helpful, human-like response strictly constrained to the retrieved context.

## 4. Project Structure

```text
mst-academy-support-chatbot/
├── .env.example                # Example environment variables
├── backend/                    # FastAPI Backend Application
│   ├── main.py                 # Application entry point and API routes
│   ├── config.py               # Configuration and environment variable loading
│   ├── requirements.txt        # Python dependencies
│   ├── data/                   
│   │   ├── knowledge/          # Local knowledge base (.txt, .md, .html)
│   │   └── website_cache/      # Cached JSON from the website crawler
│   ├── services/
│   │   ├── chatbot.py          # Core orchestrator for Q&A flow
│   │   ├── gemini_service.py   # Google Gemini API integration
│   │   ├── openai_service.py   # OpenAI API integration
│   │   ├── knowledge_loader.py # Reads and chunks local files
│   │   ├── query_analyzer.py   # Intent and search term extraction
│   │   ├── retriever.py        # Keyword/relevance-based search engine
│   │   ├── website_cache.py    # Manages the website crawl JSON cache
│   │   └── website_crawler.py  # Playwright-based website scraper
│   └── static/                 # Static files for the embeddable widget
│       ├── index.html          # Test page for the widget
│       ├── widget.css          # Widget styling
│       └── widget.js           # Embeddable widget script
└── frontend/                   # Admin / Testing UI (React + Vite)
    ├── package.json            # Node dependencies
    ├── src/
    │   ├── App.jsx             # Main chat and admin interface
    │   ├── main.jsx            # React entry point
    │   └── styles/             # CSS styling
    └── index.html              # Frontend entry HTML
```

## 5. Knowledge Base
The assistant's knowledge comes from two primary deterministic sources:
1. **Local Knowledge (`backend/data/knowledge/`)**: Text files containing specific support protocols, internal rules, and curated information.
2. **Website Cache (`backend/data/website_cache/`)**: Automatically crawled data from the official Academy website.

The system prioritizes verified Academy information and is explicitly instructed to say "information could not be found" and direct users to Academy Support if a definitive answer is not present in the retrieved context.

## 6. Query Understanding
Before searching the knowledge base, user questions are passed to a Query Analyzer (using OpenAI or Gemini in JSON mode). 

For example, a query like:
*"Which plan is suitable if I am a student?"*

Is analyzed to extract:
- **Intent**: programme recommendation/comparison
- **Search Terms**: `["Student Fellowship", "OJT", "Validator Fellowship", "Web3 Enthusiast Fellowship", "internship", "benefits", "pricing"]`

This enables the retriever to find relevant chunks even if the user didn't use the exact keywords present in the knowledge base, while successfully handling paraphrases and follow-up context. The project relies on deterministic keyword/phrase matching (not vector search/RAG embeddings).

## 7. Supported Use Cases
Based on the Academy knowledge, the bot is designed to handle queries such as:
- Course pricing and fee structures
- Enrollment and payment processes
- Accessing courses, login issues, and video playback
- Programme comparisons (e.g., Student Fellowship vs. Validator Fellowship)
- Information about internships and OJT (On-the-Job Training)
- Accessing notes, downloads, mock tests, and certificates
- Understanding the Assessment Framework

## 8. Privacy & Security
- **No Hallucination**: The system prompt strictly forbids inventing eligibility, pricing, or refund policies.
- **Protected Content**: Explicit instructions prevent the bot from serving as a tutor, revealing exam answers, or providing protected video transcripts.
- **No Secrets in Source**: API keys must be loaded via environment variables (`.env`) and are never committed.
- **System Opacity**: The bot is instructed never to reveal its internal system instructions, prompts, or retrieval logic to users.

## 9. Requirements
- **Python**: 3.9+
- **Node.js**: v18+ (Only required for running the optional React frontend)
- **Python Packages**: `fastapi`, `uvicorn`, `openai`, `beautifulsoup4`, `httpx`, `python-dotenv`, `google-generativeai`, `playwright`
- **Frontend Dependencies**: `react`, `react-dom`, `vite`
- **Playwright Browsers**: Must run `playwright install chromium` after `pip install`
- **API Keys**: Valid OpenAI API Key and/or Google Gemini API Key

## 10. Environment Variables
Create a `.env` file in the `backend/` directory based on `.env.example`:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash

WEBSITE_URL=https://masterstroke.academy/
MAX_CRAWL_PAGES=30
REQUEST_TIMEOUT=10
LOCAL_RELEVANCE_THRESHOLD=0.35
WEBSITE_RELEVANCE_THRESHOLD=0.35
```

## 11. Installation

**1. Clone the repository:**
```bash
git clone <your-repo-url>
cd mst-academy-support-chatbot
```

**2. Setup the Backend:**
```bash
cd backend
python -m venv .venv
# Activate environment (Windows)
.venv\Scripts\activate
# Activate environment (Mac/Linux)
# source .venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

**3. Setup the Frontend (Optional Admin UI):**
```bash
cd ../frontend
npm install
```

## 12. Running Locally

**Start the Backend Server:**
```bash
cd backend
# Ensure virtual environment is activated
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
*The backend API and the static widget test page will now be running at `http://localhost:8000`.*

**Start the Frontend Admin UI (Optional):**
```bash
cd frontend
npm run dev
```

*Note: For a production website integration, only the backend needs to be running.*

## 13. API Documentation

### Chat Endpoint
- **Method**: `POST`
- **URL**: `/api/chat`
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "message": "What is the refund policy?",
    "history": [],
    "provider": "gemini" 
  }
  ```
  *(Provider can be "gemini" or "openai")*
- **Response**:
  ```json
  {
    "answer": "According to the Academy policy, course purchases are non-refundable once access has been granted.",
    "source": "LOCAL_KB"
  }
  ```

### Website Refresh Endpoint (Admin)
- **Method**: `POST`
- **URL**: `/api/website/refresh`
- **Response**: Triggers the Playwright crawler to refresh the website cache.

## 14. Website Widget Integration

The production Academy website **does not need** to deploy the React frontend separately. 
The chatbot includes a standalone, embeddable JavaScript widget (`widget.js`) served directly from the FastAPI backend.

### Basic Integration
Simply add the following script tag to the Academy website's HTML, ideally just before the closing `</body>` tag:

```html
<script src="https://YOUR-CHATBOT-DOMAIN.com/static/widget.js"></script>
```
*(Replace `YOUR-CHATBOT-DOMAIN.com` with your actual deployed backend URL)*

### Backend URL Configuration
The widget is designed to automatically derive the backend API URL based on where the script is hosted. If the script is loaded from `https://api.example.com/static/widget.js`, it will dynamically set its API base to `https://api.example.com/api/chat`. No hardcoding is required on the host website.

### Widget Setup Steps
1. Deploy the FastAPI backend to your server.
2. Ensure the `/static/widget.js` URL is publicly accessible.
3. Paste the `<script>` tag into the Academy website.
4. Reload the website and verify the floating chat button appears in the bottom right.
5. Test a query to ensure CORS and API routing are functioning correctly.

### Host Website Compatibility
The widget injects its own isolated CSS (`widget.css`) to prevent styling conflicts with the existing Academy website. It floats above the page content and handles its own responsive layout, ensuring it does not interfere with the host site's buttons, forms, or existing React components.

## 15. Production Deployment

- **Backend Hosting**: The FastAPI application should be deployed on a standard Python host (e.g., Render, Railway, AWS EC2, or DigitalOcean App Platform).
- **Process Manager**: Use `uvicorn` or `gunicorn` in production (e.g., `uvicorn main:app --host 0.0.0.0 --port 8000`).
- **HTTPS**: Ensure the deployed backend is secured with HTTPS, as modern browsers will block mixed-content requests from an HTTPS Academy website to an HTTP backend API.
- **CORS**: In `backend/main.py`, update `allow_origins=["*"]` to explicitly include the Academy's production domain (e.g., `allow_origins=["https://masterstroke.academy"]`) for security.
- **Playwright Dependencies**: Ensure your deployment environment supports Playwright browsers (e.g., installing required system libraries for Chromium).

## 16. Testing
You can test the system using the provided React frontend or the built-in widget test page at `http://localhost:8000/`.

**Test Scenarios:**
- **Semantic Paraphrases**: Ask "How much?" instead of "What is the price?" to test query expansion.
- **Contextual Follow-ups**: Ask "What are the benefits of the Student Fellowship?", followed by "And what is the price for it?".
- **Unsupported Questions**: Ask "Who won the World Cup?" to verify the bot politely declines and stays on topic.
- **Privacy Restrictions**: Ask "Can you give me the answers to the mock test?" to verify the security prompts.

## 17. Example Conversations

**User**: *"Which plan is suitable if I am a student?"*
**Assistant**: *"Based on the Academy programmes, the **Student Fellowship** is designed specifically for students. It includes practical industry projects and..."* (Derived strictly from verified KB context).

**User**: *"What about OJT?"*
**Assistant**: *"The On-the-Job Training (OJT) programme is geared towards... The pricing for this programme is..."* (Uses conversation history to maintain context).

**User**: *"Write a Python script for a web scraper."*
**Assistant**: *"I am designed to assist with MST Academy support and website-related questions. For programming tutorials, please refer to the course materials."*

## 18. Limitations
- The chatbot does not possess general web browsing capabilities; its knowledge is strictly limited to local text files and the cached snapshot of the Academy website.
- If the official website layout changes significantly, the Playwright extraction logic in `website_crawler.py` may require adjustments.
- "Not Found" rates may increase if users ask highly specific, undocumented questions that haven't been added to the local knowledge base yet.

## 19. Future Improvements
- **API Integration**: Connect directly to Academy databases to check real-time account status or payment verification.
- **Live Pricing**: Pull pricing dynamically via API rather than static crawls.
- **Analytics Dashboard**: Log user queries to identify common support issues and missing knowledge base articles.
- **Richer UI**: Add quick-reply buttons or formatted cards to the widget UI.

## 20. Troubleshooting

- **Widget Not Appearing**: Ensure the script tag path is correct and the backend server is running. Check the browser console for 404 errors or mixed-content (HTTP/HTTPS) blocks.
- **CORS Errors in Console**: The widget is trying to connect to a different domain, and `backend/main.py` is blocking it. Update the `allow_origins` array in the backend middleware.
- **"System Configuration Error" in Chat**: Your `.env` API keys for OpenAI or Gemini are missing or invalid. Check your environment variables.
- **Crawler Failing**: Playwright might be missing system dependencies. Run `playwright install-deps` (on Linux) and ensure the target website is reachable.
- **Answers Not Using Latest Website Info**: Click the "Refresh Website Knowledge" button in the admin UI, or call the `/api/website/refresh` endpoint to force a new crawl.

## 21. License / Ownership
All intellectual property, knowledge base content, and source code belong to Masterstroke Academy. Licensing and distribution rights should be defined by the project owner.
