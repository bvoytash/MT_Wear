from argon2 import PasswordHasher
from fastapi import HTTPException

ph = PasswordHasher()


def hash_password(password):
    return ph.hash(password)


def check_password(password, hashed_password):
    try:
        return ph.verify(hashed_password, password)
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")
