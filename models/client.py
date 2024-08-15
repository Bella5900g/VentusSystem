from pydantic import BaseModel, EmailStr
from typing import List, Optional

class Client(BaseModel):
    _id: Optional[str] = None  # O _id será uma string opcional
    name: str
    address: str
    phone: str
    email: EmailStr
    # CPF: int = ("000.000.000-00");
    service_history: Optional[List[str]] = []
