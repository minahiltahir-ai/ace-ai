from langchain_huggingface import HuggingFaceEmbeddings


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_embeddings() -> HuggingFaceEmbeddings:
    """Create and return the embedding model."""

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
    )