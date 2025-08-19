from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    email: str
    password: str


class UserSchema(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True
