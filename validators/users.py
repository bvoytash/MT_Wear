# from pydantic import BaseModel, Field
# from typing import Annotated
# from fastapi import Form


# class CreateUserRequest(BaseModel):
#     username: str = Field(min_length=1, max_length=50)
#     password: str = Field(min_length=1, max_length=50)
#     email: str = Field(min_length=1, max_length=50)

#     model_config = {
#         "json_schema_extra": {
#             "example": {
#                 "username": "client_username",
#                 "password": "client_pass1234",
#                 "email": "abv@abv.bg",
#             }
#         }
#     }


# class DeleteUserRequest(BaseModel):
#     username: str = Field(min_length=1, max_length=50)
#     password: str = Field(min_length=1, max_length=50)

#     model_config = {
#         "json_schema_extra": {
#             "example": {
#                 "username": "client_username",
#                 "password": "client_pass1234",
#             }
#         }
#     }


# create_user_dependency = Annotated[CreateUserRequest, Form()]
# delete_user_dependency = Annotated[DeleteUserRequest, Form()]
