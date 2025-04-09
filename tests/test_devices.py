# tests/test_devices.py

import pytest
from ipaddress import IPv4Address

@pytest.mark.asyncio
async def test_create_device(client):
    response = await client.post("/api/v1/devices/", json={
        "name": "hw-olt-01",
        "device_type": "olt",
        "mgmt_ipv4": "192.168.100.42",
        "snmp_version": 2,
        "snmp_community": "public"
    })
    data = response.json()
    assert response.status_code == 201
    assert data["name"] == "hw-olt-01"
    assert data["device_type"] == "olt"
    assert data["mgmt_ipv4"] == "192.168.100.42"
    assert data["snmp_version"] == 2
    assert data["snmp_community"] == "public"
    assert "id" in data
    return data["id"]

@pytest.mark.asyncio
async def test_list_all_devices(client):
    await client.post("/api/v1/devices/", json={
        "name": "hw-olt-02",
        "device_type": "olt",
        "mgmt_ipv4": "192.168.100.43",
        "snmp_version": 2,
        "snmp_community": "public"
    })
    response = await client.get("/api/v1/devices/")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "hw-olt-02"
    assert data[0]["device_type"] == "olt"
    assert data[0]["mgmt_ipv4"] == "192.168.100.43"
    assert data[0]["snmp_version"] == 2
    assert data[0]["snmp_community"] == "public"

@pytest.mark.asyncio
async def test_retrieve_device(client):
    create_response = await client.post("/api/v1/devices/", json={
        "name": "hw-olt-03",
        "device_type": "olt",
        "mgmt_ipv4": "192.168.100.44",
        "snmp_version": 2,
        "snmp_community": "public"
    })
    device_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/devices/{device_id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == device_id
    assert data["name"] == "hw-olt-03"
    assert data["device_type"] == "olt"
    assert data["mgmt_ipv4"] == "192.168.100.44"
    assert data["snmp_version"] == 2
    assert data["snmp_community"] == "public"

@pytest.mark.asyncio
async def test_retrieve_device_not_found(client):
    response = await client.get("/api/v1/devices/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"

@pytest.mark.asyncio
async def test_update_device(client):
    create_response = await client.post("/api/v1/devices/", json={
        "name": "hw-olt-04",
        "device_type": "olt",
        "mgmt_ipv4": "192.168.100.45",
        "snmp_version": 2,
        "snmp_community": "public"
    })
    device_id = create_response.json()["id"]

    response = await client.put(f"/api/v1/devices/{device_id}", json={
        "name": "hw-olt-04-updated",
        "device_type": "switch",
        "mgmt_ipv4": "192.168.100.46",
        "snmp_version": 3,
        "snmp_community": "private"
    })
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == device_id
    assert data["name"] == "hw-olt-04-updated"
    assert data["device_type"] == "switch"
    assert data["mgmt_ipv4"] == "192.168.100.46"
    assert data["snmp_version"] == 3
    assert data["snmp_community"] == "private"

@pytest.mark.asyncio
async def test_update_device_not_found(client):
    response = await client.put("/api/v1/devices/9999", json={
        "name": "hw-olt-05",
        "device_type": "olt",
        "mgmt_ipv4": "192.168.100.47",
        "snmp_version": 2,
        "snmp_community": "public"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"

@pytest.mark.asyncio
async def test_delete_device(client):
    create_response = await client.post("/api/v1/devices/", json={
        "name": "hw-olt-06",
        "device_type": "olt",
        "mgmt_ipv4": "192.168.100.48",
        "snmp_version": 2,
        "snmp_community": "public"
    })
    device_id = create_response.json()["id"]

    response = await client.delete(f"/api/v1/devices/{device_id}")
    assert response.status_code == 204
    assert response.text == ""

    get_response = await client.get(f"/api/v1/devices/{device_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Device not found"

@pytest.mark.asyncio
async def test_delete_device_not_found(client):
    response = await client.delete("/api/v1/devices/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"