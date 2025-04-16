# api/services/device_service.py

import asyncio
import api.queries.actions.open_bmc as open_bmc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.orm import selectinload
from api.models.device import Device
from api.schemas.device_schema import DeviceCreate, DeviceUpdate
from api.queries import common
from api.queries.olt.huawei.get_unauthorized_onu import get_unauthorized_onu

async def create_device(db: AsyncSession, device_data: DeviceCreate) -> Device:
    values = device_data.model_dump(mode='json')
    stmt = insert(Device).values(**values).returning(Device.id)
    result = await db.execute(stmt)
    device_id = result.scalar_one()
    await db.commit()
    return await get_device_by_id(db, device_id)

async def get_devices(db: AsyncSession, page: int = 1, limit: int = 5):
    offset = (page - 1) * limit

    stmt = select(Device).offset(offset).limit(limit)
    result = await db.execute(stmt)
    devices = result.scalars().all()

    count_stmt = select(func.count()).select_from(Device)
    total = (await db.execute(count_stmt)).scalar_one()

    return devices, total

async def get_device_by_id(db: AsyncSession, device_id: int) -> Device | None:
    stmt = select(Device).where(Device.id == device_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_current_users(db: AsyncSession, device_id: int) -> list[dict]:
    stmt = select(Device).where(Device.id == device_id)
    result = await db.execute(stmt)
    device = result.scalar_one_or_none()

    if not device:
        raise ValueError("Dispositivo não encontrado")

    data_json = await asyncio.to_thread(
        common.get_users,
        device_mgmt_ipv4=device.device_mgmt_ipv4,
        device_username=device.device_username,
        device_password=device.device_password,
        device_type=device.device_type,
        port=device.device_mgmt_port
    )

    if not isinstance(data_json, list):
        raise TypeError("Esperado uma lista de dados, mas recebeu outro tipo.")

    return {"users": data_json}

async def get_device_unauthorized_onu(db: AsyncSession, device_id: int) -> list[dict]:
    stmt = select(Device).where(Device.id == device_id)
    result = await db.execute(stmt)
    device = result.scalar_one_or_none()

    if not device:
        raise ValueError("Dispositivo não encontrado")

    data_json = await asyncio.to_thread(
        get_unauthorized_onu,
        device_mgmt_ipv4=device.device_mgmt_ipv4,
        device_username=device.device_username,
        device_password=device.device_password,
        device_type=device.device_type,
        port=device.device_mgmt_port
    )

    if not isinstance(data_json, list):
        raise TypeError("Esperado uma lista de dados, mas recebeu outro tipo.")

    return data_json

async def update_device(db: AsyncSession, device_id: int, updates: DeviceUpdate) -> Device | None:
    values = updates.model_dump(exclude_unset=True, mode='json')
    stmt = update(Device).where(Device.id == device_id).values(**values).returning(Device.id)
    result = await db.execute(stmt)
    updated_id = result.scalar_one_or_none()
    await db.commit()
    if updated_id is None:
        return None
    return await get_device_by_id(db, updated_id)

async def delete_device(db: AsyncSession, device_id: int) -> bool:
    stmt = delete(Device).where(Device.id == device_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

async def power_actions(db: AsyncSession, device_id: int, action: str):
    stmt = select(Device).where(Device.id == device_id)
    result = await db.execute(stmt)
    device = result.scalar_one_or_none()

    if not device:
        raise ValueError("Dispositivo não encontrado")

    if device.device_type == "open_bmc":
        return open_bmc.power_actions(device, action)
    
    else:
        return { "tipo": "não suportado" }