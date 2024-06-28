from pydantic import BaseModel
from typing import Optional

class Service(BaseModel):
    type: str
    description: str
    price: float
    duration: str  # Duração em um formato adequado, ex: "2h", "30min"
