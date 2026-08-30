from collections.abc import Iterator

from langchain_ollama import ChatOllama

from app.agents.prompts import ACE_SYSTEM_PROMPT
from config.settings import settings


def get_llm() -> ChatOllama:
    """Create and return the ACE AI language model."""

    return ChatOllama(
        model=settings.model_name,
        temperature=0.7,
    )


def build_messages(
    message: str,
    history: list[tuple[str, str]] | None = None,
) -> list[tuple[str, str]]:
    """Build messages sent to the language model."""

    messages = [
        ("system", ACE_SYSTEM_PROMPT),
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