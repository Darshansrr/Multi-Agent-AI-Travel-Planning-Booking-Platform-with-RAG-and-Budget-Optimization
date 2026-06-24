

What it does:
1. Loads every .md / .txt file from rag/docs/
2. Splits them into overlapping chunks
3. Embeds the chunks with a free local HuggingFace embedding model
   (no OpenAI key needed)
4. Persists everything into a local Chroma DB at rag/chroma_db/


import os
import glob

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def load_documents():
    """Read every .md/.txt file in rag/docs/ into (text, source) pairs."""
    texts = []
    paths = glob.glob(os.path.join(DOCS_DIR, "*.md")) + glob.glob(
        os.path.join(DOCS_DIR, "*.txt")
    )

    if not paths:
        raise FileNotFoundError(
            f"No .md or .txt files found in {DOCS_DIR}. "
            "Add your visa/city-guide/tips documents there first."
        )

    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            texts.append({"content": f.read(), "source": os.path.basename(path)})

    return texts


def build_vector_store():
    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
    )

    chunks = []
    metadatas = []

    for doc in docs:
        split_texts = splitter.split_text(doc["content"])
        for chunk in split_texts:
            chunks.append(chunk)
            metadatas.append({"source": doc["source"]})

    print(f"Loaded {len(docs)} document(s), split into {len(chunks)} chunks.")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    vector_store = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=DB_DIR,
    )

    print(f"Vector store built and saved to: {DB_DIR}")
    return vector_store


if __name__ == "__main__":
    build_vector_store()