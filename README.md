# MST Academy Support Chatbot

This project is a full-stack web application designed as a support chatbot for MST Academy.

## Architecture

1. **Backend**: FastAPI, Uvicorn, OpenAI Python SDK, BeautifulSoup4, httpx.
2. **Frontend**: React (Vite), plain CSS for styling.
3. **Retrieval**: Deterministic local knowledge base and website cache search using relevance thresholds.

### Question-Answer Flow

When a user asks a question, the backend processes it using the following logic:
1. **Local Knowledge Search**: Searches the uploaded local `.txt`, `.md`, or `.html` knowledge files.
2. **Website Search**: If the local search is insufficient, it searches the cached MST Academy website pages.
3. **Combination**: If both sources contain relevant information, they are combined.
4. **OpenAI API**: The relevant context (from local, website, or both) and the user question are sent to OpenAI (model `gpt-4.1-mini` by default) to generate the final answer.
5. **Not Found**: If no source contains sufficient information, the system returns a standard support message instead of hallucinating an answer.

## Setup Instructions (Windows)

### 1. Backend Setup

1. Open PowerShell and navigate to the `backend` directory:
   ```powershell
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Configuration:
   - Navigate back to the project root and copy `.env.example` to `.env`.
   - Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`.
   - Ensure the model is correct (default `gpt-4.1-mini`).
   
5. Adding Local Knowledge:
   - Place your scraped `.txt`, `.md`, or `.html` files in `backend/data/knowledge/`.
   
6. Start the server:
   ```powershell
   uvicorn main:app --reload
   ```
   *The backend will run on `http://localhost:8000`.*

### 2. Frontend Setup

1. Open a new PowerShell window and navigate to the `frontend` directory:
   ```powershell
   cd frontend
   ```
2. Install Node modules:
   ```powershell
   npm install
   ```
3. Start the development server:
   ```powershell
   npm run dev
   ```
   *The frontend will run on a local URL (e.g., `http://localhost:5173`). Open this URL in your browser.*

## Application Usage

- **Local Knowledge**: Loaded automatically on backend startup.
- **Refresh Website Knowledge**: Click the button in the admin panel on the frontend to crawl the configured website URL and update the cache.
- **Chat**: Use the main chat interface to interact with the support assistant.
