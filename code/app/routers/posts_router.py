from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from code.database.declarations.posts import get_posts, add_post, get_posts_containing
from code.app.models.posts import PostBase
from code.database.utils import get_db
from code.package_utils import logger

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

@router.get("/search/{phrase}")
async def search_posts(phrase: str, db: Session = Depends(get_db)):
    logger.info(f"Searching posts with phrase: {phrase}")
    return get_posts_containing(db, phrase)