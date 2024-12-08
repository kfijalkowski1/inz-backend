from pydantic import BaseModel


class User(BaseModel):
    name: str | None
    surname: str | None
    username: str

class UserBase(User):
    id: str

class UserRegister(User):
    password: str
    estate_id: str

class UserInfo(UserBase):
    estate_name: str
    role: str