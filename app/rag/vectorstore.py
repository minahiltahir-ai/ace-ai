from pathlib import Path

from langchain_chroma import Chroma

from app.rag.embeddings import get_embeddings


PROJECT_ROOT = Path(__file__).resolve().parents[2]

VECTORSTORE_DIR = (
    PROJECT_ROOT
    / "data"
    / "vectorstore"
)

COLLECTION_NAME = "ace_documents"


def get_vectorstore() -> Chroma:
    """Create or load the ACE AI Chroma vector store."""

    embeddings = get_embeddings()

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(VECTORSTORE_DIR),
    )