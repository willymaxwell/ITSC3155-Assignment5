from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from Assignment5.api.dependencies.database import get_db
from Assignment5.api.models.models import OrderDetail
from Assignment5.api.models.schemas import OrderDetailCreate, OrderDetailRead, OrderDetailUpdate

router = APIRouter()

@router.post("/", response_model=OrderDetailRead)
def create_order_detail(order_detail: OrderDetailCreate, db: Session = Depends(get_db)):
    db_order_detail = OrderDetail(**order_detail.dict())
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

@router.get("/", response_model=List[OrderDetailRead])
def read_all_order_details(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    order_details = db.query(OrderDetail).offset(skip).limit(limit).all()
    return order_details

@router.get("/{order_detail_id}", response_model=OrderDetailRead)
def read_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    order_detail = db.query(OrderDetail).filter(OrderDetail.id == order_detail_id).first()
    if order_detail is None:
        raise HTTPException(status_code=404, detail="OrderDetail not found")
    return order_detail

@router.put("/{order_detail_id}", response_model=OrderDetailRead)
def update_order_detail(order_detail_id: int, order_detail: OrderDetailUpdate, db: Session = Depends(get_db)):
    db_order_detail = db.query(OrderDetail).filter(OrderDetail.id == order_detail_id).first()
    if db_order_detail is None:
        raise HTTPException(status_code=404, detail="OrderDetail not found")
    for key, value in order_detail.dict().items():
        setattr(db_order_detail, key, value)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

@router.delete("/{order_detail_id}")
def delete_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    order_detail = db.query(OrderDetail).filter(OrderDetail.id == order_detail_id).first()
    if order_detail is None:
        raise HTTPException(status_code=404, detail="OrderDetail not found")
    db.delete(order_detail)
    db.commit()
    return {"message": "OrderDetail deleted successfully"}
