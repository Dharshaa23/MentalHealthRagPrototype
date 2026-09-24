# RAG Prototype

A Retrieval-Augmented Generation (RAG) prototype built to understand and implement the core components of a grounded LLM application.

## Current Features

- Document ingestion
- Text chunking
- Sentence Transformer embeddings
- FAISS vector search
- Similarity-based retrieval
- Relevance threshold filtering
- Groq LLM integration
- Grounded response generation
- Basic conversation memory
- Query rewriting
- Basic safety filtering
- Retrieval and generation evaluation
- LangChain-based RAG implementation

## Architecture

```text
User Query
    ↓
Query Processing
    ↓
Embedding Model
    ↓
FAISS Vector Store
    ↓
Similarity Retrieval
    ↓
Relevance Filtering
    ↓
Retrieved Context
    ↓
Groq LLM
    ↓
Grounded Response
