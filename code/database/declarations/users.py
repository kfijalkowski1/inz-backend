import uuid
from .common import Base
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from code.app.models.users import UserBase


class Users(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4())
    name: Mapped[str] = mapped_column(String, nullable=True)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String)


def get_user(session: Session, username: str) -> Users | None:
    return session.query(Users).filter(Users.username == username).first()


def add_user(session: Session, user: UserBase, hashed_password: str) -> Users:
    user_database = Users(name=user.name, surname=user.surname, hashed_password=hashed_password, username=user.username)
    session.add(user_database)
    session.commit()
    return user_database
