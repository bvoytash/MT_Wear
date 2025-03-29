from pydantic import BaseModel, Field, SecretStr, EmailStr, validator, field_validator
from typing import Annotated, Optional
from fastapi import Form
from re import fullmatch


class LoginOrCreateOrUpdateUserRequest(BaseModel):
    email: EmailStr = Field(
        description="User email address",
        example="user@example.com",
    )
    password: SecretStr = Field(
        description="User password",
        example="SecureP@ssw0rd",
    )

    @field_validator("email")
    def validate_email(cls, v):
        if len(v) < 3 or len(v) > 64:
            raise ValueError("Email must be between 3 and 64 characters long")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if len(v.get_secret_value()) < 3 or len(v.get_secret_value()) > 64:
            raise ValueError("Password must be between 3 and 64 characters long")
        return v

    class Config:
        json_schema_extra = {
            "example": {"email": "user@example.com", "password": "SecureP@ssw0rd"}
        }


login_or_create_or_update_user_dependency = Annotated[
    LoginOrCreateOrUpdateUserRequest, Form()
]


class MakeAdminRequest(BaseModel):
    email: EmailStr = Field(
        description="User email address",
        example="user@example.com",
    )
    master_password: SecretStr = Field(
        description="Master password",
        example="MasterP@ssw0rd",
    )

    @field_validator("email")
    def validate_email(cls, v):
        if len(v) < 3 or len(v) > 64:
            raise ValueError("Email must be between 3 and 64 characters long")
        return v

    @field_validator("master_password")
    def validate_master_password(cls, v):
        if len(v.get_secret_value()) < 3 or len(v.get_secret_value()) > 64:
            raise ValueError("Master password must be between 3 and 64 characters long")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "master_password": "MasterP@ssw0rd",
            }
        }


make_or_remove_admin_dependency = Annotated[MakeAdminRequest, Form()]


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

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        if v:
            if len(v) < 3 or len(v) > 20:
                raise ValueError("Phone number must be 3-20 characters")
            if not fullmatch(r"^\+?\d{3,20}$", v):
                raise ValueError("Invalid phone number format")
        return v

    @field_validator("address")
    def validate_address(cls, v):
        if v:
            if len(v) < 1 or len(v) > 200:
                raise ValueError("Address must be 1-200 characters")
        return v

    @field_validator("city")
    def validate_city(cls, v):
        if v:
            if len(v) < 1 or len(v) > 50:
                raise ValueError("City must be 1-50 characters")
        return v

    @field_validator("postal_code")
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


user_profile_dependency = Annotated[UserProfileRequest, Form()]


class ChangePasswordRequest(BaseModel):
    current_password: SecretStr = Field(
        description="Current user password",
        example="SecureP@ssw0rd",
    )
    new_password: SecretStr = Field(
        description="New user password",
        example="NewSecureP@ssw0rd",
    )
    re_password: SecretStr = Field(
        description="Confirm new password",
        example="NewSecureP@ssw0rd",
    )

    @field_validator("current_password")
    def validate_current_password(cls, v):
        if len(v.get_secret_value()) < 3 or len(v.get_secret_value()) > 64:
            raise ValueError(
                "Current password must be between 3 and 64 characters long"
            )
        return v

    @field_validator("new_password")
    def validate_new_password(cls, v):
        if len(v.get_secret_value()) < 3 or len(v.get_secret_value()) > 64:
            raise ValueError("New password must be between 3 and 64 characters long")
        return v

    @field_validator("re_password")
    def validate_re_password(cls, v, values):
        if v is None or values.get("new_password") is None:
            raise ValueError("You must use a valid password and confirm it")

        if v.get_secret_value() != values.get("new_password").get_secret_value():
            raise ValueError("Passwords do not match")

        return v

    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "SecureP@ssw0rd",
                "new_password": "NewSecureP@ssw0rd",
                "re_password": "NewSecureP@ssw0rd",
            }
        }


change_password_dependency = Annotated[ChangePasswordRequest, Form()]
