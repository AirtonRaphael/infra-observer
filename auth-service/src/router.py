from typing import List

from fastapi import APIRouter, HTTPException, Depends, status

import auth
from config import settings
from config.database import get_session
from schema import LoginSchema, UserSchema, CreateUserSchema, UpdateUserSchema
from models import User, Roles
from utils import create_jwt, verify_password, get_hashed_password


router = APIRouter()


@router.post("/session")
async def login(login: LoginSchema, session=Depends(get_session)):
    db_user = auth.get_user_by_email(session, login.email)
    if not db_user:
        raise HTTPException("User does not exist")

    if not verify_password(login.password, db_user.hash_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password!")

    user_role = db_user.role.value

    jwt_token = create_jwt(settings.PRIVATE_KEY, 30, db_user.user_id, user_role)
    refresh = create_jwt(settings.PRIVATE_KEY, 30, db_user.user_id, user_role)

    return {
        'access_token': jwt_token,
        'refresh_token': refresh,
        'token_type': 'bearer',
    }


@router.get("/users", response_model=List[UserSchema])
async def list_users(payload=Depends(auth.admin_route), session=Depends(get_session)):
    users = session.query(User).all()

    return users


@router.post("/users", response_model=UserSchema)
async def create_user(new_user: CreateUserSchema, payload=Depends(auth.admin_route), session=Depends(get_session)):
    user_email = new_user.email.lower()
    user = session.query(User).filter_by(email=user_email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists.")

    role = session.query(Roles).filter_by(role=new_user.role).first()

    user = User(
            username=new_user.username,
            email=user_email,
            hash_password=get_hashed_password(new_user.password),
            role_id=role.role_id
            )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.delete("/users")
async def delete_user(user_id: int, payload=Depends(auth.admin_route), session=Depends(get_session)):
    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    session.delete(user)
    session.commit()

    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/users", response_model=UserSchema)
async def update_user(user_id: int, updated_user: UpdateUserSchema, payload=Depends(auth.admin_route), session=Depends(get_session)):
    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not founded.")

    role = session.query(Roles).filter_by(role=updated_user.role).first()

    # TODO Update user password
    user.username = updated_user.username
    user.email = updated_user.email
    user.role_id = role.role_id

    session.commit()
    session.refresh(user)

    return user
