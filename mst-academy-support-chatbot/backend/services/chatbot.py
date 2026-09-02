from services.knowledge_loader import get_knowledge_chunks
from services.website_cache import get_website_chunks
from services.retriever import search_chunks
from services.openai_service import generate_openai_answer
from services.gemini_service import generate_gemini_answer
from services.query_analyzer import analyze_query
from config import LOCAL_RELEVANCE_THRESHOLD, WEBSITE_RELEVANCE_THRESHOLD

NOT_FOUND_MESSAGE = "I couldn't find that information in the available MST Academy knowledge. Please contact Academy Support for further assistance."

def answer_question(question: str, history: list = None, provider: str = "openai") -> dict:
    import re
    q_lower = question.lower()
    forbidden_terms = [
        "true or false", "true/false", "mcq", "multiple choice", 
        "test answers", "exam answers", "assessment answers",
        "is this true", "is that true", "is it true", "is this false",
        "is that false", "is it false", "check true", "check false",
        "which of the following"
    ]
    
    # Check for MCQ pattern (e.g., "A. option1 B. option2 C. option3")
    has_mcq_pattern = bool(re.search(r'\b[a-d]\.\s', question, re.IGNORECASE))
    
    if any(term in q_lower for term in forbidden_terms) or has_mcq_pattern:
        return {
            "answer": "As per the Masterstroke Academy's integrity guidelines, I cannot provide answers to assessment questions, MCQs, or True/False questions. Please review the course materials to complete your evaluation.",
            "source": "SYSTEM"
        }

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
        answer = generate_gemini_answer(question, context, history)
    else:
        answer = generate_openai_answer(question, context, history)
    
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
