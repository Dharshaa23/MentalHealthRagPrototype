# safety.py

# Simple prototype safety categories
NORMAL = "normal"
SENSITIVE = "sensitive"


def check_safety(query):
    """
    Classify a user query for the prototype safety layer.

    This is intentionally conservative and keyword-based.
    It is NOT a clinical risk assessment system.
    """

    query_lower = query.lower()

    sensitive_terms = [
        "suicide",
        "kill myself",
        "end my life",
        "self harm",
        "self-harm",
        "hurt myself",
        "want to die",
        "don't want to live",
        "do not want to live",
    ]

    for term in sensitive_terms:
        if term in query_lower:
            return SENSITIVE

    return NORMAL


def get_safe_response():
    """
    Return a supportive response for safety-sensitive queries.
    """

    return (
        "I'm sorry you're dealing with something this difficult. "
        "I can't provide instructions or detailed information about "
        "self-harm or suicide. Please reach out to a trusted adult, "
        "parent/guardian, teacher, counselor, or mental-health professional "
        "who can support you directly. If you feel you may be in immediate "
        "danger, contact your local emergency service or seek immediate "
        "help from a trusted person nearby."
    )