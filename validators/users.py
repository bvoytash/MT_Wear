from pydantic import BaseModel, Field, SecretStr, EmailStr
from typing import Annotated
from fastapi import Form


class LoginOrCreateUserRequest(BaseModel):
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


class MakeAdminRequest(BaseModel):
    email: EmailStr = Field(
        min_length=3,
        max_length=64,
        description="User email address",
        example="user@example.com",
    )
    master_password: SecretStr = Field(
        min_length=3,
        max_length=64,
        description="Master password",
        example="SecureP@ssw0rd",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "master_password": "MasterP@ssw0rd",
            }
        }


login_or_create_user_dependency = Annotated[LoginOrCreateUserRequest, Form()]
make_admin_dependency = Annotated[MakeAdminRequest, Form()]
