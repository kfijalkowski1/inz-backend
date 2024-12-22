from typing import Annotated, List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from code.app.models.requests import RequestCommentInput, RequestComment
from code.app.utils.security import get_current_active_user
from code.database.declarations.requests_comments import add_request_comment, get_request_comments
from code.database.utils import get_db
from code.database.declarations.users import Users

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_active_user)]
)


@router.post("/add_request", response_model=None)
async def add_comment(comment: RequestCommentInput,
                      current_user: Annotated[Users, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return add_request_comment(db, comment.request_id, comment.content, current_user.id)

@router.get("_request/{request_id}")
async def get_comments(request_id: str, current_user: Annotated[Users, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return get_request_comments(db, current_user.id, request_id)