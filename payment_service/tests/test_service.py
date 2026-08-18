from unittest.mock import patch, AsyncMock

import pytest

from payment_service.app.models import PaymentORM
from payment_service.app.schemas import PaymentCreateSchema


@pytest.mark.asyncio
async def test_create_payment(payment_service):
    payment_data = PaymentCreateSchema(
        order_id="order-123",
        amount=1200.0,
    )

    payment = await payment_service.create(payment_data)

    assert payment.order_id == "order-123"
    assert payment.amount == 1200.0
    assert payment.status == "created"


@pytest.mark.asyncio
async def test_get_payment(payment_service, test_db_session):
    payment = PaymentORM(
        id="payment-123",
        order_id="order-123",
        status="created",
        amount=1200.0,
    )

    test_db_session.add(payment)
    await test_db_session.commit()

    result = await payment_service.get("payment-123")

    assert result is not None
    assert result.id == "payment-123"
    assert result.order_id == "order-123"


@pytest.mark.asyncio
async def test_complete_payment(payment_service, test_db_session):
    payment = PaymentORM(
        id="payment-123",
        order_id="order-123",
        status="created",
        amount=1200.0,
    )

    test_db_session.add(payment)
    await test_db_session.commit()

    exchange = AsyncMock()

    with patch(
        "payment_service.app.service.asyncio.sleep",
        new_callable=AsyncMock
    ), patch(
        "payment_service.app.service.rabbitmq_publish_event",
        new_callable=AsyncMock
    ) as mock_publish:

        result = await payment_service.complete_payment(payment, exchange)

    assert result.status == "completed"
    assert payment.status == "completed"

    mock_publish.assert_awaited_once()