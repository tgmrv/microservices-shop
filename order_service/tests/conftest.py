import os

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

os.environ["CATALOG_SERVICE_URL"] = "http://catalog:8000"
os.environ["PAYMENT_SERVICE_URL"] = "http://payment:8000"
os.environ["RABBITMQ_URL"] = "amqp://guest:guest@localhost:5672/"
os.environ["ORDER_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from order_service.app.database import get_db
from order_service.app.main import app
from order_service.app.models import Base
from order_service.app.api_clients import CatalogClient, PaymentClient
from order_service.app.service import OrderService


engine = create_async_engine(os.environ["ORDER_DATABASE_URL"])
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


@pytest.fixture
def mock_catalog():
    mock = AsyncMock(spec=CatalogClient)
    mock.get_product.return_value = {
            "id": "product-123",
            "name": "Macbook Pro",
            "price": 1400.0,
            "category": "Electronics"
        }
    return mock

@pytest.fixture
def mock_payment():
    mock = AsyncMock(spec=PaymentClient)
    mock.create_payment.return_value = {"id": "pay-123", "status": "completed"}
    return mock

@pytest.fixture
def order_service(mock_catalog, mock_payment, test_db_session: AsyncSession):
    return OrderService(
        db=test_db_session,
        catalog_client=mock_catalog,
        payment_client=mock_payment
    )