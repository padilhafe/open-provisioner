# tests/test_users.py
import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/api/v1/users/", json={
        "name": "Test User",
        "email": "user@test.com",
        "password": "123456"
    })
    data = response.json()
    assert response.status_code == 201
    assert data["name"] == "Test User"
    assert data["email"] == "user@test.com"
    assert "id" in data
    return data["id"]

@pytest.mark.asyncio
async def test_list_all_users(client):
    await client.post("/api/v1/users/", json={
        "name": "User 1",
        "email": "user1@test.com",
        "password": "123456"
    })
    response = await client.get("/api/v1/users/")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "User 1"
    assert data[0]["email"] == "user1@test.com"

@pytest.mark.asyncio
async def test_retrieve_user(client):
    create_response = await client.post("/api/v1/users/", json={
        "name": "User to Retrieve",
        "email": "retrieve@test.com",
        "password": "123456"
    })
    user_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/users/{user_id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == user_id
    assert data["name"] == "User to Retrieve"
    assert data["email"] == "retrieve@test.com"

@pytest.mark.asyncio
async def test_retrieve_user_not_found(client):
    response = await client.get("/api/v1/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_update_user(client):
    create_response = await client.post("/api/v1/users/", json={
        "name": "User to Update",
        "email": "update@test.com",
        "password": "123456"
    })
    user_id = create_response.json()["id"]

    response = await client.put(f"/api/v1/users/{user_id}", json={
        "name": "Updated User",
        "email": "updated@test.com",
        "password": "654321"
    })
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == user_id
    assert data["name"] == "Updated User"
    assert data["email"] == "updated@test.com"

@pytest.mark.asyncio
async def test_update_user_not_found(client):
    response = await client.put("/api/v1/users/9999", json={
        "name": "Updated User",
        "email": "updated@test.com",
        "password": "654321"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_delete_user(client):
    create_response = await client.post("/api/v1/users/", json={
        "name": "User to Delete",
        "email": "delete@test.com",
        "password": "123456"
    })
    user_id = create_response.json()["id"]

    response = await client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204
    assert response.text == ""

    get_response = await client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_delete_user_not_found(client):
    response = await client.delete("/api/v1/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"