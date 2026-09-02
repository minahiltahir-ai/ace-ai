from collections.abc import Iterator

from app.agents.llm import stream_ace
from app.memory.conversation import get_recent_history
from app.rag.pipeline import retrieve_context


DOCUMENT_NOT_FOUND = (
    "I couldn't find this information in the provided documents."
)


def _looks_like_document_question(message: str) -> bool:
    """Detect questions that explicitly ask about document content."""

    keywords = (
        "according to the document",
        "according to the documents",
        "in the document",
        "in the documents",
        "from the document",
        "from the documents",
        "what does the document say",
        "what do the documents say",
    )

    cleaned = message.lower()

    return any(
        keyword in cleaned
        for keyword in keywords
    )


def _build_rag_message(
    message: str,
    context: str,
) -> str:
    """Build a strictly document-grounded prompt."""

    return f"""
Answer the user's question using ONLY the document context below.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{message}

RULES:
- Use only information explicitly present in the document context.
- Do not use general knowledge.
- Do not guess or infer missing information.
- Do not invent examples, facts, explanations, or applications.
- Preserve numbers, hexadecimal values, names, and technical details exactly as written.
- If the context contains an example, reproduce its values exactly.
- Answer only what is directly supported by the document context.
- Give a concise and direct answer.
""".strip()


def chat(
    message: str,
    history: list[tuple[str, str]] | None = None,
) -> tuple[str, list[dict]]:
    """Process a user message and return the answer with sources."""

    cleaned_message = message.strip()

    if not cleaned_message:
        return (
            "Please enter a message so I can help you.",
            [],
        )

    try:
        recent_history = get_recent_history(
            history or []
        )

        sources = []

        # -----------------------------------------------------
        # DOCUMENT QUESTION
        # -----------------------------------------------------

        if _looks_like_document_question(
            cleaned_message
        ):
            context, sources = retrieve_context(
                query=cleaned_message,
                k=3,
            )

            if not context.strip():
                return (
                    DOCUMENT_NOT_FOUND,
                    [],
                )

            prompt = _build_rag_message(
                message=cleaned_message,
                context=context,
            )

        # -----------------------------------------------------
        # NORMAL / MEMORY QUESTION
        # -----------------------------------------------------

        else:
            prompt = cleaned_message

        response_parts = []

        for chunk in stream_ace(
            message=prompt,
            history=recent_history,
        ):
            response_parts.append(chunk)

        response = "".join(response_parts).strip()

        return response, sources

    except Exception as error:
        print(f"ACE CHAT ERROR: {error}")

        return (
            "I'm sorry, but I'm having trouble processing "
            "your request right now. Please try again.",
            [],
        )


def chat_stream(
    message: str,
    history: list[tuple[str, str]] | None = None,
) -> tuple[Iterator[str], list[dict]]:
    """Stream the ACE AI response and return RAG sources."""

    cleaned_message = message.strip()

    if not cleaned_message:
        return (
            iter(["Please enter a message so I can help you."]),
            [],
        )

    try:
        recent_history = get_recent_history(
            history or []
        )

        sources = []

        # -----------------------------------------------------
        # DOCUMENT QUESTION
        # -----------------------------------------------------

        if _looks_like_document_question(
            cleaned_message
        ):
            context, sources = retrieve_context(
                query=cleaned_message,
                k=3,
            )

            if not context.strip():
                return (
                    iter([DOCUMENT_NOT_FOUND]),
                    [],
                )

            prompt = _build_rag_message(
                message=cleaned_message,
                context=context,
            )

        # -----------------------------------------------------
        # NORMAL / MEMORY QUESTION
        # -----------------------------------------------------

        else:
            prompt = cleaned_message

        response_stream = stream_ace(
            message=prompt,
            history=recent_history,
        )

        return response_stream, sources

    except Exception as error:
        print(f"ACE CHAT STREAM ERROR: {error}")

        return (
            iter([
                "I'm sorry, but I'm having trouble processing "
                "your request right now. Please try again."
            ]),
            [],
        )


def get_chat_response(
    message: str,
    history: list[tuple[str, str]] | None = None,
) -> tuple[str, list[dict]]:
    """
    Return an ACE response together with structured RAG sources.

    This helper is intended for UI/API layers that need both
    the generated answer and its document citations.
    """

    return chat(
        message=message,
        history=history,
    )