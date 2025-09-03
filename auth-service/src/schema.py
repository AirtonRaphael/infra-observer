from enum import Enum
from pydantic import BaseModel


class RolesEnum(Enum):
    usuario = "User"
    admin = "Admin"


class LoginSchema(BaseModel):
    email: str
    password: str


class CreateUserSchema(BaseModel):
    username: str
    email: str
    password: str
    role: RolesEnum = RolesEnum.usuario


class UpdateUserSchema(BaseModel):
    username: str
    email: str
    role: RolesEnum = RolesEnum.usuario


class UserSchema(BaseModel):
    user_id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True
