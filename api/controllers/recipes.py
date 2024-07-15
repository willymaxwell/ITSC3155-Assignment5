from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..dependencies.database import get_db
from ..models.models import Recipe
from ..models.schemas import RecipeCreate, RecipeRead, RecipeUpdate

router = APIRouter()

@router.post("/", response_model=RecipeRead)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.get("/", response_model=List[RecipeRead])
def read_all_recipes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).offset(skip).limit(limit).all()
    return recipes

@router.get("/{recipe_id}", response_model=RecipeRead)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/{recipe_id}", response_model=RecipeRead)
def update_recipe(recipe_id: int, recipe: RecipeUpdate, db: Session = Depends(get_db)):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    for key, value in recipe.dict().items():
        setattr(db_recipe, key, value)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(recipe)
    db.commit()
    return {"message": "Recipe deleted successfully"}
