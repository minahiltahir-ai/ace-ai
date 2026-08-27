from app.agents.chat import chat


def main() -> None:
    print("=" * 45)
    print("ACE AI - Chat Engine Check")
    print("=" * 45)

    message = "What is artificial intelligence? Explain briefly."

    print(f"\nUser: {message}\n")

    response = chat(message)

    print(f"ACE AI: {response}")

    print("\n" + "=" * 45)
    print("Chat engine: OK")
    print("=" * 45)


if __name__ == "__main__":
    main()