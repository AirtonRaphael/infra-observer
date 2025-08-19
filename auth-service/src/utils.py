from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from config.settings import PRIVATE_KEY, ALGORITHM


password_context = CryptContext(schemes=["bcrypt"])


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)


def decode_jwt(encoded_jwt):
    return jwt.decode(encoded_jwt, PRIVATE_KEY, algorithms=[ALGORITHM])


def create_jwt(secret_key: str, expire_minutes: int, user_id: int, role: str):
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    }

    encoded_jwt = jwt.encode(payload, secret_key, ALGORITHM)

    return encoded_jwt
