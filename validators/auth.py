from pydantic import BaseModel, Field, SecretStr, EmailStr
from typing import Annotated
from fastapi import Form


class LoginRequest(BaseModel):
    email: EmailStr = Field(
        min_length=3,
        max_length=64,
        description="User email address",
        example="user@example.com",
    )
    password: SecretStr = Field(
        min_length=3,
        max_length=64,
        description="User password",
        example="SecureP@ssw0rd",
    )

    class Config:
        json_schema_extra = {
            "example": {"email": "user@example.com", "password": "SecureP@ssw0rd"}
        }


login_dependency = Annotated[LoginRequest, Form()]
