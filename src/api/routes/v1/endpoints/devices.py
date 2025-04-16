# api/api/v1/endpoints/devices.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from api.core.enums import OpenBmcPowerActions
from api.db.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceOut
from api.services import device_service
from databases import Database

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
async def list_all(
    page: int = Query(1, ge=1),
    limit: int = Query(5, le=100),
    db: AsyncSession = Depends(get_db)
):
    devices, total = await device_service.get_devices(db, page=page, limit=limit)
    return {"devices": devices, "total": total}


@router.get("/{device_id}", response_model=DeviceOut, status_code=status.HTTP_200_OK)
async def retrieve(device_id: int, db: Database = Depends(get_db)):
    user = await device_service.get_device_by_id(db, device_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return user

@router.get("/{device_id}/get-current-users", status_code=status.HTTP_200_OK)
async def retrieve_current_users(device_id: int, db: Database = Depends(get_db)):
    data = await device_service.get_current_users(db, device_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ONU pending authorization")
    return data

@router.get("/{device_id}/get-unauthorized-onu", status_code=status.HTTP_200_OK)
async def retrieve(device_id: int, db: Database = Depends(get_db)):
    unauthorized_onus = await device_service.get_device_unauthorized_onu(db, device_id)
    if not unauthorized_onus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ONU pending authorization")
    return unauthorized_onus

@router.post("/", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
async def create(user: DeviceCreate, db: Database = Depends(get_db)):
    return await device_service.create_device(db, user)

@router.put("/{device_id}", response_model=DeviceOut, status_code=status.HTTP_200_OK)
async def update(device_id: int, device_update: DeviceUpdate, db: Database = Depends(get_db)):
    user = await device_service.update_device(db, device_id, device_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return user

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(device_id: int, db: Database = Depends(get_db)):
    success = await device_service.delete_device(db, device_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

@router.get("/{device_id}/power-action", status_code=status.HTTP_200_OK)
async def reboot(
    device_id: int, 
    action: OpenBmcPowerActions, 
    db: Database = Depends(get_db)
):
    result = await device_service.power_actions(db, device_id, action.value)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

    return result
