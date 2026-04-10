# Pydantic Settings — loads all environment variables from .env with type validation
# Expected settings:
#   DATABASE_URL: str
#   SECRET_KEY: str
#   ALGORITHM: str = "HS256"
#   ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
#   REFRESH_TOKEN_EXPIRE_DAYS: int = 7
#   MISTRAL_API_KEY: str
#   MISTRAL_MODEL: str = "mistral-large-latest"
#   APP_ENV: str = "development"
#   CLOUDINARY_CLOUD_NAME: str
#   CLOUDINARY_API_KEY: str
#   CLOUDINARY_API_SECRET: str
# app/core/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "development"
    
    DATABASE_URL: str
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    MISTRAL_API_KEY: str
    MISTRAL_MODEL: str = "mistral-large-latest"
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str = ""

    ELEVENLABS_API_KEY: str = ""
    ELEVENLABS_VOICE_ID: str = ""
    GROQ_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
