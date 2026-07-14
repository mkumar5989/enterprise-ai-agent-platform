from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Enterprise AI Agent Platform"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+asyncpg://agents:agents@localhost:5432/agents"
    redis_url: str = "redis://localhost:6379/0"
    llm_provider: str = "local"
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    memory_ttl_seconds: int = 3600
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
