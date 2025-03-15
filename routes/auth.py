import os
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import RedirectResponse, JSONResponse
from jose import jwt, JWTError
from pydantic import BaseModel
from models.users import User
from security import check_password
from database import db_dependency

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="login")

token_dependency = Annotated[str, Depends(oauth2_bearer)]
oauth_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(email: str, expires_delta: timedelta):
    encode = {"sub": email}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: token_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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


# for endpoint usage
auth_user_dependency = Annotated[str, Depends(get_current_user)]


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: oauth_dependency, db: db_dependency):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    check_password(form_data.password, user.password)
    token = create_access_token(user.email, timedelta(minutes=15))
    return JSONResponse(
        content={"access_token": token, "token_type": "bearer"}, status_code=200
    )


@router.post("/logout")
async def logout():
    response = JSONResponse(
        content={"detail": "Logged out successfully"}, status_code=200
    )
    response.delete_cookie(key="access_token")
    return response
