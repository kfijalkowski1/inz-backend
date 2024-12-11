import uuid
from .common import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Enum, ForeignKey
from enum import Enum as EnumC


class Roles(EnumC):
    ADMIN = "administrator"
    USER = "mieszkaniec"
    WORKER = "pracownik"

class UsersRoles(Base):
    __tablename__ = "users_roles"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    role: Mapped[Roles] = mapped_column(Enum(Roles), nullable=False)
    estate_id: Mapped[str] = mapped_column(ForeignKey("estate.id"))


def get_user_roles(session, user_id):
    return session.query(UsersRoles).filter(UsersRoles.user_id == user_id).first().role