from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated, Optional
from fastapi import Form
from fastapi import Depends
from enum import Enum


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


class UpdateProductRequest(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=100, example="Updated Product Name")
    description: Optional[str] = Field(default=None, max_length=500, example="Updated product description.")
    price: Optional[float] = Field(gt=0, example=29.99)
    category: Optional[str] = Field(min_length=1, max_length=50, example="Updated Category")
    image_url: Optional[str] = Field(default=None, example="path/to/updated/image.jpg")
    is_active: Optional[bool] = Field(default=True, example=False)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Updated Product Name",
                "description": "Updated product description.",
                "price": 29.99,
                "category": "Updated Category",
                "image_url": "path/to/updated/image.jpg",
                "is_active": False,
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



class ProductIDRequest(BaseModel):
    product_id: int = Field(gt=0, example=1)




class SortByEnum(str, Enum):
    name = "name"
    price = "price"


class OrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class SortingRequest(BaseModel):
    sort_by: SortByEnum = Field(default=SortByEnum.name, example="name")
    order: OrderEnum = Field(default=OrderEnum.asc, example="asc")

    class Config:
        schema_extra = {
            "example": {
                "sort_by": "price",
                "order": "desc",
            }
        }


class FilteringRequest(BaseModel):
    category: Optional[str] = Field(default=None, max_length=50, example="T-Shirts")
    is_active: Optional[bool] = Field(default=None, example=True)
    min_price: Optional[float] = Field(default=None, gt=0, example=10.0)
    max_price: Optional[float] = Field(default=None, gt=0, example=100.0)

    class Config:
        schema_extra = {
            "example": {
                "category": "T-Shirts",
                "is_active": True,
                "min_price": 10.0,
                "max_price": 100.0,
            }
        }
    


sorting_dependency = Annotated[SortingRequest, Depends()]
filtering_dependency = Annotated[FilteringRequest, Depends()]
get_id_dependency = Annotated[ProductIDRequest, Depends()]
create_product_dependency = Annotated[CreateProductRequest, Form()]
update_product_dependency = Annotated[UpdateProductRequest, Form()]
delete_product_dependency = Annotated[DeleteProductRequest, Form()]