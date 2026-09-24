from retrieve import retrieve
from model import generate_answer


test_cases = [
    "What is anxiety?",
    "What are common experiences of anxiety?",
    "What are the effects of prolonged stress?",
    "How does sleep affect wellbeing?",
    "What factors contribute to emotional wellbeing?"
]


def calculate_grounding_score(answer, context):
    """
    Simple evidence-overlap score.

    Measures how many meaningful words in the generated
    answer also appear in the retrieved context.
    """

    answer_words = set(
        word.lower().strip(".,!?;:()")
        for word in answer.split()
        if len(word) > 3
    )

    context_words = set(
        word.lower().strip(".,!?;:()")
        for word in context.split()
        if len(word) > 3
    )

    if not answer_words:
        return 0.0

    supported_words = answer_words.intersection(context_words)

    score = len(supported_words) / len(answer_words)

    return score


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


total_score = 0

print("=" * 60)
print("AUTOMATED GROUNDING EVALUATION")
print("=" * 60)

for query in test_cases:

    answer, results = generate_grounded_answer(query)

    context = ""

    for result in results:
        context += result["text"] + "\n\n"

    score = calculate_grounding_score(answer, context)

    total_score += score

    print("\n" + "=" * 60)
    print("Question:")
    print(query)

    print("\nGenerated answer:")
    print(answer)

    print(f"\nGrounding score: {score:.2f}")


average_score = total_score / len(test_cases)

print("\n" + "=" * 60)
print(f"Average grounding score: {average_score:.2f}")
print("=" * 60)