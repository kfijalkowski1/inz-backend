from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from code.app.models.users import UserRegister, UserInfo, UserBase
from code.database.declarations.users import Users as User, add_user, get_user_estate_roles, get_all_estate_users, \
    get_user_name_surname_db
from code.app.models.token import Token
from code.app.utils.security import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, \
    get_current_active_user, get_password_hash
from code.database.declarations.users_roles import Roles
from code.database.utils import get_db

router = APIRouter(
    prefix="/security",
    tags=["security"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db_session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/users/add", response_model=None)
async def create_user(user: UserRegister, db: Session = Depends(get_db)):
    pass_hash = get_password_hash(user.password)
    return add_user(db, user, pass_hash, Roles.USER)

@router.get("/users/me/", response_model=UserInfo)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    estate, role = get_user_estate_roles(db, current_user.id)
    return UserInfo(username=current_user.username, name=current_user.name, surname=current_user.surname,
                    id=current_user.id, estate_name=estate, role=role)


@router.get("/users/all", response_model=list[UserBase])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    Returns users of the admin estate that have role USER
    :param current_user:
    :param db:
    :return:
    """
    estate, role = get_user_estate_roles(db, current_user.id)
    if role != Roles.ADMIN.value:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return get_all_estate_users(db, current_user)

@router.get("/user_name_surname/{user_id}", response_model=str)
async def get_user_name_surname(user_id: str, db: Session = Depends(get_db)):
    return get_user_name_surname_db(db, user_id)