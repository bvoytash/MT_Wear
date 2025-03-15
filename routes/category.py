from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.category import Category
from database import db_dependency
from validators.category import create_category_dependency

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_category(create_category_request: create_category_dependency,db: db_dependency,):
    existing_category = db.query(Category).filter(Category.name == create_category_request.name).first()

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category '{create_category_request.name}' already exists"
        )
    
    new_category = Category(name=create_category_request.name)
    
    db.add(new_category)
    db.commit()
    
    return {"message": "Category created successfully", "category": {"id": new_category.id, "name": new_category.name}}
