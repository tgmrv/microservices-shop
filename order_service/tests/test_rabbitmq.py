import pytest

from order_service.app.models import OrderORM
from order_service.app.rabbitmq import process_payment_event


@pytest.mark.asyncio
async def test_process_payment_event(test_db_session):
    order = OrderORM(
        id="order-123",
        user_id="user-123",
        status="created",
        total_price=1200.0
    )
    test_db_session.add(order)
    await test_db_session.commit()

    event = {
        "event_id": "event-123",
        "payment_id": "pay-123",
        "order_id": "order-123",
        "amount": 1200.0,
        "status": "completed",
    }

    await process_payment_event(event, test_db_session)

    updated_order = await test_db_session.get(OrderORM, "order-123")
    assert updated_order.status == "paid"