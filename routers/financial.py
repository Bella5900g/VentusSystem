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

# Rota para consultar um registro financeiro pelo type
@router.get("/financials/{type}", response_model=Financial)
async def get_financial(type: str):
    financial = financial_collection.find_one({"type": type})
    if financial is None:
        raise HTTPException(status_code=404, detail="Financial record not found")
    financial["_id"] = str(financial["_id"])  # Converte ObjectId para string
    return financial

# Rota para atualizar um registro financeiro pelo type
@router.put("/financials/{type}", response_model=Financial)
async def update_financial(type: str, updated_financial: Financial):
    result = financial_collection.update_one({"type": type}, {"$set": updated_financial.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Financial record not found")
    financial = financial_collection.find_one({"type": type})
    financial["_id"] = str(financial["_id"])  # Converte ObjectId para string
    return financial

# Rota para excluir um registro financeiro pelo type
@router.delete("/financials/{type}")
async def delete_financial(type: str):
    result = financial_collection.delete_one({"type": type})
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
