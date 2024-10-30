from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Define a data model for a simple item
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    quantity: int


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}


# GET endpoint
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}


# POST endpoint
@app.post("/items/")
def create_item(item: Item):
    return {"item": item}
