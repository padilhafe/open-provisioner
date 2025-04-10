# app/services/device_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import selectinload
from app.models.device import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate

async def create_device(db: AsyncSession, device_data: DeviceCreate) -> Device:
    values = device_data.model_dump(mode='json')
    stmt = insert(Device).values(**values).returning(Device.id)
    result = await db.execute(stmt)
    device_id = result.scalar_one()
    await db.commit()
    return await get_device_by_id(db, device_id)

async def get_devices(db: AsyncSession) -> list[Device]:
    stmt = select(Device)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_device_by_id(db: AsyncSession, device_id: int) -> Device | None:
    stmt = select(Device).where(Device.id == device_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

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
