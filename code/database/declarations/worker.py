import uuid

from .common import Base
from sqlalchemy.orm import Mapped, Session, aliased
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, Enum, Boolean, text
from enum import Enum as EnumC
from code.package_utils.exceptions import DBException, BAD_WORKER_TYPE
from .users import add_user, get_user_estate_id, Users
from .users_roles import UsersRoles, Roles

from ...app.models.users import WorkerRegister, UserRegister, WorkerInfo


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


def add_worker(session: Session, worker: WorkerRegister) -> Worker:
    try:
        worker_type = Types(worker.type)
    except ValueError:
        raise DBException(BAD_WORKER_TYPE)
    # change user to worker
    session.query(UsersRoles).filter(UsersRoles.user_id == worker.user_id).update({UsersRoles.role: Roles.WORKER})
    if worker.manager_id:
        worker_database = Worker(user_id=worker.user_id, type=worker_type, manager_id=worker.manager_id, is_manager=worker.is_manager)
    else:
        worker_database = Worker(user_id=worker.user_id, type=worker_type, is_manager=worker.is_manager)
    session.add(worker_database)
    session.commit()
    return worker_database


def get_workers(session: Session, admin_id) -> list[WorkerInfo]:
    estate_id = get_user_estate_id(session, admin_id)
    manager_alias = aliased(Users)  # Use an alias for the manager table
    return (
        session.query(
            Users.id,
            Users.name,
            Users.surname,
            Users.username,
            Worker.type,
            Worker.is_manager,
            manager_alias.name.label("manager_name"),
            manager_alias.surname.label("manager_surname")
        )
        .select_from(Worker)
        .join(UsersRoles, UsersRoles.user_id == Worker.user_id)
        .join(Users, Users.id == Worker.user_id)
        .join(manager_alias, manager_alias.id == Worker.manager_id, isouter=True)  # Use the alias for the manager join
        .filter(UsersRoles.estate_id == estate_id)
        .all()
    )



def get_estate_managers(session: Session, admin_id: str) -> list[Users]:
    estate_id = get_user_estate_id(session, admin_id)
    return (session.query(
        Users.id, Users.name, Users.surname, Users.username)
            .select_from(Worker).join(Users, Worker.user_id == Users.id).join(UsersRoles,
                                                                                 Users.id == UsersRoles.user_id)
            .filter(UsersRoles.estate_id == estate_id, Worker.is_manager == True).group_by(Users.id).all())
