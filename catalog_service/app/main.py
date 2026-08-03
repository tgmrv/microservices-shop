from contextlib import asynccontextmanager

from typing import AsyncIterator, List
from fastapi import FastAPI, HTTPException, status
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import engine, get_db
from .models import Base, ProductORM
from .schemas import ProductCreateSchema, ProductReadSchema


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/products", response_model=List[ProductReadSchema])
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductORM).order_by(ProductORM.name))
    return list(result.scalars().all())

@app.get("/products/{product_id}", response_model=ProductReadSchema)
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductORM).where(ProductORM.id == product_id))
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

@app.post("/products", response_model=ProductReadSchema, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreateSchema, db: AsyncSession = Depends(get_db)):
    product = ProductORM(**payload.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductORM).where(ProductORM.id == product_id))
    product = result.scalar_one_or_none()
    await db.delete(product)
    await db.commit()

