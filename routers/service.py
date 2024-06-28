from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from models.service import Service
from bson import ObjectId
from typing import List
import os

router = APIRouter()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.VentusSystemDB
service_collection = db.services

@router.post("/services/", response_model=Service)
async def create_service(service: Service):
    service_dict = service.dict()
    result = service_collection.insert_one(service_dict)
    service_dict["_id"] = str(result.inserted_id)
    return service_dict

@router.get("/services/{service_id}", response_model=Service)
async def get_service(service_id: str):
    service = service_collection.find_one({"_id": ObjectId(service_id)})
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    service["_id"] = str(service["_id"])
    return service

@router.put("/services/{service_id}", response_model=Service)
async def update_service(service_id: str, updated_service: Service):
    result = service_collection.update_one({"_id": ObjectId(service_id)}, {"$set": updated_service.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    service = service_collection.find_one({"_id": ObjectId(service_id)})
    service["_id"] = str(service["_id"])
    return service

@router.delete("/services/{service_id}")
async def delete_service(service_id: str):
    result = service_collection.delete_one({"_id": ObjectId(service_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}

@router.get("/services/", response_model=List[Service])
async def list_services():
    services = []
    for service in service_collection.find():
        service["_id"] = str(service["_id"])
        services.append(service)
    return services
