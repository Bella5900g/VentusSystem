from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from models.financial import Financial
from bson import ObjectId
from typing import List
import os

router = APIRouter()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.VentusSystemDB
financial_collection = db.financials

@router.post("/financials/", response_model=Financial)
async def create_financial(financial: Financial):
    financial_dict = financial.dict()
    result = financial_collection.insert_one(financial_dict)
    financial_dict["_id"] = str(result.inserted_id)
    return financial_dict

@router.get("/financials/{financial_id}", response_model=Financial)
async def get_financial(financial_id: str):
    financial = financial_collection.find_one({"_id": ObjectId(financial_id)})
    if financial is None:
        raise HTTPException(status_code=404, detail="Financial record not found")
    financial["_id"] = str(financial["_id"])
    return financial

@router.put("/financials/{financial_id}", response_model=Financial)
async def update_financial(financial_id: str, updated_financial: Financial):
    result = financial_collection.update_one({"_id": ObjectId(financial_id)}, {"$set": updated_financial.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Financial record not found")
    financial = financial_collection.find_one({"_id": ObjectId(financial_id)})
    financial["_id"] = str(financial["_id"])
    return financial

@router.delete("/financials/{financial_id}")
async def delete_financial(financial_id: str):
    result = financial_collection.delete_one({"_id": ObjectId(financial_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Financial record not found")
    return {"message": "Financial record deleted successfully"}

@router.get("/financials/", response_model=List[Financial])
async def list_financials():
    financials = []
    for financial in financial_collection.find():
        financial["_id"] = str(financial["_id"])
        financials.append(financial)
    return financials
