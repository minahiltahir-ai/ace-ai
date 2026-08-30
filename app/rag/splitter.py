from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    documents: list[Document],
) -> list[Document]:
    """Split documents into smaller chunks for RAG."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )

    return splitter.split_documents(documents)