from retrieve import retrieve
from model import generate_answer


test_cases = [
    "What is anxiety?",
    "What are common experiences of anxiety?",
    "What are the effects of prolonged stress?",
    "How does sleep affect wellbeing?",
    "What factors contribute to emotional wellbeing?"
]


def generate_grounded_answer(query):

    results = retrieve(query)

    if not results:
        return None, []

    context = ""

    for result in results:
        context += result["text"] + "\n\n"

    prompt = f"""
You are an educational assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Use only information supported by the context.
2. Do not add outside facts.
3. Do not invent information.
4. If the context does not contain enough information, say:
   "The provided information does not contain an answer to that question."
5. Keep the answer concise.

Context:
{context}

User question:
{query}
"""

    answer = generate_answer(prompt)

    return answer, results


for query in test_cases:

    answer, results = generate_grounded_answer(query)

    print("\n" + "=" * 60)

    print("Question:")
    print(query)

    print("\nRetrieved context:")

    for result in results:
        print(f"\n[{result['source']}]")
        print(result["text"])

    print("\nGenerated answer:")
    print(answer)