# tests/test_users.py
import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/api/v1/users/", json={
        "name": "Felipe Teste",
        "email": "felipe@test.com",
        "password": "123456"
    })

    data = response.json()

    assert response.status_code == 201
    assert data["name"] == "Felipe Teste"
