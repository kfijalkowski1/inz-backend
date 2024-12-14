from typing import Annotated, List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from code.app.models.users import WorkerInfo, WorkerRegister, UserBase
from code.app.utils.security import get_current_active_user
from code.database.declarations.users_roles import Roles, get_user_roles
from code.database.declarations.worker import add_worker, get_workers, Types, get_estate_managers
from code.database.utils import get_db
from code.database.declarations.users import Users

router = APIRouter(
    prefix="/workers",
    tags=["workers"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_active_user)]
)


@router.post("/add", response_model=None)
async def add(worker_info: WorkerRegister, current_user: Annotated[Users, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    if get_user_roles(db, current_user.id) != Roles.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return add_worker(db, worker_info)


@router.get("/all", response_model=List[WorkerInfo])
async def get_all_workers(current_user: Annotated[Users, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    if get_user_roles(db, current_user.id) != Roles.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return get_workers(db, current_user.id)

@router.get("/types", response_model=List[str])
async def get_types():
    return [worker_type.value for worker_type in Types]

@router.get("/managers", response_model=List[UserBase])
async def get_managers(current_user: Annotated[Users, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return get_estate_managers(db, current_user.id)
