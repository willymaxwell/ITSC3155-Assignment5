from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..dependencies.database import get_db
from ..models.models import Sandwich
from ..models.schemas import SandwichCreate, SandwichRead, SandwichUpdate

router = APIRouter()

@router.post("/", response_model=SandwichRead)
def create_sandwich(sandwich: SandwichCreate, db: Session = Depends(get_db)):
    db_sandwich = Sandwich(**sandwich.dict())
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

@router.get("/", response_model=List[SandwichRead])
def read_all_sandwiches(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    sandwiches = db.query(Sandwich).offset(skip).limit(limit).all()
    return sandwiches

@router.get("/{sandwich_id}", response_model=SandwichRead)
def read_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich

@router.put("/{sandwich_id}", response_model=SandwichRead)
def update_sandwich(sandwich_id: int, sandwich: SandwichUpdate, db: Session = Depends(get_db)):
    db_sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if db_sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    for key, value in sandwich.dict().items():
        setattr(db_sandwich, key, value)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

@router.delete("/{sandwich_id}")
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    db.delete(sandwich)
    db.commit()
    return {"message": "Sandwich deleted successfully"}
