from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from safety import check_safety, get_safe_response
from model import generate_answer
from memory import ConversationMemory
from query_rewriter import rewrite_query


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    "langchain_faiss",
    embeddings,
    allow_dangerous_deserialization=True
)


memory = ConversationMemory(max_turns=5)


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


def answer_question(query):
    safety_status = check_safety(query)
    print("Safety status:", safety_status)

    if safety_status == "sensitive":
        answer = get_safe_response()
        return answer, []
    # ------------------------------------------------
    # 1. Get conversation history
    # ------------------------------------------------

    history = memory.get_history()


    # ------------------------------------------------
    # 2. Rewrite query if conversation exists
    # ------------------------------------------------

    rewritten_query = rewrite_query(
        query,
        history
    )

    print("\nSearch query:")
    print(rewritten_query)


    # ------------------------------------------------
    # 3. Retrieve relevant documents
    # ------------------------------------------------

    documents = retrieve(
        rewritten_query
    )


    # ------------------------------------------------
    # 4. Handle no relevant information
    # ------------------------------------------------

    if not documents:

        answer = (
            "The provided information does not contain "
            "an answer to that question."
        )

        memory.add_turn(
            query,
            answer
        )

        return answer, []


    # ------------------------------------------------
    # 5. Build context
    # ------------------------------------------------

    context = "\n\n".join(
        document.page_content
        for document in documents
    )


    # ------------------------------------------------
    # 6. Collect sources
    # ------------------------------------------------

    sources = []

    for document in documents:

        source = document.metadata.get("source")

        if source and source not in sources:

            sources.append(source)


    # ------------------------------------------------
    # 7. Build conversation history
    # ------------------------------------------------

    history_text = ""

    for turn in history:

        history_text += (
            f"User: {turn['user']}\n"
            f"Assistant: {turn['assistant']}\n\n"
        )


    # ------------------------------------------------
    # 8. Generate grounded answer
    # ------------------------------------------------

    prompt = f"""
You are an educational assistant.

Your task is to answer the user's question using ONLY
the information provided in the context.

Rules:

1. Do not use outside knowledge.
2. Do not invent facts.
3. Give a clear and concise answer.
4. If the context does not contain enough information,
   say exactly:

"The provided information does not contain an answer
to that question."

5. Do not diagnose or provide medical treatment.
6. Do not mention information that is not supported
   by the context.
7. Use conversation history only to understand
   what the user is referring to.
8. Do not treat previous assistant answers
   as factual evidence.

Conversation history:

{history_text}

Context:

{context}

User question:

{query}

Answer:
"""


    answer = generate_answer(prompt)


    # ------------------------------------------------
    # 9. Store conversation turn
    # ------------------------------------------------

    memory.add_turn(
        query,
        answer
    )


    # ------------------------------------------------
    # 10. Return answer + sources
    # ------------------------------------------------

    return answer, sources


if __name__ == "__main__":

    while True:

        query = input(
            "\nEnter a question (or type 'exit'): "
        )

        if query.lower() == "exit":

            break


        answer, sources = answer_question(
            query
        )


        print("\nAnswer:")

        print(answer)


        if sources:

            print("\nSources:")

            for source in sources:

                print(f"- {source}")