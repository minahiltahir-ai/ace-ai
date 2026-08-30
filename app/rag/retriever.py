from langchain_core.documents import Document

from app.rag.vectorstore import get_vectorstore


def retrieve_documents(
    query: str,
    k: int = 4,
) -> list[Document]:
    """Retrieve the most relevant document chunks."""

    cleaned_query = query.strip()

    if not cleaned_query:
        return []

    vectorstore = get_vectorstore()

    return vectorstore.similarity_search(
        cleaned_query,
        k=k,
    )