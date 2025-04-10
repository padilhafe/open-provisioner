# tests/test_cpes.py

import pytest

@pytest.mark.asyncio
async def test_create_cpe(client):
    customer = await client.post("/api/v1/customers/", json={"name": "Cliente CPE"})
    customer_id = customer.json()["id"]

    device = await client.post("/api/v1/devices/", json={
        "name": "cpe-device",
        "device_type": "router",
        "mgmt_ipv4": "192.168.1.10",
        "snmp_version": 2,
        "snmp_community": "public"
    })
    device_id = device.json()["id"]

    response = await client.post("/api/v1/cpes/", json={
        "cpe_type": "onu",
        "state": "active",
        "customer_id": customer_id,
        "device_id": device_id
    })
    data = response.json()
    assert response.status_code == 201
    assert data["cpe_type"] == "onu"
    assert data["state"] == "active"
    assert data["customer_id"] == customer_id
    assert data["device_id"] == device_id
    return data["id"]

@pytest.mark.asyncio
async def test_list_all_cpes(client):
    response = await client.get("/api/v1/cpes/")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_retrieve_cpe(client):
    customer = await client.post("/api/v1/customers/", json={"name": "Cliente X"})
    customer_id = customer.json()["id"]

    device = await client.post("/api/v1/devices/", json={
        "name": "device-x",
        "device_type": "olt",
        "mgmt_ipv4": "192.168.1.11",
        "snmp_version": 2,
        "snmp_community": "public"
    })

    device_id = device.json()["id"]

    cpe = await client.post("/api/v1/cpes/", json={
        "cpe_type": "onu",
        "state": "inactive",
        "customer_id": customer_id,
        "device_id": device_id
    })
    assert cpe.status_code == 201, cpe.text
    cpe_id = cpe.json()["id"]

    response = await client.get(f"/api/v1/cpes/{cpe_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == cpe_id

@pytest.mark.asyncio
async def test_update_cpe(client):
    customer = await client.post("/api/v1/customers/", json={"name": "Cliente Y"})
    customer_id = customer.json()["id"]

    device = await client.post("/api/v1/devices/", json={
        "name": "device-y",
        "device_type": "olt",
        "mgmt_ipv4": "192.168.1.12",
        "snmp_version": 2,
        "snmp_community": "public"
    })
    device_id = device.json()["id"]

    cpe = await client.post("/api/v1/cpes/", json={
        "cpe_type": "onu",
        "state": "active",
        "customer_id": customer_id,
        "device_id": device_id
    })
    assert cpe.status_code == 201, cpe.text
    cpe_id = cpe.json()["id"]

    response = await client.put(f"/api/v1/cpes/{cpe_id}", json={
        "state": "inactive"
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["state"] == "inactive"

@pytest.mark.asyncio
async def test_delete_cpe(client):
    customer = await client.post("/api/v1/customers/", json={"name": "Cliente Z"})
    customer_id = customer.json()["id"]
    device = await client.post("/api/v1/devices/", json={
        "name": "device-z",
        "device_type": "router",
        "mgmt_ipv4": "192.168.1.13",
        "snmp_version": 2,
        "snmp_community": "public"
    })
    device_id = device.json()["id"]
    cpe = await client.post("/api/v1/cpes/", json={
        "cpe_type": "router",
        "state": "active",
        "customer_id": customer_id,
        "device_id": device_id
    })
    cpe_id = cpe.json()["id"]

    response = await client.delete(f"/api/v1/cpes/{cpe_id}")
    assert response.status_code == 204
    get_response = await client.get(f"/api/v1/cpes/{cpe_id}")
    assert get_response.status_code == 404
