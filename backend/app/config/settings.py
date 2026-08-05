from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Lifeline Backend"
    ENVIRONMENT: str = "development"

    SUPABASE_URL: str
    SUPABASE_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    LOG_LEVEL: str = "INFO"

    GEMINI_API_KEY: str
    OPENROUTER_API_KEY: str

    GROQ_API_KEY: str
    AI_PROVIDER: str = "groq"
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
