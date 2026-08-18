import pytest

from order_service.app.schemas import OrderCreateSchema, OrderItemCreateSchema


@pytest.mark.asyncio
async def test_create_order(mock_catalog, mock_payment, order_service):
    order_data = OrderCreateSchema(
        user_id="user-123",
        items=[OrderItemCreateSchema(product_id="product-123", quantity=2)]
    )
    order = await order_service.create(order_data)

    assert order.user_id == "user-123"
    assert order.total_price == 2800.0
    assert order.status == "paid"

    mock_catalog.get_product.assert_called_once_with("product-123")
    mock_payment.create_payment.assert_called_once_with(
        order_id=order.id,
        amount=2800.0
    )