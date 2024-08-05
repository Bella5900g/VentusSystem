from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from models.financial import Financial
from typing import List
import os

router = APIRouter()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.VentusSystemDB
financial_collection = db.financials

# Rota para criar um novo registro financeiro
@router.post("/financials/", response_model=Financial)
async def create_financial(financial: Financial):
    financial_dict = financial.dict()
    result = financial_collection.insert_one(financial_dict)
    financial_dict["_id"] = str(result.inserted_id)
    return financial_dict

# Rota para consultar um registro financeiro pelo nome
@router.get("/financials/{name}", response_model=Financial)
async def get_financial(name: str):
    financial = financial_collection.find_one({"name": name})
    if financial is None:
        raise HTTPException(status_code=404, detail="Financial record not found")
    financial["_id"] = str(financial["_id"])  # Converte ObjectId para string
    return financial

# Rota para atualizar um registro financeiro pelo nome
@router.put("/financials/{name}", response_model=Financial)
async def update_financial(name: str, updated_financial: Financial):
    result = financial_collection.update_one({"name": name}, {"$set": updated_financial.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Financial record not found")
    financial = financial_collection.find_one({"name": name})
    financial["_id"] = str(financial["_id"])  # Converte ObjectId para string
    return financial

# Rota para excluir um registro financeiro pelo nome
@router.delete("/financials/{name}")
async def delete_financial(name: str):
    result = financial_collection.delete_one({"name": name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Financial record not found")
    return {"message": "Financial record deleted successfully"}

# Rota para listar todos os registros financeiros
@router.get("/financials/", response_model=List[Financial])
async def list_financials():
    financials = []
    for financial in financial_collection.find():
        financial["_id"] = str(financial["_id"])  # Converte ObjectId para string
        financials.append(financial)
    return financials
