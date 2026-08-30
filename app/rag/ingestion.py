from pathlib import Path

from app.rag.loaders import load_documents
from app.rag.splitter import split_documents
from app.rag.vectorstore import get_vectorstore


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOCUMENTS_DIR = (
    PROJECT_ROOT
    / "data"
    / "documents"
)


def ingest_documents() -> int:
    """Load, split, and store documents in the vector database."""

    documents = load_documents(
        DOCUMENTS_DIR
    )

    if not documents:
        return 0

    chunks = split_documents(
        documents
    )

    if not chunks:
        return 0

    vectorstore = get_vectorstore()

    vectorstore.add_documents(
        chunks
    )

    return len(chunks)