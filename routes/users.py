from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from database import db_dependency
from security import hash_password
from models.users import User
from validators.users import create_user_dependency
from routes.auth import auth_user_dependency, csrf_dependency

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    db: db_dependency,
    create_user_request: create_user_dependency,
    crsf_token: csrf_dependency,
):
    existing_user = db.query(User).filter_by(email=create_user_request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(create_user_request.password)
    user = User(email=create_user_request.email, password=hashed_password)
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
