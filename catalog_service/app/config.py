import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("CATALOG_DATABASE_URL")

settings = Settings()