import pytest


@pytest.mark.asyncio
async def test_create_payment(client, override_payment_service, payment_exchange):
    payment = {
        "id": "payment-123",
        "order_id": "order-123",
        "status": "created",
        "amount": 1200.0,
    }

    completed_payment = {
        "id": "payment-123",
        "order_id": "order-123",
        "status": "completed",
        "amount": 1200.0,
    }

    override_payment_service.create.return_value = payment
    override_payment_service.complete_payment.return_value = completed_payment

    response = await client.post("/payments", json=payment)

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == "payment-123"
    assert data["status"] == "completed"

    override_payment_service.create.assert_awaited_once()
    override_payment_service.complete_payment.assert_awaited_once()