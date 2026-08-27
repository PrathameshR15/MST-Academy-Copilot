import json
from services.gemini_service import analyze_query_gemini
from services.openai_service import analyze_query_openai

def analyze_query(query: str, history: list, provider: str = "openai") -> dict:
    """
    Analyzes the user query and returns a dictionary with 'intent' and 'search_terms'.
    """
    try:
        if provider.lower() == "gemini":
            result = analyze_query_gemini(query, history)
        else:
            result = analyze_query_openai(query, history)
            
        # Ensure the result is valid json/dict and has search_terms
        if isinstance(result, dict) and "search_terms" in result:
            return result
    except Exception as e:
        print(f"Query analysis failed: {e}")
        
    # Fallback to the original query
    return {
        "intent": query,
        "search_terms": [query]
    }
