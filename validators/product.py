from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Optional
from fastapi import Form, Depends
from enum import Enum


class CreateProductRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100, example="Sample Product")
    description: Optional[str] = Field(default=None, max_length=500, example="This is a sample product description.")
    price: float = Field(gt=0, example=19.99)
    category: str = Field(min_length=1, max_length=50, example="T-Shirts")
    image_url: Optional[str] = Field(default=None, example="path/to/the/image/image.jpg")
    is_active: Optional[bool] = Field(default=True, example=True)
    size: Optional[str] = Field(default=None, max_length=10, example="M")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Sample Product",
                "description": "This is a sample product description.",
                "price": 19.99,
                "category": "T-Shirts",
                "image_url": "path/to/the/image/image.jpg",
                "is_active": True,
                "size": "M",
            }
        }
    }


class UpdateProductRequest(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        example="Updated Product Name",
        description="Name of the product"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        example="Updated product description.",
        description="Description of the product"
    )
    price: Optional[float] = Field(
        None,
        gt=0,
        example=29.99,
        description="Price of the product (must be greater than 0)"
    )
    category: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        example="Updated Category",
        description="Category of the product"
    )
    image_url: Optional[str] = Field(
        None,
        example="path/to/updated/image.jpg",
        description="URL of the product image"
    )
    is_active: Optional[bool] = Field(
        default=True,
        example=False,
        description="Indicates whether the product is active"
    )
    size: Optional[str] = Field(
        None,
        max_length=10,
        example="M",
        description="Size of the product"
    )

    @field_validator("name")
    def validate_name(cls, v):
        if v is not None and (len(v) < 1 or len(v) > 100):
            raise ValueError("Name must be between 1 and 100 characters long")
        return v

    @field_validator("description")
    def validate_description(cls, v):
        if v is not None and len(v) > 500:
            raise ValueError("Description must not exceed 500 characters")
        return v

    @field_validator("price")
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @field_validator("category")
    def validate_category(cls, v):
        if v is not None and (len(v) < 1 or len(v) > 50):
            raise ValueError("Category must be between 1 and 50 characters long")
        return v

    @field_validator("size")
    def validate_size(cls, v):
        if v is not None and len(v) > 10:
            raise ValueError("Size must not exceed 10 characters")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Updated Product Name",
                    "description": "Updated product description.",
                    "price": 29.99,
                    "category": "Updated Category",
                    "image_url": "path/to/updated/image.jpg",
                    "is_active": False,
                    "size": "M",
                }
            ]
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

    model_config = {
        "json_schema_extra": {
            "example": {
                "sort_by": "price",
                "order": "desc",
            }
        }
    }

class FilteringRequest(BaseModel):
    category: Optional[str] = Field(default=None, max_length=50, example="T-Shirts")
    is_active: Optional[bool] = Field(default=None, example=True)
    min_price: Optional[float] = Field(default=None, gt=0, example=10.0)
    max_price: Optional[float] = Field(default=None, gt=0, example=100.0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "category": "T-Shirts",
                "is_active": True,
                "min_price": 10.0,
                "max_price": 100.0,
            }
        }
    }

class UpdateIsActiveRequest(BaseModel):
    is_active: bool = Field(..., example=True)

    model_config = {
        "json_schema_extra": {
            "example": {
                "is_active": True
            }
        }
    }
    

is_active_dependency = Annotated[UpdateIsActiveRequest, Depends()]
sorting_dependency = Annotated[SortingRequest, Depends()]
filtering_dependency = Annotated[FilteringRequest, Depends()]
get_id_dependency = Annotated[ProductIDRequest, Depends()]
create_product_dependency = Annotated[CreateProductRequest, Form()]
update_product_dependency = Annotated[UpdateProductRequest, Form()]
delete_product_dependency = Annotated[DeleteProductRequest, Form()]