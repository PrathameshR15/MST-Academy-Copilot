import re
from typing import List, Dict

STOP_WORDS = set([
    "a", "an", "the", "and", "or", "but", "if", "then", "is", "are", "am", "was", "were", 
    "be", "being", "been", "to", "of", "in", "for", "with", "on", "at", "by", "from", 
    "up", "about", "into", "over", "after", "how", "what", "why", "when", "where", 
    "who", "which", "this", "that", "these", "those", "it", "they", "he", "she", 
    "we", "you", "i", "my", "your", "their", "our", "can", "could", "will", "would", 
    "shall", "should", "may", "might", "must", "do", "does", "did"
])

def _normalize_text(text: str) -> str:
    # Lowercase and remove punctuation except spaces
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return ' '.join(text.split())

def _extract_keywords(text: str) -> List[str]:
    words = _normalize_text(text).split()
    return [w for w in words if w not in STOP_WORDS]

def calculate_relevance(search_terms: List[str], text: str) -> float:
    """
    Evaluates relevance across multiple synonyms/search terms and takes the maximum score.
    """
    norm_text = _normalize_text(text)
    text_keywords_set = set(_extract_keywords(text))
    
    max_score = 0.0
    
    for term in search_terms:
        score = 0.0
        norm_term = _normalize_text(term)
        
        # Exact phrase match gives a big boost
        if norm_term and norm_term in norm_text:
            score += 0.5
            
        term_keywords = _extract_keywords(term)
        if not term_keywords:
            continue
            
        match_count = sum(1 for kw in term_keywords if kw in text_keywords_set)
        
        # Ratio of matched keywords
        kw_ratio = match_count / len(term_keywords)
        score += kw_ratio
        
        if score > max_score:
            max_score = score
            
    return min(1.0, max_score)

def search_chunks(search_terms: List[str], chunks: List[Dict], threshold: float, top_k: int = 15) -> List[Dict]:
    scored_chunks = []
    for chunk in chunks:
        score = calculate_relevance(search_terms, chunk["content"])
        if score >= threshold:
            scored_chunks.append({**chunk, "score": score})
            
    # Sort by score descending
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks[:top_k]
