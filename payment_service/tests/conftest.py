import os
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

os.environ["CATALOG_SERVICE_URL"] = "http://catalog:8000"
os.environ["PAYMENT_SERVICE_URL"] = "http://payment:8000"
os.environ["RABBITMQ_URL"] = "amqp://guest:guest@localhost:5672/"
os.environ["PAYMENT_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from payment_service.app.database import get_db
from payment_service.app.main import app
from payment_service.app.models import Base
from payment_service.app.dependencies import get_payment_service
from payment_service.app.service import PaymentService

engine = create_async_engine(os.environ["PAYMENT_DATABASE_URL"])
TestingSessionLocal = async_sessionmaker(bind=engine)


async def get_test_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = get_test_db


@pytest_asyncio.fixture
async def test_db_session():
    async with TestingSessionLocal() as session:
        yield session


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


@pytest.fixture
def payment_service(test_db_session):
    return PaymentService(db=test_db_session)


@pytest.fixture
def payment_exchange():
    exchange = AsyncMock()
    app.state.payment_exchange = exchange
    return exchange


@pytest.fixture
def override_payment_service():
    mock_payment = AsyncMock()
    app.dependency_overrides[get_payment_service] = lambda: mock_payment

    yield mock_payment

    app.dependency_overrides.clear()