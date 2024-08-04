from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from models.appointment import Appointment
from bson import ObjectId
from typing import List
import os

router = APIRouter()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.VentusSystemDB
appointment_collection = db.appointments

@router.post("/appointments/", response_model=Appointment)
async def create_appointment(appointment: Appointment):
    appointment_dict = appointment.dict()
    result = appointment_collection.insert_one(appointment_dict)
    appointment_dict["_id"] = str(result.inserted_id)
    return appointment_dict

@router.get("/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str):
    appointment = appointment_collection.find_one({"_id": ObjectId(appointment_id)})
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment["_id"] = str(appointment["_id"])
    return appointment

@router.put("/appointments/{appointment_id}", response_model=Appointment)
async def update_appointment(appointment_id: str, updated_appointment: Appointment):
    result = appointment_collection.update_one({"_id": ObjectId(appointment_id)}, {"$set": updated_appointment.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment = appointment_collection.find_one({"_id": ObjectId(appointment_id)})
    appointment["_id"] = str(appointment["_id"])
    return appointment

@router.delete("/appointments/{appointment_id}")
async def delete_appointment(appointment_id: str):
    result = appointment_collection.delete_one({"_id": ObjectId(appointment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment deleted successfully"}

@router.get("/appointments/", response_model=List[Appointment])
async def list_appointments():
    appointments = []
    for appointment in appointment_collection.find():
        appointment["_id"] = str(appointment["_id"])
        appointments.append(appointment)
    return appointments
