import os

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "rag", "chroma_db")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

_vector_store = None  # lazy-loaded singleton so we don't reload the model every call


def _get_vector_store():
    global _vector_store

    if _vector_store is not None:
        return _vector_store

    if not os.path.exists(DB_DIR):
        return None

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    _vector_store = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings,
    )
    return _vector_store


def retrieve_context(query: str, k: int = 3) -> str:
    """
    Retrieve the top-k most relevant chunks from the travel knowledge base.

    Returns an empty string (never raises) if the vector store hasn't been
    built yet, so the rest of the pipeline keeps working without RAG context.
    """
    store = _get_vector_store()

    if store is None:
        return ""

    results = store.similarity_search(query, k=k)

    if not results:
        return ""

    formatted = []
    for doc in results:
        source = doc.metadata.get("source", "unknown")
        formatted.append(f"[Source: {source}]\n{doc.page_content}")

    return "\n\n".join(formatted)
