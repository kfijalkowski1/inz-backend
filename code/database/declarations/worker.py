import uuid

from .common import Base
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, Enum, Boolean
from enum import Enum as EnumC
from code.package_utils.exceptions import DBException, BAD_WORKER_TYPE
from .users import add_user, get_user_estate_id, Users
from .users_roles import UsersRoles, Roles

from ...app.models.users import WorkerRegister, UserRegister


class Types(EnumC):
    OTHER = "inne"
    MAINTEINANCE = "konserwacja"
    CLEANING = "sprzątanie"
    REPAIR = "naprawa"
    SECURITY = "ochrona"


class Worker(Base):
    __tablename__ = "worker"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True)
    type: Mapped[Types] = mapped_column(Enum(Types), nullable=False)
    manager_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    is_manager: Mapped[bool] = mapped_column(Boolean, default=False)


def get_worker(session: Session, user_id: str) -> Worker | None:
    return session.query(Worker).filter(Worker.user_id == user_id).first()


def add_worker(session: Session, worker: WorkerRegister, admin_user_id, hashed_password) -> Worker:
    try:
        worker_type = Types(worker.type)
    except ValueError:
        raise DBException(BAD_WORKER_TYPE)
    estate_id = get_user_estate_id(session, admin_user_id)
    user_model = UserRegister(name=worker.name, surname=worker.surname, password=worker.password,
                              username=worker.username, estate_id=estate_id)
    user = add_user(session, user_model, hashed_password, Roles.WORKER)
    if worker.manager_id:
        worker_database = Worker(user_id=user.id, type=worker_type, manager_id=worker.manager_id, is_manager=worker.is_manager)
    else:
        worker_database = Worker(user_id=user.id, type=worker_type, is_manager=worker.is_manager)
    session.add(worker_database)
    session.commit()
    return worker_database


def get_workers(session: Session, admin_id) -> list[Worker]:
    estate_id = get_user_estate_id(session, admin_id)
    return session.query(Worker).select_from(Worker).join(UsersRoles).filter(UsersRoles.estate_id == estate_id).all()


def get_estate_managers(session: Session, admin_id: str) -> list[Users]:
    estate_id = get_user_estate_id(session, admin_id)
    return (session.query(
        Users.id, Users.name, Users.surname, Users.username)
            .select_from(Worker).join(Users, Worker.user_id == Users.id).join(UsersRoles,
                                                                                 Users.id == UsersRoles.user_id)
            .filter(UsersRoles.estate_id == estate_id, Worker.is_manager == True).group_by(Users.id).all())
