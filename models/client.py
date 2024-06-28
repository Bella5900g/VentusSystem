from pydantic import BaseModel, EmailStr
from typing import List, Optional

class Client(BaseModel):
    name: str
    address: str
    phone: str
    email: EmailStr
    service_history: Optional[List[str]] = []
