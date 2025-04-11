# app/services/customer_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import selectinload
from app.models.customer import Customer
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate

async def create_customer(db: AsyncSession, customer_data: CustomerCreate) -> Customer:
    values = customer_data.model_dump(mode='json')
    stmt = insert(Customer).values(**values).returning(Customer.id)
    result = await db.execute(stmt)
    customer_id = result.scalar_one()
    await db.commit()
    return await get_customer_by_id(db, customer_id)

async def get_customers(db: AsyncSession) -> list[Customer]:
    stmt = select(Customer).options(selectinload(Customer.cpe))
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_customer_by_id(db: AsyncSession, customer_id: int) -> Customer | None:
    stmt = (
        select(Customer)
        .options(selectinload(Customer.cpe))
        .where(Customer.id == customer_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_customer_by_username(db: AsyncSession, customer_username: str) -> Customer | None:
    stmt = (
        select(Customer)
        .options(selectinload(Customer.cpe))
        .where(Customer.username == customer_username)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def update_customer(db: AsyncSession, customer_id: int, updates: CustomerUpdate) -> Customer | None:
    values = updates.model_dump(exclude_unset=True, mode='json')
    stmt = update(Customer).where(Customer.id == customer_id).values(**values).returning(Customer.id)
    result = await db.execute(stmt)
    updated_id = result.scalar_one_or_none()
    await db.commit()
    if updated_id is None:
        return None
    return await get_customer_by_id(db, updated_id)

async def delete_customer(db: AsyncSession, customer_id: int) -> bool:
    stmt = delete(Customer).where(Customer.id == customer_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0
