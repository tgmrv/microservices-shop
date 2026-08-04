import asyncio
from datetime import datetime, UTC
from uuid import uuid4

from aio_pika.abc import AbstractExchange
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .rabbitmq import rabbitmq_publish_event
from .schemas import PaymentCreateSchema, PaymentReadSchema
from .models import PaymentORM


class PaymentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payment_data: PaymentCreateSchema) -> PaymentORM:
        payment = PaymentORM(
            order_id=payment_data.order_id,
            status="created",
            amount=payment_data.amount,
        )
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)

        return payment

    async def get(self, payment_id: str):
        result = await self.db.get(PaymentORM, payment_id)
        return result

    async def get_all(self):
        result = await self.db.execute(select(PaymentORM))
        payments = result.scalars().all()
        return list(payments)

    async def complete_payment(
            self,
            payment: PaymentORM,
            exchange: AbstractExchange,
    ) -> PaymentReadSchema:
        await asyncio.sleep(3)

        payment.status = "completed"
        await self.db.commit()
        await self.db.refresh(payment)

        event = {
            "event_id": str(uuid4()),
            "created_at": datetime.now(UTC).isoformat(),
            "payment_id": payment.id,
            "order_id": payment.order_id,
            "amount": payment.amount,
            "status": "completed",
        }

        await rabbitmq_publish_event(exchange, settings.PAYMENT_COMPLETED_ROUTING_KEY, event)

        return PaymentReadSchema.model_validate(payment)
