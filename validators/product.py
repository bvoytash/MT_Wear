from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated, Optional
from fastapi import Form


class CreateProductRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100, example="Sample Product")
    description: Optional[str] = Field(default=None, max_length=500, example="This is a sample product description.")
    price: float = Field(gt=0, example=19.99)
    category: str = Field(min_length=1, max_length=50, example="T-Shirts")
    image_url: Optional[str] = Field(default=None, example="path/to/the/image/image.jpg")
    is_active: Optional[bool] = Field(default=True, example=True)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Sample Product",
                "description": "This is a sample product description.",
                "price": 19.99,
                "category": "T-Shirts",
                "image_url": "path/to/the/image/image.jpg",
                "is_active": True,
            }
        }
    }


class DeleteProductRequest(BaseModel):
    product_id: int = Field(gt=0, example=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "product_id": 1,
            }
        }
    }


create_product_dependency = Annotated[CreateProductRequest, Form()]
delete_product_dependency = Annotated[DeleteProductRequest, Form()]
