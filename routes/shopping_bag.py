from fastapi import APIRouter, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database import db_dependency
from models.shopping_bag import ShoppingBag, BagItem, Order, OrderStatus
from models.users import UserProfile
from routes.auth import auth_user_dependency
from validators.shopping_bag import create_bag_item_dependency,update_bag_item_dependency, create_shopping_bag_dependency
import json
from datetime import datetime

router = APIRouter(
    prefix="/shopping_bag",
    tags=["Shopping Bag"]
)

COOKIE_NAME = "guest_shopping_bag"


@router.post("/add_item", status_code=status.HTTP_201_CREATED)
async def add_item_to_bag(
    request: create_bag_item_dependency,
    response: Response,
):
    cookie_data = response.cookies.get(COOKIE_NAME)
    if cookie_data:
        try:
            items = json.loads(cookie_data)
        except json.JSONDecodeError:
            items = []
    else:
        items = []

    for item in items:
        if item["product_id"] == request.product_id and item.get("size") == request.size:
            item["quantity"] += request.quantity
            item["total_price"] = item["price"] * item["quantity"]
            break
    else:
        items.append({
            "product_id": request.product_id,
            "product_name": request.product_name,
            "quantity": request.quantity,
            "price": request.price,
            "size": request.size,
            "total_price": request.price * request.quantity
        })

    response.set_cookie(key=COOKIE_NAME, value=json.dumps(items), httponly=True)
    return JSONResponse(
        content={"shopping_bag_items": items},
        status_code=status.HTTP_201_CREATED
    )
    


@router.delete("/remove_item", status_code=status.HTTP_200_OK)
async def remove_item_from_bag(
    product_id: int,
    size: str,
    response: Response,
):

    cookie_data = response.cookies.get(COOKIE_NAME)

    if not cookie_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found in the shopping bag")
    try:
        items = json.loads(cookie_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid cookie data")


    updated_items = [item for item in items if not (item["product_id"] == product_id and item["size"] == size)]
    
    response.set_cookie(key=COOKIE_NAME, value=json.dumps(updated_items), httponly=True)

    return JSONResponse(
        content={"detail": "Item removed successfully"},
        status_code=status.HTTP_200_OK
    )


@router.get("/items", status_code=status.HTTP_200_OK)
async def get_shopping_bag_items(
    request: Request,
):

    cookie_data = request.cookies.get(COOKIE_NAME)

    if not cookie_data:
        return {"items": []}

    try:
        items = json.loads(cookie_data)
        return JSONResponse(
            content={"items": items},
            status_code=status.HTTP_200_OK
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid cookie data")
    

@router.post("/checkout", status_code=status.HTTP_201_CREATED)
async def checkout_shopping_bag(
    user_profile_id: int,
    request: Request,
    response: Response,
    db: db_dependency,
    auth_user_dependency: auth_user_dependency
):

    cookie_data = request.cookies.get(COOKIE_NAME)

    if not cookie_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Shopping bag is empty")

    try:
        items = json.loads(cookie_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid cookie data")


    user_profile = db.query(UserProfile).filter(UserProfile.id == user_profile_id).first()
    
    if not user_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")

    new_shopping_bag = ShoppingBag()
    db.add(new_shopping_bag)
    db.commit()

    for item in items:
        new_item = BagItem(
            bag_id=new_shopping_bag.id,
            product_id=item["product_id"],
            product_name=item["product_name"],
            quantity=item["quantity"],
            price=item["price"],
            size=item.get("size"),
            total_price=item["total_price"]
        )
        db.add(new_item)

    db.commit()

    order_number = f"ORD-{new_shopping_bag.id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    new_order = Order(
        user_profile_id=user_profile_id,
        shopping_bag_id=new_shopping_bag.id,
        created=datetime.utcnow(),
        order_number=order_number,
        is_paid=False,
        status=OrderStatus.PREPARING
    )
    
    db.add(new_order)
    db.commit()

    response.delete_cookie(COOKIE_NAME)

    return JSONResponse(
        content={"detail":"Shopping bag successfully checked out and linked to an order"},
        status_code=status.HTTP_201_CREATED
    )
