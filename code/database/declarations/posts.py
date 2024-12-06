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
from code.app.models.posts import PostBase, PostResponse
from code.elastic_utils.queries import get_posts_id_containing
from code.database.declarations.users import Users as User


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

def add_post(session: Session, post: PostBase, user_id: str):
    db_post = Posts(title=post.title, description=post.description, author_id=user_id, created_at=str(datetime.datetime.now()), file_group_paths=[])
    session.add(db_post)
    session.commit()
    return db_post

def get_post(session: Session, post_id: str) -> Posts | None:
    return session.query(Posts).filter(Posts.id == post_id).first()

def get_user_posts(session: Session, user_id: str):
    return session.query(Posts).filter(Posts.author_id == user_id).all()

def get_posts_containing(session: Session, phrase: str):
    posts_ids = get_posts_id_containing(phrase)
    return session.query(Posts).filter(Posts.id.in_(posts_ids)).all()

def edit_post_in_db(session: Session, post_id: str, post: PostBase):
    db_post = get_post(session, post_id)
    db_post.title = post.title
    db_post.description = post.description
    db_post.created_at = str(datetime.datetime.now())
    session.commit()
    return db_post


def parse_post_to_response(session: Session, post: Posts) -> PostResponse:
    author = session.query(User).filter(User.id == post.author_id).first()
    author_name = f"{author.surname}, {author.name}"
    return PostResponse(id=post.id, title=post.title, description=post.description,
                        created_at=str(post.created_at), author_name=author_name, author_id=post.author_id)