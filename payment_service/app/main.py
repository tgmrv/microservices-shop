from contextlib import asynccontextmanager

from typing import AsyncIterator, List
from fastapi import FastAPI, HTTPException, Request
from fastapi.params import Depends

from .config import settings
from .database import engine
from .rabbitmq import connect_rabbitmq, declare_payment_exchange
from .dependencies import get_payment_service
from .models import Base
from .schemas import PaymentReadSchema, PaymentCreateSchema
from .service import PaymentService


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    rabbitmq_connection = await connect_rabbitmq(url=settings.RABBITMQ_URL)
    channel = await rabbitmq_connection.channel()
    app.state.payment_exchange = await declare_payment_exchange(channel, settings.PAYMENT_EXCHANGE_NAME)

    try:
        yield
    finally:
        await rabbitmq_connection.close()


app = FastAPI(lifespan=lifespan)

@app.get("/payments", response_model=List[PaymentReadSchema])
async def get_payments(payment_service: PaymentService = Depends(get_payment_service)):
    return await payment_service.get_all()

@app.get("/payments/{payment_id}", response_model=PaymentReadSchema)
async def get_payment(payment_id, payment_service: PaymentService = Depends(get_payment_service)):
    result = await payment_service.get(payment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Payment not found")
    return result

@app.post("/payments", response_model=PaymentReadSchema)
async def create_payment(
        request: Request,
        payload: PaymentCreateSchema,
        payment_service: PaymentService = Depends(get_payment_service)
):
    payment = await payment_service.create(payload)

    result =  await payment_service.complete_payment(
        payment,
        exchange=request.app.state.payment_exchange
    )

    return result