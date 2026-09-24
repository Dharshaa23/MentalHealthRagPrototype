from query_rewriter import rewrite_query
from retrieve import retrieve


test_cases = [
    {
        "history": [
            {
                "user": "What is anxiety?",
                "assistant": "Anxiety is a common emotional response."
            }
        ],
        "query": "What are its common experiences?",
        "expected_source": "anxiety.txt"
    },

    {
        "history": [
            {
                "user": "What is stress?",
                "assistant": "Stress is a response to challenging situations."
            }
        ],
        "query": "What are its effects?",
        "expected_source": "stress.txt"
    },

    {
        "history": [
            {
                "user": "What is sleep?",
                "assistant": "Sleep is important for wellbeing."
            }
        ],
        "query": "How does it affect wellbeing?",
        "expected_source": "sleep.txt"
    },

    {
        "history": [
            {
                "user": "What is emotional wellbeing?",
                "assistant": "Emotional wellbeing relates to managing emotions."
            }
        ],
        "query": "What factors contribute to it?",
        "expected_source": "emotional_wellbeing.txt"
    }
]


correct = 0

print("=" * 60)
print("END-TO-END CONVERSATIONAL RETRIEVAL EVALUATION")
print("=" * 60)


for test in test_cases:

    # Rewrite follow-up question
    rewritten_query = rewrite_query(
        test["query"],
        test["history"]
    )

    # Retrieve using rewritten query
    results = retrieve(rewritten_query)

    retrieved_sources = [
        result["source"]
        for result in results
    ]

    expected_source = test["expected_source"]

    passed = expected_source in retrieved_sources

    if passed:
        correct += 1

    print("\nOriginal question:")
    print(test["query"])

    print("Rewritten query:")
    print(rewritten_query)

    print("Expected source:")
    print(expected_source)

    print("Retrieved:")
    print(retrieved_sources)

    print("Result:")
    print("PASS" if passed else "FAIL")


accuracy = correct / len(test_cases)

print("\n" + "=" * 60)
print(f"Conversational Retrieval Accuracy: {accuracy:.2%}")
print("=" * 60)