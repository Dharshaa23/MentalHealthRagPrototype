from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

DATA_DIR = Path("data/knowledge_base")


def load_documents():
    documents = []

    for file_path in DATA_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "source": file_path.name,
            "text": text
        })

    return documents


def chunk_text(text):
    paragraphs = text.split("\n\n")

    chunks = []

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # Ignore standalone headings
        if paragraph.isupper() and len(paragraph.split()) <= 5:
            continue

        chunks.append(paragraph)

    return chunks

# Load documents
documents = load_documents()

chunks = []
metadata = []

for document in documents:

    document_chunks = chunk_text(document["text"])

    for chunk_id, chunk in enumerate(document_chunks):

        chunks.append(chunk)

        metadata.append({
            "source": document["source"],
            "chunk_id": chunk_id,
            "text": chunk
        })


print(f"Documents loaded: {len(documents)}")
print(f"Chunks created: {len(chunks)}")


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Generate embeddings
embeddings = model.encode(
    chunks,
    convert_to_numpy=True
)

print("Embedding shape:", embeddings.shape)


# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    embeddings.astype("float32")
)

print("Vectors stored:", index.ntotal)


# Save index and metadata
faiss.write_index(
    index,
    "knowledge_base.index"
)

np.save(
    "metadata.npy",
    np.array(metadata, dtype=object)
)

print("RAG knowledge base created successfully.")