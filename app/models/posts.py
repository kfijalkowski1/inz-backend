from pydantic import BaseModel
from fastapi import UploadFile, File
from typing import List

class PostBase(BaseModel):
    title: str
    description: str


class PostResponse(PostBase):
    id: str
    created_at: str

    class Config:
        orm_mode = True
