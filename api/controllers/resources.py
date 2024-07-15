from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..dependencies.database import get_db
from ..models.models import Resource
from ..models.schemas import ResourceCreate, ResourceRead, ResourceUpdate

router = APIRouter()

@router.post("/", response_model=ResourceRead)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    db_resource = Resource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@router.get("/", response_model=List[ResourceRead])
def read_all_resources(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    resources = db.query(Resource).offset(skip).limit(limit).all()
    return resources

@router.get("/{resource_id}", response_model=ResourceRead)
def read_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.put("/{resource_id}", response_model=ResourceRead)
def update_resource(resource_id: int, resource: ResourceUpdate, db: Session = Depends(get_db)):
    db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    for key, value in resource.dict().items():
        setattr(db_resource, key, value)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@router.delete("/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(resource)
    db.commit()
    return {"message": "Resource deleted successfully"}
