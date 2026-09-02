from langchain_core.documents import Document

from app.rag.vectorstore import get_vectorstore


def retrieve_documents(
    query: str,
    k: int = 3,
) -> list[Document]:
    """Retrieve the most relevant document chunks."""

    cleaned_query = query.strip()

    if not cleaned_query:
        return []

    vectorstore = get_vectorstore()

    results = vectorstore._collection.query(
        query_texts=[cleaned_query],
        n_results=k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    documents = []

    result_documents = results.get("documents", [[]])[0]
    result_metadatas = results.get("metadatas", [[]])[0]

    for content, metadata in zip(
        result_documents,
        result_metadatas,
    ):
        if not content or not content.strip():
            continue

        documents.append(
            Document(
                page_content=content,
                metadata=metadata or {},
            )
        )

    return documents