from fastapi import APIRouter, Depends, HTTPException, status
from models.product import Product
from models.category import Category
from fastapi.responses import JSONResponse
from database import db_dependency
from fastapi.encoders import jsonable_encoder
from validators.product import create_product_dependency, update_product_dependency, get_id_dependency

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

@router.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    update_product_request: update_product_dependency,
    db: db_dependency,
):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    if update_product_request.category:
        category = db.query(Category).filter(Category.name == update_product_request.category).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category '{update_product_request.category}' not found"
            )
        product.category_id = category.id
    
    # Update the fields only if they are provided in the request
    if update_product_request.name is not None:
        product.name = update_product_request.name
    
    if update_product_request.description is not None:
        product.description = update_product_request.description
    
    if update_product_request.price is not None:
        product.price = update_product_request.price
    
    if update_product_request.image_url is not None:
        product.image_url = update_product_request.image_url
    
    if update_product_request.is_active is not None:
        product.is_active = update_product_request.is_active
    
    db.commit()
    
    return JSONResponse(
        content={
            "message": "Product updated successfully",
            "product": {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category_id": product.category_id,
                "image_url": product.image_url,
                "is_active": product.is_active,
            },
        },
        status_code=status.HTTP_200_OK,
    )


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_by_id(
    product_id: int,
    product_request: get_id_dependency,
    db: db_dependency):

    product = db.query(Product).filter(Product.id == product_request.product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    serialized_product = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category_id": product.category_id,
        "image_url": product.image_url,
        "is_active": product.is_active,
    }
    
    return JSONResponse(
        content={"product": serialized_product}, 
        status_code=status.HTTP_200_OK
    )


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, db: db_dependency):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    db.delete(product)
    db.commit()
    
    return {"message": f"Product with ID {product_id} deleted successfully"}
