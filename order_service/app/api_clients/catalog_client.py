import httpx


class CatalogClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    async def get_product(self, product_id: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/products/{product_id}")

        return response.json()