from code.app.utils.security import get_password_hash
from code.database.declarations import Users
from code.database.declarations.estate import Estate
from code.database.declarations.users_roles import UsersRoles, Roles


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