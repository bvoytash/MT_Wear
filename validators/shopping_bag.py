from pydantic import BaseModel, Field
from typing import Annotated, Optional, List
from fastapi import Form

class CreateBagItemRequest(BaseModel):
    product_id: int = Field(..., example=1, description="ID of the product being added to the bag")
    product_name: str = Field(..., min_length=1, max_length=255, example="Sample Product", description="Name of the product")
    quantity: int = Field(default=1, ge=1, example=2, description="Quantity of the product")
    price: float = Field(..., gt=0, example=19.99, description="Price of the product at the time of adding to the bag")
    size: Optional[str] = Field(default=None, max_length=10, example="M", description="Size of the product (e.g., S, M, L). Optional field.")


    model_config = {
        "json_schema_extra": {
            "example": {
                "product_id": 1,
                "product_name": "Sample Product",
                "quantity": 2,
                "price": 19.99,
                "size": "M"
            }
        }
    }

class UpdateBagItemRequest(BaseModel):
    quantity: Optional[int] = Field(default=None, ge=1, example=3, description="Updated quantity of the product")

    model_config = {
        "json_schema_extra": {
            "example": {
                "quantity": 3,
            }
        }
    }



create_bag_item_dependency = Annotated[CreateBagItemRequest, Form()]
update_bag_item_dependency = Annotated[UpdateBagItemRequest, Form()]
