from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    "langchain_faiss",
    embeddings,
    allow_dangerous_deserialization=True
)


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


if __name__ == "__main__":
    query = input("Enter a question: ")

    results = retrieve(query)

    print("\nRetrieved documents:\n")

    if not results:
        print("No relevant information found in the knowledge base.")
    else:
        for i, document in enumerate(results, start=1):
            print("=" * 60)
            print(f"Result {i}")
            print(f"Source: {document.metadata.get('source')}")
            print("\nContent:")
            print(document.page_content)