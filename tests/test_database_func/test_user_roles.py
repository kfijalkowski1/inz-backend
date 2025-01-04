from code.database.declarations.users_roles import get_user_roles, Roles


def test_get_user_roles_user(mocked_session):
    role = get_user_roles(mocked_session, "1")
    assert role == Roles.USER

def test_get_user_roles_admin(mocked_session):
    role = get_user_roles(mocked_session, "4")
    assert role == Roles.ADMIN

def test_get_user_roles_worker(mocked_session):
    role = get_user_roles(mocked_session, "5")
    assert role == Roles.WORKER