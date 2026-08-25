from services.knowledge_loader import get_knowledge_chunks
from services.website_cache import get_website_chunks
from services.retriever import search_chunks
from services.openai_service import generate_openai_answer
from services.gemini_service import generate_gemini_answer
from services.query_analyzer import analyze_query
from config import LOCAL_RELEVANCE_THRESHOLD, WEBSITE_RELEVANCE_THRESHOLD

NOT_FOUND_MESSAGE = "I couldn't find that information in the available MST Academy knowledge. Please contact Academy Support for further assistance."

def answer_question(question: str, history: list = None, provider: str = "gemini") -> dict:
    if history is None:
        history = []
        
    # Analyze the query for intent and search terms
    analysis = analyze_query(question, history, provider)
    search_terms = analysis.get("search_terms", [question])
    intent = analysis.get("intent", question)
    
    print("="*40)
    print(f"Original query : {question}")
    print(f"Detected intent: {intent}")
    print(f"Search terms   : {search_terms}")
    print("="*40)

    # 1. Search local knowledge
    local_chunks = get_knowledge_chunks()
    local_results = search_chunks(search_terms, local_chunks, LOCAL_RELEVANCE_THRESHOLD)
    
    local_relevant = len(local_results) > 0
    
    # 2. Search website cache if local is not enough
    website_results = []
    website_relevant = False
    
    website_chunks = get_website_chunks()
    if website_chunks:
        website_results = search_chunks(search_terms, website_chunks, WEBSITE_RELEVANCE_THRESHOLD)
        website_relevant = len(website_results) > 0
        
    # 3. Determine flow based on relevance
    if local_relevant and website_relevant:
        source = "BOTH"
        context = _combine_context(local_results, website_results)
    elif local_relevant:
        source = "LOCAL_KB"
        context = _combine_context(local_results, [])
    elif website_relevant:
        source = "WEBSITE"
        context = _combine_context([], website_results)
    else:
        # None found. DO NOT call OpenAI or Gemini to answer from general knowledge.
        return {
            "answer": NOT_FOUND_MESSAGE,
            "source": "NONE"
        }
        
    # 4. Generate answer based on selected provider
    if provider.lower() == "gemini":
        answer = generate_gemini_answer(question, context)
    else:
        answer = generate_openai_answer(question, context)
    
    return {
        "answer": answer,
        "source": source
    }

def _combine_context(local_results, website_results) -> str:
    parts = []
    if local_results:
        parts.append("--- LOCAL ACADEMY KNOWLEDGE ---")
        for res in local_results:
            parts.append(f"Source: {res['source']}\n{res['content']}")
            
    if website_results:
        parts.append("--- MST ACADEMY WEBSITE KNOWLEDGE ---")
        for res in website_results:
            parts.append(f"Source: {res['source']}\n{res['content']}")
            
    return "\n\n".join(parts)
