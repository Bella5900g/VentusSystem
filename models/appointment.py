from pydantic import BaseModel
from datetime import datetime

class Appointment(BaseModel):
    client_name: str
    service_type: str
    technician_name: str
    appointment_date: datetime
