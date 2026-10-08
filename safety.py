from semantic_safety import semantic_safety_score


NORMAL = "normal"
SENSITIVE = "sensitive"

SEMANTIC_THRESHOLD = 0.60


def keyword_safety_check(query):
    """
    Detect explicit safety-sensitive wording.

    This is a simple first-pass detector and is not
    a clinical risk assessment system.
    """

    query_lower = query.lower()

    sensitive_terms = [
        "suicide",
        "suicidal",
        "kill myself",
        "end my life",
        "self harm",
        "self-harm",
        "selfharm",
        "hurt myself",
        "want to die",
        "don't want to live",
        "do not want to live",
    ]

    for term in sensitive_terms:
        if term in query_lower:
            return True

    return False


def check_safety(query):
    """
    Combined safety detection.

    Layer 1:
        Keyword detection

    Layer 2:
        Semantic similarity detection

    If either layer detects safety-sensitive intent,
    return SENSITIVE.
    """

    # Layer 1: explicit keyword detection
    if keyword_safety_check(query):
        return SENSITIVE

    # Layer 2: semantic detection
    semantic_score = semantic_safety_score(query)

    if semantic_score >= SEMANTIC_THRESHOLD:
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