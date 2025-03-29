from fastapi import APIRouter, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database import db_dependency
from models.shopping_bag import ShoppingBag, BagItem
from models.users import UserProfile
from routes.auth import auth_user_dependency
from validators.shopping_bag import create_bag_item_dependency,update_bag_item_dependency, create_shopping_bag_dependency
import json
from os import getenv

router = APIRouter(
    prefix="/shopping_bag",
    tags=["Shopping Bag"]
)

COOKIE_NAME = "guest_shopping_bag"


@router.post("/add_item", status_code=201)
async def add_item_to_bag(
    request: Request,
    request_dependency: create_bag_item_dependency,
    response: Response,
):
    
    cookie_data = request.cookies.get(COOKIE_NAME)
    COOKIE_MAX_AGE = int(getenv("COOKIE_MAX_AGE"))
    items = []

    if cookie_data:
        try:
            items = json.loads(cookie_data)
        except json.JSONDecodeError:
            pass

    for item in items:
        if item["product_id"] == request_dependency.product_id and item.get("size") == request_dependency.size:
            item["quantity"] += request_dependency.quantity
            item["total_price"] = item["price"] * item["quantity"]
            break
    else:
        items.append({
            "product_id": request_dependency.product_id,
            "product_name": request_dependency.product_name,
            "quantity": request_dependency.quantity,
            "price": request_dependency.price,
            "size": request_dependency.size,
            "total_price": request_dependency.price * request_dependency.quantity
        })

    response.set_cookie(
        COOKIE_NAME,  
        json.dumps(items),  
        max_age=COOKIE_MAX_AGE,  
        path="/",  
        domain=None,
        secure=True,  
        httponly=True,  
        samesite="Strict",
)

    response.status_code = status.HTTP_201_CREATED
    response.content = json.dumps({"shopping_bag_items": items})
    return JSONResponse
    

@router.get("/items", status_code=status.HTTP_200_OK)
async def get_shopping_bag_items(
    request: Request,
):

    cookie_data = request.cookies.get(COOKIE_NAME)
    print(cookie_data)
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
    

