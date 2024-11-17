from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database.declarations.posts import get_posts, add_post
from app.models.posts import PostBase
from database.utils import get_db
from package_utils import logger

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def read_posts(db: Session = Depends(get_db)):
    logger.info("Reading items")
    return get_posts(db)

@router.post("/add")
async def create_item(item: PostBase, db: Session = Depends(get_db)):
    logger.info(f"Creating item: {item}")
    return add_post(session=db, post=item)