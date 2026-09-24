from retrieve import retrieve


test_cases = [
    {
        "query": "What is anxiety?",
        "expected_source": "anxiety.txt"
    },
    {
        "query": "What are common experiences of anxiety?",
        "expected_source": "anxiety.txt"
    },
    {
        "query": "What are the effects of prolonged stress?",
        "expected_source": "stress.txt"
    },
    {
        "query": "How does sleep affect wellbeing?",
        "expected_source": "sleep.txt"
    },
    {
        "query": "What factors contribute to emotional wellbeing?",
        "expected_source": "emotional_wellbeing.txt"
    },

    # Out-of-scope test
    {
        "query": "What is the capital of France?",
        "expected_source": None
    }
]


correct = 0

print("=" * 60)
print("RAG RETRIEVAL EVALUATION")
print("=" * 60)


for test in test_cases:

    query = test["query"]
    expected = test["expected_source"]

    results = retrieve(query)

    retrieved_sources = [
        result["source"]
        for result in results
    ]

    # Expected answer exists in knowledge base
    if expected is not None:
        passed = expected in retrieved_sources

    # Expected answer does NOT exist
    else:
        passed = len(results) == 0

    if passed:
        correct += 1

    print("\nQuery:")
    print(query)

    print("Expected:")
    print(expected if expected else "No relevant source")

    print("Retrieved:")
    print(retrieved_sources)

    print("Result:")
    print("PASS" if passed else "FAIL")


accuracy = correct / len(test_cases)

print("\n" + "=" * 60)
print(f"Evaluation Accuracy: {accuracy:.2%}")
print("=" * 60)