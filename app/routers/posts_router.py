from fastapi import APIRouter, HTTPException
from app.utils import logger

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


fake_items_db = [
    {"id": "1", "title": "Item1", "description": "Item1 description", "date": "2021-01-01"},
    {"id": "2", "title": "Item2", "description": "Item2 description", "date": "2021-01-02"},
    {"id": "3", "title": "Item3", "description": "Item3 description", "date": "2021-01-03"},
    {"id": "4", "title": "Item4", "description": "Item4 description", "date": "2021-01-04"},
    {"id": "5", "title": "Item5", "description": "Item5 description", "date": "2021-01-05"},
]


@router.get("/")
async def read_items():
    logger.info("Reading items")
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    item = next((item for item in fake_items_db if item["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/")
async def create_item(item: dict):
    logger.info(f"Creating item: {item}")
    fake_items_db.append(item)
    return item