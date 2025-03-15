from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from database import db_dependency
from security import check_password, hash_password
from models.users import User
from validators.users import create_user_dependency
from routes.auth import auth_user_dependency, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def add_user(db: db_dependency, create_user_request: create_user_dependency):
    existing_user = db.query(User).filter_by(email=create_user_request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(create_user_request.password)
    user = User(email=create_user_request.email, password=hashed_password)
    db.add(user)
    db.commit()
    return JSONResponse(
        content={"detail": "User created successfully"}, status_code=201
    )


# endpoint usage
@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_user(email: auth_user_dependency, db: db_dependency):
    if email:
        user = db.query(User).filter(User.email == email).first()
        if user:
            db.delete(user)
            db.commit()
            return JSONResponse(
                content={"detail": "User deleted successfully"}, status_code=200
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )


# page usage
@router.delete("/delete-page")
async def delete_user2(request: Request, db: db_dependency):
    try:
        email = await get_current_user(
            request.cookies.get("access_token")
        )  # this can fail
        user = db.query(User).filter(User.email == email).first()  # this can fail
        db.delete(user)
        db.commit()
        return JSONResponse(
            content={"detail": "User deleted successfully"}, status_code=200
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
