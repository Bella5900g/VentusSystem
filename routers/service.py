from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from models.service import Service
from bson import ObjectId
from typing import List
import os
from fastapi import status

router = APIRouter()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.VentusSystemDB
service_collection = db.services


# Rota para criar um novo serviço
@router.post("/services/", response_model=Service, status_code=status.HTTP_201_CREATED)
async def create_service(service: Service):
    service_dict = service.dict()
    result = service_collection.insert_one(service_dict)
    service_dict["_id"] = str(result.inserted_id)
    return service_dict


# Rota para consultar um serviço pelo tipo
@router.get("/services/{type}", response_model=Service)
async def get_service(type: str):
    service = service_collection.find_one({"type": type})
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    service["_id"] = str(service["_id"])  # Converte ObjectId para string
    return service

# Rota para atualizar um serviço pelo tipo
@router.put("/services/{type}", response_model=Service)
async def update_service(type: str, updated_service: Service):
    result = service_collection.update_one({"type": type}, {"$set": updated_service.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    service = service_collection.find_one({"type": type})
    service["_id"] = str(service["_id"])  # Converte ObjectId para string
    return service

# Rota para excluir um serviço pelo tipo
@router.delete("/services/{type}")
async def delete_service(type: str):
    result = service_collection.delete_one({"type": type})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}

# Rota para listar todos os serviços
@router.get("/services/", response_model=List[Service])
async def list_services():
    services = []
    for service in service_collection.find():
        service["_id"] = str(service["_id"])  # Converte ObjectId para string
        services.append(service)
    return services
