from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ACE AI"
    environment: str = "development"
    debug: bool = True

    model_name: str = "llama3.2:1b"

    langsmith_tracing: bool = False
    langsmith_project: str = "ace-ai"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()