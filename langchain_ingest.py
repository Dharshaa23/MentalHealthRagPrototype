from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


DATA_DIR = Path("data/knowledge_base")


def load_documents():

    documents = []

    for file_path in DATA_DIR.glob("*.txt"):

        text = file_path.read_text(encoding="utf-8")

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file_path.name
                }
            )
        )

    return documents


documents = load_documents()

print(f"Documents loaded: {len(documents)}")


# Split documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print(f"Chunks created: {len(chunks)}")


# Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Create FAISS vector store
vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)


# Save vector store
vectorstore.save_local("langchain_faiss")

print("LangChain FAISS vector store created successfully.")