from pydantic import BaseModel, Field, SecretStr, EmailStr, validator
from typing import Annotated, Optional
from fastapi import Form
from re import fullmatch


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


class UserProfileRequest(BaseModel):
    phone_number: Optional[str] = Field(
        description="User phone number",
        example="+1234567890",
    )
    address: Optional[str] = Field(
        description="Address",
        example="123 Main St",
    )
    city: Optional[str] = Field(
        description="City name",
        example="New York",
    )
    postal_code: Optional[str] = Field(
        description="Postal code",
        example="10001",
    )

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if v:
            if len(v) < 3 or len(v) > 20:
                raise ValueError("Phone number must be 3-20 characters")
            if not fullmatch(r"^\+?\d{3,20}$", v):
                raise ValueError("Invalid phone number format")
        return v

    @validator("address")
    def validate_address(cls, v):
        if v:
            if len(v) < 1 or len(v) > 200:
                raise ValueError("Address must be 1-200 characters")
        return v

    @validator("city")
    def validate_city(cls, v):
        if v:
            if len(v) < 1 or len(v) > 50:
                raise ValueError("City must be 1-50 characters")
        return v

    @validator("postal_code")
    def validate_postal_code(cls, v):
        if v:
            if len(v) < 2 or len(v) > 20:
                raise ValueError("Postal code must be 2-20 characters")
            if not fullmatch(r"^\d{2,20}$", v):
                raise ValueError("Invalid postal code format")
        return v

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
