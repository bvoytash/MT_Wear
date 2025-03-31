from pydantic import BaseModel, Field
from typing import List, Annotated
from enum import Enum
from fastapi import Form
from validators.shopping_bag import CreateBagItemRequest

class OrderStatus(str, Enum):
    PREPARING = "preparing"
    ACCEPTED = "accepted"
    SENT = "sent"
    CANCELED = "canceled"
    REJECTED = "rejected"

class CreateOrderRequest(BaseModel):
    user_profile_id: int = Field(..., example=123, description="ID of the user profile placing the order")
    items: List[CreateBagItemRequest] = Field(..., min_items=1, description="List of products in the order")
    payment_method: str = Field(..., example="cash", description="Payment method selected for the order")
    is_paid: bool = Field(default=False, example=False, description="Payment status of the order")

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_profile_id": 123,
                "items": [
                    {
                        "product_id": 1,
                        "product_name": "Sample Product",
                        "quantity": 2,
                        "price": 19.99,
                        "size": "M"
                    }
                ],
                "payment_method": "cash",
                "is_paid": False
            }
        }
    }

create_order_dependency = Annotated[CreateOrderRequest, Form()]