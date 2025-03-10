import os
from argon2 import PasswordHasher
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

ph = PasswordHasher()


def hash_password(password):
    return ph.hash(password)


def check_password(password, hashed_password):
    try:
        return ph.verify(hashed_password, password)
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")
