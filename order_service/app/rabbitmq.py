import json
import logging

import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractIncomingMessage

from .config import settings
from .database import AsyncSessionLocal
from .models import OrderORM

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


async def connect_rabbitmq() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.RABBITMQ_URL)


async def handle_payment_events(message: AbstractIncomingMessage):
    async with message.process():
        logger.info(f"Order consumer started")
        try:

            body = message.body.decode("utf-8")
            logger.info(f"Received message: {body}")

            event = json.loads(body)
            order_id = event.get("order_id")

            if order_id is None:
                logger.error(f"Invalid event: missing order_id")
                return

            async with AsyncSessionLocal() as session:
                order = await session.get(OrderORM, order_id)

                if order is None:
                    logger.warning(f"Order {order_id} not found in database")
                    return

                if order.status == "paid":
                    logger.info(f"Order {order_id} already paid")
                    return

                order.status = "paid"
                await session.commit()
                logger.info(f"Order {order_id} successfully paid")

        except Exception as e:
            logger.exception(f"Failed to process payment event: {e}")


async def start_payments_consume(connection: AbstractRobustConnection):
    channel = await connection.channel()
    payment_exchange = await channel.declare_exchange(settings.PAYMENT_EXCHANGE_NAME)
    payment_queue = await channel.declare_queue(settings.PAYMENT_QUEUE_NAME)

    await payment_queue.bind(payment_exchange, routing_key=settings.PAYMENT_COMPLETED_ROUTING_KEY)
    await payment_queue.consume(handle_payment_events)
