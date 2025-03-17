from pydantic import BaseModel, Field
from typing import Annotated, Optional
from fastapi import Form, Depends


class CreateCategoryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100, example="T-Shirts")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "T-Shirts",
            }
        }
    }


class UpdateCategoryRequest(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=100, example="Updated T-Shirts")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Updated T-Shirts",
            }
        }
    }



class CategoryIDRequest(BaseModel):
    category_id: int = Field(gt=0, example=1)





get_id_dependency = Annotated[CategoryIDRequest, Depends()]
create_category_dependency = Annotated[CreateCategoryRequest, Form()]
update_category_dependency = Annotated[UpdateCategoryRequest, Form()]
