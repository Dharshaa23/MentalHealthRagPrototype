from rag import answer_question


test_cases = [
    "What is anxiety?",
    "What are common experiences of anxiety?",
    "What are the effects of prolonged stress?",
    "How does sleep affect wellbeing?",
    "What factors contribute to emotional wellbeing?"
]


print("=" * 60)
print("GROUNDED ANSWER GENERATION TEST")
print("=" * 60)


for query in test_cases:

    answer, results = answer_question(query)

    print("\nQuestion:")
    print(query)

    print("\nAnswer:")
    print(answer)

    print("\nSources:")

    sources = []

    for result in results:
        if result["source"] not in sources:
            sources.append(result["source"])

    for source in sources:
        print(f"- {source}")

    print("\n" + "-" * 60)
    