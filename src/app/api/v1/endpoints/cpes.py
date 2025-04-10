# app/api/v1/endpoints/cpes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db
from app.schemas.cpe_schema import CpeCreate, CpeUpdate, CpeOut
from app.services import cpe_service

router = APIRouter()

@router.post("/", response_model=CpeOut, status_code=status.HTTP_201_CREATED)
async def create(cpe: CpeCreate, db: AsyncSession = Depends(get_db)):
    return await cpe_service.create_cpe(db, cpe)

@router.get("/", response_model=list[CpeOut], status_code=status.HTTP_200_OK)
async def list_all(db: AsyncSession = Depends(get_db)):
    return await cpe_service.get_cpes(db)

@router.get("/{cpe_id}", response_model=CpeOut, status_code=status.HTTP_200_OK)
async def retrieve(cpe_id: int, db: AsyncSession = Depends(get_db)):
    cpe = await cpe_service.get_cpe_by_id(db, cpe_id)
    if not cpe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CPE not found")
    return cpe

@router.put("/{cpe_id}", response_model=CpeOut, status_code=status.HTTP_200_OK)
async def update(cpe_id: int, updates: CpeUpdate, db: AsyncSession = Depends(get_db)):
    cpe = await cpe_service.update_cpe(db, cpe_id, updates)
    if not cpe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CPE not found")
    return cpe

@router.delete("/{cpe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(cpe_id: int, db: AsyncSession = Depends(get_db)):
    success = await cpe_service.delete_cpe(db, cpe_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CPE not found")
