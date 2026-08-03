import os

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET: SecretStr = SecretStr(os.getenv("JWT_SECRET"))
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    CORS_ORIGINS: list[str] = Field(default_factory=lambda: ["*"])

    CATALOG_SERVICE_URL: str = "http://catalog-service:8000"
    ORDER_SERVICE_URL: str = "http://order-service:8000"
    AUTH_SERVICE_URL: str = "http://auth-service:8000"

settings = Settings()