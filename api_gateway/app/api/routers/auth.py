from fastapi import APIRouter, Depends, status

from ...api_client import request_service
from ...auth import get_current_user
from ...config import settings
from ...schemas import UserRegisterSchema, TokenResponseSchema, UserLoginSchema, CurrentUserSchema

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=TokenResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegisterSchema):
    return await request_service(
        method="POST",
        url=f"{settings.AUTH_SERVICE_URL}/register",
        json_body=payload.model_dump(mode="json")
    )


@router.post("/login", response_model=TokenResponseSchema)
async def login(payload: UserLoginSchema):
    return await request_service(
        method="POST",
        url=f"{settings.AUTH_SERVICE_URL}/login",
        json_body=payload.model_dump(mode="json")
    )


@router.get("/me", response_model=CurrentUserSchema)
async def get_me(current_user = Depends(get_current_user)):
    return current_user
