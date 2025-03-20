from pydantic import BaseModel, Field, SecretStr, EmailStr
from typing import Annotated, Optional
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


class UserProfileRequest(BaseModel):
    phone_number: Optional[str] = Field(
        min_length=3,
        max_length=20,
        description="User phone number",
        example="+1234567890",
        regex=r"^\+?\d{3,20}$",
    )
    address: Optional[str] = Field(
        min_length=1,
        max_length=200,
        description="Address",
        example="123 Main St",
    )
    city: Optional[str] = Field(
        min_length=1,
        max_length=50,
        description="City name",
        example="New York",
    )
    postal_code: Optional[str] = Field(
        min_length=2,
        max_length=20,
        description="Postal code",
        example="10001",
        regex=r"^\d{2,20}$",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+1234567890",
                "address": "123 Main St",
                "city": "New York",
                "postal_code": "10001",
            }
        }


login_or_create_user_dependency = Annotated[LoginOrCreateUserRequest, Form()]
make_admin_dependency = Annotated[MakeAdminRequest, Form()]
user_profile_dependency = Annotated[UserProfileRequest, Form()]
