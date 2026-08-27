from config.settings import settings


def main() -> None:
    print("=" * 40)
    print("ACE AI - Configuration Check")
    print("=" * 40)

    print(f"App Name: {settings.app_name}")
    print(f"Environment: {settings.environment}")
    print(f"Debug Mode: {settings.debug}")
    print(f"Model: {settings.model_name}")
    print(f"LangSmith Project: {settings.langsmith_project}")

    print("=" * 40)
    print("Configuration loaded successfully.")
    print("Secrets are not displayed.")
    print("=" * 40)


if __name__ == "__main__":
    main()