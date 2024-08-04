from pydantic import BaseModel
from typing import List

class Report(BaseModel):
    report_type: str
    data: List[dict]
