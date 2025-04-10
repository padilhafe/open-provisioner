# app/api/v1/endpoints/customers.py

from fastapi import APIRouter, Depends, HTTPException, status
from databases import Database
from app.db.dependencies import get_db
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate, CustomerOut
from app.services import customer_service

router = APIRouter()

@router.post("/", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
async def create(customer: CustomerCreate, db: Database = Depends(get_db)):
    return await customer_service.create_customer(db, customer)

@router.get("/", response_model=list[CustomerOut], status_code=status.HTTP_200_OK)
async def list_all(db: Database = Depends(get_db)):
    return await customer_service.get_customers(db)

@router.get("/{customer_id}", response_model=CustomerOut, status_code=status.HTTP_200_OK)
async def retrieve(customer_id: int, db: Database = Depends(get_db)):
    customer = await customer_service.get_customer_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=CustomerOut, status_code=status.HTTP_200_OK)
async def update(customer_id: int, updates: CustomerUpdate, db: Database = Depends(get_db)):
    customer = await customer_service.update_customer(db, customer_id, updates)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(customer_id: int, db: Database = Depends(get_db)):
    success = await customer_service.delete_customer(db, customer_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
