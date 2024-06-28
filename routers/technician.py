from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from models.technician import Technician
from bson import ObjectId
from typing import List
import os

router = APIRouter()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.VentusSystemDB
technician_collection = db.technicians

@router.post("/technicians/", response_model=Technician)
async def create_technician(technician: Technician):
    technician_dict = technician.dict()
    result = technician_collection.insert_one(technician_dict)
    technician_dict["_id"] = str(result.inserted_id)
    return technician_dict

@router.get("/technicians/{technician_id}", response_model=Technician)
async def get_technician(technician_id: str):
    technician = technician_collection.find_one({"_id": ObjectId(technician_id)})
    if technician is None:
        raise HTTPException(status_code=404, detail="Technician not found")
    technician["_id"] = str(technician["_id"])
    return technician

@router.put("/technicians/{technician_id}", response_model=Technician)
async def update_technician(technician_id: str, updated_technician: Technician):
    result = technician_collection.update_one({"_id": ObjectId(technician_id)}, {"$set": updated_technician.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Technician not found")
    technician = technician_collection.find_one({"_id": ObjectId(technician_id)})
    technician["_id"] = str(technician["_id"])
    return technician

@router.delete("/technicians/{technician_id}")
async def delete_technician(technician_id: str):
    result = technician_collection.delete_one({"_id": ObjectId(technician_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Technician not found")
    return {"message": "Technician deleted successfully"}

@router.get("/technicians/", response_model=List[Technician])
async def list_technicians():
    technicians = []
    for technician in technician_collection.find():
        technician["_id"] = str(technician["_id"])
        technicians.append(technician)
    return technicians
