import uuid
from .common import Base
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column
from sqlalchemy import String


class Estate(Base):
    __tablename__ = "estate"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)


def get_all_estates(session: Session):
    return session.query(Estate).all()

def get_user_estate_info(session: Session, user_id: str):
    estate = session.query(Estate).join("users_roles").filter("users_roles.user_id" == user_id).first()
    return estate


