from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from models.technician import Technician
from typing import List
import os
from fastapi import status

router = APIRouter()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.VentusSystemDB
technician_collection = db.technicians

# Rota para criar um novo técnico
@router.post("/technicians/", response_model=Technician, status_code=status.HTTP_201_CREATED)
async def create_technician(technician: Technician):
    technician_dict = technician.dict()
    result = technician_collection.insert_one(technician_dict)
    technician_dict["_id"] = str(result.inserted_id)
    return technician_dict


# Rota para consultar um técnico pelo nome
@router.get("/technicians/{name}", response_model=Technician)
async def get_technician(name: str):
    technician = technician_collection.find_one({"name": name})
    if technician is None:
        raise HTTPException(status_code=404, detail="Technician not found")
    technician["_id"] = str(technician["_id"])  # Converte ObjectId para string
    return technician

# Rota para atualizar um técnico pelo nome
@router.put("/technicians/{name}", response_model=Technician)
async def update_technician(name: str, updated_technician: Technician):
    result = technician_collection.update_one({"name": name}, {"$set": updated_technician.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Technician not found")
    technician = technician_collection.find_one({"name": name})
    technician["_id"] = str(technician["_id"])  # Converte ObjectId para string
    return technician

# Rota para excluir um técnico pelo nome
@router.delete("/technicians/{name}")
async def delete_technician(name: str):
    result = technician_collection.delete_one({"name": name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Technician not found")
    return {"message": "Technician deleted successfully"}

# Rota para listar todos os técnicos
@router.get("/technicians/", response_model=List[Technician])
async def list_technicians():
    technicians = []
    for technician in technician_collection.find():
        technician["_id"] = str(technician["_id"])  # Converte ObjectId para string
        technicians.append(technician)
    return technicians
