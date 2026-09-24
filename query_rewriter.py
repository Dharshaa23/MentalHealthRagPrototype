from model import generate_answer


def rewrite_query(query, history):

    if not history:
        return query

    history_text = ""

    for turn in history:
        history_text += f"User: {turn['user']}\n"
        history_text += f"Assistant: {turn['assistant']}\n\n"

    prompt = f"""
You are a query rewriting component for a Retrieval-Augmented Generation system.

Your task is to rewrite the user's latest question into a standalone
search query that can be understood without the conversation history.

Rules:
1. Resolve references such as "it", "its", "they", "them", "this", and "that"
   using the conversation history.
2. Preserve the original meaning of the user's question.
3. Do not answer the question.
4. Do not add information that is not supported by the conversation.
5. Return ONLY the rewritten search query.
6. If the question is already standalone, return it unchanged.

Conversation history:
{history_text}

Latest user question:
{query}

Standalone search query:
"""

    rewritten_query = generate_answer(prompt)

    return rewritten_query.strip()