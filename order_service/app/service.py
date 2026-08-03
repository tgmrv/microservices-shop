from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .api_clients import CatalogClient, PaymentClient
from .schemas import OrderCreateSchema, OrderReadSchema
from .models import OrderORM, OrderItemORM


class OrderService:
    def __init__(self, db: AsyncSession, catalog_client: CatalogClient, payment_client: PaymentClient):
        self.db = db
        self.catalog_client = catalog_client
        self.payment_client = payment_client

    async def create(self, order_data: OrderCreateSchema) -> OrderReadSchema:
        products = []
        for item in order_data.items:
            product = await self.catalog_client.get_product(item.product_id)
            products.append({
                "product_id": product["id"],
                "product_name": product["name"],
                "quantity": item.quantity,
                "item_price": product["price"]
            })
        total_price = sum([product["item_price"] * product["quantity"] for product in products])

        order = OrderORM(
            user_id=order_data.user_id,
            status="created",
            total_price=total_price
        )
        self.db.add(order)
        await self.db.flush()

        order_items = [OrderItemORM(order_id=order.id, **product) for product in products]
        self.db.add_all(order_items)

        await self.db.commit()
        await self.db.refresh(order)

        payment_result = await self.payment_client.create_payment(
            order_id=order.id,
            amount=total_price
        )

        if payment_result["status"] == "completed":
            order.status = "paid"
        else:
            order.status = "payment_failed"
        await self.db.commit()
        await self.db.refresh(order)

        return OrderReadSchema.model_validate(order)

    async def get(self, order_id: str):
        result = await self.db.get(OrderORM, order_id)
        return result

    async def get_all(self):
        result = await self.db.execute(select(OrderORM))
        orders = result.scalars().all()
        return list(orders)

