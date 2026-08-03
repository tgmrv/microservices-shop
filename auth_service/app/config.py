import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("AUTH_DATABASE_URL")
    JWT_SECRET: SecretStr = SecretStr(os.getenv("JWT_SECRET"))
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_LIFETIME_SEC: int = 900

settings = Settings()