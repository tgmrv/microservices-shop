import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

os.environ["AUTH_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["JWT_SECRET"] = "test_ultra_jwt_secret_coding_key"

from auth_service.app.database import get_db
from auth_service.app.main import app
from auth_service.app.models import Base


engine = create_async_engine(os.environ["AUTH_DATABASE_URL"])
TestingSessionLocal = async_sessionmaker(bind=engine)

async def get_test_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = get_test_db

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client