from typing import Annotated, List, Optional, Union

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from code.app.models.requests import RequestInput, RequestInfo, RequestUpdate, RequestCommentInput, RequestComment
from code.app.utils.security import get_current_active_user
from code.database.declarations.requests import add_request, get_user_requests, get_public_requests, \
    get_request, Status, update_request_state, \
    get_requests_containing, get_user_assigned_requests, get_all_requests_admin
from code.database.declarations.requests_comments import RequestComments, add_request_comment, get_request_comments
from code.database.declarations.users_roles import get_user_roles, Roles
from code.database.declarations.worker import is_user_manager, is_user_worker
from code.database.utils import get_db
from code.database.declarations.users import Users, get_user_name_surname_db

router = APIRouter(
    prefix="/requests",
    tags=["requests"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_active_user)]
)


@router.post("/add", response_model=None)
async def add(request_info: RequestInput, current_user: Annotated[Users, Depends(get_current_active_user)],
              db: Session = Depends(get_db)):
    return add_request(db, request_info, current_user.id)


@router.get("/all", response_model=List[RequestInfo])
async def get_all_requests(current_user: Annotated[Users, Depends(get_current_active_user)],
                           db: Session = Depends(get_db)):
    if get_user_roles(db, current_user.id) == Roles.ADMIN or is_user_worker(db, current_user.id):
        return get_all_requests_admin(db, current_user.id)
    public_requests = set(get_public_requests(db, current_user.id))
    user_requests = set(get_user_requests(db, current_user.id))
    return public_requests.union(user_requests)


@router.get("/user", response_model=List[RequestInfo])
async def get_cur_user_requests(current_user: Annotated[Users, Depends(get_current_active_user)],
                                db: Session = Depends(get_db)):
    return get_user_requests(db, current_user.id)

@router.post("/update", response_model=None)
async def set_department(request_update: RequestUpdate, current_user: Annotated[Users, Depends(get_current_active_user)],
                         db: Session = Depends(get_db)):
    if (get_user_roles(db, current_user.id) == Roles.ADMIN) or is_user_worker(db, current_user.id):
        return update_request_state(db, request_update)
    raise HTTPException(status_code=403, detail="Not enough permissions")


@router.get("/{request_id}", response_model=Optional[RequestInfo])
async def get_request_(request_id: str, current_user: Annotated[Users, Depends(get_current_active_user)],
                       db: Session = Depends(get_db)):
    return get_request(db, request_id, current_user.id)

@router.get("/search/{phrase}", response_model=List[RequestInfo])
async def search_posts(phrase: str,current_user: Annotated[Users, Depends(get_current_active_user)],
                       db: Session = Depends(get_db)):
    return get_requests_containing(db, phrase, current_user.id)

@router.post("/add_comment", response_model=RequestComment)
async def add_comment(request_id: str, comment: RequestCommentInput,
                      current_user: Annotated[Users, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return add_request_comment(db, request_id, comment, current_user.id)

@router.get("/comments/{request_id}", response_model=List[RequestComment])
async def get_comments(request_id: str, current_user: Annotated[Users, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return get_request_comments(db, current_user.id, request_id)