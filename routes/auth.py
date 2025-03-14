import os
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from ..models.users import User
from security import check_password
from database import db_dependency

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

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


async def get_current_user(token: token_dependency, db: db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        user = db.query(User).filter(User.email == email).first()
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: oauth_dependency, db: db_dependency):
    user = db.query(User).filter(User.email == form_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    check_password(form_data.password, user.password)
    token = create_access_token(user.email, timedelta(minutes=15))
    return {"access_token": token, "token_type": "bearer"}


auth_user_dependency = Annotated[dict, Depends(get_current_user)]
