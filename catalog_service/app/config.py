from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../../auth_service/.env", extra="ignore")

    DATABASE_URL: str = "postgresql+asyncpg://catalog:catalog@localhost:5433/catalog_db"

settings = Settings()