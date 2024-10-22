from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from models.stock import Stock
from bson import ObjectId
from typing import List
import os
from fastapi import status

router = APIRouter()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.VentusSystemDB
stock_collection = db.stocks


# Rota para criar um novo item de estoque
@router.post("/stocks/", response_model=Stock, status_code=status.HTTP_201_CREATED)
async def create_stock(stock: Stock):
    stock_dict = stock.dict()
    result = stock_collection.insert_one(stock_dict)
    stock_dict["_id"] = str(result.inserted_id)
    return stock_dict


@router.get("/stocks/{item_name}", response_model=Stock)
async def get_stock(item_name: str):
    stock = stock_collection.find_one({"item_name": item_name})
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    stock["_id"] = str(stock["_id"])
    return stock

@router.put("/stocks/{item_name}", response_model=Stock)
async def update_stock(item_name: str, updated_stock: Stock):
    result = stock_collection.update_one({"item_name": item_name}, {"$set": updated_stock.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Stock not found")
    stock = stock_collection.find_one({"item_name": item_name})
    stock["_id"] = str(stock["_id"])
    return stock

@router.delete("/stocks/{item_name}")
async def delete_stock(item_name: str):
    result = stock_collection.delete_one({"item_name": item_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Stock not found")
    return {"message": "Stock deleted successfully"}

@router.get("/stocks/", response_model=List[Stock])
async def list_stocks():
    stocks = []
    for stock in stock_collection.find():
        stock["_id"] = str(stock["_id"])
        stocks.append(stock)
    return stocks
