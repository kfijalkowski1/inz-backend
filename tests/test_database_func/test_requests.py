from code.app.models.requests import RequestUpdate
from code.database.declarations.requests import get_user_requests, get_all_requests_admin, get_request, \
    update_request_state, Status, Visibility, get_user_assigned_requests, get_public_requests
from code.database.declarations.worker import Department

"""
Unable to test:
- add_request: mock use SQLLite, and it doesn't support UUID, which is generated while adding request
- get_request_containing: elactic search is used, and it's not mocked
"""

def test_get_user_requests_existing(mocked_session):
    request = get_user_requests(mocked_session, "1")
    assert len(request) == 1
    assert request[0].title == "Test Request"
    assert request[0].description == "Test Request Description"
    assert request[0].author_id == "1"

def test_get_user_requests_not_existing(mocked_session):
    request = get_user_requests(mocked_session, "not_existing")
    assert len(request) == 0

def test_get_request_existing(mocked_session):
    request = get_request(mocked_session, "1", "1")
    assert request.title == "Test Request"
    assert request.description == "Test Request Description"
    assert request.author_id == "1"

def test_get_request_different_estate(mocked_session):
    request = get_request(mocked_session, "1", "3")
    assert request is None

def test_get_request_not_existing(mocked_session):
    request = get_request(mocked_session, "not_existing", "1")
    assert request is None

def test_get_public_requests_existing(mocked_session):
    request = get_user_requests(mocked_session, "1")
    assert len(request) == 1
    assert request[0].title == "Test Request"
    assert request[0].description == "Test Request Description"
    assert request[0].author_id == "1"

    second_request = get_user_requests(mocked_session, "3")
    assert len(second_request) == 1
    assert second_request[0].title == "Test Request 3"
    assert second_request[0].description == "Test Request Description 3"
    assert second_request[0].author_id == "3"

def test_get_all_requests_admin_existing(mocked_session):
    requests = get_all_requests_admin(mocked_session, "4")
    assert len(requests) == 2
    assert requests[0].title == "Test Request"
    assert requests[1].title == "Test Request 2"


def test_update_request_state(mocked_session):
    request = get_request(mocked_session, "1", "1")
    assert request.status == Status.NEW
    assert request.visibility == Visibility.PRIVATE
    assert request.assignee_id is None
    requests_assigned = get_user_assigned_requests(mocked_session, "2")
    assert len(requests_assigned) == 0

    request_update = RequestUpdate(
        request_id="1", status="zakończone", visibility="publiczne", department="konserwacja", assignee_id="2")

    update_request_state(mocked_session, request_update)

    request = get_request(mocked_session, "1", "1")
    assert request.status == Status.DONE
    assert request.visibility == Visibility.PUBLIC
    assert request.department == Department.MAINTEINANCE
    assert request.assignee_id == "2"

    requests_assigned = get_user_assigned_requests(mocked_session, "2")
    assert len(requests_assigned) == 1

    public_req = get_public_requests(mocked_session, "1")
    assert len(public_req) == 1

