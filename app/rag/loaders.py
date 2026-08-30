from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
}


def load_documents(
    documents_dir: str | Path,
) -> list:
    """Load supported documents from the documents directory."""

    documents_path = Path(documents_dir)

    if not documents_path.exists():
        return []

    documents = []

    for file_path in documents_path.rglob("*"):

        if not file_path.is_file():
            continue

        suffix = file_path.suffix.lower()

        if suffix == ".pdf":

            loader = PyPDFLoader(
                str(file_path)
            )

            documents.extend(
                loader.load()
            )

        elif suffix == ".txt":

            loader = TextLoader(
                str(file_path),
                encoding="utf-8",
            )

            documents.extend(
                loader.load()
            )

    return documents