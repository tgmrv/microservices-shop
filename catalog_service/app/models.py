from uuid import uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class ProductORM(Base):
    __tablename__ = "products"

    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float]
    image_url: Mapped[str] = mapped_column(nullable=True)
    category: Mapped[str]