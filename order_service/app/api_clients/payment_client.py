import httpx


class PaymentClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    async def create_payment(self, order_id: str, amount: int) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            json_data = {"order_id": order_id, "amount": amount}
            response = await client.post(f"{self.base_url}/payments", json=json_data)
            response.raise_for_status()
        return response.json()