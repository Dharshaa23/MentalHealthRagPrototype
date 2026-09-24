import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("knowledge_base.index")

# Load metadata
metadata = np.load(
    "metadata.npy",
    allow_pickle=True
)


def retrieve(query, k=3, threshold=1.0):

    # Convert query into embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = query_embedding.astype("float32")

    # Search FAISS
    distances, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for distance, index_id in zip(
        distances[0],
        indices[0]
    ):

        if distance > threshold:
            continue

        results.append({
            "source": metadata[index_id]["source"],
            "text": metadata[index_id]["text"],
            "distance": float(distance)
        })

    return results