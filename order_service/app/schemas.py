from pydantic import BaseModel, ConfigDict

class OrderCreateSchema(BaseModel):
    user_id: str
    items: list[OrderItemCreateSchema]

class OrderItemCreateSchema(BaseModel):
    product_id: str
    quantity: int

class OrderReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    status: str
    total_price: float
    items: list[OrderItemReadSchema]

class OrderItemReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: str
    product_name: str
    quantity: int
    item_price: float