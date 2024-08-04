from pydantic import BaseModel

class Stock(BaseModel):
    item_name: str
    quantity: int
    price: float
