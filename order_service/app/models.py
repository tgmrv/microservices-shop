from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))


class OrderORM(Base):
    __tablename__ = "orders"

    user_id: Mapped[str]
    status: Mapped[str] = mapped_column(default="created")
    total_price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    items: Mapped[list[OrderItemORM]] = relationship("OrderItemORM", back_populates="order", lazy="selectin")


class OrderItemORM(Base):
    __tablename__ = "order_items"

    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"), index=True)
    product_id: Mapped[str]
    product_name: Mapped[str]
    quantity: Mapped[int]
    item_price: Mapped[float]
    order: Mapped[OrderORM] = relationship("OrderORM", back_populates="items")
