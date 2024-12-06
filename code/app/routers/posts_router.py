from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from code.database.declarations.users import Users as User

from code.app.utils.security import get_current_active_user
from code.database.declarations.posts import get_posts, add_post, get_posts_containing, get_post, get_user_posts, \
    edit_post_in_db, parse_post_to_response
from code.app.models.posts import PostBase, PostResponse
from code.database.utils import get_db
from code.package_utils import logger

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_active_user)]
)


@router.get("", response_model=List[PostResponse])
async def read_posts(db: Session = Depends(get_db)):
    return [parse_post_to_response(db, found_post) for found_post in get_posts(db)]

@router.post("/add", response_model=PostResponse)
async def create_item(item: PostBase, current_user: Annotated[User, Depends(get_current_active_user)], db_session: Session = Depends(get_db)):
    logger.info(f"Adding post: {item}")
    return parse_post_to_response(db_session, add_post(session=db_session, post=item, user_id=current_user.id))

@router.get("/search/{phrase}", response_model=List[PostResponse])
async def search_posts(phrase: str, db: Session = Depends(get_db)):
    logger.info(f"Searching posts with phrase: {phrase}")
    return [parse_post_to_response(db, found_post) for found_post in get_posts_containing(db, phrase)]

@router.get("/{post_id}", response_model=PostResponse)
async def post(post_id: str, db: Session = Depends(get_db)):
    logger.info(f"Getting post with id: {post_id}")
    return parse_post_to_response(db, get_post(db, post_id))

@router.get("user", response_model=List[PostResponse])
async def user_posts(current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return [parse_post_to_response(db, found_post) for found_post in get_user_posts(db, current_user.id)]

@router.get("user/{post_id}", response_model=bool)
async def user_post(post_id: str, current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    if get_post(db, post_id) is not None and  get_post(db, post_id).author_id == current_user.id:
        return True
    return False

@router.post("/edit/{post_id}", response_model=PostResponse)
async def edit_post(post_id: str, item: PostBase, current_user: Annotated[User, Depends(get_current_active_user)], db_session: Session = Depends(get_db)):
    post_db = get_post(db_session, post_id)
    logger.info("DDDUPPPA") #TODO delete
    if post_db is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post_db.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return parse_post_to_response(db_session, edit_post_in_db(db_session, post_id, item))