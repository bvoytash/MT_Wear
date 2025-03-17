from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import Form


class LoginRequest(BaseModel):
    email: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)

    model_config = {
        "json_schema_extra": {
            "example": {"email": "abv@abv.bg", "password": "client_pass1234"}
        }
    }


login_dependency = Annotated[LoginRequest, Form()]
