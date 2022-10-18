from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
	name: str
	price: float
	brand: Optional[str] = None

class UpdateItem(BaseModel):
	name: Optional[str] = None
	price: Optional[float] = None
	brand: Optional[str] = None


"""
@app.get("/")
def home():
	return {"Data": "Testing"}

# Set up a/multiple part parameter
inventory = {
		1: {
			"name": "Milk",
			"price": 3.99,
			"brand": "Yogourt"
		},

		2: {
			"name": "Meat",
			"price": 10.99,
			"brand": "Cow"
		}
	}
"""

inventory = {}

# Set up an end-point that can retrieve based on its 'Id'
@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of the item you'd like to view", gt=0)):
	return inventory[item_id]
"""
# multiple part parameter
@app.get("/get-item/{item_id}/{name}")
def get_item(item_id: int, name: str):
	return inventory[item_id]
"""
"""
# Query parameter
@app.get("/get-by-name")
def get_item(*, name: Optional[str] = None, test: int):
	for item_id in inventory:
		if inventory[item_id]["name"] == name:
			return inventory[item_id]
	return {"Data": "Not found"}
"""
"""
# Combine query parameters and part parameters together
@app.get("/get-by-name/{item_id}")
def get_item(*, item_id: int, name: Optional[str] = None, test: int):
	for item_id in inventory:
		if inventory[item_id].name == name:
			return inventory[item_id]
	return {"Data": "Not found"}
"""

# Get item by name
@app.get("/get-by-name")
def get_item(name: str = Query(None, title="Name", description="Name of item.", max_length=10, min_length=2)):
	for item_id in inventory:
		if inventory[item_id].name == name:
			return inventory[item_id]
	#return {"Data": "Not found"}
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found")

# Request body
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
	if item_id in inventory:
		#return {"Error": "Item ID already exist"}
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item ID already exist")


	inventory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price}
	return inventory[item_id]

# Update 
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
	if item_id not in inventory:
		#return {"Error": "Iten ID does not exist"}
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exist")


	inventory[item_id].update(item)
	return inventory[item_id]

	if item.name != None:
		inventory[item_id].name = item.name

	if item.price != None:
		inventory[item_id].price = item.price

	if item.brand != None:
		inventory[item_id].brand = item.brand

	return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the Item to delete", gt=0)):
	if item_id not in inventory:
		#return {"Error": "ID does not exist"}
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exist")

	del inventory[item_id]
	return {"Success": "Item deleted!"}