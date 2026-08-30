from collections.abc import Iterator

from app.agents.llm import stream_ace
from app.memory.conversation import get_recent_history
from app.rag.pipeline import retrieve_context


def _build_rag_message(
    message: str,
    context: str,
) -> str:
    """Build the prompt using retrieved document context."""

    if not context.strip():
        return message

    return f"""
Use the following document context to answer the user's question.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{message}

Instructions:
- Answer using the document context when the question is about the document.
- Do not invent information.
- Do not expand acronyms unless the document defines them.
- If the answer is not present in the document context, say that it is
  not mentioned in the document.
- Answer clearly and concisely.
""".strip()


def chat(
    message: str,
    history: list[tuple[str, str]] | None = None,
) -> str:
    """Process a user message through ACE AI with RAG context."""

    cleaned_message = message.strip()

    if not cleaned_message:
        return "Please enter a message so I can help you."

    try:
        recent_history = get_recent_history(
            history or []
        )

        context = retrieve_context(
            cleaned_message
        )

        rag_message = _build_rag_message(
            message=cleaned_message,
            context=context,
        )

        response_parts = []

        for chunk in stream_ace(
            message=rag_message,
            history=recent_history,
        ):
            response_parts.append(chunk)

        return "".join(response_parts)

    except Exception as error:
        print(f"ACE CHAT ERROR: {error}")

        return (
            "I'm sorry, but I'm having trouble processing "
            "your request right now. Please try again."
        )


def chat_stream(
    message: str,
    history: list[tuple[str, str]] | None = None,
) -> Iterator[str]:
    """Stream ACE AI response chunk by chunk with RAG context."""

    cleaned_message = message.strip()

    if not cleaned_message:
        yield "Please enter a message so I can help you."
        return

    try:
        recent_history = get_recent_history(
            history or []
        )

        context = retrieve_context(
            cleaned_message
        )

        rag_message = _build_rag_message(
            message=cleaned_message,
            context=context,
        )

        yield from stream_ace(
            message=rag_message,
            history=recent_history,
        )

    except Exception as error:
        print(f"ACE CHAT STREAM ERROR: {error}")

        yield (
            "I'm sorry, but I'm having trouble processing "
            "your request right now. Please try again."
        )