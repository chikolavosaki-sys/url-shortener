from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    database_url: str
    redis_url:    str
    base_url:     str = "http://localhost:8000"
    secret_key:   str = "change_me"
    short_code_length: int = 6

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

# One singleton — imported everywhere as: for later purpo
# from app.core.config import settings
settings = Settings()