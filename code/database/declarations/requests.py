import datetime
import uuid

from sqlalchemy import ForeignKey, Enum, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, Session
from enum import Enum as EnumC
from .common import Base
from .users import get_user_estate_id, Users
from .users_roles import UsersRoles
from .worker import Department
from ...app.models.requests import RequestInput, RequestUpdate
from ...elastic_utils.queries import get_requests_id_containing


class Status(EnumC):
    NEW = "nowe"
    IN_PROGRESS = "w trakcie"
    DONE = "zakończone"

class Visibility(EnumC):
    PRIVATE = "prywatne"
    PUBLIC = "publiczne"

class Requests(Base):
    __tablename__ = "requests"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    author_id: Mapped[str] = mapped_column(ForeignKey(Users.id))
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    department: Mapped[Enum] = mapped_column(Enum(Department), nullable=True)
    status: Mapped[Enum] = mapped_column(Enum(Status), default=Status.NEW)
    visibility: Mapped[Enum] = mapped_column(Enum(Visibility), default=Visibility.PRIVATE)
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    assignee_id: Mapped[str] = mapped_column(ForeignKey(Users.id), nullable=True)


def add_request(session, request: RequestInput, author_id: str) -> Requests:
    db_request = Requests(author_id=author_id, title=request.title, description=request.description,
                          start_time=datetime.datetime.now(), department=Department.OTHER)
    session.add(db_request)
    session.commit()
    return db_request

def get_user_requests(session, user_id: str) -> list[Requests]:
    return session.query(Requests).filter(Requests.author_id == user_id).all()

def get_request(session, request_id: str, user_id: str) -> Requests | None:
    user_estate = get_user_estate_id(session, user_id)
    return (session.query(Requests)
            .select_from(Requests)
            .join(UsersRoles, UsersRoles.user_id == Requests.author_id)
            .filter(Requests.id == request_id, UsersRoles.estate_id == user_estate)
            .first())

def get_public_requests(session, user_id: str) -> list[Requests]:
    user_estate = get_user_estate_id(session, user_id)
    return (session.query(Requests)
            .select_from(Requests)
            .join(UsersRoles, UsersRoles.user_id == user_id)
            .filter(Requests.visibility == Visibility.PUBLIC, UsersRoles.estate_id == user_estate)
            .all())

def get_all_requests_admin(session: Session, user_id: str) -> list[Requests]:
    user_estate = get_user_estate_id(session, user_id)
    return (session.query(Requests)
            .select_from(Requests)
            .join(UsersRoles, UsersRoles.user_id == Requests.author_id)
            .filter(UsersRoles.estate_id == user_estate)
            .all())

def update_request_state(session, request: RequestUpdate) -> None:
    enum_status = Status(request.status)
    enum_visibility = Visibility(request.visibility)
    enum_department = Department(request.department)
    if enum_status == Status.DONE:
        session.query(Requests).filter(Requests.id == request.request_id).update({Requests.end_time: datetime.datetime.now()})

    session.query(Requests).filter(Requests.id == request.request_id).update(
        {
            Requests.department: enum_department,
            Requests.status: enum_status,
            Requests.visibility: enum_visibility,
            Requests.assignee_id: request.assignee_id
        })
    session.commit()


def get_requests_containing(session: Session, phrase: str, user_id: str) -> list[Requests]:
    user_estate = get_user_estate_id(session, user_id)
    requests_ids = get_requests_id_containing(phrase)
    return (session.query(Requests)
            .select_from(Requests)
            .join(UsersRoles, UsersRoles.user_id == user_id)
            .filter(Requests.id.in_(requests_ids), UsersRoles.estate_id == user_estate)
            .all())

def get_user_assigned_requests(session: Session, user_id: str) -> list[Requests]:
    ret = session.query(Requests).filter(Requests.assignee_id == user_id).all()
    if ret:
        return ret
    return []