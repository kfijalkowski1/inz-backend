from fastapi import FastAPI

from code.app.utils.work_arounds import create_admin_if_not_exists, create_estate_if_not_exists, \
    create_workers_if_not_exists
from code.database.utils import SqlEngine, get_db
from code.app.routers import posts_router, security_router, estates_router, workers_router, requests_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer


connectors = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    connectors["engine"] = SqlEngine()
    yield
    connectors.clear()

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(posts_router.router)
app.include_router(security_router.router)
app.include_router(estates_router.router)
app.include_router(workers_router.router)
app.include_router(requests_router.router)

app.add_middleware( # TODO test for prod?
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# workaround for creating estates and admins
create_estate_if_not_exists(get_db())
create_admin_if_not_exists(get_db())
create_workers_if_not_exists(get_db())