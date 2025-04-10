# tests/test_customers.py

import pytest

@pytest.mark.asyncio
async def test_create_customer(client):
    response = await client.post("/api/v1/customers/", json={
        "name": "João Silva",
        "username": "joaosilva",
        "integration_id": 101
    })
    data = response.json()
    assert response.status_code == 201
    assert data["name"] == "João Silva"
    assert data["username"] == "joaosilva"
    assert data["integration_id"] == 101
    assert "id" in data
    return data["id"]

@pytest.mark.asyncio
async def test_list_all_customers(client):
    await client.post("/api/v1/customers/", json={
        "name": "Maria Souza",
        "username": "mariasouza"
    })
    response = await client.get("/api/v1/customers/")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_retrieve_customer(client):
    create_response = await client.post("/api/v1/customers/", json={
        "name": "Carlos Silva"
    })
    customer_id = create_response.json()["id"]
    response = await client.get(f"/api/v1/customers/{customer_id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == customer_id
    assert data["name"] == "Carlos Silva"

@pytest.mark.asyncio
async def test_retrieve_customer_not_found(client):
    response = await client.get("/api/v1/customers/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"

@pytest.mark.asyncio
async def test_update_customer(client):
    create_response = await client.post("/api/v1/customers/", json={
        "name": "Roberto Rocha"
    })
    customer_id = create_response.json()["id"]
    response = await client.put(f"/api/v1/customers/{customer_id}", json={
        "name": "Roberto Rocha Jr.",
        "username": "robertojr",
        "integration_id": 202
    })
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == customer_id
    assert data["name"] == "Roberto Rocha Jr."
    assert data["username"] == "robertojr"
    assert data["integration_id"] == 202

@pytest.mark.asyncio
async def test_update_customer_not_found(client):
    response = await client.put("/api/v1/customers/9999", json={
        "name": "Inexistente"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"

@pytest.mark.asyncio
async def test_delete_customer(client):
    create_response = await client.post("/api/v1/customers/", json={
        "name": "Lucas Lima"
    })
    customer_id = create_response.json()["id"]
    response = await client.delete(f"/api/v1/customers/{customer_id}")
    assert response.status_code == 204
    get_response = await client.get(f"/api/v1/customers/{customer_id}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_customer_not_found(client):
    response = await client.delete("/api/v1/customers/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"
