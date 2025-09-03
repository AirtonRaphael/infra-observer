from fastapi import Request, HTTPException, Depends, status
from sqlalchemy.orm import joinedload, Session

from models import User


def get_user_by_id(session: Session, user_id: int):
    return session.query(User).options(joinedload(User.permission)).filter_by(user_id=user_id).first()


def get_user_by_email(session: Session, email: str):
    return session.query(User).filter_by(email=email).first()


def get_user_from_headers(request: Request):
    user_id = request.headers.get("x-user-id")
    user_role = request.headers.get("x-user-role")

    if not user_id or not user_role:
        raise HTTPException(status_code=403, detail="Missing user info")

    return {"id": user_id, "role": user_role}


def admin_route(payload=Depends(get_user_from_headers)) -> dict:
    if payload.get('role', '') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid permission')

    return payload
