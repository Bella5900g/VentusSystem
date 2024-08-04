from pydantic import BaseModel
from datetime import datetime

class Appointment(BaseModel):
    client_id: str
    service_id: str
    technician_id: str
    appointment_date: datetime
