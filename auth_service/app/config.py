import os

from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET: SecretStr = SecretStr(os.getenv("JWT_SECRET"))
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_LIFETIME_SEC: int = 900

settings = Settings()