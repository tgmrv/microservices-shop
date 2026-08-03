from uuid import uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class ProductORM(Base):
    __tablename__ = "products"

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    image_url: Mapped[str]
    category: Mapped[str]