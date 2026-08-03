from contextlib import asynccontextmanager

from typing import AsyncIterator

from fastapi import FastAPI, HTTPException, status
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import engine, get_db
from .models import Base, UserORM
from .schemas import TokenResponseSchema, UserRegisterSchema, UserReadSchema, UserLoginSchema
from .security import verify_password, create_access_token, hash_password


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/register", response_model=TokenResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegisterSchema, db: AsyncSession = Depends(get_db)):
    existing = await db.scalar(select(UserORM).where(UserORM.email == payload.email))
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = UserORM(email=payload.email, hashed_password=await hash_password(payload.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)

    access_token = await create_access_token(user)
    return TokenResponseSchema(access_token=access_token, user=UserReadSchema.model_validate(user))


@app.post("/login", response_model=TokenResponseSchema)
async def login(payload: UserLoginSchema, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(UserORM).where(UserORM.email == payload.email))

    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = await create_access_token(user)
    return TokenResponseSchema(access_token=access_token, user=UserReadSchema.model_validate(user))
