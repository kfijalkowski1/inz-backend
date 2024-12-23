import datetime

from pydantic import BaseModel

class RequestInput(BaseModel):
    title: str
    description: str

class RequestInfo(RequestInput):
    id: str
    author_id: str | None
    title: str
    description: str
    department: str | None
    status: str
    start_time: datetime.datetime
    end_time: datetime.datetime | None
    assignee_id: str | None
    visibility: str

class RequestUpdate(BaseModel):
    request_id: str
    department: str
    status: str
    visibility: str
    assignee_id: str


class RequestCommentInput(BaseModel):
    content: str
    request_id: str

class RequestComment(RequestCommentInput):
    id: str
    author_name: str
    author_surname: str
    created_at: datetime.datetime
    author_type: str
    content: str