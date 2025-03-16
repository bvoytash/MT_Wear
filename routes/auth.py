import os
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from models.users import User
from security import check_password
from database import db_dependency
from validators.auth import login_dependency

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_access_token(email: str, expires_delta: timedelta):
    encode = {"sub": email}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user_email(access_token: str = Cookie(None)):
    try:
        if access_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )


auth_email_dependency = Annotated[str, Depends(get_current_user_email)]


@router.post("/login")
async def login_for_access_token(
    form_data: login_dependency, db: db_dependency, access_token: str = Cookie(None)
):
    if access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Already logged in"
        )
    user = db.query(User).filter(User.email == form_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    check_password(form_data.password, user.password)
    token = create_access_token(user.email, timedelta(minutes=30))
    response = JSONResponse(content={"detail": "Logged in successfully"})
    response.set_cookie(
        "access_token",
        token,
        max_age=1800,
        domain=None,
        path="/",
        secure=True,
        httponly=True,
        samesite="None",
    )
    return response


@router.post("/logout")
async def logout(email: auth_email_dependency):
    response = JSONResponse(
        content={"detail": "Logged out successfully"}, status_code=200
    )
    response.delete_cookie(key="access_token")
    return response
