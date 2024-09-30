from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from models.client import Client
from bson import ObjectId
from typing import List
import os
from fastapi import status

router = APIRouter()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.VentusSystemDB
client_collection = db.clients


# Rota para criar um novo cliente
@router.post("/clients/", response_model=Client, status_code=status.HTTP_201_CREATED)
async def create_client(client: Client):
    client_dict = client.dict()
    result = client_collection.insert_one(client_dict)
    client_dict["_id"] = str(result.inserted_id)
    return client_dict

# Rota para consultar um cliente pelo nome
@router.get("/clients/{name}", response_model=Client)
async def get_client(name: str):
    client = client_collection.find_one({"name": name})
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    client["_id"] = str(client["_id"])  # Converte ObjectId para string
    return client

# Rota para atualizar um cliente pelo nome
@router.put("/clients/{name}", response_model=Client)
async def update_client(name: str, updated_client: Client):
    result = client_collection.update_one({"name": name}, {"$set": updated_client.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    client = client_collection.find_one({"name": name})
    client["_id"] = str(client["_id"])  # Converte ObjectId para string
    return client

# Rota para excluir um cliente pelo nome
@router.delete("/clients/{name}")
async def delete_client(name: str):
    result = client_collection.delete_one({"name": name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"message": "Cliente deletado com sucesso"}

# Rota para listar todos os clientes
@router.get("/clients/", response_model=List[Client])
async def list_clients():
    clients = []
    for client in client_collection.find():
        client["_id"] = str(client["_id"])  # Converte ObjectId para string
        clients.append(client)
    return clients
