import sys
import os

# Ensure backend directory is in path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# pyrefly: ignore [missing-import]
from services.chatbot import answer_question
# pyrefly: ignore [missing-import]
from services.knowledge_loader import get_knowledge_chunks

# Ensure chunks are loaded
get_knowledge_chunks()

queries = [
    # Pricing variations
    "What is the fee of the course?",
    "What is the cost of the course?",
    "What is the price of the course?",
    "How much is the course?",
    
    # Login variations
    "How do I login?",
    "I can't sign in",
    "My login isn't working",
    
    # Context follow-up
    "What about OJT?"
]

history = []

for q in queries:
    print("\n" + "*"*50)
    print(f"Testing Query: {q}")
    if q == "What about OJT?":
        # Simulate previous context
        test_history = [{"role": "user", "text": "What is the Student Fellowship price?"}, 
                        {"role": "assistant", "text": "The price is Rs 19,999."}]
        result = answer_question(q, history=test_history, provider="openai")
    else:
        result = answer_question(q, history=[], provider="openai")
        
    print(f"\nFinal Answer Snippet:\n{result['answer'][:200]}...")
    print(f"Source: {result['source']}")
    print("*"*50)
