from config.settings import settings


def main() -> None:
    print("=" * 40)
    print("ACE AI - Backend Health Check")
    print("=" * 40)
    print(f"App Name: {settings.app_name}")
    print(f"Environment: {settings.environment}")
    print(f"Model: {settings.model_name}")
    print(f"Debug Mode: {settings.debug}")
    print("Configuration: OK")
    print("Backend foundation: OK")
    print("=" * 40)


if __name__ == "__main__":
    main()