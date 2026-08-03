import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("ORDER_DATABASE_URL")
    CATALOG_SERVICE_URL: str = os.getenv("CATALOG_SERVICE_URL")
    PAYMENT_SERVICE_URL: str = os.getenv("PAYMENT_SERVICE_URL")
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL")
    PAYMENT_COMPLETED_ROUTING_KEY: str = "payment.completed"
    PAYMENT_EXCHANGE_NAME: str = "payment.events"
    PAYMENT_QUEUE_NAME: str = "payment.results"


settings = Settings()