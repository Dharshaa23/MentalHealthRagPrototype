from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from model import generate_answer


# -----------------------------
# Load embeddings and vector DB
# -----------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    "langchain_faiss",
    embeddings,
    allow_dangerous_deserialization=True
)


# -----------------------------
# Retrieval
# -----------------------------

def retrieve(query, k=3, threshold=1.0):

    results = vectorstore.similarity_search_with_score(
        query,
        k=k
    )

    filtered_results = []

    for document, score in results:

        if score <= threshold:
            filtered_results.append(document)

    return filtered_results


# -----------------------------
# RAG answer generation
# -----------------------------

def answer_question(query):

    documents = retrieve(query)

    if not documents:
        return (
            "The provided information does not contain "
            "an answer to that question."
        )

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are an educational assistant.

Answer the user's question using ONLY the information
provided in the context.

Rules:
1. Do not use outside knowledge.
2. Do not invent facts.
3. Give a clear and concise answer.
4. If the context does not contain enough information,
   say exactly:

"The provided information does not contain an answer to that question."

5. Do not diagnose or provide medical treatment.
6. Do not mention information that is not supported by the context.

Context:
{context}

User question:
{query}

Answer:
"""

    answer = generate_answer(prompt)

    return answer


# -----------------------------
# CLI
# -----------------------------

if __name__ == "__main__":

    while True:

        query = input("\nEnter a question (or type 'exit'): ")

        if query.lower() == "exit":
            break

        answer = answer_question(query)

        print("\nAnswer:")
        print(answer)