# app/services/device_service.py

from databases import Database
from sqlalchemy import select
from app.models.device import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate
from app.models.device import Device

async def create_device(db: Database, device_data: DeviceCreate) -> Device:
    values = device_data.model_dump(mode='json')
    query = Device.__table__.insert().values(**values)
    device_id = await db.execute(query)
    return await get_device_by_id(db, device_id)

async def get_devices(db: Database):
    query = select(Device)
    rows = await db.fetch_all(query)
    return rows

async def get_device_by_id(db: Database, device_id: int):
    query = select(Device).where(Device.id == device_id)
    return await db.fetch_one(query)

async def update_device(db: Database, device_id: int, updates: DeviceUpdate):
    values = updates.model_dump(exclude_unset=True, mode='json')
    query = (
        Device.__table__
        .update()
        .where(Device.id == device_id)
        .values(**values)
    )
    await db.execute(query)
    return await get_device_by_id(db, device_id)

async def delete_device(db: Database, device_id: int):
    query = Device.__table__.delete().where(Device.id == device_id)
    result = await db.execute(query)
    return result > 0
