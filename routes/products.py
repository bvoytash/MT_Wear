from fastapi import APIRouter, HTTPException, status, Request
from models.product import Product
from models.category import Category
from fastapi.responses import JSONResponse
from database import db_dependency
from fastapi.encoders import jsonable_encoder
from validators.product import create_product_dependency, update_product_dependency,get_id_dependency, sorting_dependency, filtering_dependency, OrderEnum, is_active_dependency
from routes.auth import csrf_dependency, auth_admin_dependency
from html import escape
from security import limiter

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product(create_product_request: create_product_dependency, db: db_dependency, 
                         crsf_token: csrf_dependency, auth_admin_dependency: auth_admin_dependency, 
                         ):
    category = db.query(Category).filter(Category.name == create_product_request.category).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category '{create_product_request.category}' not found"
        )
    
    sanitized_name=escape(create_product_request.name)
    sanitized_description=escape(create_product_request.description)
    sanitized_price=create_product_request.price
    sanitized_size=escape(create_product_request.size)
    
    new_product = Product(
        name=sanitized_name,
        description=sanitized_description,
        price=sanitized_price,
        size=sanitized_size,
        category_id=category.id,
        image_url=create_product_request.image_url,
        is_active=create_product_request.is_active,
    )
    
    db.add(new_product)
    db.commit()
    return JSONResponse(
        {"detail": "Product created successfully"},
        status_code=status.HTTP_201_CREATED
    )
    

@router.get("/all", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def get_all_products(request: Request, skip: int = 0, limit: int = 10, db: db_dependency = db_dependency,
                           crsf_token: csrf_dependency=csrf_dependency,
                        ):
    products = db.query(Product).offset(skip).limit(limit).all()
    
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found"
        )
    
    serialized_products = jsonable_encoder(products)
    
    return JSONResponse(
        content={"products": serialized_products}, 
        status_code=status.HTTP_200_OK
    )

@router.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    update_product_request: update_product_dependency,
    db: db_dependency,
    crsf_token: csrf_dependency, auth_admin_dependency: auth_admin_dependency,
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
    

    if update_product_request.name is not None:
        sanitized_name = escape(update_product_request.name)
        product.name = sanitized_name
    
    if update_product_request.description is not None:
        sanitized_description = escape(update_product_request.description)
        product.description = sanitized_description
    
    if update_product_request.price is not None:
        sanitized_price = update_product_request.price
        product.price = sanitized_price
    
    if update_product_request.image_url is not None:
        sanitized_image_url = escape(update_product_request.image_url)
        product.image_url = sanitized_image_url
    
    if update_product_request.is_active is not None:
        sanitized_is_active = escape(update_product_request.is_active)
        product.is_active = sanitized_is_active
    
    db.commit()
    
    return JSONResponse(
        content={
            "detail": "Product updated successfully",
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


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, db: db_dependency,
                         crsf_token: csrf_dependency, auth_admin_dependency: auth_admin_dependency,
                         ):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    db.delete(product)
    db.commit()
    
    return JSONResponse(
        {"detail": f"Product with ID {product_id} deleted successfully"}
    )

@router.get("/sorted", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def get_sorted_products(
    request: Request,
    # skip: int = 0,
    # limit: int = 10,
    db: db_dependency = db_dependency,
    sorting_dependency: sorting_dependency = sorting_dependency,
    crsf_token: csrf_dependency = csrf_dependency,
):

    order_column = getattr(Product, sorting_dependency.sort_by.value)
    if sorting_dependency.order == OrderEnum.desc:
        order_column = order_column.desc()

    products = db.query(Product).order_by(order_column).all()

    serialized_products = jsonable_encoder(products)
    
    return JSONResponse(
        content={"products": serialized_products},
        status_code=status.HTTP_200_OK,
    )

@router.get("/filtered", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def get_filtered_products(
    request: Request,
    filtering_dependency: filtering_dependency,
    db: db_dependency = db_dependency,
    crsf_token: csrf_dependency = csrf_dependency,
):
    query = db.query(Product)

    if filtering_dependency.category:
        query = query.join(Category).filter(Category.name == filtering_dependency.category)
    
    if filtering_dependency.is_active is not None:
        query = query.filter(Product.is_active == filtering_dependency.is_active)
    
    if filtering_dependency.min_price is not None:
        query = query.filter(Product.price >= filtering_dependency.min_price)
    
    if filtering_dependency.max_price is not None:
        query = query.filter(Product.price <= filtering_dependency.max_price)
    
    products = query.all()

    serialized_products = jsonable_encoder(products)
    
    return JSONResponse(
        content={"products": serialized_products},
        status_code=status.HTTP_200_OK,
    )

@router.get("/{product_id}", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def get_product_by_id(
    request: Request,
    product_id: int,
    product_request: get_id_dependency,
    db: db_dependency,
    crsf_token: csrf_dependency,
    ):

    product = db.query(Product).filter(Product.id == product_request.product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    serialized_product = jsonable_encoder(product)
    return JSONResponse(
        content={"product": serialized_product}, 
        status_code=status.HTTP_200_OK
    )

@router.patch("/{product_id}/is_active", status_code=status.HTTP_200_OK)
async def update_is_active(
    product_id: int,
    is_active_dependency: is_active_dependency,
    db: db_dependency = db_dependency,
    crsf_token: csrf_dependency = csrf_dependency,
    auth_admin_dependency: auth_admin_dependency = auth_admin_dependency, 
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )

    product.is_active = is_active_dependency.is_active
    db.commit()

    return JSONResponse(
        content={
            "detail": f"Product with ID {product_id} updated successfully",
            "product": {
                "id": product.id,
                "name": product.name,
                "is_active": product.is_active,
            },
        },
        status_code=status.HTTP_200_OK,
    )
