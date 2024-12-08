import uuid
from typing import List

from .common import Base
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from code.app.models.users import UserRegister
from .estate import Estate
from .users_roles import UsersRoles, Roles


class Users(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4())
    name: Mapped[str] = mapped_column(String, nullable=True)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, unique=True)


def get_user(session: Session, username: str) -> Users | None:
    return session.query(Users).filter(Users.username == username).first()


def add_user(session: Session, user: UserRegister, hashed_password: str) -> Users:
    user_database = Users(name=user.name, surname=user.surname, hashed_password=hashed_password, username=user.username)
    session.add(user_database)
    session.commit()
    user_id = session.query(Users).filter(Users.username == user.username).first().id
    estate_id = session.query(Estate).first().id
    user_role = UsersRoles(user_id=user_id, role=Roles.USER, estate_id=estate_id)
    session.add(user_role)
    session.commit()

    return user_database

def get_user_estate_roles(session: Session, user_id: str) -> tuple[str, str]:
    roles = session.query(UsersRoles).filter(UsersRoles.user_id == user_id).first()
    estate_name = session.query(Estate).filter(Estate.id == roles.estate_id).first().name
    role = str(roles.role.value)
    return estate_name, role

