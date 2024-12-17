from code.app.utils.security import get_password_hash
from code.database.declarations import Users
from code.database.declarations.estate import Estate
from code.database.declarations.users_roles import UsersRoles, Roles
from code.database.declarations.worker import Department, Worker
from code.package_utils import logger


def create_admin_if_not_exists(session_g):
    session = next(session_g)
    admin = session.query(Users).filter(Users.username == "admin").first()
    if admin is None:
        hashed_pass = get_password_hash("pass")
        session.add(Users(name="admin", surname="admin", hashed_password=hashed_pass, username="admin"))
        session.commit()
        user_id = session.query(Users).filter(Users.username == "admin").first().id
        estate_id = session.query(Estate).first().id
        user_role = UsersRoles(user_id=user_id, role=Roles.ADMIN, estate_id=estate_id)
        session.add(user_role)
        session.commit()
        return
    return

def create_estate_if_not_exists(session_g):
    session = next(session_g)
    estate = session.query(Estate).first()
    if estate is None:
        session.add(Estate(name="Testowa spółdzielnia", description="Testowa spółdzielnia mieszkaniowa"))
        session.commit()
        logger.info("Estate created")
        return
    logger.info("Estate already exists")

def create_workers_if_not_exists(session_g):
    session = next(session_g)
    for (username, department) in [("kier1", Department.OTHER), ("worker-r1", Department.REPAIR),
                                   ("worker-r2", Department.REPAIR), ("worker-c1", Department.CLEANING),
                                   ("worker-c2", Department.CLEANING), ("worker-m1", Department.MAINTEINANCE),
                                   ("worker-m2", Department.MAINTEINANCE), ("worker-s1", Department.SECURITY),
                                   ("worker-s2", Department.SECURITY)]:
        worker = session.query(Users).filter(Users.username == username).first()
        if worker is None:
            hashed_pass = get_password_hash("pass")
            session.add(Users(name=f"{username}-name", surname=f"{username}-surname", hashed_password=hashed_pass, username=username))
            session.commit()
            user_id = session.query(Users).filter(Users.username == username).first().id
            estate_id = session.query(Estate).first().id
            user_role = UsersRoles(user_id=user_id, role=Roles.WORKER, estate_id=estate_id)
            session.add(user_role)
            session.commit()
            session.add(Worker(user_id=user_id, type=department, is_manager=False))
            session.commit()