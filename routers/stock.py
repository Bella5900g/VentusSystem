from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from models.stock import Stock
from bson import ObjectId
from typing import List
import os

router = APIRouter()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.VentusSystemDB
stock_collection = db.stocks

@router.post("/stocks/", response_model=Stock)
async def create_stock(stock: Stock):
    stock_dict = stock.dict()
    result = stock_collection.insert_one(stock_dict)
    stock_dict["_id"] = str(result.inserted_id)
    return stock_dict

@router.get("/stocks/{stock_name}", response_model=Stock)
async def get_stock(stock_name: str):
    stock = stock_collection.find_one({"name": stock_name})
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    stock["_id"] = str(stock["_id"])
    return stock

@router.put("/stocks/{stock_name}", response_model=Stock)
async def update_stock(stock_name: str, updated_stock: Stock):
    result = stock_collection.update_one({"name": stock_name}, {"$set": updated_stock.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Stock not found")
    stock = stock_collection.find_one({"name": stock_name})
    stock["_id"] = str(stock["_id"])
    return stock

@router.delete("/stocks/{stock_name}")
async def delete_stock(stock_name: str):
    result = stock_collection.delete_one({"name": stock_name})
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
