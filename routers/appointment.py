from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from models.appointment import Appointment
from typing import List
import os

router = APIRouter()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.VentusSystemDB
appointment_collection = db.appointments

# Rota para criar um novo compromisso
@router.post("/appointments/", response_model=Appointment)
async def create_appointment(appointment: Appointment):
    appointment_dict = appointment.dict()
    result = appointment_collection.insert_one(appointment_dict)
    appointment_dict["_id"] = str(result.inserted_id)
    return appointment_dict

# Rota para consultar um compromisso pelo nome
@router.get("/appointments/{name}", response_model=Appointment)
async def get_appointment(name: str):
    appointment = appointment_collection.find_one({"name": name})
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment["_id"] = str(appointment["_id"])  # Converte ObjectId para string
    return appointment

# Rota para atualizar um compromisso pelo nome
@router.put("/appointments/{name}", response_model=Appointment)
async def update_appointment(name: str, updated_appointment: Appointment):
    result = appointment_collection.update_one({"name": name}, {"$set": updated_appointment.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment = appointment_collection.find_one({"name": name})
    appointment["_id"] = str(appointment["_id"])  # Converte ObjectId para string
    return appointment

# Rota para excluir um compromisso pelo nome
@router.delete("/appointments/{name}")
async def delete_appointment(name: str):
    result = appointment_collection.delete_one({"name": name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment deleted successfully"}

# Rota para listar todos os compromissos
@router.get("/appointments/", response_model=List[Appointment])
async def list_appointments():
    appointments = []
    for appointment in appointment_collection.find():
        appointment["_id"] = str(appointment["_id"])  # Converte ObjectId para string
        appointments.append(appointment)
    return appointments
