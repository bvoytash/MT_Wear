from argon2 import PasswordHasher
from fastapi import HTTPException, status
from os import getenv

ph = PasswordHasher()

MASTER_PASSWORD = getenv("MASTER_PASSWORD")
MASTER_PASSWORD_HASH = ph.hash(MASTER_PASSWORD)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
)


def hash_password(password):
    return ph.hash(password)


def check_password(password, hashed_password):
    try:
        return ph.verify(hashed_password, password)
    except:
        raise credentials_exception
