from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

# @app.get("/")
# def home():
#     return {"Data": "Testing"}

# @app.get("/about")
# def about():
#     return {"Data": "About"}

inventory = {}

# @app.get("/get-item/{item_id}/{name}")
# def get_item(item_id: int, name: str):
#     return inventory[item_id]

# PATH / ENDPOINT PARAMETER(S)
@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of the item you would like to view")):
    return inventory[item_id]

# QUERY PARAMETER(S)
# @app.get("/get-by-name")
# def get_item(*, name: Optional[str] = None, test: int): # if parameter equal to none this actually meaning is this endpoint query parameter is optional
#     for item_id in inventory:
#         if inventory[item_id]["name"] == name:
#             return inventory[item_id]
#     return {"Data": "Not found"}

@app.get("/get-by-name")
def get_item(name: str = Query(None, title="Name", description="Name of item.", max_length=50, min_length=1)): # if parameter equal to none this actually meaning is this endpoint query parameter is optional
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=400, detail="Item name not found.")

@app.get("/test")
def get_test():
    return "THIS IS WORKING!"

# COMBINE BOTH OF THEM
# @app.get("/get-by-name/{item_id}")
# def get_item(*, item_id: int, name: Optional[str] = None, test: int): # if parameter equal to none this actually meaning is this endpoint query parameter is optional
#     for item_id in inventory:
#         if inventory[item_id].name == name:
#             return inventory[item_id]
#     return {"Data": "Not found"}

# REQUEST BODY & POST METHOD
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exists.")
    
    inventory[item_id] = item
    return inventory[item_id]

# PUT METHOD
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=400, detail="Item ID does not exist.")

    
    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]

# DELETE METHOD
@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete.")):
    if item_id not in inventory:
        raise HTTPException(status_code=400, detail="Item ID does not exist.")

    del inventory[item_id]
    return {"Success": "Item deleted!"}
