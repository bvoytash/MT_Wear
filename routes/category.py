from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.category import Category
from database import db_dependency
from validators.category import create_category_dependency, update_category_dependency
from routes.auth import auth_user_dependency, csrf_dependency

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_category(
    create_category_request: create_category_dependency,
    db: db_dependency,
    ):
    existing_category = db.query(Category).filter(Category.name == create_category_request.name).first()

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category '{create_category_request.name}' already exists"
        )
    
    new_category = Category(name=create_category_request.name)
    
    db.add(new_category)
    db.commit()
    
    return {"message": "Category created successfully",
            "category": {"id": new_category.id, "name": new_category.name}}


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_categories(db: db_dependency = db_dependency):
    categories = db.query(Category).all()
    
    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No categories found"
        )
    
    serialized_categories = [{"id": category.id, "name": category.name} for category in categories]
    
    return {"categories": serialized_categories}


@router.get("/{category_id}", status_code=status.HTTP_200_OK)
async def get_category_by_id(category_id: int, db: db_dependency):
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found"
        )
    
    return {"category": {"id": category.id, "name": category.name}}


@router.put("/{category_id}", status_code=status.HTTP_200_OK)
async def update_category(category_id: int, updated_data: update_category_dependency, db: db_dependency):
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found"
        )
    
    category.name = updated_data.name
    
    db.commit()
    
    return {"message": "Category updated successfully", "category": {"id": category.id, "name": category.name}}


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, db: db_dependency):
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found"
        )
    
    db.delete(category)
    db.commit()
    
    return {"message": f"Category with ID {category_id} deleted successfully"}
