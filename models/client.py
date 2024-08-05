from pydantic import BaseModel, EmailStr
from typing import List, Optional

class Client(BaseModel):
    _id: Optional[str] = None  # O _id será uma string opcional
    name: str
    address: str
    phone: str
    email: EmailStr
    service_history: Optional[List[str]] = []
