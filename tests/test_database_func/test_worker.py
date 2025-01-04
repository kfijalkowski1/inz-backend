import pytest

from code.database.declarations.worker import get_worker, Department, get_workers, get_estate_managers, is_user_manager, \
    is_user_worker
from code.package_utils.exceptions import DBException, BAD_DEPARTMENT


def test_get_worker(mocked_session):
    worker = get_worker(mocked_session, "5")
    assert worker.user_id == "5"
    assert worker.type == Department.CLEANING
    assert worker.is_manager == False
    assert worker.manager_id == "7"

def test_get_workers_all_departments(mocked_session):
    workers = get_workers(mocked_session, "4")
    assert len(workers) == 2
    assert workers[0].id == "5"
    assert workers[0].name == "Worker"
    assert workers[0].username == "worker_1"
    assert workers[0].type == Department.CLEANING
    assert workers[0].is_manager == False
    assert workers[1].id == "7"
    assert workers[1].name == "Michael"
    assert workers[1].surname == "Scott"

def test_get_workers_one_department(mocked_session):
    workers = get_workers(mocked_session, "4", [Department.OTHER])
    assert len(workers) == 1
    assert workers[0].id == "7"
    assert workers[0].name == "Michael"
    assert workers[0].surname == "Scott"
    assert workers[0].username == "worker_3"
    assert workers[0].type == Department.OTHER
    assert workers[0].is_manager == True

def test_get_workers_bad_department(mocked_session):
    with pytest.raises(DBException) as e:
        get_workers(mocked_session, "4", ["BAD_DEPARTMENT"])
    assert str(e.value) == BAD_DEPARTMENT

def test_get_estate_managers(mocked_session):
    managers = get_estate_managers(mocked_session, "4")
    assert len(managers) == 1
    assert managers[0].id == "7"
    assert managers[0].name == "Michael"
    assert managers[0].surname == "Scott"
    assert managers[0].username == "worker_3"

@pytest.mark.parametrize("user_id, expected", [
    ("5", False),
    ("7", True),
    ("1", False),
    ("4", False)
])
def test_is_user_manager(mocked_session, user_id, expected):
    assert is_user_manager(mocked_session, user_id) == expected

@pytest.mark.parametrize("user_id, expected", [
    ("5", True),
    ("7", True),
    ("1", False),
    ("4", False)
])
def test_is_user_worker(mocked_session, user_id, expected):
    assert is_user_worker(mocked_session, user_id) == expected