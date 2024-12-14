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

class WorkerRegister(BaseModel):
    user_id: str
    type: str
    manager_id: str
    is_manager: bool

class WorkerInfo(UserBase):
    type: str
    is_manager: bool
    manager_name: str | None
    manager_surname: str | None