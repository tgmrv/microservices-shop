from unittest.mock import AsyncMock, patch

import httpx
import pytest

from api_gateway.app.api_client import request_service


@pytest.mark.asyncio
async def test_request_service_success():
    response = httpx.Response(
        status_code=200,
        json={"id": "product-123"},
    )

    with patch("api_gateway.app.api_client.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.request = AsyncMock(
            return_value=response
        )

        result = await request_service(
            "GET",
            "http://catalog:8000/products/product-123",
        )

    assert result == {"id": "product-123"}