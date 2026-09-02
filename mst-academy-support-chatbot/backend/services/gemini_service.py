# pyrefly: ignore [missing-import]
import google.generativeai as genai
# pyrefly: ignore [missing-import]
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from config import GEMINI_API_KEY, GEMINI_MODEL
from services.openai_service import SYSTEM_PROMPT

def generate_gemini_answer(question: str, context: str, history: list = None) -> str:
    if not GEMINI_API_KEY:
        return "System Configuration Error: Gemini API key is missing. Please configure GEMINI_API_KEY."

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT
        )
        
        history_str = ""
        if history:
            history_str = "Conversation History:\n" + "\n".join([f"{msg.get('role', 'user')}: {msg.get('text', '')}" for msg in history[-4:]]) + "\n\n"
            
        prompt = f"{history_str}USER QUESTION: {question}\n\nCONTEXT:\n{context}"
        
        # Turn off safety filters as this is a support chatbot relying on strict context
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        response = model.generate_content(prompt, safety_settings=safety_settings)
        return response.text
        
    except Exception as e:
        error_msg = str(e).lower()
        if "api_key" in error_msg or "authentication" in error_msg or "invalid" in error_msg and "key" in error_msg:
            return "System Configuration Error: Invalid Gemini API key. Please check your configuration."
        elif "quota" in error_msg or "429" in error_msg:
            return "System Error: Gemini rate limit or quota exceeded. Please try again later."
        elif "model" in error_msg and "not found" in error_msg:
            return f"System Error: Invalid Gemini model '{GEMINI_MODEL}'. Please configure a valid model."
        else:
            print(f"Gemini API Error: {str(e)}")
            return "An unexpected error occurred while generating the answer via Gemini. Please try again later."

import json

def analyze_query_gemini(query: str, history: list) -> dict:
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key is missing")

    genai.configure(api_key=GEMINI_API_KEY)
    
    # We use a standard model but output in JSON
    model = genai.GenerativeModel(model_name=GEMINI_MODEL)
    
    history_str = ""
    if history:
        # Take the last few messages for context
        recent_history = history[-4:] 
        history_str = "Conversation History:\n" + "\n".join([f"{msg['role']}: {msg['text']}" for msg in recent_history if 'text' in msg])

    prompt = f"""You are a query analysis AI for an Academy Support chatbot.
Your job is to understand the user's intent and generate search terms to find the right information in the knowledge base.
The chatbot helps with: pricing, enrollment, payment, login, course access, videos, notes/downloads, mock tests, results, certificates, internships, course structure, technical issues, assessments, evaluation, and assignments.

{history_str}
Current User Query: {query}

Output a valid JSON object with the following schema:
{{
  "intent": "A short summary of the user's intent",
  "search_terms": ["list", "of", "relevant", "synonyms", "and", "phrases", "to", "search", "the", "knowledge", "base"]
}}

Include multiple variations in search_terms (e.g. for pricing: fee, cost, price, charge, how much). Do not wrap in markdown blocks, just raw JSON.
"""
    
    response = model.generate_content(prompt)
    
    text = response.text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
        
    return json.loads(text.strip())

