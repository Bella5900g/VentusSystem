from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from models.client import Client
from bson import ObjectId
from typing import List
import os

router = APIRouter()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.VentusSystemDB
client_collection = db.clients

@router.post("/clients/", response_model=Client)
async def create_client(client: Client):
    client_dict = client.dict()
    result = client_collection.insert_one(client_dict)
    client_dict["_id"] = str(result.inserted_id)
    return client_dict

@router.get("/clients/{client_id}", response_model=Client)
async def get_client(client_id: str):
    client = client_collection.find_one({"_id": ObjectId(client_id)})
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    client["_id"] = str(client["_id"])
    return client

@router.put("/clients/{client_id}", response_model=Client)
async def update_client(client_id: str, updated_client: Client):
    result = client_collection.update_one({"_id": ObjectId(client_id)}, {"$set": updated_client.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    client = client_collection.find_one({"_id": ObjectId(client_id)})
    client["_id"] = str(client["_id"])
    return client

@router.delete("/clients/{client_id}")
async def delete_client(client_id: str):
    result = client_collection.delete_one({"_id": ObjectId(client_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}

@router.get("/clients/", response_model=List[Client])
async def list_clients():
    clients = []
    for client in client_collection.find():
        client["_id"] = str(client["_id"])
        clients.append(client)
    return clients
