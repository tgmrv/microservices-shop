from unittest.mock import patch, AsyncMock

import pytest

from api_gateway.app.auth import get_current_user
from api_gateway.app.main import app
from api_gateway.app.schemas import CurrentUserSchema


@pytest.mark.asyncio
async def test_get_me(client):
    user = CurrentUserSchema(
        id="user-123",
        email="test@example.com",
    )

    app.dependency_overrides[get_current_user] = lambda: user

    response = await client.get("/api/auth/me")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == user.model_dump(mode="json")


@pytest.mark.asyncio
async def test_get_products(client):
    products = [
        {
            "id": "product-123",
            "name": "Macbook",
            "price": 1400.0,
        }
    ]

    with patch(
        "api_gateway.app.api.routers.catalog.request_service",
        new_callable=AsyncMock,
    ) as mock_request:

        mock_request.return_value = products

        response = await client.get("/api/products")

    assert response.status_code == 200
    assert response.json() == products


@pytest.mark.asyncio
async def test_create_order(client):
    user = CurrentUserSchema(
        id="user-123",
        email="test@example.com",
    )

    order = {
        "id": "order-123",
        "user_id": "user-123",
        "status": "created",
        "total_price": 1400.0,
        "items": [
            {
                "product_id": "product-123",
                "product_name": "Macbook",
                "quantity": 1,
                "item_price": 1400.0,
            }
        ],
    }

    app.dependency_overrides[get_current_user] = lambda: user

    with patch(
        "api_gateway.app.api.routers.orders.request_service",
        new_callable=AsyncMock,
    ) as mock_request:

        mock_request.return_value = order

        response = await client.post(
            "/api/orders",
            json={
                "user_id": "fake-user",
                "items": [
                    {
                        "product_id": "product-123",
                        "quantity": 1,
                    }
                ],
            },
        )

    app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json() == order

    mock_request.assert_awaited_once_with(
        "POST",
        "http://order-service:8000/orders",
        json_body={
            "user_id": "user-123",
            "items": [
                {
                    "product_id": "product-123",
                    "quantity": 1,
                }
            ],
        },
    )