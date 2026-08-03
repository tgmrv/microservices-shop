from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../../auth_service/.env", extra="ignore")

    DATABASE_URL: str = "postgresql+asyncpg://order:order@localhost:5434/order_db"
    CATALOG_SERVICE_URL: str = "http://127.0.0.1:8001"
    PAYMENT_SERVICE_URL: str = "http://127.0.0.1:8003"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672"
    PAYMENT_COMPLETED_ROUTING_KEY: str = "payment.completed"
    PAYMENT_EXCHANGE_NAME: str = "payment.events"
    PAYMENT_QUEUE_NAME: str = "payment.results"

settings = Settings()