from pydantic import BaseModel, Field
from typing import Annotated, Optional
from fastapi import Form


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
    name: Optional[str] = Field(min_length=1, max_length=100, example="Updated Electronics")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Updated Electronics",
            }
        }
    }


# Dependencies for FastAPI forms
create_category_dependency = Annotated[CreateCategoryRequest, Form()]
update_category_dependency = Annotated[UpdateCategoryRequest, Form()]
