import pytest

@pytest.mark.asyncio
async def test_create_product(client):
    response = await client.post(
        "/products",
        json={
            "name": "Macbook Pro",
            "description": "Macbook Pro 14",
            "price": 1400.0,
            "category": "Electronics"
        }
    )
    body = response.json()
    assert response.status_code == 201
    assert "id" in body
    assert body["name"] == "Macbook Pro"
    assert body["price"] == 1400.0


@pytest.mark.asyncio
async def test_create_product_missing_required_field(client):
    response = await client.post(
        "/products",
        json={
            "price": 1400.0,
            "category": "Electronics"
        }
    )
    assert response.status_code == 422
    body = response.json()
    assert "name" in str(body)


@pytest.mark.asyncio
async def test_get_products(client):
    await client.post(
        "/products",
        json={
            "name": "Macbook Pro",
            "price": 1400.0,
            "category": "Electronics"
        }
    )
    await client.post(
        "/products",
        json={
            "name": "Iphone Pro",
            "price": 1000.0,
            "category": "Electronics"
        }
    )

    response = await client.get("/products")
    body = response.json()
    assert response.status_code == 200
    assert len(response.json()) >= 2
    names = [product["name"] for product in body]
    assert "Macbook Pro" in names
    assert "Iphone Pro" in names


@pytest.mark.asyncio
async def test_delete_product(client):
    crate_resp = await client.post(
        "/products",
        json={
            "name": "Macbook Pro",
            "price": 1400.0,
            "category": "Electronics"
        }
    )
    product_id = crate_resp.json()["id"]

    response = await client.delete(f"/products/{product_id}")
    assert response.status_code == 204

    get_response = await client.get(f"/products/{product_id}")
    assert get_response.status_code == 404