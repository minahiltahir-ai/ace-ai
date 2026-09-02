from app.rag.retriever import retrieve_documents


def retrieve_context(
    query: str,
    k: int = 3,
) -> tuple[str, list[dict]]:
    """Retrieve relevant document chunks and structured source metadata."""

    documents = retrieve_documents(
        query=query,
        k=k,
    )

    if not documents:
        return "", []

    context_parts = []
    sources = []

    for document in documents:
        content = document.page_content.strip()

        if not content:
            continue

        metadata = document.metadata

        source = metadata.get(
            "source",
            "Unknown source",
        )

        page_label = metadata.get("page_label")

        page = metadata.get("page")

        if page_label is not None:
            page_number = str(page_label)
        elif page is not None:
            page_number = str(page + 1)
        else:
            page_number = None

        if page_number:
            source_label = f"{source} | Page {page_number}"
        else:
            source_label = source

        context_parts.append(
            f"[Source: {source_label}]\n"
            f"{content}"
        )

        source_info = {
            "source": source,
            "page": page_number,
            "label": source_label,
        }

        if source_info not in sources:
            sources.append(source_info)

    return "\n\n".join(context_parts), sources