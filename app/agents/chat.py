from app.agents.llm import ask_ace


def chat(message: str) -> str:
    """Process a user message through ACE AI."""

    cleaned_message = message.strip()

    if not cleaned_message:
        return "Please enter a message so I can help you."

    try:
        response = ask_ace(cleaned_message)
        return response

    except Exception:
        return (
            "I'm sorry, but I'm having trouble processing your request "
            "right now. Please try again."
        )