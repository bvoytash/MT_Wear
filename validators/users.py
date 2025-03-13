from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import Form


class CreateUserRequest(BaseModel):
    email: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)

    model_config = {
        "json_schema_extra": {
            "example": {"email": "abv@abv.bg", "password": "client_pass1234"}
        }
    }


class DeleteUserRequest(BaseModel):
    email: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "abv@abv.bg",
                "password": "client_pass1234",
            }
        }
    }


create_user_dependency = Annotated[CreateUserRequest, Form()]
delete_user_dependency = Annotated[DeleteUserRequest, Form()]
