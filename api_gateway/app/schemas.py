from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CredentialsBaseSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserRegisterSchema(CredentialsBaseSchema):
    pass


class UserLoginSchema(CredentialsBaseSchema):
    pass


class UserReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserReadSchema


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


class CurrentUserSchema(BaseModel):
    id: str
    email: EmailStr
