from pydantic import BaseModel, EmailStr
from typing import Optional

class Technician(BaseModel):
    name: str
    specialization: str
    contact: str
    email: EmailStr
    availability: str  # Disponibilidade em um formato adequado, ex: "9h-18h"
