from fastapi import APIRouter, Depends, HTTPException, status

from ...auth import get_current_user
from ...api_client import request_service
from ...config import settings
from ...schemas import OrderCreateSchema, OrderReadSchema, CurrentUserSchema

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderReadSchema, status_code=status.HTTP_201_CREATED)
async def create_order(
    payload: OrderCreateSchema,
    user: CurrentUserSchema = Depends(get_current_user),
):
    order_payload = payload.model_dump()
    order_payload["user_id"] = user.id
    return await request_service(
        "POST",
        f"{settings.ORDER_SERVICE_URL}/orders",
        json_body=order_payload,
    )


@router.get("/{order_id}", response_model=OrderReadSchema)
async def get_order(
    order_id: str,
    user: CurrentUserSchema = Depends(get_current_user),
):
    order = await request_service(
        "GET",
        f"{settings.ORDER_SERVICE_URL}/orders/{order_id}",
    )
    ensure_order_owner(order, user)
    return order


def ensure_order_owner(order, user: CurrentUserSchema) -> None:
    if not order or not isinstance(order, dict) or order.get("user_id") != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )