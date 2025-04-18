# api/api/v1/endpoints/devices.py

from fastapi import APIRouter, Depends, HTTPException, status
from api.db.dependencies import get_db
from api.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceOut
from api.services import device_service
from databases import Database

router = APIRouter()

@router.post("/", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
async def create(user: DeviceCreate, db: Database = Depends(get_db)):
    return await device_service.create_device(db, user)

@router.get("/", response_model=list[DeviceOut], status_code=status.HTTP_200_OK)
async def list_all(db: Database = Depends(get_db)):
    return await device_service.get_devices(db)

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
