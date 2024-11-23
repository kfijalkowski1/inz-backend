import datetime
import uuid

from .common import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import String, ARRAY
from sqlalchemy import DateTime
from sqlalchemy.orm import Session
from typing import List
from code.app.models.posts import PostBase
from code.elastic_utils.queries import get_posts_id_containing


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    author_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[str] = mapped_column(DateTime)
    file_group_paths: Mapped[List[str]] = mapped_column(ARRAY(String), default=[], nullable=True)


def get_posts(session: Session):
    return session.query(Posts).all()

def add_post(session: Session, post: PostBase):
    db_post = Posts(title=post.title, description=post.description, author_id="AUTHOR_ID", created_at=str(datetime.datetime.now()), file_group_paths=[]) # TODO: Add author_id
    session.add(db_post)
    session.commit()
    return db_post

def get_post(session: Session, post_id: int):
    return session.query(Posts).filter(Posts.id == post_id).first()

def get_posts_containing(session: Session, phrase: str):
    posts_ids = get_posts_id_containing(phrase)
    return session.query(Posts).filter(Posts.id.in_(posts_ids)).all()