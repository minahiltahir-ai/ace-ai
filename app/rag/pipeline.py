from app.rag.retriever import retrieve_documents


def retrieve_context(
    query: str,
    k: int = 4,
) -> str:
    """Retrieve relevant document context for a query."""

    documents = retrieve_documents(
        query=query,
        k=k,
    )

    if not documents:
        return ""

    return "\n\n".join(
        document.page_content
        for document in documents
        if document.page_content.strip()
    )