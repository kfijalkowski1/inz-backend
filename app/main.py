from fastapi import FastAPI

from database.utils import SqlEngine
from .routers import posts_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

connectors = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create the database engine
    connectors["engine"] = SqlEngine()
    yield
    # Clean up the ML models and release the resources
    connectors.clear()

app = FastAPI()

app.include_router(posts_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}