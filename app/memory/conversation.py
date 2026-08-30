from app.memory.database import get_messages


def get_conversation_history(
    conversation_id: int,
) -> list[tuple[str, str]]:
    """Return conversation history in the format expected by the LLM."""

    messages = get_messages(conversation_id)

    history = []

    for message in messages:
        role = (
            "human"
            if message["role"] == "user"
            else "assistant"
        )

        history.append(
            (
                role,
                message["content"],
            )
        )

    return history


def get_recent_history(
    history: list[tuple[str, str]],
    limit: int = 10,
) -> list[tuple[str, str]]:
    """Return the most recent conversation messages."""

    return history[-limit:]