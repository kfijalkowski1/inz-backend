from code.app.models.users import UserRegister
from code.database.declarations.users import Users, get_user, add_user, get_user_estate_roles, get_all_estate_users, \
    get_user_estate_id, get_user_name_surname_db
from code.database.declarations.users_roles import Roles


def test_users_get_user_existing(mocked_session):
    user = get_user(mocked_session, "dwight")
    assert user.name == "Dwight"
    assert user.id == '2'
    assert user.hashed_password == "hashed_password"

def test_users_get_user_not_existing(mocked_session):
    user = get_user(mocked_session, "not_existing")
    assert user is None

# Unable to test bcs, mock use SQLLite, and it doesn't support UUID, which is generated while adding user
# def test_add_user(mocked_session):
#     user = UserRegister(name="testName", surname="testSurname", username="test", password="test", estate_id="1")
#     add_user(mocked_session, user, "hash", Roles.USER)
#     user = get_user(mocked_session, "test")
#     assert user.name == "testName"
#     assert user.surname == "testSurname"

def test_get_user_estate_roles(mocked_session):
    estate, role = get_user_estate_roles(mocked_session, "2")
    assert estate == "Test Estate"
    assert role == Roles.USER.value

def test_all_estate_user(mocked_session):
    cur_user = get_user(mocked_session, "admin")
    users = get_all_estate_users(mocked_session, cur_user)
    assert len(users) == 2
    assert users[0].name == "Kevin"
    assert users[1].name == "Dwight"

def test_get_user_estate_id(mocked_session):
    estate_id = get_user_estate_id(mocked_session, "2")
    assert estate_id == "1"

def test_get_user_name_surname_db(mocked_session):
    name_surname = get_user_name_surname_db(mocked_session, "2")
    assert name_surname == "Dwight, Schrute"