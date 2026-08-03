from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../../auth_service/.env", extra="ignore")

    DATABASE_URL: str = "postgresql+asyncpg://payment:payment@localhost:5435/payment_db"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672"
    PAYMENT_COMPLETED_ROUTING_KEY: str = "payment.completed"
    PAYMENT_EXCHANGE_NAME: str = "payment.events"

settings = Settings()