import datetime

from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    description: str


class PostResponse(PostBase):
    id: str
    created_at: datetime.datetime
    author_name: str
    author_id: str
