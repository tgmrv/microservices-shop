import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("PAYMENT_DATABASE_URL")
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL")
    PAYMENT_COMPLETED_ROUTING_KEY: str = "payment.completed"
    PAYMENT_EXCHANGE_NAME: str = "payment.events"

settings = Settings()