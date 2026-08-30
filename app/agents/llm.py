from collections.abc import Iterator

from langchain_ollama import ChatOllama

from app.agents.prompts import ACE_SYSTEM_PROMPT
from app.rag.pipeline import retrieve_context
from config.settings import settings


def get_llm() -> ChatOllama:
    """Create and return the ACE AI language model."""

    return ChatOllama(
        model=settings.model_name,
        temperature=0.1,
    )


def build_messages(
    message: str,
    history: list[tuple[str, str]] | None = None,
) -> list[tuple[str, str]]:
    """Build messages sent to the language model."""

    context = retrieve_context(
        query=message,
        k=3,
    )

    rag_instruction = f"""
DOCUMENT CONTEXT:
{context if context.strip() else "[NO RELEVANT DOCUMENT CONTEXT FOUND]"}

STRICT DOCUMENT-GROUNDED RULES:
- Answer the user's question ONLY using the DOCUMENT CONTEXT above.
- Do NOT use your general knowledge to answer.
- Do NOT infer, guess, or invent information.
- If the answer is not explicitly supported by the DOCUMENT CONTEXT, say:
  "I couldn't find this information in the provided documents."
- Never treat the user's question itself as evidence.
- Never assume that an unrelated retrieved passage answers the question.
"""

    messages = [
        (
            "system",
            ACE_SYSTEM_PROMPT + "\n\n" + rag_instruction,
        )
    ]

    if history:
        messages.extend(history)

    messages.append(
        ("human", message)
    )

    return messages


def ask_ace(
    message: str,
    history: list[tuple[str, str]] | None = None,
) -> str:
    """Send a message and return the complete response."""

    llm = get_llm()

    messages = build_messages(
        message=message,
        history=history,
    )

    response = llm.invoke(messages)

    return response.content


def stream_ace(
    message: str,
    history: list[tuple[str, str]] | None = None,
) -> Iterator[str]:
    """Stream the ACE AI response chunk by chunk."""

    llm = get_llm()

    messages = build_messages(
        message=message,
        history=history,
    )

    for chunk in llm.stream(messages):

        if chunk.content:
            yield chunk.content