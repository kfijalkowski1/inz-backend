from fastapi import FastAPI
from .routers import posts_router
from fastapi.middleware.cors import CORSMiddleware

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