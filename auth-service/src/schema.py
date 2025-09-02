from enum import Enum
from pydantic import BaseModel


class PermissionEnum(Enum):
    usuario = "User"
    admin = "Admin"


class LoginSchema(BaseModel):
    email: str
    password: str


class UserSchema(BaseModel):
    user_id: int
    username: str
    email: str
    permission: str

    class Config:
        from_attributes = True
