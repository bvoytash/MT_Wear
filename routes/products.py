from fastapi import APIRouter, Depends, HTTPException, status
from models.product import Product
from models.category import Category
from fastapi.responses import JSONResponse
from database import db_dependency
from fastapi.encoders import jsonable_encoder
from validators.product import create_product_dependency, delete_product_dependency

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product(create_product_request: create_product_dependency, db: db_dependency,):
    category = db.query(Category).filter(Category.name == create_product_request.category).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category '{create_product_request.category}' not found"
        )
    
    new_product = Product(
        name=create_product_request.name,
        description=create_product_request.description,
        price=create_product_request.price,
        category_id=category.id,
        image_url=create_product_request.image_url,
        is_active=create_product_request.is_active,
    )
    
    db.add(new_product)
    db.commit()
    return JSONResponse(
        content={"message": "Product created successfully"}, status_code=status.HTTP_201_CREATED
    )

@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_products(skip: int = 0, limit: int = 10, db: db_dependency = db_dependency):
    products = db.query(Product).offset(skip).limit(limit).all()
    
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found"
        )
    
     # Serialize products into a list of dictionaries
    serialized_products = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_id": product.category_id,
            "image_url": product.image_url,
            "is_active": product.is_active,
        }
        for product in products
    ]
    
    return JSONResponse(
        content={"products": serialized_products}, 
        status_code=status.HTTP_200_OK
    )
