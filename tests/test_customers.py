# tests/test_customers.py

import pytest

CUSTOMERS_BASE = "/api/v1/customers"

def customer_by_id_path(cid): return f"{CUSTOMERS_BASE}/search-id/{cid}"
def customer_by_username_path(username): return f"{CUSTOMERS_BASE}/search-username/{username}"

@pytest.mark.asyncio
async def test_create_customer(client):
    response = await client.post(f"{CUSTOMERS_BASE}/", json={
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
    await client.post(f"{CUSTOMERS_BASE}/", json={
        "name": "Maria Souza",
        "username": "mariasouza"
    })
    response = await client.get(f"{CUSTOMERS_BASE}/")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_retrieve_customer_by_id(client):
    create_response = await client.post(f"{CUSTOMERS_BASE}/", json={
        "name": "Carlos Silva",
        "username": "carlos.silva"
    })
    customer_id = create_response.json()["id"]
    response = await client.get(customer_by_id_path(customer_id))
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == customer_id
    assert data["name"] == "Carlos Silva"

@pytest.mark.asyncio
async def test_retrieve_customer_by_username(client):
    create_response = await client.post(f"{CUSTOMERS_BASE}/", json={
        "name": "Carlos Silva",
        "username": "carlos.silva"
    })
    customer_username = create_response.json()["username"]
    response = await client.get(customer_by_username_path(customer_username))
    data = response.json()
    assert response.status_code == 200
    assert data["username"] == customer_username

@pytest.mark.asyncio
async def test_retrieve_customer_not_found(client):
    response = await client.get(customer_by_id_path(9999))
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"

@pytest.mark.asyncio
async def test_update_customer(client):
    create_response = await client.post(f"{CUSTOMERS_BASE}/", json={
        "name": "Roberto Rocha",
        "username": "roberto.rocha"
    })
    customer_id = create_response.json()["id"]
    response = await client.put(f"{CUSTOMERS_BASE}/{customer_id}", json={
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
    response = await client.put(f"{CUSTOMERS_BASE}/9999", json={
        "name": "Padre Quevedo",
        "username": "non.ecxiste"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"

@pytest.mark.asyncio
async def test_delete_customer(client):
    create_response = await client.post(f"{CUSTOMERS_BASE}/", json={
        "name": "Lucas Lima",
        "username": "lucas.lima"
    })
    customer_id = create_response.json()["id"]
    response = await client.delete(customer_by_id_path(customer_id))
    assert response.status_code == 204
    get_response = await client.get(customer_by_id_path(customer_id))
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_customer_not_found(client):
    response = await client.delete(customer_by_id_path(9999))
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"
