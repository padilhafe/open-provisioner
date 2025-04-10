# app/services/cpe_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import selectinload
from app.schemas.cpe_schema import CpeCreate, CpeUpdate
from app.models.cpe import Cpe

async def create_cpe(db: AsyncSession, cpe_data: CpeCreate) -> Cpe:
    values = cpe_data.model_dump(mode='json')
    stmt = insert(Cpe).values(**values).returning(Cpe.id)
    result = await db.execute(stmt)
    cpe_id = result.scalar_one()
    await db.commit()
    return await get_cpe_by_id(db, cpe_id)

async def get_cpes(db: AsyncSession) -> list[Cpe]:
    stmt = select(Cpe).options(
        selectinload(Cpe.device),
        selectinload(Cpe.customer)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_cpe_by_id(db: AsyncSession, cpe_id: int) -> Cpe | None:
    stmt = select(Cpe).where(Cpe.id == cpe_id).options(
        selectinload(Cpe.device),
        selectinload(Cpe.customer)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def update_cpe(db: AsyncSession, cpe_id: int, updates: CpeUpdate) -> Cpe | None:
    values = updates.model_dump(exclude_unset=True, mode='json')
    stmt = update(Cpe).where(Cpe.id == cpe_id).values(**values).returning(Cpe.id)
    result = await db.execute(stmt)
    updated_id = result.scalar_one_or_none()
    await db.commit()
    if updated_id is None:
        return None
    return await get_cpe_by_id(db, updated_id)

async def delete_cpe(db: AsyncSession, cpe_id: int) -> bool:
    stmt = delete(Cpe).where(Cpe.id == cpe_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0
