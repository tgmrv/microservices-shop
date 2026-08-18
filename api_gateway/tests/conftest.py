import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

os.environ["JWT_ALGORITHM"] = "HS256"

from api_gateway.app.main import app

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client