from fastapi import APIRouter

from ...api_client import request_service
from ...config import settings


router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
async def get_products():
    return await request_service("GET", f"{settings.CATALOG_SERVICE_URL}/products")


@router.get("/{product_id}")
async def get_product(product_id: str):
    return await request_service(
        "GET",
        f"{settings.CATALOG_SERVICE_URL}/products/{product_id}",
    )