# api/db/seeders/cpe_seeder.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import random

from api.models.cpe import Cpe
from api.models.device import Device
from api.db.seeders.customer_seeder import create_customer
from api.core.enums import GponOperState
from api.core.types import CPE_TYPE
from api.core.types import CUSTOMER_STATUS

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
                status = random.choice(CUSTOMER_STATUS)
            )

            cpe = Cpe(
                cpe_type=random.choice(CPE_TYPE),
                oper_state=random.choice(list(GponOperState)).value,
                customer_id=customer.id,
                device_id=device.id,
            )
            session.add(cpe)

    await session.commit()
