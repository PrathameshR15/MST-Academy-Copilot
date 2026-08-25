import json
from services.chatbot import answer_question
from services.knowledge_loader import get_knowledge_chunks

get_knowledge_chunks()

questions = [
    "Which course is suitable for a student?",
    "Which plan should I choose?",
    "Which programme is best for internship?",
    "What is the difference between Student Fellowship and OJT?",
    "Which programme is focused on blockchain validators?",
    "Which plan gives a paid internship?",
    "Which option gives industry project experience?",
    "Which plan is suitable if I am a student?"
]

results = []
for q in questions:
    print(f"Testing: {q}")
    res = answer_question(q, history=[], provider='openai')
    results.append({"question": q, "answer": res['answer']})

with open("test_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("Done.")
