from app.agents.llm import ask_ace


def main() -> None:
    print("=" * 45)
    print("ACE AI - Identity & Prompt Check")
    print("=" * 45)

    response = ask_ace(
        "Who are you? Briefly explain what you can help me with."
    )

    print(response)

    print("=" * 45)
    print("ACE AI system prompt: OK")
    print("=" * 45)


if __name__ == "__main__":
    main()