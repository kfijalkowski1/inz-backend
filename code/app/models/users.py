from pydantic import BaseModel


class User(BaseModel):
    name: str | None
    surname: str | None
    username: str

class UserBase(User):
    name: str | None
    surname: str | None
    username: str
    id: str

class UserRegister(User):
    password: str
