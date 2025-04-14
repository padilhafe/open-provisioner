# tests/test_cpes.py

import pytest

@pytest.mark.asyncio
async def test_create_cpe(client):
    customer = await client.post("/api/v1/customers/", json={"name": "Cliente F", "username": "cliente.f"})
    customer_id = customer.json()["id"]

    device = await client.post("/api/v1/devices/", json={
        "hostname": "cpe-device",
        "device_type": "router",
        "device_mgmt_ipv4": "192.168.1.10",
        "device_username": "sshuser",
        "device_password": "sshpass",
        "device_mgmt_port": 22,
        "snmp_version": 2,
        "snmp_port": 161,
        "snmp_community": "public"
    })

    device_id = device.json()["id"]

    response = await client.post("/api/v1/cpes/", json={
        "cpe_type": "onu",
        "oper_state": 4,
        "customer_id": customer_id,
        "device_id": device_id
    })

    print(response.status_code)
    print(response.json())

    data = response.json()
    assert response.status_code == 201
    assert data["cpe_type"] == "onu"
    assert data["oper_state"] == 4
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
    customer = await client.post("/api/v1/customers/", json={"name": "Cliente X", "username": "cliente.x"})
    customer_id = customer.json()["id"]

    device = await client.post("/api/v1/devices/", json={
        "hostname": "device x",
        "device_type": "mikrotik",
        "device_mgmt_ipv4": "192.168.1.140",
        "device_username": "sshuser",
        "device_password": "sshpass",
        "device_mgmt_port": 22,
        "snmp_version": 2,
        "snmp_port": 161,
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
    customer = await client.post("/api/v1/customers/", json={"name": "Cliente Y", "username": "cliente.y"})
    customer_id = customer.json()["id"]

    device = await client.post("/api/v1/devices/", json={
        "hostname": "device-y",
        "device_type": "huawei_smartax",
        "device_mgmt_ipv4": "192.168.1.14",
        "device_username": "sshuser",
        "device_password": "sshpass",
        "device_mgmt_port": 22,
        "snmp_version": 2,
        "snmp_port": 161,
        "snmp_community": "public"
    })
    device_id = device.json()["id"]

    cpe = await client.post("/api/v1/cpes/", json={
        "cpe_type": "onu",
        "oper_state": 1,
        "customer_id": customer_id,
        "device_id": device_id
    })
    assert cpe.status_code == 201, cpe.text
    cpe_id = cpe.json()["id"]

    response = await client.put(f"/api/v1/cpes/{cpe_id}", json={
        "oper_state": 2
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["oper_state"] == 2

@pytest.mark.asyncio
async def test_delete_cpe(client):
    customer = await client.post("/api/v1/customers/", json={"name": "Cliente Z", "username": "cliente.z"})
    customer_id = customer.json()["id"]
    device = await client.post("/api/v1/devices/", json={
        "hostname": "device-z",
        "device_type": "huawei",
        "device_mgmt_ipv4": "192.168.1.21",
        "device_username": "sshuser",
        "device_password": "sshpass",
        "device_mgmt_port": 22,
        "snmp_version": 2,
        "snmp_port": 161,
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
