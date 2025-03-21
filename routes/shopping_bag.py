from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database import db_dependency
from models.shopping_bag import ShoppingBag, BagItem

router = APIRouter(
    prefix="/shopping_bag",
    tags=["Shopping Bag"]
)


@router.get("/get_or_create", status_code=status.HTTP_200_OK)
async def get_or_create_shopping_bag(
    user_id: int,
    db: db_dependency,
):
    shopping_bag = db.query(ShoppingBag).filter(ShoppingBag.user_id == user_id).first()
    
    if not shopping_bag:
        shopping_bag = ShoppingBag(user_id=user_id)
        db.add(shopping_bag)
        db.commit()
        db.refresh(shopping_bag)

    serialized_bag = jsonable_encoder(shopping_bag)
    
    return JSONResponse(
        content={"shopping_bag": serialized_bag},
        status_code=status.HTTP_200_OK
    )


@router.post("/add_item", status_code=status.HTTP_201_CREATED)
async def add_item_to_bag(
    user_id: int,
    product_id: int,
    product_name: str,
    price: float,
    quantity: int,
    db: db_dependency
):
    # Get or create the shopping bag for the user
    shopping_bag = db.query(ShoppingBag).filter(ShoppingBag.user_id == user_id).first()
    
    if not shopping_bag:
        shopping_bag = ShoppingBag(user_id=user_id)
        db.add(shopping_bag)
        db.commit()
        db.refresh(shopping_bag)

    existing_item = db.query(BagItem).filter(
        BagItem.bag_id == shopping_bag.id,
        BagItem.product_id == product_id,
    ).first()

    if existing_item:
        existing_item.quantity += quantity
        existing_item.total_price = existing_item.price * existing_item.quantity
        db.commit()
        
        serialized_item = jsonable_encoder(existing_item)
        return JSONResponse(
            content={"item": serialized_item},
            status_code=status.HTTP_200_OK
        )

    new_item = BagItem(
        bag_id=shopping_bag.id,
        product_id=product_id,
        product_name=product_name,
        price=price,
        quantity=quantity,
        total_price=price * quantity,
    )
    
    db.add(new_item)
    db.commit()
    
    serialized_new_item = jsonable_encoder(new_item)
    
    return JSONResponse(
        content={"item": serialized_new_item},
        status_code=status.HTTP_201_CREATED
    )


@router.delete("/remove_item", status_code=status.HTTP_200_OK)
async def remove_item_from_bag(
    user_id: int,
    product_id: int,
    db: db_dependency
):
    
    shopping_bag = db.query(ShoppingBag).filter(ShoppingBag.user_id == user_id).first()
    
    if not shopping_bag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopping bag not found"
        )

    item_to_remove = db.query(BagItem).filter(
        BagItem.bag_id == shopping_bag.id,
        BagItem.product_id == product_id,
    ).first()

    if not item_to_remove:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in bag"
        )

    db.delete(item_to_remove)
    db.commit()

    return JSONResponse(
        content={"message": "Item removed successfully"},
        status_code=status.HTTP_200_OK
    )


@router.get("/items", status_code=status.HTTP_200_OK)
async def get_shopping_bag_items(
    user_id: int,
    db: db_dependency = db_dependency,
):
   
    shopping_bag = db.query(ShoppingBag).filter(ShoppingBag.user_id == user_id).first()
    
    if not shopping_bag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopping bag not found"
        )


    items_query = db.query(BagItem).filter(BagItem.bag_id == shopping_bag.id).all()

    if not items_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No items found in the shopping bag"
        )

    serialized_items = jsonable_encoder(items_query)

    return JSONResponse(
        content={"items": serialized_items},
        status_code=status.HTTP_200_OK
    )
