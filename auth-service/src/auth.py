from typing import Optional

from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from sqlalchemy.orm import joinedload, Session

from models import User
from utils import decode_jwt


def get_user_by_id(session: Session, user_id: int):

    return session.query(User).options(joinedload(User.permission)).filter_by(user_id=user_id).first()


def get_user_by_email(session: Session, email: str):
    return session.query(User).options(joinedload(User.permission)).filter_by(email=email).first()


class JwtBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        credential = await super(JwtBearer, self).__call__(request)
        if not credential:
            raise HTTPException(status_code=403, detail="Invalid authorization code")

        if not credential.scheme == "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

        token = credential.credentials

        payload = self.validate_jwt(token)
        if not payload:
            raise HTTPException(status_code=403, detail="Invalid token")

        print(payload)

        return payload

    def validate_jwt(self, jwt_token: str) -> object | None:
        try:
            return decode_jwt(jwt_token)
        except ExpiredSignatureError:
            return
        except PyJWTError:
            return


def admin_permission(payload=Depends(JwtBearer())) -> object:
    if payload.get('role', '') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid permission')

    return payload
