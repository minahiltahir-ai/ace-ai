from langchain_ollama import ChatOllama

from app.agents.prompts import ACE_SYSTEM_PROMPT
from config.settings import settings


def get_llm() -> ChatOllama:
    """Create and return the local ACE AI language model."""

    return ChatOllama(
        model=settings.model_name,
        temperature=0.7,
    )


def ask_ace(message: str) -> str:
    """Send a user message to ACE AI and return its response."""

    llm = get_llm()

    messages = [
        ("system", ACE_SYSTEM_PROMPT),
        ("human", message),
    ]

    response = llm.invoke(messages)

    return response.content