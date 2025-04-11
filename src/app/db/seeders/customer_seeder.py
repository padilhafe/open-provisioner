# app/db/seeders/customer_seeder.py

import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.customer import Customer

async def create_customer(session: AsyncSession, name: str, username: str = None, integration_id: int = None) -> Customer:
    customer = Customer(name=name, username=username, integration_id=integration_id)
    session.add(customer)
    await session.flush()
    return customer

async def get_or_create_customer(session: AsyncSession, name: str) -> Customer:
    result = await session.execute(select(Customer).where(Customer.name == name))
    customer = result.scalar_one_or_none()
    if customer:
        return customer
    return await create_customer(session, name=name)

async def seed_customers(session: AsyncSession):
    for i in range(10):
        name = f"Cliente Exemplo {i}"
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        integration_id = random.randint(1000, 9999)

        await create_customer(session, name=name, username=username, integration_id=integration_id)

    await session.commit()
    print("Clientes inseridos com sucesso.")
