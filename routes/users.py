from os import getenv
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from html import escape
from datetime import timedelta
from database import db_dependency
from security import (
    hash_password,
    MASTER_PASSWORD_HASH,
    check_password,
    simple_check_password,
)
from models.users import User, UserProfile
from validators.users import (
    login_or_create_or_update_user_dependency,
    make_admin_dependency,
    user_profile_dependency,
    change_password_dependency,
)
from routes.auth import auth_user_dependency, csrf_dependency, create_access_token

router = APIRouter(prefix="/users", tags=["users"])

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
COOKIE_DELTA = int(getenv("COOKIE_DELTA"))
COOKIE_MAX_AGE = int(getenv("COOKIE_MAX_AGE"))


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    db: db_dependency,
    form_data: login_or_create_or_update_user_dependency,
    crsf_token: csrf_dependency,
):
    existing_user = db.query(User).filter_by(email=form_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    hashed_password = hash_password(form_data.password.get_secret_value())
    sanitized_email = escape(form_data.email)
    if sanitized_email != form_data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Don't attack the website please",
        )
    user = User(email=sanitized_email, password=hashed_password, profile=UserProfile())
    db.add(user)
    db.commit()
    return JSONResponse(
        content={"detail": "User created successfully"},
        status_code=status.HTTP_201_CREATED,
    )


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_user(
    user: auth_user_dependency,
    db: db_dependency,
    crsf_token: csrf_dependency,
):
    db.delete(user)
    db.commit()
    response = JSONResponse(
        content={"detail": "User deleted successfully"}, status_code=status.HTTP_200_OK
    )
    response.delete_cookie(key="access_token")
    return response


@router.post("/make_admin", status_code=status.HTTP_200_OK)
async def delete_user(
    db: db_dependency,
    crsf_token: csrf_dependency,
    form_data: make_admin_dependency,
):
    check_password(form_data.master_password.get_secret_value(), MASTER_PASSWORD_HASH)
    user = db.query(User).filter_by(email=form_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is already an admin"
        )
    user.is_admin = True
    db.commit()
    return JSONResponse(
        content={"detail": "User is now admin"}, status_code=status.HTTP_200_OK
    )


@router.patch("/profile", status_code=status.HTTP_200_OK)
async def update_profile(
    user: auth_user_dependency,
    db: db_dependency,
    form_data: user_profile_dependency,
    crsf_token: csrf_dependency,
):
    user.profile.phone_number = (
        escape(form_data.phone_number) or user.profile.phone_number
    )
    user.profile.address = escape(form_data.address) or user.profile.address
    user.profile.city = escape(form_data.city) or user.profile.city
    user.profile.postal_code = escape(form_data.postal_code) or user.profile.postal_code
    db.commit()
    return JSONResponse(
        content={"detail": "Profile updated successfully"},
        status_code=status.HTTP_200_OK,
    )


@router.get("/profile", status_code=status.HTTP_200_OK)
async def update_profile(user: auth_user_dependency, crsf_token: csrf_dependency):
    return JSONResponse(
        content={"detail": user.to_dict()}, status_code=status.HTTP_200_OK
    )


@router.post("/change_email")
async def change_email(
    user: auth_user_dependency,
    db: db_dependency,
    crsf_token: csrf_dependency,
    form_data: login_or_create_or_update_user_dependency,
):
    check_password(form_data.password.get_secret_value(), user.password)
    sanitized_email = escape(form_data.email)
    if sanitized_email != form_data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Don't attack the website please",
        )
    if user.email == form_data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New Email is the same as the old one",
        )
    existing_email = db.query(User).filter_by(email=form_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user.email = form_data.email
    db.commit()

    response = JSONResponse(
        content={"detail": "Email changed successfully"}, status_code=status.HTTP_200_OK
    )
    access_token = create_access_token(user.email, timedelta(minutes=COOKIE_DELTA))
    response.set_cookie(
        "access_token",
        access_token,
        max_age=COOKIE_MAX_AGE,
        domain=None,
        path="/",
        secure=True,
        httponly=True,
        samesite="Strict",
    )
    return response


@router.post("/change_password")
async def change_email(
    user: auth_user_dependency,
    db: db_dependency,
    crsf_token: csrf_dependency,
    form_data: change_password_dependency,
):
    check_password(form_data.current_password.get_secret_value(), user.password)
    if simple_check_password(form_data.new_password.get_secret_value(), user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password is the same as the old one",
        )
    hashed_password = hash_password(form_data.new_password.get_secret_value())
    user.password = hashed_password
    db.commit()
    return JSONResponse(
        content={"detail": "Password changed successfully"},
        status_code=status.HTTP_200_OK,
    )
