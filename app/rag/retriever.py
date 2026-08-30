from langchain_core.documents import Document

from app.rag.vectorstore import get_vectorstore


def retrieve_documents(
    query: str,
    k: int = 3,
    score_threshold: float = 0.7,
) -> list[Document]:
    """Retrieve relevant document chunks using similarity scores."""

    cleaned_query = query.strip()

    if not cleaned_query:
        return []

    vectorstore = get_vectorstore()

    results = vectorstore.similarity_search_with_score(
        cleaned_query,
        k=k,
    )

    documents = []

    for document, score in results:
        if score <= score_threshold:
            documents.append(document)

    return documents