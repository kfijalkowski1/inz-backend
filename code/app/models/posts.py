from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    description: str


class PostResponse(PostBase):
    id: str
    created_at: str
    author_name: str
    author_id: str

    class Config:
        orm_mode = True
