from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from models.report import Report
from bson import ObjectId
from typing import List
import os

router = APIRouter()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.VentusSystemDB

@router.get("/reports/", response_model=Report)
async def generate_report(report_type: str):
    if report_type == "clients":
        data = list(db.clients.find())
    elif report_type == "services":
        data = list(db.services.find())
    elif report_type == "technicians":
        data = list(db.technicians.find())
    elif report_type == "stocks":
        data = list(db.stocks.find())
    elif report_type == "appointments":
        data = list(db.appointments.find())
    elif report_type == "financials":
        data = list(db.financials.find())
    else:
        raise HTTPException(status_code=400, detail="Invalid report type")

    # Converte ObjectId para string
    for item in data:
        item["_id"] = str(item["_id"])

    report = Report(report_type=report_type, data=data)
    return report
