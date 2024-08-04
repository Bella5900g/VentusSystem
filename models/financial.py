from pydantic import BaseModel

class Financial(BaseModel):
    type: str  # Entrada ou Saída
    amount: float
    description: str
