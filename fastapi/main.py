from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()
"""

class Item(BaseModel):
    item: str

items = []

@app.post("/items")
def create_item(item: Item):
    items.append(item.item)
    return item.item


@app.get("/items/{item_id}")
def get_item(item_id: int) -> str:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.get("/items/")
def list_items(limit: int = 10):
    return items[0:limit]

"""

class Item(BaseModel):
    text: str 
    is_done: bool = False

items = []

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return item

@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    

@app.get("/items", response_model=list[Item])
def list_item(limit: int = 10):
    return items[0:limit]

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
