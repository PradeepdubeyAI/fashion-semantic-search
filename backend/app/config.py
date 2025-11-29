"""Basic configuration helpers for the FastAPI backend."""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Dress Search API"
    frontend_origin: list = ["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"]

    class Config:
        env_prefix = "DRESS_SEARCH_"
        env_file = ".env"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()
