from safety import check_safety, SENSITIVE, NORMAL
from semantic_safety import semantic_safety_score


SEMANTIC_THRESHOLD = 0.60


def combined_safety_check(query):
    """
    Combine keyword-based and semantic safety detection.

    If either layer detects safety-sensitive intent,
    classify the query as sensitive.
    """

    # Layer 1: keyword detection
    keyword_result = check_safety(query)

    if keyword_result == SENSITIVE:
        return SENSITIVE, "keyword"

    # Layer 2: semantic detection
    semantic_score = semantic_safety_score(query)

    if semantic_score >= SEMANTIC_THRESHOLD:
        return SENSITIVE, "semantic"

    return NORMAL, "none"


TEST_QUERIES = [
    # Should be detected by keyword layer
    "What is suicide?",
    "I am suicidal.",

    # Should be detected mainly by semantic layer
    "I don't feel safe with my own thoughts.",
    "I am worried I might hurt myself.",
    "I don't trust myself to stay safe right now.",

    # Should remain normal
    "What is anxiety?",
    "How can someone manage exam stress?",
    "Why do people experience depression?",
    "What are common signs of burnout?",
    "What is machine learning?",
]


if __name__ == "__main__":

    print("Combined Safety Detector Test")
    print("=" * 60)

    for query in TEST_QUERIES:

        result, detected_by = combined_safety_check(query)

        score = semantic_safety_score(query)

        print(f"\nQuery: {query}")
        print(f"Semantic score: {score:.4f}")
        print(f"Classification: {result}")
        print(f"Detected by: {detected_by}")
        