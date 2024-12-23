import datetime
import uuid

from .common import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import Session

from .users import get_user_estate_id, Users
from .users_roles import UsersRoles
from ...app.models.requests import RequestComment


class RequestComments(Base):
    __tablename__ = "request_comments"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column(String)
    author_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[str] = mapped_column(DateTime)
    request_id: Mapped[str] = mapped_column(ForeignKey("requests.id"))


def get_request_comments(session: Session, user_id: str, request_id: str):
    user_estate = get_user_estate_id(session, user_id)

    results = (
        session.query(
            RequestComments.id,
            Users.name,
            Users.surname,
            UsersRoles.role,
            RequestComments.created_at,
            RequestComments.content
        )
        .join(UsersRoles, RequestComments.author_id == UsersRoles.user_id)
        .join(Users, RequestComments.author_id == Users.id)
        .filter(
            UsersRoles.estate_id == user_estate,
            RequestComments.request_id == request_id
        ).order_by(RequestComments.created_at.desc()).all()
    )

    return  [
        {
            "id": row.id,
            "author_name": row.name,
            "author_surname": row.surname,
            "author_type": row.role,
            "created_at": row.created_at,
            "content": row.content
        } for row in results
    ]

def add_request_comment(session: Session, request_id: str, comment: str, user_id: str):
    db_comment = RequestComments(content=comment, author_id=user_id,
                    created_at=str(datetime.datetime.now()), request_id=request_id)
    session.add(db_comment)
    session.commit()
    return db_comment