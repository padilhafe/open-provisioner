# app/db/seeders/cpe_seeder.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import random

from app.models.cpe import Cpe
from app.models.device import Device
from app.db.seeders.customer_seeder import create_customer
from app.core.enums import GponOperState
from app.core.types import CPE_TYPE

async def seed_cpes(session: AsyncSession):
    result = await session.execute(select(Device))
    devices = result.scalars().all()

    for device in devices:
        for i in range(50):
            customer = await create_customer(
                session,
                name=f"Cliente {device.id}-{i}",
                username=f"user_{device.id}_{i}",
                integration_id=random.randint(1000, 9999),
            )

            cpe = Cpe(
                cpe_type=random.choice(CPE_TYPE),
                oper_state=random.choice(list(GponOperState)).value,
                customer_id=customer.id,
                device_id=device.id,
            )
            session.add(cpe)

    await session.commit()
