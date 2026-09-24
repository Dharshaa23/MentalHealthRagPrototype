from safety import check_safety, NORMAL, SENSITIVE


test_queries = [
    "What is anxiety?",
    "What are common symptoms of stress?",
    "What is emotional wellbeing?",
    "I want to kill myself",
    "I want to hurt myself",
    "I don't want to live anymore",
]


for query in test_queries:

    result = check_safety(query)

    print(f"Query: {query}")
    print(f"Category: {result}")
    print("-" * 50)