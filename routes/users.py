# from fastapi import APIRouter, Request, HTTPException, status
# from fastapi.responses import JSONResponse
# from database import db_dependency
# from security import check_password, MASTER_PASSWORD_HASH, hash_password
# from models.users import User
# from validators import create_user_dependency, delete_user_dependency

# router = APIRouter(prefix="/users", tags=["users"])


# @router.post("/create", status_code=status.HTTP_201_CREATED)
# async def add_user(db: db_dependency, create_user_request: create_user_dependency):
#     existing_user = (
#         db.query(User).filter_by(username=create_user_request.username).first()
#     )
#     if existing_user:
#         raise HTTPException(status_code=400, detail="User already exists")
#     hashed_password = hash_password(create_user_request.password)
#     user = User(username=create_user_request.username, password=hashed_password)
#     db.add(user)
#     db.commit()
#     return JSONResponse(
#         content={"detail": "User created successfully"}, status_code=201
#     )


# @router.delete("/delete", status_code=status.HTTP_200_OK)
# async def delete_user(db: db_dependency, delete_user_request: delete_user_dependency):
#     user = db.query(User).filter_by(username=delete_user_request.username).first()
#     if user:
#         db.delete(user)
#         db.commit()
#         return JSONResponse(
#             content={"detail": "User deleted successfully"}, status_code=200
#         )
#     else:
#         raise HTTPException(status_code=404, detail="User not found")
