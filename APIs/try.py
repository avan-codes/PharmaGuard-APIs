from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

# Create the FastAPI app
app = FastAPI(
    title="Basic FastAPI App",
    description="A simple FastAPI application",
    version="0.1.0"
)

# Sample database (in-memory)
fake_db = {
    1: {"name": "Item 1", "price": 10.99, "is_offer": False},
    2: {"name": "Item 2", "price": 20.50, "is_offer": True},
}

# Pydantic model for request/response validation
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Get all items
@app.get("/items/")
async def read_items():
    return fake_db

# Get a specific item by ID
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return fake_db[item_id]

# Create a new item
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    new_id = max(fake_db.keys()) + 1
    fake_db[new_id] = item.dict()
    return {"id": new_id, **item.dict()}

# Update an existing item
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    fake_db[item_id] = item.dict()
    return {"id": item_id, **item.dict()}

# Delete an item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    del fake_db[item_id]
    return {"message": "Item deleted successfully"}