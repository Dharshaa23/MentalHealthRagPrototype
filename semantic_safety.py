from sentence_transformers import SentenceTransformer
import numpy as np


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# Representative safety-intent examples.
# These are used for semantic comparison, not exact keyword matching.
SAFETY_EXAMPLES = [
    "I am having thoughts about suicide.",
    "I am thinking about ending my life.",
    "I feel like I might hurt myself.",
    "I don't want to be alive anymore.",
    "I am thinking about killing myself.",
    "I feel unsafe and might harm myself.",
    "I am having thoughts of self harm.",
    # Additional variations
    "I feel like I may not be able to keep myself safe.",
    "I am worried I might hurt myself.",
    "I am struggling to stay safe right now.",
    "I am having thoughts that make me feel unsafe.",
    "I feel at risk of hurting myself.",
    "I am scared of what I might do to myself.",
    "I don't trust myself to stay safe right now.",
]


# Convert the examples into embeddings once.
SAFETY_EMBEDDINGS = model.encode(
    SAFETY_EXAMPLES,
    convert_to_numpy=True,
    normalize_embeddings=True
)

SAFETY_THRESHOLD = 0.60

def semantic_safety_score(query):
    """
    Return the highest semantic similarity between the
    query and the safety-intent examples.
    """

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )[0]

    scores = np.dot(
        SAFETY_EMBEDDINGS,
        query_embedding
    )

    return float(np.max(scores))

def is_semantically_sensitive(query):
    score = semantic_safety_score(query)
    return score >= SAFETY_THRESHOLD

if __name__ == "__main__":

    print("Semantic Safety Detector")
    print("=" * 50)

    while True:

        query = input(
            "\nEnter a query (or type 'exit'): "
        )

        if query.lower() == "exit":
            break

        score = semantic_safety_score(query)
        sensitive = is_semantically_sensitive(query)

        print(f"\nSafety similarity score: {score:.4f}")
        print(f"Safety classification: {'SENSITIVE' if sensitive else 'NORMAL'}")