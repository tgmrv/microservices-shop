from contextlib import asynccontextmanager

from typing import AsyncIterator, List
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends

from .database import engine
from .dependencies import get_order_service
from .models import Base
from .rabbitmq import connect_rabbitmq, start_payments_consume
from .service import OrderService
from .schemas import OrderReadSchema, OrderCreateSchema


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    connection = await connect_rabbitmq()
    await start_payments_consume(connection)

    try:
        yield
    finally:
        await connection.close()

app = FastAPI(lifespan=lifespan)

@app.get("/orders", response_model=List[OrderReadSchema])
async def get_orders(order_service: OrderService = Depends(get_order_service)):
    return await order_service.get_all()

@app.get("/orders/{order_id}", response_model=OrderReadSchema)
async def get_order(order_id, order_service: OrderService = Depends(get_order_service)):
    result = await order_service.get(order_id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return result

@app.post("/orders", response_model=OrderReadSchema)
async def create_order(payload: OrderCreateSchema, order_service: OrderService = Depends(get_order_service)):
    return await order_service.create(payload)

