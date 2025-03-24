from argon2 import PasswordHasher
from fastapi import HTTPException, status
from os import getenv
from slowapi import Limiter
from slowapi.util import get_remote_address

ph = PasswordHasher()

MASTER_PASSWORD = getenv("MASTER_PASSWORD")
MASTER_PASSWORD_HASH = ph.hash(MASTER_PASSWORD)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
)

limiter = Limiter(
    key_func=get_remote_address,
    strategy="fixed-window",
    storage_uri="memory://",
    enabled=True,
)


def hash_password(password):
    return ph.hash(password)


def check_password(password, hashed_password):
    try:
        return ph.verify(hashed_password, password)
    except:
        raise credentials_exception


def simple_check_password(password, hashed_password):
    try:
        return ph.verify(hashed_password, password)
    except:
        return False
