from typing import List

from fastapi import APIRouter, HTTPException, Depends

from config import settings
from config.database import get_session
from schema import LoginSchema
import auth
from utils import create_jwt, verify_password


router = APIRouter(
    prefix="/auth",
    tags=['auth'],
)


@router.post("/login")
def login(login: LoginSchema, session=Depends(get_session)):
    db_user = auth.get_user_by_email(session, login.email)
    if not db_user:
        raise HTTPException("User does not exist")

    if not verify_password(login.password, db_user.hash_password):
        raise HTTPException(status_code=403, detail="Wrong password!")

    permission = db_user.permission.permission_type.value

    jwt_token = create_jwt(settings.PRIVATE_KEY, 30, db_user.user_id, permission)
    refresh = create_jwt(settings.PRIVATE_KEY, 30, db_user.user_id, permission)

    return {
        'access_token': jwt_token,
        'refresh_token': refresh,
        'token_type': 'bearer',
    }
