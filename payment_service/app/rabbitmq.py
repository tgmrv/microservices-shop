import json

import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractChannel, AbstractExchange


async def connect_rabbitmq(url: str) -> AbstractRobustConnection:
    return await aio_pika.connect_robust(url)

async def declare_payment_exchange(channel: AbstractChannel, exchange_name: str):
    return await channel.declare_exchange(exchange_name)

async def publish_event(exchange: AbstractExchange, routing_key: str, body: dict):
    message = aio_pika.Message(json.dumps(body).encode())
    await exchange.publish(message, routing_key)
