from typing import Any

import httpx
from fastapi import HTTPException, status


def _upstream_error(response: httpx.Response) -> HTTPException:
    try:
        detail = response.json()
    except:
        detail = response.text

    return HTTPException(status_code=response.status_code, detail=detail)


async def request_service(
        method: str,
        url: str,
        json_body: Any = None,
        headers: dict = None,
):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, json=json_body, headers=headers)
        except httpx.RequestError as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"{e.request.url}")

        if response.status_code >= 400:
            raise _upstream_error(response)
        return response.json()