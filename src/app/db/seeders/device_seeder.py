# app/seeders/device_seeder.py

from app.models.device import Device
from sqlalchemy.ext.asyncio import AsyncSession

async def seed_devices(session: AsyncSession):
    existing = await session.execute(Device.__table__.select().limit(1))
    if existing.first():
        print("Dispositivos já existem.")
        return

    devices = [
        Device(
            hostname=f"OLT {i}", 
            device_type="huawei", 
            snmp_version=2, 
            snmp_community="public", 
            device_mgmt_ipv4=f"192.168.0.{i}",
            device_username="sshuser",
            device_password="sshpass"
        )
        for i in range(5)
    ]
    session.add_all(devices)
    await session.commit()
    print("Dispositivos inseridos com sucesso.")
