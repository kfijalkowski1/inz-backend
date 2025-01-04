from code.database.declarations.requests_comments import get_request_comments
from code.database.declarations.users_roles import Roles

"""
Unable to test:
- add_request_comment: mock use SQLLite, and it doesn't support UUID, which is generated while adding request   
"""

def test_get_request_comments_existing(mocked_session):
    comments = get_request_comments(mocked_session, "2", "1")
    assert len(comments) == 1
    assert comments[0]["author_name"] == "Kevin"
    assert comments[0]["author_surname"] == "Scott"
    assert comments[0]["author_type"] == Roles.USER
    assert comments[0]["content"] == "Test Comment"
    assert comments[0]["created_at"] is not None

def test_get_request_comments_not_existing(mocked_session):
    comments = get_request_comments(mocked_session, "2", "not_existing")
    assert len(comments) == 0

def test_get_request_comment_worker_author(mocked_session):
    comments = get_request_comments(mocked_session, "5", "3")
    assert len(comments) == 1
    assert comments[0]["author_name"] == "Worker"
    assert comments[0]["author_type"] == Roles.WORKER
    assert comments[0]["content"] == "Test Comment Worker"
    assert comments[0]["created_at"] is not None

def test_get_request_comment_admin_author(mocked_session):
    comments = get_request_comments(mocked_session, "4", "2")
    assert len(comments) == 1
    assert comments[0]["author_name"] == "Admin"
    assert comments[0]["author_type"] == Roles.ADMIN
    assert comments[0]["content"] == "Test Comment Admin"
    assert comments[0]["created_at"] is not None
