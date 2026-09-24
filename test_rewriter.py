from query_rewriter import rewrite_query


test_cases = [
    {
        "history": [
            {
                "user": "What is anxiety?",
                "assistant": "Anxiety is a common emotional response."
            }
        ],
        "query": "What are its common experiences?",
        "expected_term": "anxiety"
    },

    {
        "history": [
            {
                "user": "What is stress?",
                "assistant": "Stress is a response to challenging situations."
            }
        ],
        "query": "What are its effects?",
        "expected_term": "stress"
    },

    {
        "history": [
            {
                "user": "What is emotional wellbeing?",
                "assistant": "Emotional wellbeing relates to how people manage emotions."
            }
        ],
        "query": "What factors contribute to it?",
        "expected_term": "emotional wellbeing"
    },

    {
        "history": [],
        "query": "What is anxiety?",
        "expected_term": "anxiety"
    }
]


correct = 0

print("=" * 60)
print("QUERY REWRITING EVALUATION")
print("=" * 60)


for test in test_cases:

    rewritten = rewrite_query(
        test["query"],
        test["history"]
    )

    expected_term = test["expected_term"]

    passed = expected_term.lower() in rewritten.lower()

    if passed:
        correct += 1

    print("\nOriginal:")
    print(test["query"])

    print("Rewritten:")
    print(rewritten)

    print("Expected reference:")
    print(expected_term)

    print("Result:")
    print("PASS" if passed else "FAIL")


accuracy = correct / len(test_cases)

print("\n" + "=" * 60)
print(f"Query Rewriting Accuracy: {accuracy:.2%}")
print("=" * 60)