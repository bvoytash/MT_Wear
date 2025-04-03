from fastapi import APIRouter, HTTPException, status, Request
from models.orders import Order, OrderStatus, BagItem
from models.users import UserProfile
import json
from routes.auth import csrf_dependency, auth_user_dependency, auth_admin_dependency
from database import db_dependency
from validators.order import create_order_dependency
from validators.shopping_bag import create_bag_item_dependency
from fastapi.responses import JSONResponse
from models.orders import Order

router = APIRouter(prefix="/orders", tags=["Orders"])
COOKIE_NAME = "guest_shopping_bag"



@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_order_by_user_id (
    user_id: int, db: db_dependency,
    auth_user_dependency: auth_user_dependency,
    ):

     user_profile = db.query(UserProfile).filter_by(user_id=user_id).first()

     if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found."
        )
     
     orders = db.query(Order).filter_by(user_profile_id=user_profile.id).all()

     if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No orders found for this user."
        )
        
     orders_response = [
        {
            "id": order.id,
            "order_number": order.order_number,
            "created": order.created,
            "is_paid": order.is_paid,
            "status": order.status.value,
            "total_price": order.total_price,
        }
        for order in orders
    ]
     return {"orders": orders_response}





@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_order(
    request: Request,
    auth_user_dependency: auth_user_dependency, db: db_dependency,
    # create_order_dependency: create_order_dependency, create_bag_item_dependency: create_bag_item_dependency,
    csrf_dependency: csrf_dependency,
):
    
    cookie_data = request.cookies.get(COOKIE_NAME)
    print(cookie_data)

    if not cookie_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No shopping bag data found.")

    try:
        items = json.loads(cookie_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid shopping bag data.")
    
    user_profile = db.query(UserProfile).filter_by(user_id=auth_user_dependency.id).first()
    if not user_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found.")
    

    #Retrieve selected payment method
    body = await request.json()
    payment_method = body.get("payment_method")
    if payment_method not in ["debit-card", "cash"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payment method.")

    new_order = Order(
        user_profile_id=user_profile.id,
        status=OrderStatus.PREPARING,
        is_paid=False,
    )
    db.add(new_order)
    db.commit()

    new_order.generate_order_number()
    db.commit()

    for item in items:
        bag_item = BagItem(
            order_id=new_order.id,
            product_id=item["product_id"],
            product_name=item["product_name"],
            quantity=item["quantity"],
            price=item["price"],
            size=item["size"],
            total_price=item["price"] * item["quantity"],
        )
        db.add(bag_item)
    
    db.commit()

    response = JSONResponse(
        {"message": "Order created successfully", "order_number": new_order.order_number}
    )
    response.delete_cookie(COOKIE_NAME)

    return response




@router.get("/all_orders", status_code=status.HTTP_200_OK)
async def get_all_orders(db: db_dependency,
                         auth_admin_dependency,
                         ):
    orders = db.query(Order).all()
    if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No orders found."
        )
    orders_response = [
        {
            "id": order.id,
            "order_number": order.order_number,
            "created": order.created,
            "is_paid": order.is_paid,
            "status": order.status.value,
            "total_price": order.total_price,
        }
        for order in orders
    ]

    return {"orders": orders_response}
