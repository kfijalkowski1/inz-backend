from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from code.app.models.estate import Estate
from code.database.declarations.estate import get_all_estates, get_user_estate_info
from code.app.utils.security import get_current_active_user
from code.database.declarations.users import Users as User
from code.database.utils import get_db
from code.package_utils import logger

router = APIRouter(
    prefix="/estates",
    tags=["estates"],
    responses={404: {"description": "Not found"}},
    dependencies=[]
)

@router.get("", response_model=List[Estate])
async def get_estates(db: Session = Depends(get_db)):
    return get_all_estates(db)

@router.get("/mine", response_model=Estate)
def get_user_estate(current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return get_user_estate_info(db, current_user.id)