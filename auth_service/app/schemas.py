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