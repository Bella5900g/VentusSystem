from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class Venda(BaseModel):
    id: Optional[str] = None
    client_id: str
    products: List[ProductItem]
    total_value: Optional[float] = None
    status: str = "pending"  # Status da venda: 'pending' ou 'completed'
    data_finalizacao: Optional[str] = None  # Data de finalização da venda

    def calculate_total(self):
        """Calcula o valor total da venda."""
        self.total_value = sum(item.price * item.quantity for item in self.products)
        return self.total_value

    def set_data_finalizacao(self):
        """Define a data de finalização no formato brasileiro."""
        self.data_finalizacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
