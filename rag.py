from retrieve import retrieve
from model import generate_answer
from memory import ConversationMemory
from query_rewriter import rewrite_query
from safety import check_safety, NORMAL, SENSITIVE, get_safe_response

# Create conversation memory
memory = ConversationMemory(max_turns=5)


def build_history():
    history = memory.get_history()

    if not history:
        return ""

    history_text = ""

    for turn in history:
        history_text += f"User: {turn['user']}\n"
        history_text += f"Assistant: {turn['assistant']}\n\n"

    return history_text


def answer_question(query):

    # Check safety before processing the question
    safety_result = check_safety(query)

    if safety_result == SENSITIVE:
        return get_safe_response(), []

    # Get conversation history
    history_data = memory.get_history()

    # Rewrite the query for retrieval
    standalone_query = rewrite_query(
        query,
        history_data
    )

    print("\nSearch query:", standalone_query)

    # Retrieve using the rewritten query
    results = retrieve(standalone_query)    

    # No relevant information
    if not results:
        return None, []

    # Build context
    context = ""

    for result in results:
        context += result["text"] + "\n\n"

    # Build conversation history
    history = build_history()

    # Grounded prompt
    prompt = f"""
You are an educational assistant.

Your task is to answer the user's question using ONLY the
information provided in the context.

Rules:
1. Do not use outside knowledge.
2. Do not invent facts.
3. Give a clear and concise answer.
4. If the context does not contain enough information,
   say exactly:
   "The provided information does not contain an answer to that question."
5. Do not diagnose or provide medical treatment.
6. Do not mention information that is not supported by the context.
7. Use conversation history only to understand what the user is referring to.
8. Do not treat previous assistant answers as factual evidence.

Conversation history:
{history}

Context:
{context}

User question:
{query}
"""

    # Generate answer
    answer = generate_answer(prompt)

    # Store conversation
    memory.add_turn(query, answer)

    return answer, results


# Run RAG
if __name__ == "__main__":

    while True:

        query = input("\nAsk a question (type 'exit' to stop): ")

        if query.lower() == "exit":
            break

        answer, results = answer_question(query)

        if answer is None:
            print("\nNo sufficiently relevant information found.")
            continue

        print("\n" + "=" * 60)

        print("Answer:\n")
        print(answer)

        # Unique sources
        sources = []

        for result in results:
            if result["source"] not in sources:
                sources.append(result["source"])

        print("\nSources:\n")

        for source in sources:
            print(f"- {source}")