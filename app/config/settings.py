from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = "Enterprise Knowledge Assistant"
    app_version: str = "1.0.0"
    environment: str = "development"
    database_url: str = Field(default=...)
    secret_key: str = Field(default=...)
    access_token_expire_minutes: int = 30
    jwt_algorithm: str = "HS256"
    azure_openai_endpoint: str = Field(default=..., alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_key: str = Field(default=..., alias="AZURE_OPENAI_KEY")
    azure_openai_api_version: str = Field(default=..., alias="AZURE_OPENAI_API_VERSION")
    azure_openai_deployment: str = Field(default=..., alias="AZURE_OPENAI_DEPLOYMENT")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
    )

    langchain_tracing_v2: bool = True

    langchain_api_key: str | None = None

    langchain_project: str = (
        "enterprise-knowledge-assistant"
    )

    redis_url: str = "redis://localhost:6379"

settings = Settings()
