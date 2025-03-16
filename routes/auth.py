import os
import secrets
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from models.users import User
from security import check_password
from database import db_dependency
from validators.auth import login_dependency

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
)


def create_access_token(email: str, expires_delta: timedelta):
    encode = {"sub": email}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(db: db_dependency, access_token: str = Cookie(None)):
    try:
        if access_token is None:
            raise credentials_exception
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


def csrf_validator(request: Request):
    cookie_csrf_token = request.cookies.get("csrf_token")
    session_csrf_token = request.session.get("csrf_token")
    if not session_csrf_token == cookie_csrf_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="CSRF validation failed"
        )
    return cookie_csrf_token


auth_user_dependency = Annotated[str, Depends(get_current_user)]
csrf_dependency = Annotated[str, Depends(csrf_validator)]


@router.post("/login")
async def login_for_access_token(
    crsf_token: csrf_dependency,
    form_data: login_dependency,
    db: db_dependency,
    request: Request,
    access_token: str = Cookie(None),
):
    if access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Already logged in"
        )
    user = db.query(User).filter(User.email == form_data.email).first()
    if not user:
        raise credentials_exception
    check_password(form_data.password, user.password)
    csrf_token = secrets.token_urlsafe(32)
    access_token = create_access_token(user.email, timedelta(minutes=30))
    response = JSONResponse(content={"detail": "Logged in successfully"})
    response.set_cookie(
        "access_token",
        access_token,
        max_age=1800,
        domain=None,
        path="/",
        secure=True,
        httponly=True,
        samesite="Lax",
    )
    response.set_cookie(
        "csrf_token",
        csrf_token,
        max_age=1800,
        domain=None,
        path="/",
        secure=True,
        httponly=True,
        samesite="Lax",
    )
    request.session["csrf_token"] = csrf_token
    return response


@router.post("/logout")
async def logout(
    request: Request, user: auth_user_dependency, crsf_token: csrf_dependency
):
    response = JSONResponse(
        content={"detail": "Logged out successfully"}, status_code=200
    )
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="csrf_token")
    if "csrf_token" in request.session:
        del request.session["csrf_token"]
    return response
