from fastapi import FastAPI
from .routers import posts_router

app = FastAPI()

app.include_router(posts_router.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}