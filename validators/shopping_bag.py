from pydantic import BaseModel, Field
from typing import Annotated, Optional, List
from fastapi import Form

class CreateBagItemRequest(BaseModel):
    product_id: int = Field(..., example=1, description="ID of the product being added to the bag")
    product_name: str = Field(..., min_length=1, max_length=255, example="Sample Product", description="Name of the product")
    quantity: int = Field(default=1, ge=1, example=2, description="Quantity of the product")
    price: float = Field(..., gt=0, example=19.99, description="Price of the product at the time of adding to the bag")

    model_config = {
        "json_schema_extra": {
            "example": {
                "product_id": 1,
                "product_name": "Sample Product",
                "quantity": 2,
                "price": 19.99,
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



class CreateShoppingBagRequest(BaseModel):
    user_id: int = Field(..., example=1, description="ID of the user who owns this shopping bag")
    items: Optional[List[CreateBagItemRequest]] = Field(default=[], description="List of items to be added to the bag")

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "items": [
                    {
                        "product_id": 1,
                        "product_name": "Sample Product",
                        "quantity": 2,
                        "price": 19.99,
                    },
                    {
                        "product_id": 2,
                        "product_name": "Another Product",
                        "quantity": 1,
                        "price": 9.99,
                    },
                ],
            }
        }
    }


# class BagItemResponse(BaseModel):
#     id: int = Field(..., example=1, description="ID of the bag item")
#     product_id: int = Field(..., example=1, description="ID of the product")
#     product_name: str = Field(..., example="Sample Product", description="Name of the product")
#     quantity: int = Field(..., example=2, description="Quantity of the product")
#     price: float = Field(..., example=19.99, description="Price of the product at the time it was added")
#     total_price: float = Field(..., example=39.98, description="Total price (price * quantity)")



#     model_config = {
#         "json_schema_extra": {
#             "example": {
#                 "id": 1,
#                 "user_id": 1,
#                 "items": [
#                     {
#                         "id": 1,
#                         "product_id": 1,
#                         "product_name": "Sample Product",
#                         "quantity": 2,
#                         "price": 19.99,
#                         "total_price": 39.98,
#                     },
#                     {
#                         "id": 2,
#                         "product_id": 2,
#                         "product_name": "Another Product",
#                         "quantity": 1,
#                         "price": 9.99,
#                         "total_price": 9.99,
#                     },
#                 ],
#             }
#         }
#     }


create_bag_item_dependency = Annotated[CreateBagItemRequest, Form()]
update_bag_item_dependency = Annotated[UpdateBagItemRequest, Form()]
create_shopping_bag_dependency = Annotated[CreateShoppingBagRequest, Form()]
