import os
import faiss
import numpy as np
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer


# -----------------------------
# Load environment variables
# -----------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found.")


# -----------------------------
# Load Groq LLM
# -----------------------------

client = Groq(api_key=api_key)


# -----------------------------
# Load embedding model
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# Load FAISS index
# -----------------------------

index = faiss.read_index("knowledge_base.index")

metadata = np.load(
    "metadata.npy",
    allow_pickle=True
)


# -----------------------------
# Retrieve relevant information
# -----------------------------

def retrieve(query, k=3, threshold=1.0):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = query_embedding.astype("float32")

    distances, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for distance, index_id in zip(
        distances[0],
        indices[0]
    ):

        if distance > threshold:
            continue

        results.append({
            "source": metadata[index_id]["source"],
            "text": metadata[index_id]["text"],
            "distance": float(distance)
        })

    return results


# -----------------------------
# Ask the user
# -----------------------------

query = input("Ask a question: ")


# -----------------------------
# Retrieve context
# -----------------------------

results = retrieve(query)


if not results:

    print("\nNo sufficiently relevant information found.")

else:

    print("\nRetrieved Context:\n")

    context = ""

    for result in results:

        print("=" * 60)
        print("Source:", result["source"])
        print("Distance:", result["distance"])
        print(result["text"])

        context += result["text"] + "\n\n"


    # -----------------------------
    # Create RAG prompt
    # -----------------------------

    prompt = f"""
You are an educational assistant.

Answer the user's question using ONLY the information provided
in the context below.

If the context does not contain enough information to answer
the question, say that the provided information does not
contain the answer.

Context:
{context}

User question:
{query}
"""


    # -----------------------------
    # Send context + question to LLM
    # -----------------------------

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    # -----------------------------
    # Display answer
    # -----------------------------

    print("\n" + "=" * 60)
    print("LLM Answer:\n")

    print(response.choices[0].message.content)